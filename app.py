#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys

from module.install import install_agent
from module.update import update_agent
from module.backup import backup_agent, recover_agent, recover_and_install_agent
from utils.helpers import get_command_prefix, get_version_info
from utils.i18n import get_message as _


def main():
    """项目主入口，负责解析参数并分发到安装、更新或备份恢复模块。"""
    cmd_prefix = get_command_prefix()
    
    parser = argparse.ArgumentParser(
        description=_('app_description'),
        epilog=_('app_examples', cmd_prefix, cmd_prefix, cmd_prefix, cmd_prefix, cmd_prefix, cmd_prefix),
        formatter_class=argparse.RawTextHelpFormatter
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-i', '--install', metavar='PATH', help=_('install_description'))
    group.add_argument('-u', '--update', metavar='PATH', help=_('update_description'))
    group.add_argument('-ua', '--upgrade', metavar='PATH', help=_('upgrade_description'))
    group.add_argument('-b', '--backup', nargs=2, metavar=('DATA_DIR', 'BACKUP_DIR'), help=_('backup_description'))
    group.add_argument('-r', '--recovery', nargs=2, metavar=('BACKUP_FILE', 'DATA_DIR'), help=_('recovery_description'))
    group.add_argument('-ri', '--recover-install', nargs=2, metavar=('BACKUP_FILE', 'INSTALL_DIR'), help=_('recover_install_description'))
    group.add_argument('-v', '--version', action='store_true', help=_('version_description'))

    # 安装选项
    parser.add_argument('--with-napcat', action='store_true', help=_('with_napcat_description'))
    parser.add_argument('--dry-run', action='store_true', help=_('dry_run_description'))
    
    #通用选项
    parser.add_argument('-y', '--yes', action='store_true', help=_('yes_description'))

    args = parser.parse_args()

    if args.version:
        print(get_version_info())
        return

    if args.install:
        install_agent(
            nekro_data_dir=args.install,
            with_napcat=args.with_napcat,
            dry_run=args.dry_run,
            non_interactive=args.yes
        )
    elif args.update:
        if not os.path.isdir(args.update):
            print(_("error_directory_not_exist", args.update), file=sys.stderr)
            sys.exit(1)
        update_agent(
            nekro_data_dir=args.update,
            update_all=False,
            non_interactive=args.yes
        )
    elif args.upgrade:
        if not os.path.isdir(args.upgrade):
            print(_("error_directory_not_exist", args.upgrade), file=sys.stderr)
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
