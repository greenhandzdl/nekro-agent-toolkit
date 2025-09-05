#!/usr/bin/env python3
import argparse
import os
import sys
import time

# 将项目根目录添加到 sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.backup_utils import create_archive, extract_archive, get_archive_root_dir, get_docker_volumes, get_docker_volumes_for_recovery
from module.install import install_agent

# 定义需要备份的 Docker 卷
DOCKER_VOLUMES_TO_BACKUP = ["nekro_postgres_data", "nekro_qdrant_data"]

def backup_agent(data_dir: str, backup_dir: str):
    """备份 Nekro Agent 数据及相关的 Docker 卷。"""
    print(f"开始备份 Nekro Agent, 数据目录: {data_dir}")
    
    source_paths = {}

    # 1. 处理主数据目录
    # 如果是备份当前目录，特殊处理以避免裸目录
    if os.path.abspath(data_dir) == os.path.abspath('.'):
        parent_dir = os.path.dirname(os.getcwd())
        current_folder_name = os.path.basename(os.getcwd())
        # 实际添加的源是当前目录，但在归档中它位于其父目录下
        source_paths[os.getcwd()] = current_folder_name
        print(f"  - 将当前目录 '.' 归档为 '{current_folder_name}'")
    else:
        if not os.path.isdir(data_dir):
            print(f"错误: 指定的数据目录 '{data_dir}' 不存在或不是一个目录。", file=sys.stderr)
            return
        arcname = os.path.basename(os.path.normpath(data_dir))
        source_paths[data_dir] = arcname

    # 2. 获取并添加 Docker 卷路径
    print("\n正在查找需要备份的 Docker 卷...")
    volume_paths = get_docker_volumes(DOCKER_VOLUMES_TO_BACKUP)
    for name, path_or_method in volume_paths.items():
        if path_or_method == "container_backup":
            # 使用容器方式备份的卷
            source_paths[f"volumes/{name}"] = "container_backup"
        elif os.path.isdir(path_or_method):
            # 直接可访问的卷路径 (Linux)
            source_paths[path_or_method] = os.path.join('volumes', name)
        # 如果卷不可用，get_docker_volumes 已经打印了警告

    if len(source_paths) == 1 and list(source_paths.keys())[0] == data_dir and not os.path.isdir(data_dir):
        # 如果只有数据目录一个源，且该目录无效，则终止
        return

    # 3. 创建备份目录和文件名
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = int(time.time())
    backup_filename_base = f"na_backup_{timestamp}"
    dest_path_base = os.path.join(backup_dir, backup_filename_base)

    # 4. 执行备份
    print("\n开始创建归档文件...")
    final_archive_path = create_archive(source_paths, dest_path_base)

    if final_archive_path:
        print(f"\n备份成功！备份文件已保存至:")
        print(final_archive_path)
    else:
        print("\n备份失败。")

def recover_agent(backup_file: str, data_dir: str, non_interactive: bool = False):
    """从备份文件恢复 Nekro Agent 数据和 Docker 卷。"""
    print(f"准备从备份文件恢复: {backup_file}")
    if not os.path.isfile(backup_file):
        print(f"错误: 指定的备份文件 '{backup_file}' 不存在或不是一个文件。", file=sys.stderr)
        return False
    
    if not backup_file.endswith(('.tar', '.tar.zstd')):
        print(f"错误: 无效的备份文件格式。只支持 '.tar' 和 '.tar.zstd'。", file=sys.stderr)
        return False

    os.makedirs(data_dir, exist_ok=True)

    # 检查目标数据目录是否为空
    if os.listdir(data_dir) and not non_interactive:
        print(f"警告: 目标数据目录 '{data_dir}' 非空。恢复操作可能会覆盖现有文件。")
        if not get_user_confirmation():
            return False

    # 1. 查找需要恢复的 Docker 卷
    print("\n正在查找需要恢复的 Docker 卷...")
    available_volumes = get_docker_volumes_for_recovery(DOCKER_VOLUMES_TO_BACKUP)
    
    if available_volumes and not non_interactive:
        print("警告: 将恢复以下 Docker 卷，这会覆盖卷中的现有内容:")
        for name in available_volumes:
            print(f"  - {name}")
        if not get_user_confirmation():
            # 如果用户取消，可以选择只恢复数据，不恢复卷
            print("将仅恢复数据目录，跳过 Docker 卷的恢复。")
            available_volumes = {}

    # 2. 执行恢复
    print("\n开始解压和恢复文件...")
    # 传递卷名映射，extract_archive 会根据系统类型选择恢复方式
    volume_mountpoints = {name: info for name, info in available_volumes.items()}
    if extract_archive(backup_file, data_dir, volume_mountpoints=volume_mountpoints):
        print(f"\n恢复成功！数据已恢复至: {data_dir}")
        if volume_mountpoints:
            print("Docker 卷也已恢复。")
        return True
    else:
        print("\n恢复失败。")
        return False

def get_user_confirmation() -> bool:
    """获取用户的确认。"""
    try:
        response = input("是否继续？ (y/N): ")
        if response.lower() != 'y':
            print("操作已取消。" )
            return False
        return True
    except (EOFError, KeyboardInterrupt):
        print("\n操作已取消。" )
        return False

def recover_and_install_agent(backup_file: str, install_dir: str, **kwargs):
    """恢复数据，然后在其上执行安装流程。"""
    dry_run = kwargs.get('dry_run', False)

    if dry_run:
        print("--- 开始恢复并安装流程 (Dry Run 模式) ---")
        print(f"[Dry Run] 将从备份文件恢复: {backup_file}")
        print(f"[Dry Run] 数据将被解压到: {install_dir}")
        print(f"[Dry Run] Docker 卷将被恢复（如果存在于备份中）。")
        print(f"[Dry Run] 将在解压后的数据上运行安装流程。" )
        print("(未执行任何实际文件操作)")
        print("--- Dry Run 结束 ---")
        return

    print("--- 开始恢复并安装流程 ---")
    
    # 1. 确定解压出的数据根目录名
    print("正在分析备份文件...")
    archive_root = get_archive_root_dir(backup_file)
    if not archive_root:
        print("警告: 无法在备份文件中确定主数据目录，或备份中只包含 Docker 卷。", file=sys.stderr)
        # 即使没有主数据目录，也可能需要恢复卷，所以流程继续

    # 2. 调用 recover_agent 进行解压 (非交互模式)
    print(f"正在将备份恢复到: {install_dir}")
    if not recover_agent(backup_file, install_dir, non_interactive=True):
        print("恢复步骤失败，中止操作。", file=sys.stderr)
        return

    # 3. 确定解压后的数据目录的完整路径
    if archive_root:
        recovered_data_path = os.path.join(install_dir, archive_root)
        if not os.path.isdir(recovered_data_path):
            print(f"错误: 恢复后未找到预期的目录 '{recovered_data_path}'。", file=sys.stderr)
            # 即使数据目录恢复失败，安装流程可能仍需继续（例如，如果它能处理空目录）
        
        # 4. 在解压出的目录上执行安装流程
        print(f"\n--- 数据已恢复，开始在 {recovered_data_path} 上执行安装流程 ---")
        install_agent(nekro_data_dir=recovered_data_path, **kwargs)
    else:
        # 如果没有找到数据根目录，可能需要一个默认或空的目录来运行安装
        print("\n--- 未恢复特定数据目录，将在目标安装目录上执行安装流程 ---")
        install_agent(nekro_data_dir=install_dir, **kwargs)

    print("--- 恢复并安装流程结束 ---")


def main():
    """备份与恢复工具的独立命令行入口。"""
    parser = argparse.ArgumentParser(description="Nekro Agent 备份与恢复工具。" )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-b', '--backup', nargs=2, metavar=('DATA_DIR', 'BACKUP_DIR'), 
                       help='备份指定的数据目录和相关 Docker 卷到目标备份目录。')
    group.add_argument('-r', '--recovery', nargs=2, metavar=('BACKUP_FILE', 'DATA_DIR'), 
                       help='从指定的备份文件恢复数据和 Docker 卷到目标目录。')

    args = parser.parse_args()

    if args.backup:
        data_dir, backup_dir = args.backup
        backup_agent(data_dir, backup_dir)
    elif args.recovery:
        backup_file, data_dir = args.recovery
        recover_agent(backup_file, data_dir)

if __name__ == "__main__":
    main()