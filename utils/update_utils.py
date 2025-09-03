"""
Nekro Agent 更新脚本的辅助函数模块。

包含所有与更新流程相关的具体步骤函数。
"""
import os
import sys

from .helpers import run_sudo_command

def update_nekro_agent_only(docker_compose_cmd, nekro_data_dir):
    """仅更新 Nekro Agent 和沙盒镜像 (推荐)"""
    print("正在执行更新方式一：仅更新 Nekro Agent 和沙盒镜像")
    
    os.chdir(nekro_data_dir)
    
    # 检查 .env 文件是否存在
    if not os.path.exists(".env"):
        print("错误: .env 文件不存在，请检查 Nekro Agent 是否已正确安装。", file=sys.stderr)
        sys.exit(1)
    
    run_sudo_command("docker pull kromiose/nekro-agent-sandbox", 
                     "拉取最新的 kromiose/nekro-agent-sandbox 镜像")
    
    run_sudo_command(f"{docker_compose_cmd} --env-file .env pull nekro_agent", 
                     "拉取最新的 nekro_agent 镜像")
    
    run_sudo_command(f"{docker_compose_cmd} --env-file .env up --build -d nekro_agent", 
                     "重新构建并启动 nekro_agent 容器")

def update_all_services(docker_compose_cmd, nekro_data_dir):
    """更新所有镜像并重启容器"""
    print("正在执行更新方式二：更新所有镜像并重启容器")
    
    os.chdir(nekro_data_dir)
    
    # 检查 .env 文件是否存在
    if not os.path.exists(".env"):
        print("错误: .env 文件不存在，请检查 Nekro Agent 是否已正确安装。", file=sys.stderr)
        sys.exit(1)
    
    run_sudo_command(f"{docker_compose_cmd} --env-file .env pull", 
                     "拉取所有服务的最新镜像")
    
    run_sudo_command(f"{docker_compose_cmd} --env-file .env up --build -d", 
                     "重新构建并启动所有服务")
