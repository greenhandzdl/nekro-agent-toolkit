"""
Nekro Agent 更新脚本的辅助函数模块。

包含所有与更新流程相关的具体步骤函数。
"""
import os
import sys

from .helpers import run_sudo_command
from utils.i18n import get_message as _

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
