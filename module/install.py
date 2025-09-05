#!/usr/bin/env python3
import os
import sys
import argparse

# 将项目根目录添加到 sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.helpers import check_dependencies
from utils.install_utils import (
    setup_directories, configure_env_file, confirm_installation,
    download_compose_file, run_docker_operations, configure_firewall, print_summary
)
from utils.i18n import get_message as _

def install_agent(nekro_data_dir: str, with_napcat: bool = False, dry_run: bool = False, non_interactive: bool = False):
    """执行 Nekro Agent 的安装流程。

    Args:
        nekro_data_dir (str): 应用数据目录。
        with_napcat (bool): 是否部署 NapCat 服务。
        dry_run (bool): 是否为预演模式，仅生成配置文件。
        non_interactive (bool): 是否跳过交互式确认步骤。
    """
    original_cwd = os.getcwd()
    nekro_data_dir = os.path.abspath(nekro_data_dir)

    # --- 执行安装步骤 ---
    docker_compose_cmd = check_dependencies()
    setup_directories(nekro_data_dir)
    env_path = configure_env_file(nekro_data_dir, original_cwd)

    if dry_run:
        print(_("dry_run_complete", env_path))
        return
    
    if not non_interactive:
        confirm_installation()
    
    final_with_napcat = download_compose_file(with_napcat)
    run_docker_operations(docker_compose_cmd, env_path)
    configure_firewall(env_path, final_with_napcat)
    print_summary(env_path, final_with_napcat)

# --- 主执行函数 ---

def main():
    """主安装脚本的协调器，负责解析命令行参数并调用安装逻辑。"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_data_dir = os.path.join(script_dir, "na_data")
    
    parser = argparse.ArgumentParser(
        description=_('install_module_description'),
        epilog=_('install_module_examples'),
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('nekro_data_dir', nargs='?', default=default_data_dir, 
                        help=_('install_module_data_dir_help'))
    parser.add_argument('--with-napcat', action='store_true', 
                        help=_('install_module_with_napcat_help'))
    parser.add_argument('--dry-run', action='store_true', 
                        help=_('install_module_dry_run_help'))
    parser.add_argument('-y', '--yes', action='store_true', 
                        help=_('install_module_yes_help'))
    
    args = parser.parse_args()

    install_agent(
        nekro_data_dir=args.nekro_data_dir,
        with_napcat=args.with_napcat,
        dry_run=args.dry_run,
        non_interactive=args.yes
    )

if __name__ == "__main__":
    main()
