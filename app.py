#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys

from module.install import install_agent
from module.update import update_agent
from module.backup import backup_agent, recover_agent, recover_and_install_agent

def main():
    """项目主入口，负责解析参数并分发到安装、更新或备份恢复模块。"""
    parser = argparse.ArgumentParser(
        description="Nekro Agent 安装、更新与备份的统一管理工具。",
        epilog=(
            "用法示例:\n"
            "   # 如果你从源代码安装，你将直接运行python app.py，否则运行nekro-agent-toolkit。\n\n"
            "  python app.py --install ./na_data\n"
            "    # 在 ./na_data 目录中安装 Nekro Agent\n\n"
            "  python app.py --update ./na_data\n"
            "    # 对指定目录的安装执行部分更新\n\n"
            "  python app.py --upgrade ./na_data\n"
            "    # 对指定目录的安装执行完全更新（升级）\n\n"
            "  python app.py --backup ./na_data ./backups\n"
            "    # 备份 na_data 目录到 backups 文件夹\n\n"
            "  python app.py --recovery ./backups/na_backup_123.tar.zstd ./na_data_new\n"
            "    # 从备份文件恢复到 na_data_new 目录\n\n"
            "  python app.py --recover-install ./backup.tar.zst ./restored_install\n"
            "    # 从备份恢复数据，并在此基础上执行安装"
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', '--install', metavar='PATH', help='安装 Nekro Agent 到指定路径。')
    group.add_argument('-u', '--update', metavar='PATH', help='对指定路径的安装执行部分更新。')
    group.add_argument('-ua', '--upgrade', metavar='PATH', help='对指定路径的安装执行完全更新（升级）。')
    group.add_argument('-b', '--backup', nargs=2, metavar=('DATA_DIR', 'BACKUP_DIR'), help='备份数据目录到指定文件夹。')
    group.add_argument('-r', '--recovery', nargs=2, metavar=('BACKUP_FILE', 'DATA_DIR'), help='从备份文件恢复到指定数据目录。')
    group.add_argument('-ri', '--recover-install', nargs=2, metavar=('BACKUP_FILE', 'INSTALL_DIR'), help='恢复并安装。这会解压备份文件到目标目录，然后在此之上运行安装流程。')

    # 安装选项
    parser.add_argument('--with-napcat', action='store_true', help='与 --install 或 --recover-install 配合使用，部署 NapCat 服务。')
    parser.add_argument('--dry-run', action='store_true', help='与 --install 或 --recover-install 配合使用，执行预演。')
    
    #通用选项
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
        if not os.path.isdir(args.update):
            print(f"错误: 目录 '{args.update}' 不存在。", file=sys.stderr)
            sys.exit(1)
        update_agent(
            nekro_data_dir=args.update,
            update_all=False,
            non_interactive=args.yes
        )
    elif args.upgrade:
        if not os.path.isdir(args.upgrade):
            print(f"错误: 目录 '{args.upgrade}' 不存在。", file=sys.stderr)
            sys.exit(1)
        update_agent(
            nekro_data_dir=args.upgrade,
            update_all=True,
            non_interactive=args.yes
        )
    elif args.backup:
        data_dir, backup_dir = args.backup
        backup_agent(data_dir, backup_dir)
    elif args.recovery:
        backup_file, data_dir = args.recovery
        recover_agent(backup_file, data_dir, non_interactive=args.yes)
    elif args.recover_install:
        backup_file, install_dir = args.recover_install
        recover_and_install_agent(
            backup_file=backup_file, 
            install_dir=install_dir,
            with_napcat=args.with_napcat,
            dry_run=args.dry_run,
            non_interactive=args.yes
        )

if __name__ == "__main__":
    main()
