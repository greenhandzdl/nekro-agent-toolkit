"""Nekro Agent 更新脚本的辅助函数模块。

包含所有与更新流程相关的具体步骤函数。
"""
import os
import sys

from .helpers import run_sudo_command
from utils.i18n import get_message as _
from .docker_helpers import (
    docker_pull_image
)

def update_nekro_agent_only(docker_compose_cmd, nekro_data_dir):
    """仅更新 Nekro Agent 和沙盒镜像 (推荐)"""
    print(_("update_method_one"))

    os.chdir(nekro_data_dir)

    # 检查 .env 文件是否存在
    if not os.path.exists(".env"):
        print(_("error_env_file_not_exist"), file=sys.stderr)
        sys.exit(1)

    run_sudo_command("docker pull kromiose/nekro-agent-sandbox",
                     _("pulling_latest_sandbox"))

    run_sudo_command(f"{docker_compose_cmd} --env-file .env pull nekro_agent",
                     _("pulling_latest_nekro_agent"))

    run_sudo_command(f"{docker_compose_cmd} --env-file .env up --build -d nekro_agent",
                     _("rebuilding_nekro_agent"))

def update_all_services(docker_compose_cmd, nekro_data_dir):
    """更新所有镜像并重启容器"""
    print(_("update_method_two"))

    os.chdir(nekro_data_dir)

    # 检查 .env 文件是否存在
    if not os.path.exists(".env"):
        print(_("error_env_file_not_exist"), file=sys.stderr)
        sys.exit(1)

    run_sudo_command(f"{docker_compose_cmd} --env-file .env pull",
                     _("pulling_all_services"))

    run_sudo_command(f"{docker_compose_cmd} --env-file .env up --build -d",
                     _("restarting_all_services"))


def get_current_image_channel(docker_compose_path):
    """获取当前 docker-compose.yml 中的镜像标签。

    参数:
        docker_compose_path (str): docker-compose.yml 文件路径。

    返回:
        str: 'latest'、'preview' 或 None（如果未找到匹配的镜像）。
    """
    try:
        with open(docker_compose_path, 'r', encoding='utf-8') as f:
            content = f.read()

        if 'image: kromiose/nekro-agent:preview' in content:
            return 'preview'
        elif 'image: kromiose/nekro-agent:latest' in content:
            return 'latest'
        else:
            return None
    except Exception as e:
        print(_('error_read_compose_file', e))
        return None


def switch_image_channel(docker_compose_path, target_channel):
    """切换 docker-compose.yml 中的镜像标签。

    参数:
        docker_compose_path (str): docker-compose.yml 文件路径。
        target_channel (str): 目标 channel，'latest' 或 'preview'。

    返回:
        bool: 切换是否成功。
    """
    try:
        with open(docker_compose_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 确定当前镜像标签
        current_channel = get_current_image_channel(docker_compose_path)

        if current_channel is None:
            print(_('error_nekro_agent_image_not_found'))
            return False

        if current_channel == target_channel:
            print(_('channel_already_set', target_channel))
            return True

        # 执行替换
        if target_channel == 'preview':
            new_content = content.replace(
                'image: kromiose/nekro-agent:latest',
                'image: kromiose/nekro-agent:preview'
            )
        elif target_channel == 'latest':
            new_content = content.replace(
                'image: kromiose/nekro-agent:preview',
                'image: kromiose/nekro-agent:latest'
            )
        else:
            print(_('error_invalid_channel', target_channel))
            return False

        with open(docker_compose_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(_('channel_switched', current_channel, target_channel))
        return True

    except Exception as e:
        print(_('error_switch_channel', e))
        return False
