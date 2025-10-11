#!/usr/bin/env python3
"""
根据平台自动切换 Docker 镜像加速器源。
- 自动检测平台（Linux/macOS/Windows）
- 自动查找 Docker 配置文件路径
- 读取 conf/docker_mirrors.py 里的 DOCKER_MIRRORS
- 备份原有 daemon.json
- 写入新 registry-mirrors 配置
- 提示用户重启 Docker 服务
"""
import os
import sys
import json
import shutil
import platform
from pathlib import Path

# 动态导入 conf/docker_mirrors.py
import importlib.util
spec = importlib.util.spec_from_file_location("docker_mirrors", os.path.join(os.path.dirname(__file__), "../conf/docker_mirrors.py"))
docker_mirrors = importlib.util.module_from_spec(spec)
spec.loader.exec_module(docker_mirrors)

MIRRORS = docker_mirrors.DOCKER_MIRRORS

# 平台相关配置路径
def get_daemon_json_path():
    sysstr = platform.system()
    if sysstr == "Windows":
        # 优先写入当前用户目录下 .docker/daemon.json
        return str(Path.home() / ".docker" / "daemon.json")
    else:
        # Linux/macOS
        return "/etc/docker/daemon.json"

def ensure_dir_exists(path):
    d = os.path.dirname(path)
    if not os.path.exists(d):
        os.makedirs(d, exist_ok=True)

def backup_file(path):
    if os.path.exists(path):
        backup = path + ".bak"
        shutil.copy2(path, backup)
        print(f"已备份原有配置到: {backup}")

def write_mirrors(path, mirrors):
    config = {"registry-mirrors": [f"https://{m}" if not m.startswith("http") else m for m in mirrors]}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"已写入新的 Docker 镜像加速器配置到: {path}")

def main():
    path = get_daemon_json_path()
    ensure_dir_exists(path)
    backup_file(path)
    write_mirrors(path, MIRRORS)
    print("请重启 Docker 服务以使新镜像源生效。")

if __name__ == "__main__":
    main()
