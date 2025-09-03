"""
备份与恢复功能的底层辅助函数。
"""
import os
import subprocess
import tarfile
import sys
import tempfile

from utils.helpers import command_exists

def create_archive(source_dir: str, dest_path_base: str) -> str | None:
    """创建一个目录的压缩归档文件。

    如果系统支持 zstd，则创建 .tar.zstd 文件；否则，创建 .tar 文件。
    会排除 logs/, uploads/ 目录和 .env.example 文件。

    Args:
        source_dir (str): 要归档的源目录。
        dest_path_base (str): 不带扩展名的目标归档文件基础路径。

    Returns:
        str | None: 成功则返回最终的归档文件路径，否则返回 None。
    """
    tar_path = f"{dest_path_base}.tar"
    archive_root_name = os.path.basename(source_dir)

    # 定义要排除的路径（相对于归档的根目录）
    excluded_paths = {
        os.path.join(archive_root_name, 'logs'),
        os.path.join(archive_root_name, 'uploads'),
        os.path.join(archive_root_name, '.env.example')
    }

    def exclude_filter(tarinfo: tarfile.TarInfo) -> tarfile.TarInfo | None:
        """Tarfile filter to exclude specific files/directories."""
        # 检查路径是否以任何一个被排除的路径为前缀
        if tarinfo.name in excluded_paths or any(tarinfo.name.startswith(p + '/') for p in excluded_paths):
            print(f"  - 正在排除: {tarinfo.name}")
            return None  # 返回 None 表示排除
        return tarinfo

    try:
        print(f"正在创建 tar 归档: {tar_path}...")
        with tarfile.open(tar_path, "w") as tar:
            tar.add(source_dir, arcname=archive_root_name, filter=exclude_filter)
        
        if command_exists("zstd"):
            zstd_path = f"{dest_path_base}.tar.zstd"
            print(f"检测到 zstd，正在压缩为: {zstd_path}...")
            subprocess.run(["zstd", "-f", "--quiet", tar_path, "-o", zstd_path], check=True)
            os.remove(tar_path)  # 删除临时的 tar 文件
            return zstd_path
        else:
            print("未检测到 zstd，仅创建 .tar 归档。")
            return tar_path

    except (subprocess.CalledProcessError, FileNotFoundError, OSError) as e:
        print(f"错误：创建归档失败.\n{e}", file=sys.stderr)
        # 清理可能产生的临时文件
        if os.path.exists(tar_path):
            os.remove(tar_path)
        return None

def extract_archive(archive_path: str, dest_dir: str) -> bool:
    """解压归档文件到指定目录。

    支持 .tar 和 .tar.zstd 格式。

    Args:
        archive_path (str): 要解压的归档文件路径。
        dest_dir (str): 目标解压目录。

    Returns:
        bool: 成功返回 True，失败返回 False。
    """
    try:
        if archive_path.endswith(".tar.zstd"):
            if not command_exists("zstd"):
                print("错误: 检测到 .tar.zstd 文件，但未找到 'zstd' 命令。", file=sys.stderr)
                print("请先安装 zstd，或手动解压为 .tar 文件后再试。", file=sys.stderr)
                return False
            
            tar_path = archive_path.removesuffix(".zstd")
            print(f"正在解压 .zstd 文件: {archive_path}...")
            subprocess.run(["zstd", "-d", "--quiet", archive_path, "-o", tar_path], check=True)
            
            print(f"正在提取 tar 文件: {tar_path}...")
            with tarfile.open(tar_path, "r") as tar:
                tar.extractall(path=dest_dir)
            os.remove(tar_path) # 删除临时的 tar 文件

        elif archive_path.endswith(".tar"):
            print(f"正在提取 tar 文件: {archive_path}...")
            with tarfile.open(archive_path, "r") as tar:
                tar.extractall(path=dest_dir)
        else:
            print(f"错误: 不支持的文件格式: {archive_path}", file=sys.stderr)
            return False
        
        return True

    except (subprocess.CalledProcessError, FileNotFoundError, OSError) as e:
        print(f"错误：解压归档失败.\n{e}", file=sys.stderr)
        return False

def get_archive_root_dir(archive_path: str) -> str | None:
    """读取归档文件并返回其中唯一的顶层目录名。"""
    temp_tar_path = None
    try:
        if archive_path.endswith(".tar.zstd"):
            if not command_exists("zstd"):
                return None
            # 创建一个临时文件来存放解压后的 .tar
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
            # 获取所有路径的顶层部分
            top_levels = {name.split(os.path.sep)[0] for name in members}
            if len(top_levels) == 1:
                return top_levels.pop()
            else:
                # 如果有多个顶层目录或文件，则认为没有唯一的根目录
                return None

    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None
    finally:
        # 清理临时文件
        if temp_tar_path and os.path.exists(temp_tar_path):
            os.remove(temp_tar_path)