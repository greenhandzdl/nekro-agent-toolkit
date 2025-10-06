#!/usr/bin/env python3
"""
import_docker_images.py

从 gzip 压缩的 docker save 输出文件导入镜像（stream 解压并写入 docker load）。
默认输入文件：docker-images-backup.tar.gz

用法示例：
  python3 tools/import_docker_images.py
  python3 tools/import_docker_images.py --input my-backup.tar.gz --remove-after

功能：
 - 检查 docker 是否可用
 - 检查输入文件存在
 - 以流方式打开 gzip 并把内容写入 `docker load` 的 stdin（不解压到磁盘）
 - 可选导入后列出镜像和删除源文件
"""

import argparse
import gzip
import os
import shutil
import subprocess
import sys
from typing import Optional

DEFAULT_INPUT = "docker-images-backup.tar.gz"


def parse_args():
    p = argparse.ArgumentParser(description="从 .tar.gz 导入 Docker 镜像（stream 解压并 docker load）")
    p.add_argument("--input", "-i", default=DEFAULT_INPUT, help="输入的 .tar.gz 文件路径")
    p.add_argument("--remove-after", "-r", action="store_true", help="导入成功后删除输入文件")
    p.add_argument("--show-images", "-s", action="store_true", help="导入后列出本地镜像")
    return p.parse_args()


def ensure_docker_available() -> None:
    if shutil.which("docker") is None:
        print("❌ Docker 未安装或不可用，请先安装 Docker 并确保在 PATH 中。")
        sys.exit(1)


def import_from_gzip(input_path: str) -> int:
    """将 input_path 的解压数据写入 docker load 的 stdin。返回 docker load 的退出码。"""
    if not os.path.isfile(input_path):
        print(f"❌ 找不到输入文件：{input_path}")
        return 2

    cmd = ["docker", "load"]
    print("📥 启动 docker load 并从 gzip 流中导入镜像...")

    try:
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print("❌ 无法找到 docker 可执行文件。")
        return 3

    try:
        with gzip.open(input_path, "rb") as gz:
            assert proc.stdin is not None
            while True:
                chunk = gz.read(65536)
                if not chunk:
                    break
                try:
                    proc.stdin.write(chunk)
                except BrokenPipeError:
                    # docker load 可能已经失败或退出
                    print("❌ docker load 进程提前关闭（BrokenPipe）")
                    break
            # 关闭 stdin，让 docker load 知道数据已结束
            try:
                proc.stdin.close()
            except Exception:
                pass
    except KeyboardInterrupt:
        print("⛔ 用户中断，正在终止 docker load...")
        try:
            proc.kill()
        except Exception:
            pass
        return 4
    except Exception as e:
        print("❌ 在读取 gzip 或写入 docker load 时发生异常：", e)
        try:
            proc.kill()
        except Exception:
            pass
        return 5

    # 等待 docker load 结束并输出结果
    out, err = proc.communicate()
    try:
        if out:
            print(out.decode(errors="ignore"))
    except Exception:
        pass
    if proc.returncode != 0:
        print("❌ docker load 返回非零退出码，错误信息：")
        try:
            print(err.decode(errors="ignore"))
        except Exception:
            pass
    else:
        print("✅ 镜像导入完成。")
    return proc.returncode


def list_images() -> None:
    try:
        subprocess.run(["docker", "images"], check=False)
    except Exception as e:
        print("⚠️ 无法列出 docker images：", e)


def main() -> None:
    args = parse_args()
    ensure_docker_available()

    input_path = args.input
    if not os.path.exists(input_path):
        print(f"❌ 指定的输入文件不存在：{input_path}")
        sys.exit(1)

    rc = import_from_gzip(input_path)

    if rc == 0:
        if args.show_images:
            list_images()
        if args.remove_after:
            try:
                os.remove(input_path)
                print(f"🗑️ 已删除输入文件：{input_path}")
            except Exception as e:
                print("⚠️ 无法删除输入文件：", e)
        sys.exit(0)
    else:
        print("❌ 导入失败，退出码：", rc)
        sys.exit(rc)


if __name__ == "__main__":
    main()

