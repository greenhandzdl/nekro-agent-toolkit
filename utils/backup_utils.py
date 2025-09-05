"""
备份与恢复功能的底层辅助函数。
"""
import os
import subprocess
import tarfile
import sys
import tempfile
import json

from utils.helpers import command_exists

def get_docker_volumes(volume_names: list[str]) -> dict[str, str]:
    """获取指定 Docker aaaaaaaaaaaaaa卷的挂载点路径。

    Args:
        volume_names (list[str]): 要查询的 Docker 卷名称列表。

    Returns:
        dict[str, str]: 一个字典，键是卷名，值是其在主机上的挂载点路径。
    """
    if not command_exists("docker"):
        print("警告: 未找到 'docker' 命令，将跳过 Docker 卷的备份。", file=sys.stderr)
        return {}

    volume_paths = {}
    for name in volume_names:
        try:
            # 使用 docker volume inspect 获取卷的详细信息
            result = subprocess.run(
                ["docker", "volume", "inspect", name],
                capture_output=True,
                text=True,
                check=True
            )
            volume_info = json.loads(result.stdout)
            # 提取 Mountpoint，这是卷在主机上的实际路径
            mountpoint = volume_info[0]['Mountpoint']
            volume_paths[name] = mountpoint
            print(f"  - 找到 Docker 卷 '{name}' 的路径: {mountpoint}")
        except (subprocess.CalledProcessError, json.JSONDecodeError, IndexError, KeyError) as e:
            print(f"警告: 无法获取 Docker 卷 '{name}' 的信息，将跳过。错误: {e}", file=sys.stderr)
    return volume_paths

def create_archive(source_paths: dict[str, str], dest_path_base: str) -> str | None:
    """创建一个包含多个源目录的压缩归档文件。

    如果系统支持 zstd，则创建 .tar.zstd 文件；否则，创建 .tar 文件。
    会排除 logs/, uploads/ 目录和 .env.example 文件。

    Args:
        source_paths (dict[str, str]): 一个字典，键是源路径，值是其在归档中的目标名称 (arcname)。
        dest_path_base (str): 不带扩展名的目标归档文件基础路径。

    Returns:
        str | None: 成功则返回最终的归档文件路径，否则返回 None。
    """
    tar_path = f"{dest_path_base}.tar"

    # 定义要排除的路径（相对于归档的根目录）
    # 注意：这里的逻辑需要调整，因为 archive_root_name 不再是单一的
    excluded_patterns = ['/logs', '/uploads', '/.env.example']

    def exclude_filter(tarinfo: tarfile.TarInfo) -> tarfile.TarInfo | None:
        """Tarfile filter to exclude specific files/directories."""
        for pattern in excluded_patterns:
            if pattern in tarinfo.name:
                print(f"  - 正在排除: {tarinfo.name}")
                return None
        return tarinfo

    try:
        print(f"正在创建 tar 归档: {tar_path}...")
        with tarfile.open(tar_path, "w") as tar:
            for source, arcname in source_paths.items():
                print(f"  - 正在添加: {source} (归档为: {arcname})")
                tar.add(source, arcname=arcname, filter=exclude_filter)

        if command_exists("zstd"):
            zstd_path = f"{dest_path_base}.tar.zstd"
            print(f"检测到 zstd，正在压缩为: {zstd_path}...")
            subprocess.run(["zstd", "-f", "--quiet", tar_path, "-o", zstd_path], check=True)
            os.remove(tar_path)
            return zstd_path
        else:
            print("未检测到 zstd，仅创建 .tar 归档。" )
            return tar_path

    except (subprocess.CalledProcessError, FileNotFoundError, OSError) as e:
        print(f"错误：创建归档失败.\n{e}", file=sys.stderr)
        if os.path.exists(tar_path):
            os.remove(tar_path)
        return None

def extract_archive(archive_path: str, dest_dir: str, volume_mountpoints: dict[str, str] = None) -> bool:
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
                print("错误: 恢复需要 'zstd' 命令。", file=sys.stderr)
                return False
            subprocess.run(["zstd", "-d", "--quiet", archive_path, "-o", f"{temp_extract_dir}/archive.tar"], check=True)
            tar_path = f"{temp_extract_dir}/archive.tar"
        elif archive_path.endswith(".tar"):
            tar_path = archive_path
        else:
            print(f"错误: 不支持的文件格式: {archive_path}", file=sys.stderr)
            return False

        with tarfile.open(tar_path, "r") as tar:
            tar.extractall(path=temp_extract_dir)

        # 2. 移动数据和卷文件
        data_root_name = get_archive_root_dir(archive_path, inspect_path=temp_extract_dir)
        
        if data_root_name:
            source_data_path = os.path.join(temp_extract_dir, data_root_name)
            if os.path.exists(source_data_path):
                print(f"正在恢复数据到: {dest_dir}")
                # 将数据文件移动到最终目标
                for item in os.listdir(source_data_path):
                    s = os.path.join(source_data_path, item)
                    d = os.path.join(dest_dir, item)
                    if os.path.exists(d):
                        if os.path.isdir(d):
                            import shutil
                            shutil.rmtree(d)
                        else:
                            os.remove(d)
                    if os.path.isdir(s):
                        shutil.copytree(s, d)
                    else:
                        shutil.copy2(s, d)

        # 恢复 Docker 卷
        archived_volumes_path = os.path.join(temp_extract_dir, 'volumes')
        if os.path.isdir(archived_volumes_path):
            for volume_name in os.listdir(archived_volumes_path):
                if volume_name in volume_mountpoints:
                    source_volume_path = os.path.join(archived_volumes_path, volume_name)
                    target_mountpoint = volume_mountpoints[volume_name]
                    print(f"正在恢复 Docker 卷 '{volume_name}' 到: {target_mountpoint}")
                    
                    # 清理目标挂载点并复制文件
                    if os.path.isdir(target_mountpoint):
                        import shutil
                        # 递归复制，确保所有权和权限尽可能保留
                        shutil.copytree(source_volume_path, target_mountpoint, dirs_exist_ok=True)
                else:
                    print(f"警告: 备份中包含卷 '{volume_name}'，但未提供其恢复路径，将跳过。", file=sys.stderr)

        return True

    except (subprocess.CalledProcessError, FileNotFoundError, OSError) as e:
        print(f"错误：解压归档失败.\n{e}", file=sys.stderr)
        return False
    finally:
        import shutil
        shutil.rmtree(temp_extract_dir)


def get_archive_root_dir(archive_path: str, inspect_path: str = None) -> str | None:
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
                 print(f"警告: 备份中包含多个可能的根目录: {top_levels}。无法自动确定主数据目录。", file=sys.stderr)
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
