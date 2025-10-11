#!/usr/bin/env python3
"""
根据平台自动切换 Docker 镜像加速器源（release 版，无外部依赖 conf/docker_mirrors.py）。
- 自动检测平台（Linux/macOS/Windows）
- 自动查找 Docker 配置文件路径
- 备份原有 daemon.json
- 写入新 registry-mirrors 配置
- 提示用户重启 Docker 服务
"""
import os
import json
import shutil
import platform
from pathlib import Path

# 直接内置镜像源
MIRRORS = [
    "https://docker.xuanyuan.me",
    "https://docker.1ms.run",
    "https://docker.ama.moe"
]

def get_daemon_json_path():
    sysstr = platform.system()
    if sysstr == "Windows":
        return str(Path.home() / ".docker" / "daemon.json")
    else:
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

