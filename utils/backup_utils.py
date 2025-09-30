"""
备份与恢复功能的底层辅助函数。
"""
import os
import subprocess
import tarfile
import sys
import tempfile
import json
import platform
import shutil
from typing import Union, Optional, Dict, List

from utils.helpers import command_exists, update_env_file
from utils.i18n import get_message as _


def get_volumes_to_backup(static_volumes: List[str], volume_suffixes: List[str]) -> List[str]:
    """获取需要备份的 Docker 卷列表。
    
    优先使用动态发现，如果没有发现卷则回退到静态配置。
    
    Args:
        static_volumes: 静态配置的卷列表
        volume_suffixes: 用于动态发现的卷名后缀列表
    
    Returns:
        list[str]: 需要备份的 Docker 卷名列表。
    """
    # 先尝试动态发现
    discovered_volumes = discover_docker_volumes_by_pattern(suffixes=volume_suffixes)
    
    if discovered_volumes:
        print(f"  - {_('discovered_docker_volumes', len(discovered_volumes))}")
        return discovered_volumes
    else:
        print(f"  - {_('no_matching_volumes_using_static', static_volumes)}")
        return static_volumes

def get_user_confirmation() -> bool:
    """获取用户的确认。"""
    try:
        response = input(_('confirm_continue'))
        if response.lower() != 'y':
            print(_("operation_cancelled"))
            return False
        return True
    except (EOFError, KeyboardInterrupt):
        print(f"\n{_('operation_cancelled')}")
        return False

def discover_docker_volumes_by_pattern(suffixes: Optional[List[str]] = None) -> List[str]:
    """根据后缀模式动态发现 Docker 卷。

    Args:
        suffixes (list[str], optional): 卷名后缀列表（必须匹配）。

    Returns:
        list[str]: 符合条件的 Docker 卷名列表。
    """
    if not command_exists("docker"):
        print(_("warning_docker_not_found_skip_backup"), file=sys.stderr)
        return []

    discovered_volumes = []
    suffixes = suffixes or []

    # 如果没有提供后缀，返回空列表
    if not suffixes:
        return []

    try:
        # 获取所有 Docker 卷
        result = subprocess.run(
            ["docker", "volume", "ls", "--format", "{{.Name}}"],
            capture_output=True,
            text=True,
            check=True
        )
        
        all_volumes = result.stdout.strip().split('\n')
        if all_volumes == ['']:  # 如果没有卷，返回空列表
            all_volumes = []

        for volume_name in all_volumes:
            volume_name = volume_name.strip()
            if not volume_name:
                continue
                
            # 检查后缀匹配（必须以指定后缀结尾）
            for suffix in suffixes:
                if volume_name.endswith(suffix):
                    discovered_volumes.append(volume_name)
                    print(f"  - {_('found_matching_docker_volume', volume_name, suffix)}")
                    break  # 找到一个匹配的后缀就跳出

    except subprocess.CalledProcessError as e:
        print(_('warning_cannot_get_volume_list', e), file=sys.stderr)
        return []
    except Exception as e:
        print(_('error_docker_volume_discovery_exception', e), file=sys.stderr)
        return []

    return discovered_volumes

def create_docker_volume_if_not_exists(volume_name: str) -> bool:
    """如果 Docker 卷不存在，则创建它。
    
    Args:
        volume_name (str): 要创建的 Docker 卷名称。
        
    Returns:
        bool: 卷存在或创建成功返回 True，失败返回 False。
    """
    try:
        # 首先检查卷是否已经存在
        result = subprocess.run(
            ["docker", "volume", "inspect", volume_name],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"  - {_('docker_volume_exists', volume_name)}")
        return True
        
    except subprocess.CalledProcessError:
        # 卷不存在，尝试创建它
        try:
            print(f"  - {_('creating_docker_volume', volume_name)}")
            subprocess.run(
                ["docker", "volume", "create", volume_name],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"  - {_('docker_volume_created', volume_name)}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(_("error_create_docker_volume", volume_name, e), file=sys.stderr)
            return False

def get_docker_volumes_for_recovery(volume_names: List[str]) -> Dict[str, str]:
    """为恢复操作获取或创建指定的 Docker 卷。

    在新环境中恢复时，如果 Docker 卷不存在，会自动创建它们。
    统一使用容器方式恢复，不区分平台。

    Args:
        volume_names (list[str]): 要查询或创建的 Docker 卷名称列表。

    Returns:
        dict[str, str]: 一个字典，键是卷名，值是恢复方法标识（统一为"container_restore"）。
    """
    if not command_exists("docker"):
        print(_("warning_docker_not_found_skip_recovery"), file=sys.stderr)
        return {}

    volume_info = {}
    
    for name in volume_names:
        # 先尝试创建卷（如果不存在）
        if create_docker_volume_if_not_exists(name):
            # 统一使用容器方式恢复，不区分平台
            volume_info[name] = "container_restore"
            print(f"  - {_('will_restore_docker_volume_via_container', name)}")
    
    return volume_info

def get_docker_volumes(volume_names: List[str]) -> Dict[str, str]:
    """获取指定 Docker 卷的信息并验证其可用性。

    在 macOS/Windows 系统上，Docker 卷运行在虚拟机中，无法直接通过主机路径访问。
    此函数会检测操作系统，并返回可用于备份的卷信息。

    Args:
        volume_names (list[str]): 要查询的 Docker 卷名称列表。

    Returns:
        dict[str, str]: 一个字典，键是卷名，值是其状态信息或备份方法标识。
    """
    if not command_exists("docker"):
        print(_("warning_docker_not_found_skip_backup"), file=sys.stderr)
        return {}

    volume_info = {}
    system = platform.system()
    
    for name in volume_names:
        try:
            # 使用 docker volume inspect 检查卷是否存在
            result = subprocess.run(
                ["docker", "volume", "inspect", name],
                capture_output=True,
                text=True,
                check=True
            )
            volume_data = json.loads(result.stdout)
            mountpoint = volume_data[0]['Mountpoint']
            
            if system == "Linux":
                # 在 Linux 系统上，可以直接访问 Docker 卷路径
                if os.path.isdir(mountpoint):
                    volume_info[name] = mountpoint
                    print(f"  - {_('found_docker_volume_path', name, mountpoint)}")
                else:
                    print(_("warning_docker_volume_invalid_path", name, mountpoint), file=sys.stderr)
            else:
                # 在 macOS/Windows 系统上，Docker 运行在虚拟机中，需要通过容器方式备份
                volume_info[name] = "container_backup"
                print(f"  - {_('found_docker_volume_container_backup', name)}")
                
        except (subprocess.CalledProcessError, json.JSONDecodeError, IndexError, KeyError) as e:
            print(_("warning_cannot_get_volume_info", name, e), file=sys.stderr)
    
    return volume_info

def backup_docker_volume_via_container(volume_name: str, backup_path: str) -> bool:
    """通过 Docker 容器备份指定的 Docker 卷。
    
    这种方法适用于所有操作系统，特别是 macOS/Windows 上的 Docker Desktop。
    
    Args:
        volume_name (str): 要备份的 Docker 卷名称。
        backup_path (str): 备份文件的保存路径。
        
    Returns:
        bool: 备份成功返回 True，失败返回 False。
    """
    try:
        # 获取备份文件的目录和文件名
        backup_dir = os.path.dirname(backup_path)
        backup_filename = os.path.basename(backup_path)
        
        print(f"  - {_('backup_via_container_starting', volume_name)}")
        
        # 使用 ubuntu 容器来创建卷的 tar 备份
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{volume_name}:/data",
            "-v", f"{backup_dir}:/backup-dir",
            "ubuntu",
            "tar", "czf", f"/backup-dir/{backup_filename}", "/data"
        ]
        
        # 运行命令，不将 stderr 中的正常警告视为错误
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # tar 命令可能会输出警告 "Removing leading `/' from member names"
        # 这是正常行为，只要返回码为 0 就表示成功
        if result.returncode != 0:
            # 只有当返回码非零时才是真正的错误
            raise subprocess.CalledProcessError(result.returncode, cmd, result.stdout, result.stderr)
        
        # 检查备份文件是否成功创建且不为空
        if not os.path.exists(backup_path) or os.path.getsize(backup_path) == 0:
            raise FileNotFoundError(_('backup_file_not_created', backup_path))
        
        # 如果有 stderr 输出但返回码为 0，只是显示警告，不当作错误
        if result.stderr and "Removing leading" in result.stderr:
            print(f"  - {_('tar_normal_warning', result.stderr.strip())}")
        elif result.stderr:
            print(f"  - {_('tar_warning', result.stderr.strip())}")
        
        print(f"  - {_('backup_via_container_complete', volume_name, backup_path)}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(_('backup_docker_volume_failed', volume_name, e), file=sys.stderr)
        if e.stderr:
            print(_('error_details', e.stderr), file=sys.stderr)
        return False
    except Exception as e:
        print(_('backup_docker_volume_exception', volume_name, e), file=sys.stderr)
        return False

def restore_docker_volume_via_container(volume_name: str, backup_path: str) -> bool:
    """通过 Docker 容器恢复指定的 Docker 卷。
    
    这种方法适用于所有操作系统，提供统一的恢复体验。
    
    Args:
        volume_name (str): 要恢复的 Docker 卷名称。
        backup_path (str): 备份文件的路径。
        
    Returns:
        bool: 恢复成功返回 True，失败返回 False。
    """
    try:
        # 获取备份文件的目录和文件名
        backup_dir = os.path.dirname(backup_path)
        backup_filename = os.path.basename(backup_path)
        
        print(f"  - {_('restoring_via_container_starting', volume_name)}")
        
        # 使用 ubuntu 容器来恢复卷的 tar 备份
        # 先清理卷内容，然后解压备份
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{volume_name}:/data",
            "-v", f"{backup_dir}:/backup-dir",
            "ubuntu",
            "bash", "-c",
            f"cd /data && rm -rf ./* ./.[!.]* ./..?* 2>/dev/null || true && tar xzf /backup-dir/{backup_filename} --strip-components=1"
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"  - {_('restoring_via_container_complete', volume_name)}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(_('restore_docker_volume_failed', volume_name, e), file=sys.stderr)
        return False


def restore_docker_volume_from_directory(volume_name: str, source_dir: str) -> bool:
    """通过 Docker 容器从目录恢复指定的 Docker 卷。
    
    用于恢复直接以目录形式存储的卷备份。
    
    Args:
        volume_name (str): 要恢复的 Docker 卷名称。
        source_dir (str): 包含卷数据的源目录路径。
        
    Returns:
        bool: 恢复成功返回 True，失败返回 False。
    """
    try:
        print(f"  - {_('restoring_via_container_starting', volume_name)}")
        
        # 使用 ubuntu 容器来恢复卷的目录数据
        # 先清理卷内容，然后复制数据
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{volume_name}:/data",
            "-v", f"{source_dir}:/source-data",
            "ubuntu",
            "bash", "-c",
            "cd /data && rm -rf ./* ./.[!.]* ./..?* 2>/dev/null || true && cp -a /source-data/. /data/"
        ]
        
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"  - {_('restoring_via_container_complete', volume_name)}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(_('restore_docker_volume_failed', volume_name, e), file=sys.stderr)
        return False

def create_archive(source_paths: Dict[str, str], dest_path_base: str) -> Optional[str]:
    """创建一个包含多个源目录的压缩归档文件。

    如果系统支持 zstd，则创建 .tar.zstd 文件；否则，创建 .tar 文件。
    会排除 logs/, uploads/ 目录和 .env.example 文件。
    
    对于 Docker 卷，如果值为 "container_backup"，则通过容器方式单独备份。

    Args:
        source_paths (dict[str, str]): 一个字典，键是源路径，值是其在归档中的目标名称 (arcname) 或备份方法。
        dest_path_base (str): 不带扩展名的目标归档文件基础路径。

    Returns:
        Optional[str]: 成功则返回最终的归档文件路径，否则返回 None。
    """
    tar_path = f"{dest_path_base}.tar"
    
    # 分离常规文件路径和 Docker 卷
    regular_sources = {}
    volume_sources = {}
    
    for source, arcname in source_paths.items():
        if arcname == "container_backup":
            # 这是一个需要通过容器备份的 Docker 卷
            volume_name = os.path.basename(source) if source.startswith("volumes/") else source
            volume_sources[volume_name] = source
        else:
            regular_sources[source] = arcname

    # 定义要排除的路径和文件模式
    def exclude_filter(tarinfo: tarfile.TarInfo) -> Optional[tarfile.TarInfo]:
        """Tarfile filter to exclude specific files/directories."""
        # 获取相对于归档根目录的路径
        path = tarinfo.name
        
        # 分离路径和文件名
        path_parts = path.split('/')
        filename = os.path.basename(path)
        
        # 1. 过滤根目录下的 logs 文件夹
        if len(path_parts) >= 2 and path_parts[1] == 'logs':
            print(f"  - {_('excluding_logs_directory', tarinfo.name)}")
            return None
            
        # 2. 过滤根目录下的 uploads 文件夹
        if len(path_parts) >= 2 and path_parts[1] == 'uploads':
            print(f"  - {_('excluding_uploads_directory', tarinfo.name)}")
            return None
            
        # 3. 过滤根目录下的 .env.example 文件
        if len(path_parts) == 2 and path_parts[1] == '.env.example':
            print(f"  - {_('excluding_env_template', tarinfo.name)}")
            return None
            
        # 4. 过滤根目录下以 ._ 开头的文件
        if len(path_parts) == 2 and filename.startswith('._'):
            print(f"  - {_('excluding_temp_file', tarinfo.name)}")
            return None
            
        return tarinfo

    try:
        print(_('creating_tar_archive', tar_path))
        
        # 创建主 tar 文件
        with tarfile.open(tar_path, "w") as tar:
            # 添加常规文件和目录
            for source, arcname in regular_sources.items():
                print(_('adding_to_archive', source, arcname))
                tar.add(source, arcname=arcname, filter=exclude_filter)
        
        # 处理 Docker 卷备份
        if volume_sources:
            temp_dir = tempfile.mkdtemp()
            try:
                # 为每个卷创建备份文件
                volume_backups = {}
                for volume_name, source in volume_sources.items():
                    volume_backup_path = os.path.join(temp_dir, f"{volume_name}.tar.gz")
                    if backup_docker_volume_via_container(volume_name, volume_backup_path):
                        volume_backups[volume_name] = volume_backup_path
                
                # 将卷备份添加到主 tar 文件中
                if volume_backups:
                    with tarfile.open(tar_path, "a") as tar:
                        for volume_name, backup_path in volume_backups.items():
                            arcname = f"volumes/{volume_name}.tar.gz"
                            print(_('adding_docker_volume_backup', volume_name, arcname))
                            tar.add(backup_path, arcname=arcname)
            finally:
                import shutil
                shutil.rmtree(temp_dir)

        # 压缩最终归档
        if command_exists("zstd"):
            zstd_path = f"{dest_path_base}.tar.zstd"
            print(_('detected_zstd_compressing', zstd_path))
            subprocess.run(["zstd", "-f", "--quiet", tar_path, "-o", zstd_path], check=True)
            os.remove(tar_path)
            return zstd_path
        else:
            print(_('zstd_not_detected_tar_only'))
            return tar_path

    except (subprocess.CalledProcessError, FileNotFoundError, OSError) as e:
        print(_('error_archive_creation_failed', e), file=sys.stderr)
        if os.path.exists(tar_path):
            os.remove(tar_path)
        return None

def extract_archive(archive_path: str, dest_dir: str, volume_mountpoints: Optional[Dict[str, str]] = None) -> bool:
    """解压归档文件，区分数据目录和 Docker 卷。

    Args:
        archive_path (str): 要解压的归档文件路径。
        dest_dir (str): 数据文件的主要目标解压目录。
        volume_mountpoints (dict[str, str], optional): Docker 卷名到其挂载点的映射。如果提供，则恢复卷。

    Returns:
        bool: 成功返回 True，失败返回 False。
    """
    volume_mountpoints = volume_mountpoints or {}
    temp_extract_dir = tempfile.mkdtemp()
    
    try:
        # 1. 解压整个归档到临时目录
        if archive_path.endswith(".tar.zstd"):
            if not command_exists("zstd"):
                print(_('error_zstd_required_for_recovery'), file=sys.stderr)
                return False
            subprocess.run(["zstd", "-d", "--quiet", archive_path, "-o", f"{temp_extract_dir}/archive.tar"], check=True)
            tar_path = f"{temp_extract_dir}/archive.tar"
        elif archive_path.endswith(".tar"):
            tar_path = archive_path
        else:
            print(_('error_unsupported_file_format', archive_path), file=sys.stderr)
            return False

        with tarfile.open(tar_path, "r") as tar:
            tar.extractall(path=temp_extract_dir)
        
        # 清理临时 tar 文件（如果是从 zstd 解压的）
        if tar_path != archive_path and os.path.exists(tar_path):
            os.remove(tar_path)

        # 2. 移动数据和卷文件
        data_root_name = get_archive_root_dir(archive_path, inspect_path=temp_extract_dir)
        
        if data_root_name:
            source_data_path = os.path.join(temp_extract_dir, data_root_name)
            if os.path.exists(source_data_path):
                print(_('restoring_data_to', dest_dir))
                # 将数据文件移动到最终目标
                for item in os.listdir(source_data_path):
                    s = os.path.join(source_data_path, item)
                    d = os.path.join(dest_dir, item)
                    if os.path.exists(d):
                        if os.path.isdir(d):
                            shutil.rmtree(d)
                        else:
                            os.remove(d)
                    if os.path.isdir(s):
                        shutil.copytree(s, d)
                    else:
                        shutil.copy2(s, d)

            # 获取dest_dir绝对路径
            dest_dir = os.path.abspath(dest_dir)
            # 更新.env文件数据目录
            env_path = os.path.join(dest_dir, ".env")
            if os.path.exists(env_path):
                    print(_("updating_nekro_data_dir"))

                    update_env_file(env_path, "NEKRO_DATA_DIR", dest_dir)

        # 3. 恢复 Docker 卷
        archived_volumes_path = os.path.join(temp_extract_dir, 'volumes')
        if os.path.isdir(archived_volumes_path):
            for item in os.listdir(archived_volumes_path):
                item_path = os.path.join(archived_volumes_path, item)
                
                if item.endswith('.tar.gz'):
                    # 处理 .tar.gz 格式的卷备份（容器备份方式）
                    volume_name = item[:-7]  # 移除 .tar.gz 后缀
                    
                    if volume_name in volume_mountpoints:
                        print(_('restoring_docker_volume_via_container', volume_name))
                        restore_docker_volume_via_container(volume_name, item_path)
                    else:
                        print(_('volume_backup_skipped', volume_name), file=sys.stderr)
                        
                elif os.path.isdir(item_path):
                    # 处理目录格式的卷备份（直接路径备份方式）
                    volume_name = item
                    
                    if volume_name in volume_mountpoints:
                        print(_('restoring_docker_volume_from_directory', volume_name))
                        restore_docker_volume_from_directory(volume_name, item_path)
                    else:
                        print(_('volume_backup_skipped', volume_name), file=sys.stderr)

        return True

    except (subprocess.CalledProcessError, FileNotFoundError, OSError) as e:
        print(_('error_archive_extraction_failed', e), file=sys.stderr)
        return False
    finally:
        shutil.rmtree(temp_extract_dir)


def get_archive_root_dir(archive_path: str, inspect_path: Optional[str] = None) -> Optional[str]:
    """读取归档文件并返回其中主要的顶层目录名（非 'volumes'）。"""
    temp_tar_path = None
    tar_to_inspect = None

    try:
        if inspect_path:
            # 如果提供了已解压的路径，直接在该路径下查找
            top_levels = {name for name in os.listdir(inspect_path) if name != 'volumes'}
            if len(top_levels) == 1:
                return top_levels.pop()
            # 如果解压路径下除了volumes还有多个，就无法确定哪个是主目录
            elif len(top_levels) > 1:
                 print(_('multiple_root_directories_warning', top_levels), file=sys.stderr)
                 return None
            else: # 只有volumes目录
                return None

        # 如果没有提供解压路径，则需要从归档文件中读取
        if archive_path.endswith(".tar.zstd"):
            if not command_exists("zstd"):
                return None
            with tempfile.NamedTemporaryFile(delete=False, suffix=".tar") as tmp_f:
                temp_tar_path = tmp_f.name
            subprocess.run(["zstd", "-d", "--quiet", "-f", archive_path, "-o", temp_tar_path], check=True)
            tar_to_inspect = temp_tar_path
        elif archive_path.endswith(".tar"):
            tar_to_inspect = archive_path
        else:
            return None

        with tarfile.open(tar_to_inspect, "r") as tar:
            members = tar.getnames()
            if not members:
                return None
            
            top_levels = {name.split(os.path.sep)[0] for name in members if name.split(os.path.sep)[0] != 'volumes'}
            if len(top_levels) == 1:
                return top_levels.pop()
            else:
                return None

    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None
    finally:
        if temp_tar_path and os.path.exists(temp_tar_path):
            os.remove(temp_tar_path)
