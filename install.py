#!/usr/bin/env python3
import argparse
import os
import sys

from utils.install_utils import (
    check_dependencies, setup_directories, configure_env_file, confirm_installation,
    download_compose_file, run_docker_operations, configure_firewall, print_summary
)

# --- 主执行函数 ---

def main():
    """主安装脚本的协调器，负责按顺序调用所有安装步骤。"""
    original_cwd = os.getcwd()
    
    # --- 参数解析 ---
    parser = argparse.ArgumentParser(
        description="Nekro Agent 安装与管理脚本",
        epilog="用法示例:\n" 
               "  python install.py                # 在当前目录安装\n" 
               "  python install.py /srv/nekro     # 在指定目录 /srv/nekro 安装\n" 
               "  python install.py --with-napcat  # 安装并启用 NapCat\n" 
               "  python install.py --dry-run      # 仅生成 .env 文件，不执行安装",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('nekro_data_dir', nargs='?', default=os.getcwd(), 
                        help='Nekro Agent 的应用数据目录。\n默认为当前工作目录。')
    parser.add_argument('--with-napcat', action='store_true', 
                        help='同时部署 NapCat 服务。')
    parser.add_argument('--dry-run', action='store_true', 
                        help='预演模式：仅生成 .env 文件，不执行实际安装。')
    args = parser.parse_args()

    # --- 路径处理 ---
    nekro_data_dir = os.path.abspath(args.nekro_data_dir)

    # --- 执行安装步骤 ---
    docker_compose_cmd = check_dependencies()
    setup_directories(nekro_data_dir)
    env_path = configure_env_file(nekro_data_dir, original_cwd)

    if args.dry_run:
        print(f"\n--dry-run 完成。\n.env 文件已在 {env_path} 生成。\n未执行任何安装操作。\n")
        sys.exit(0)
    
    confirm_installation()
    
    with_napcat = download_compose_file(args.with_napcat)
    run_docker_operations(docker_compose_cmd, env_path)
    configure_firewall(env_path, with_napcat)
    print_summary(env_path, with_napcat)

if __name__ == "__main__":
    main()
