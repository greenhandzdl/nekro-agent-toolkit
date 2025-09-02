#!/usr/bin/env python3
import argparse
import os
import subprocess
import sys

def command_exists(command):
    """检查指定命令是否存在于系统中。"""
    return subprocess.run(f"which {command}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0

def get_docker_compose_cmd():
    """确定要使用的正确 docker-compose 命令（v1 或 v2）。"""
    if command_exists("docker-compose"):
        return "docker-compose"
    try:
        subprocess.run("docker compose version", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return "docker compose"
    except subprocess.CalledProcessError:
        return None

def run_sudo_command(command, description):
    """使用 sudo 运行命令并处理可能出现的错误。"""
    print(f"正在执行: {description}")
    try:
        subprocess.run(f"sudo {command}", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"错误: {description} 失败。\n{e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("错误: 'sudo' 命令未找到。请确保您有管理员权限。", file=sys.stderr)
        sys.exit(1)

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

def main():
    parser = argparse.ArgumentParser(description="Nekro Agent 更新工具")
    parser.add_argument("nekro_data_dir", nargs="?", default=os.getcwd(),
                        help="Nekro Agent 数据目录 (默认为当前目录)")
    parser.add_argument("--all", action="store_true",
                        help="更新所有服务，而不仅仅是 Nekro Agent")
    
    args = parser.parse_args()
    
    # 检查 docker 是否安装
    if not command_exists("docker"):
        print("错误: 未找到 'docker' 命令，请先安装 Docker。", file=sys.stderr)
        sys.exit(1)
    
    # 获取 docker-compose 命令
    docker_compose_cmd = get_docker_compose_cmd()
    if not docker_compose_cmd:
        print("错误: 未找到 'docker-compose' 或 'docker compose' 命令。", file=sys.stderr)
        sys.exit(1)
    
    # 检查数据目录是否存在
    if not os.path.exists(args.nekro_data_dir):
        print(f"错误: 指定的数据目录 '{args.nekro_data_dir}' 不存在。", file=sys.stderr)
        sys.exit(1)
    
    # 检查是否为有效的 Nekro Agent 目录（包含 docker-compose.yml）
    docker_compose_path = os.path.join(args.nekro_data_dir, "docker-compose.yml")
    if not os.path.exists(docker_compose_path):
        print(f"警告: 目录 '{args.nekro_data_dir}' 中未找到 docker-compose.yml 文件。")
        response = input("是否继续更新? (y/N): ")
        if response.lower() != 'y':
            print("取消更新。")
            sys.exit(0)
    
    # 执行相应的更新操作
    if args.all:
        update_all_services(docker_compose_cmd, args.nekro_data_dir)
    else:
        update_nekro_agent_only(docker_compose_cmd, args.nekro_data_dir)
    
    print("\n更新完成!")

if __name__ == "__main__":
    main()