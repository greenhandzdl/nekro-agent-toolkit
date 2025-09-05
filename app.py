#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys

from module.install import install_agent
from module.update import update_agent
from module.backup import backup_agent, recover_agent, recover_and_install_agent
from utils.helpers import get_command_prefix, get_version_info, set_default_data_dir, get_default_data_dir, show_default_data_dir, confirm_use_default_data_dir
from utils.i18n import get_message as _


def main():
    """项目主入口，负责解析参数并分发到安装、更新或备份恢复模块。"""
    cmd_prefix = get_command_prefix()
    
    parser = argparse.ArgumentParser(
        description=_('app_description'),
        epilog=_('app_examples', cmd_prefix, cmd_prefix, cmd_prefix, cmd_prefix, cmd_prefix, cmd_prefix),
        formatter_class=argparse.RawTextHelpFormatter
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--install', nargs='?', const='', metavar='PATH', help=_('install_description'))
    group.add_argument('-u', '--update', metavar='PATH', help=_('update_description'))
    group.add_argument('-ua', '--upgrade', metavar='PATH', help=_('upgrade_description'))
    group.add_argument('-b', '--backup', nargs='*', metavar='ARG', help=_('backup_description'))
    group.add_argument('-r', '--recovery', nargs='*', metavar='ARG', help=_('recovery_description'))
    group.add_argument('-ri', '--recover-install', nargs=2, metavar=('BACKUP_FILE', 'INSTALL_DIR'), help=_('recover_install_description'))
    group.add_argument('-v', '--version', action='store_true', help=_('version_description'))
    
    # 独立的配置管理参数
    parser.add_argument('-sd', '--set-data', nargs='?', const='', metavar='PATH', help=_('set_data_description'))

    # 安装选项
    parser.add_argument('--with-napcat', action='store_true', help=_('with_napcat_description'))
    parser.add_argument('--dry-run', action='store_true', help=_('dry_run_description'))
    
    #通用选项
    parser.add_argument('-y', '--yes', action='store_true', help=_('yes_description'))

    args = parser.parse_args()

    if args.version:
        print(get_version_info())
        return

    if args.set_data is not None:
        if args.set_data == '':
            # 如果没有提供路径，显示当前设置
            show_default_data_dir()
        else:
            # 设置新的默认数据目录
            set_default_data_dir(args.set_data)
        return

    # 检查是否提供了必需的主命令参数
    main_commands = [args.install, args.update, args.upgrade, args.backup, args.recovery, args.recover_install]
    if not any(cmd is not None for cmd in main_commands):
        parser.error("必须提供一个主命令参数")

    # 获取默认数据目录
    default_data_dir = get_default_data_dir()

    if args.install is not None:
        # 处理安装命令
        install_path = args.install
        if install_path == '' and default_data_dir:
            # 使用默认目录
            equivalent_cmd = f"{cmd_prefix} -i {default_data_dir}"
            if not args.yes and not confirm_use_default_data_dir("install", equivalent_cmd):
                print(_("operation_cancelled"))
                return
            install_path = default_data_dir
        elif install_path == '':
            print(_("error_prefix") + " " + _("install_description"))
            sys.exit(1)
            
        install_agent(
            nekro_data_dir=install_path,
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
    elif args.backup is not None:
        # 处理备份命令
        if len(args.backup) == 2:
            # 正常的两个参数
            data_dir, backup_dir = args.backup
        elif len(args.backup) == 1 and default_data_dir:
            # 只有一个参数，使用默认数据目录
            backup_dir = args.backup[0]
            equivalent_cmd = f"{cmd_prefix} -b {default_data_dir} {backup_dir}"
            if not args.yes and not confirm_use_default_data_dir("backup", equivalent_cmd):
                print(_("operation_cancelled"))
                return
            data_dir = default_data_dir
        else:
            print(_("error_prefix") + " " + _("backup_description"))
            sys.exit(1)
            
        backup_agent(data_dir, backup_dir)
    elif args.recovery is not None:
        # 处理恢复命令
        if len(args.recovery) == 2:
            # 正常的两个参数
            backup_file, data_dir = args.recovery
        elif len(args.recovery) == 1 and default_data_dir:
            # 只有一个参数，使用默认数据目录
            backup_file = args.recovery[0]
            equivalent_cmd = f"{cmd_prefix} -r {backup_file} {default_data_dir}"
            if not args.yes and not confirm_use_default_data_dir("recovery", equivalent_cmd):
                print(_("operation_cancelled"))
                return
            data_dir = default_data_dir
        else:
            print(_("error_prefix") + " " + _("recovery_description"))
            sys.exit(1)
            
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
