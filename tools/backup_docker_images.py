#!/usr/bin/env python3
"""
简化版：只导出指定的镜像（会尝试 docker pull 确保存在），并输出一个压缩的 tar.gz
默认导出镜像：
  - mlikiowa/napcat-docker:latest
  - kromiose/nekro-agent-sandbox:latest
  - kromiose/nekro-agent:latest
  - qdrant/qdrant:latest
  - postgres:14

用法：
  python3 tools/backup_docker_images.py [--output FILE]

这个脚本尽量保持简单：自动 pull 每个镜像，然后一次性 docker save 并写入 gzip 文件（流式写入，节省内存）。
"""

import argparse
import gzip
import os
import shutil
import subprocess
import sys
from typing import List

IMAGES: List[str] = [
    "mlikiowa/napcat-docker:latest",
    # "kromiose/nekro-agent-sandbox:latest",
    "kromiose/nekro-agent:latest",
    "qdrant/qdrant:latest",
    "postgres:14",
]

DEFAULT_OUTPUT = "docker-images-backup.tar.gz"


def parse_args():
    p = argparse.ArgumentParser(description="简化的 Docker 镜像导出脚本")
    p.add_argument("--output", "-o", default=DEFAULT_OUTPUT, help="输出 .tar.gz 文件路径")
    return p.parse_args()


def ensure_docker_available() -> None:
    if shutil.which("docker") is None:
        print("❌ Docker 未安装或不可用，请先安装 Docker 并确保在 PATH 中。")
        sys.exit(1)


def pull_images(images: List[str]) -> None:
    for img in images:
        print(f"📥 拉取镜像：{img}（如果已存在会跳过或更新）")
        try:
            subprocess.run(["docker", "pull", img], check=True)
        except subprocess.CalledProcessError as e:
            print(f"⚠️ 拉取镜像 {img} 失败：{e}")
            print("继续尝试导出已存在的镜像（如果没有则会在 docker save 时失败）")


def stream_save_and_gzip(images: List[str], output_file: str) -> int:
    cmd = ["docker", "save"] + images
    print("📦 正在执行：", " ".join(cmd))
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print("❌ 无法找到 docker 命令。")
        return 2

    try:
        with gzip.open(output_file, "wb") as gz:
            assert proc.stdout is not None
            while True:
                chunk = proc.stdout.read(65536)
                if not chunk:
                    break
                gz.write(chunk)
    except Exception as e:
        proc.kill()
        proc.wait()
        print("❌ 导出/压缩过程中出错：", e)
        return 3

    proc_stdout, proc_stderr = proc.communicate()
    if proc.returncode != 0:
        print("❌ docker save 返回非零码，错误信息：")
        try:
            print(proc_stderr.decode(errors="ignore"))
        except Exception:
            pass
    return proc.returncode


def main() -> None:
    args = parse_args()
    output_file = args.output

    ensure_docker_available()

    # 尝试拉取镜像以确保存在
    pull_images(IMAGES)

    # 删除已有文件以避免追加
    if os.path.exists(output_file):
        print(f"ℹ️ 输出文件已存在，正在覆盖：{output_file}")
        try:
            os.remove(output_file)
        except Exception as e:
            print("❌ 无法删除现有输出文件：", e)
            sys.exit(1)

    print(f"🔁 开始导出并压缩到 {output_file} ...")
    rc = stream_save_and_gzip(IMAGES, output_file)

    if rc == 0:
        size = None
        try:
            size = os.path.getsize(output_file)
        except Exception:
            pass
        if size:
            print(f"✅ 导出完成：{output_file}，大小：{size} 字节")
        else:
            print(f"✅ 导出完成：{output_file}")
        print("提示：使用 ./import-images.sh <file> 来导入（或直接运行：gunzip -c file | docker load）")
        sys.exit(0)
    else:
        print("❌ 导出失败，返回码：", rc)
        sys.exit(1)


if __name__ == "__main__":
    main()

