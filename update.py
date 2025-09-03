#!/usr/bin/env python3
import argparse
import os
import sys

from utils.helpers import command_exists, get_docker_compose_cmd
from utils.update_utils import update_nekro_agent_only, update_all_services

def main():
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