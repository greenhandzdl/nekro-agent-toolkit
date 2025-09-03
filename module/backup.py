#!/usr/bin/env python3
import argparse
import os
import sys
import time

# 将项目根目录添加到 sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.backup_utils import create_archive, extract_archive, get_archive_root_dir
from module.install import install_agent

def backup_agent(data_dir: str, backup_dir: str):
    """备份 Nekro Agent 数据。"""
    print(f"开始备份目录: {data_dir}")
    if not os.path.isdir(data_dir):
        print(f"错误: 指定的数据目录 '{data_dir}' 不存在或不是一个目录。", file=sys.stderr)
        return

    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = int(time.time())
    backup_filename_base = f"na_backup_{timestamp}"
    dest_path_base = os.path.join(backup_dir, backup_filename_base)

    final_archive_path = create_archive(data_dir, dest_path_base)

    if final_archive_path:
        print(f"\n备份成功！备份文件已保存至:")
        print(final_archive_path)
    else:
        print("\n备份失败。")

def recover_agent(backup_file: str, data_dir: str, non_interactive: bool = False):
    """从备份文件恢复 Nekro Agent 数据。"""
    print(f"准备从备份文件恢复: {backup_file}")
    if not os.path.isfile(backup_file):
        print(f"错误: 指定的备份文件 '{backup_file}' 不存在或不是一个文件。", file=sys.stderr)
        return False
    
    if not backup_file.endswith(('.tar', '.tar.zstd')):
        print(f"错误: 无效的备份文件格式。只支持 '.tar' 和 '.tar.zstd'。", file=sys.stderr)
        return False

    os.makedirs(data_dir, exist_ok=True)

    if os.listdir(data_dir) and not non_interactive:
        print(f"警告: 目标目录 '{data_dir}' 非空。恢复操作可能会覆盖现有文件。")
        try:
            response = input("是否继续？ (y/N): ")
            if response.lower() != 'y':
                print("恢复操作已取消。")
                return False
        except (EOFError, KeyboardInterrupt):
            print("\n恢复操作已取消。")
            return False

    if extract_archive(backup_file, data_dir):
        print(f"\n恢复成功！数据已恢复至:")
        print(data_dir)
        return True
    else:
        print("\n恢复失败。")
        return False

def recover_and_install_agent(backup_file: str, install_dir: str, **kwargs):
    """恢复数据，然后在其上执行安装流程。"""
    dry_run = kwargs.get('dry_run', False)

    if dry_run:
        print("--- 开始恢复并安装流程 (Dry Run 模式) ---")
        print(f"[Dry Run] 将从备份文件恢复: {backup_file}")
        print(f"[Dry Run] 数据将被解压到: {install_dir}")
        print(f"[Dry Run] 将在解压后的数据上运行安装流程。")
        print("(未执行任何实际文件操作)")
        print("--- Dry Run 结束 ---")
        return

    print("--- 开始恢复并安装流程 ---")
    
    # 1. 确定解压出的根目录名
    print("正在分析备份文件...")
    archive_root = get_archive_root_dir(backup_file)
    if not archive_root:
        print("错误: 无法确定备份文件中的根目录，或备份文件格式不正确/已损坏。", file=sys.stderr)
        return
    print(f"备份中的根目录为: {archive_root}")

    # 2. 调用 recover_agent 进行解压
    # 在非交互模式下恢复到目标安装目录
    print(f"正在将备份恢复到: {install_dir}")
    if not recover_agent(backup_file, install_dir, non_interactive=True):
        print("恢复步骤失败，中止操作。", file=sys.stderr)
        return

    # 3. 确定解压后的数据目录的完整路径
    recovered_data_path = os.path.join(install_dir, archive_root)
    if not os.path.isdir(recovered_data_path):
        print(f"错误: 恢复后未找到预期的目录 '{recovered_data_path}'。", file=sys.stderr)
        return
    
    # 4. 在解压出的目录上执行安装流程
    print(f"\n--- 数据已恢复，开始在 {recovered_data_path} 上执行安装流程 ---")
    install_agent(nekro_data_dir=recovered_data_path, **kwargs)
    print("--- 恢复并安装流程结束 ---")


def main():
    """备份与恢复工具的独立命令行入口。"""
    parser = argparse.ArgumentParser(description="Nekro Agent 备份与恢复工具。")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-b', '--backup', nargs=2, metavar=('DATA_DIR', 'BACKUP_DIR'), 
                       help='备份指定的数据目录到目标备份目录。')
    group.add_argument('-r', '--recovery', nargs=2, metavar=('BACKUP_FILE', 'DATA_DIR'), 
                       help='从指定的备份文件恢复到目标数据目录。')

    args = parser.parse_args()

    if args.backup:
        data_dir, backup_dir = args.backup
        backup_agent(data_dir, backup_dir)
    elif args.recovery:
        backup_file, data_dir = args.recovery
        recover_agent(backup_file, data_dir)

if __name__ == "__main__":
    main()
