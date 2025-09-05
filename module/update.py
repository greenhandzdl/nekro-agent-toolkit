#!/usr/bin/env python3
import os
import sys
import argparse

# 将项目根目录添加到 sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.helpers import check_dependencies
from utils.update_utils import update_nekro_agent_only, update_all_services
from utils.i18n import get_message as _

def update_agent(nekro_data_dir: str, update_all: bool = False, non_interactive: bool = False):
    """执行 Nekro Agent 的更新流程。

    Args:
        nekro_data_dir (str): 应用数据目录。
        update_all (bool): 是否更新所有服务。
        non_interactive (bool): 是否跳过交互式确认步骤。
    """
    # 检查依赖
    docker_compose_cmd = check_dependencies()
    
    # 检查数据目录是否存在
    if not os.path.exists(nekro_data_dir):
        print(_("error_directory_not_exist", nekro_data_dir), file=sys.stderr)
        return
    
    # 检查是否为有效的 Nekro Agent 目录（包含 docker-compose.yml）
    docker_compose_path = os.path.join(nekro_data_dir, "docker-compose.yml")
    if not os.path.exists(docker_compose_path) and not non_interactive:
        print(_("warning_compose_file_not_found", nekro_data_dir))
        try:
            response = input(_("confirm_update"))
            if response.lower() != 'y':
                print(_("update_cancelled"))
                return
        except (EOFError, KeyboardInterrupt):
            print(f"\n{_('update_cancelled')}")
            return
    
    # 执行相应的更新操作
    if update_all:
        update_all_services(docker_compose_cmd, nekro_data_dir)
    else:
        update_nekro_agent_only(docker_compose_cmd, nekro_data_dir)
    
    print(f"\n{_('update_complete')}")

def main():
    """主更新脚本的协调器，负责解析命令行参数并调用更新逻辑。"""
    parser = argparse.ArgumentParser(
        description="Nekro Agent 更新工具",
        epilog=(
            "用法示例:\n"
            "  python update.py\n"
            "    # 在当前目录更新 Nekro Agent (推荐方式)\n\n"
            "  python update.py /srv/nekro\n"
            "    # 更新位于 /srv/nekro 的 Nekro Agent\n\n"
            "  python update.py --all\n"
            "    # 在默认目录更新所有服务 (包括数据库等)\n\n"
            "  python update.py /srv/nekro --all\n"
            "    # 组合使用：在指定目录更新所有服务"
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("nekro_data_dir", nargs="?", default=os.getcwd(),
                        help="Nekro Agent 数据目录 (默认为当前目录)")
    parser.add_argument("--all", action="store_true",
                        help="更新所有服务，而不仅仅是 Nekro Agent")
    parser.add_argument('-y', '--yes', action='store_true', 
                        help='自动确认所有提示，以非交互模式运行。')
    
    args = parser.parse_args()
    
    update_agent(
        nekro_data_dir=args.nekro_data_dir,
        update_all=args.all,
        non_interactive=args.yes
    )

if __name__ == "__main__":
    main()