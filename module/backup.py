#!/usr/bin/env python3
import argparse
import os
import sys
import time

# 将项目根目录添加到 sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.backup_utils import create_archive, extract_archive, get_archive_root_dir, get_docker_volumes, get_docker_volumes_for_recovery, discover_docker_volumes_by_pattern
from module.install import install_agent
from utils.i18n import get_message as _
from conf.backup_settings import DOCKER_VOLUMES_TO_BACKUP, DOCKER_VOLUME_SUFFIXES

def get_volumes_to_backup():
    """获取需要备份的 Docker 卷列表。
    
    优先使用动态发现，如果没有发现卷则回退到静态配置。
    
    Returns:
        list[str]: 需要备份的 Docker 卷名列表。
    """
    # 先尝试动态发现
    discovered_volumes = discover_docker_volumes_by_pattern(
        suffixes=DOCKER_VOLUME_SUFFIXES
    )
    
    if discovered_volumes:
        print(f"  - {_('discovered_docker_volumes', len(discovered_volumes))}")
        return discovered_volumes
    else:
        print(f"  - {_('no_matching_volumes_using_static', DOCKER_VOLUMES_TO_BACKUP)}")
        return DOCKER_VOLUMES_TO_BACKUP

def backup_agent(data_dir: str, backup_dir: str):
    """备份 Nekro Agent 数据及相关的 Docker 卷。"""
    print(_("starting_backup", data_dir))
    
    source_paths = {}

    # 1. 处理主数据目录
    # 如果是备份当前目录，特殊处理以避免裸目录
    if os.path.abspath(data_dir) == os.path.abspath('.'):
        parent_dir = os.path.dirname(os.getcwd())
        current_folder_name = os.path.basename(os.getcwd())
        # 实际添加的源是当前目录，但在归档中它位于其父目录下
        source_paths[os.getcwd()] = current_folder_name
        print(f"  - {_('archiving_current_directory', current_folder_name)}")
    else:
        if not os.path.isdir(data_dir):
            print(_("error_data_dir_not_exist", data_dir), file=sys.stderr)
            return
        arcname = os.path.basename(os.path.normpath(data_dir))
        source_paths[data_dir] = arcname

    # 2. 获取并添加 Docker 卷路径
    print(f"\n{_('finding_docker_volumes_backup')}")
    volumes_to_backup = get_volumes_to_backup()
    volume_paths = get_docker_volumes(volumes_to_backup)
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
    print(f"\n{_('creating_archive')}")
    final_archive_path = create_archive(source_paths, dest_path_base)

    if final_archive_path:
        print(f"\n{_('backup_success')}")
        print(final_archive_path)
    else:
        print(f"\n{_('recovery_failed')}")

def recover_agent(backup_file: str, data_dir: str, non_interactive: bool = False):
    """从备份文件恢复 Nekro Agent 数据和 Docker 卷。"""
    print(_('preparing_recovery_from_backup', backup_file))
    if not os.path.isfile(backup_file):
        print(_("error_backup_file_not_exist", backup_file), file=sys.stderr)
        return False
    
    if not backup_file.endswith(('.tar', '.tar.zstd')):
        print(_("error_invalid_backup_format"), file=sys.stderr)
        return False

    os.makedirs(data_dir, exist_ok=True)

    # 检查目标数据目录是否为空
    if os.listdir(data_dir) and not non_interactive:
        print(_("warning_data_dir_not_empty", data_dir))
        if not get_user_confirmation():
            return False

    # 1. 查找需要恢复的 Docker 卷
    print(f"\n{_('finding_docker_volumes_recovery')}")
    volumes_to_backup = get_volumes_to_backup()
    available_volumes = get_docker_volumes_for_recovery(volumes_to_backup)
    
    if available_volumes and not non_interactive:
        print(_("warning_docker_volumes_will_overwrite"))
        for name in available_volumes:
            print(f"  - {name}")
        if not get_user_confirmation():
            # 如果用户取消，可以选择只恢复数据，不恢复卷
            print(_("warning_skip_data_restore"))
            available_volumes = {}

    # 2. 执行恢复
    print(f"\n{_('starting_extraction')}")
    # 传递卷名映射，extract_archive 会根据系统类型选择恢复方式
    volume_mountpoints = {name: info for name, info in available_volumes.items()}
    if extract_archive(backup_file, data_dir, volume_mountpoints=volume_mountpoints):
        print(_("recovery_success", data_dir))
        if volume_mountpoints:
            print(_("docker_volumes_restored"))
        return True
    else:
        print(f"\n{_('recovery_failed')}")
        return False

def get_user_confirmation() -> bool:
    """获取用户的确认。"""
    try:
        response = input(_('confirm_continue'))
        if response.lower() != 'y':
            print(_("operation_cancelled"))
            return False
        return True
    except (EOFError, KeyboardInterrupt):
        print(f"\n{_('operation_cancelled')}")
        return False

def recover_and_install_agent(backup_file: str, install_dir: str, **kwargs):
    """恢复数据，然后在其上执行安装流程。"""
    dry_run = kwargs.get('dry_run', False)

    if dry_run:
        print(_("dry_run_mode_start"))
        print(_('dry_run_will_restore_from', backup_file))
        print(_('dry_run_data_extract_to', install_dir))
        print(_('dry_run_docker_volumes_restore'))
        print(_('dry_run_install_on_extracted'))
        print(_("dry_run_not_executed"))
        print(_("dry_run_mode_end"))
        return

    print(_("recovery_install_start"))
    
    # 1. 确定解压出的数据根目录名
    print(_("analyzing_backup_file"))
    archive_root = get_archive_root_dir(backup_file)
    if not archive_root:
        print(_("warning_cannot_determine_data_dir"), file=sys.stderr)
        # 即使没有主数据目录，也可能需要恢复卷，所以流程继续

    # 2. 调用 recover_agent 进行解压 (非交互模式)
    print(_('restoring_backup_to', install_dir))
    if not recover_agent(backup_file, install_dir, non_interactive=True):
        print(_('recovery_step_failed'), file=sys.stderr)
        return

    # 3. 确定解压后的数据目录的完整路径
    if archive_root:
        recovered_data_path = os.path.join(install_dir, archive_root)
        if not os.path.isdir(recovered_data_path):
            print(_("expected_directory_not_found", recovered_data_path), file=sys.stderr)
            # 即使数据目录恢复失败，安装流程可能仍需继续（例如，如果它能处理空目录）
        
        # 4. 在解压出的目录上执行安装流程
        print(_("recovery_install_data_restored", recovered_data_path))
        install_agent(nekro_data_dir=recovered_data_path, **kwargs)
    else:
        # 如果没有找到数据根目录，可能需要一个默认或空的目录来运行安装
        print(_("recovery_install_no_data_dir"))
        install_agent(nekro_data_dir=install_dir, **kwargs)

    print(_("recovery_install_end"))


def main():
    """备份与恢复工具的独立命令行入口。"""
    parser = argparse.ArgumentParser(description=_('backup_module_description'))
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-b', '--backup', nargs=2, metavar=('DATA_DIR', 'BACKUP_DIR'), 
                       help=_('backup_module_help'))
    group.add_argument('-r', '--recovery', nargs=2, metavar=('BACKUP_FILE', 'DATA_DIR'), 
                       help=_('recovery_module_help'))

    args = parser.parse_args()

    if args.backup:
        data_dir, backup_dir = args.backup
        backup_agent(data_dir, backup_dir)
    elif args.recovery:
        backup_file, data_dir = args.recovery
        recover_agent(backup_file, data_dir)

if __name__ == "__main__":
    main()