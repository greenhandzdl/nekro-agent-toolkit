#!/usr/bin/env python3
import argparse
import os
import sys

from module.install import install_agent
from module.update import update_agent

def main():
    """项目主入口，负责解析参数并分发到安装或更新模块。"""
    parser = argparse.ArgumentParser(
        description="Nekro Agent 安装与更新的统一管理工具。",
        epilog=(
            "用法示例:\n"
            "  python app.py --install ./na_data\n"
            "    # 在 ./na_data 目录中安装 Nekro Agent\n\n"
            "  python app.py --install ./na_data --with-napcat --dry-run\n"
            "    # 预演安装，并包含 NapCat 服务\n\n"
            "  python app.py --update ./na_data\n"
            "    # 对指定目录的安装执行部分更新\n\n"
            "  python app.py --upgrade ./na_data\n"
            "    # 对指定目录的安装执行完全更新（升级）\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', '--install', metavar='PATH', help='安装 Nekro Agent 到指定路径。')
    group.add_argument('-u', '--update', metavar='PATH', help='对指定路径的安装执行部分更新。')
    group.add_argument('-ua', '--upgrade', metavar='PATH', help='对指定路径的安装执行完全更新（升级）。')

    parser.add_argument('--with-napcat', action='store_true', help='与 --install 配合使用，部署 NapCat 服务。')
    parser.add_argument('--dry-run', action='store_true', help='与 --install 配合使用，执行预演，不进行实际安装。')
    parser.add_argument('-y', '--yes', action='store_true', help='自动确认所有提示，以非交互模式运行。')

    args = parser.parse_args()

    if args.install:
        install_agent(
            nekro_data_dir=args.install,
            with_napcat=args.with_napcat,
            dry_run=args.dry_run,
            non_interactive=args.yes
        )
    elif args.update:
        if not os.path.exists(args.update):
            print(f"错误: 目录 '{args.update}' 不存在。", file=sys.stderr)
            sys.exit(1)
        update_agent(
            nekro_data_dir=args.update,
            update_all=False,
            non_interactive=args.yes
        )
    elif args.upgrade:
        if not os.path.exists(args.upgrade):
            print(f"错误: 目录 '{args.upgrade}' 不存在。", file=sys.stderr)
            sys.exit(1)
        update_agent(
            nekro_data_dir=args.upgrade,
            update_all=True,
            non_interactive=args.yes
        )

if __name__ == "__main__":
    main()
