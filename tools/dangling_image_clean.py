#!/usr/bin/env python3
"""
dangling_image_clean.py

Python 版本的 Docker 悬空镜像清理脚本（等价于 tools/dangling-image-clean.sh）

功能：
 - 显示当前 Docker 磁盘使用情况（docker system df）
 - 列出所有悬空镜像（没有标签的镜像）并计算可释放空间
 - 交互式确认删除，或使用 --yes 自动确认
 - 使用 docker rmi 删除悬空镜像并可选执行 docker image prune
 - 可用 --dry-run 仅打印将要执行的命令而不实际删除

用法示例：
  python3 tools/dangling_image_clean.py
  python3 tools/dangling_image_clean.py --yes
  python3 tools/dangling_image_clean.py --dry-run

"""

import argparse
import shutil
import subprocess
import sys
import time
from typing import List


def human_readable_size(num: int) -> str:
    # IEC units (Ki, Mi, Gi)
    for unit in ["B", "KiB", "MiB", "GiB", "TiB"]:
        if abs(num) < 1024.0:
            return f"{num:.1f}{unit}"
        num /= 1024.0
    return f"{num:.1f}PiB"


def check_docker_available() -> None:
    if shutil.which("docker") is None:
        print("❌ Docker 未安装或不在 PATH 中，请先安装 Docker。")
        sys.exit(1)


def run(cmd: List[str], capture: bool = False) -> subprocess.CompletedProcess:
    try:
        if capture:
            return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, universal_newlines=True)
        else:
            return subprocess.run(cmd, check=False)
    except FileNotFoundError:
        print("❌ 找不到命令：", cmd[0])
        sys.exit(1)


def list_dangling_images() -> List[str]:
    cp = run(["docker", "images", "-q", "-f", "dangling=true"], capture=True)
    if cp.returncode != 0:
        # If docker returns error, show stderr and exit
        stderr = cp.stderr.strip() if hasattr(cp, "stderr") else ""
        print("❌ 查询悬空镜像时出错：", stderr)
        sys.exit(1)
    if not cp.stdout:
        return []
    ids = [line.strip() for line in cp.stdout.splitlines() if line.strip()]
    return ids


def show_dangling_images_verbose() -> None:
    print("\n找到以下悬空镜像（即将被删除）：")
    _ = run(["docker", "images", "--filter", "dangling=true"], capture=False)


def compute_total_size(ids: List[str]) -> int:
    total = 0
    for id_ in ids:
        cp = run(["docker", "inspect", "--format={{.Size}}", id_], capture=True)
        if cp.returncode == 0 and cp.stdout:
            try:
                size = int(cp.stdout.strip())
                total += size
            except Exception:
                # ignore bad values
                continue
    return total


def confirm(prompt: str, default: bool = False) -> bool:
    if default:
        return True
    try:
        ans = input(prompt).strip()
    except EOFError:
        return False
    return ans.lower().startswith("y")


def remove_images(ids: List[str], dry_run: bool = False) -> bool:
    if not ids:
        print("没有需要删除的悬空镜像。")
        return True
    cmd = ["docker", "rmi"] + ids
    if dry_run:
        print("[dry-run] 将执行命令：", " ".join(cmd))
        return True
    print("开始删除悬空镜像...")
    cp = run(cmd, capture=True)
    if cp.returncode != 0:
        # Print stderr but continue
        if hasattr(cp, "stderr") and cp.stderr:
            print("警告：删除过程中出现错误：\n", cp.stderr)
        else:
            print("警告：删除过程中出现未知错误，返回码：", cp.returncode)
        return False
    print("删除命令执行完成。")
    return True


def prune_images(dry_run: bool = False) -> None:
    if dry_run:
        print("[dry-run] 将执行： docker image prune -f")
        return
    print("执行 docker image prune -f 以进行最终清理...")
    _ = run(["docker", "image", "prune", "-f"], capture=False)


def show_docker_df() -> None:
    print("\n当前 Docker 磁盘使用情况:")
    _ = run(["docker", "system", "df"], capture=False)


def parse_args():
    p = argparse.ArgumentParser(description="清理 Docker 悬空镜像（没有标签的镜像）")
    p.add_argument("--yes", "-y", action="store_true", help="自动确认删除（跳过提示）")
    p.add_argument("--dry-run", action="store_true", help="模拟操作，仅打印将执行的命令")
    p.add_argument("--no-prune", action="store_true", help="删除后不运行 docker image prune")
    return p.parse_args()


def main():
    args = parse_args()

    print("=== Docker 悬空镜像清理脚本 ===")
    print("开始时间:", time.strftime("%Y-%m-%d %H:%M:%S"))

    check_docker_available()

    show_docker_df()

    print("\n扫描悬空镜像（没有标签的镜像）...")
    ids = list_dangling_images()
    if not ids:
        print("\n没有找到任何悬空镜像。\n操作完成。")
        return

    show_dangling_images_verbose()

    print("\n计算可释放的空间...")
    total = compute_total_size(ids)
    human = human_readable_size(total)
    print(f"\n⚠️  以上镜像将被删除，预计可释放: {human}")

    if args.dry_run:
        print("\n[dry-run] 模拟模式，操作不会实际执行。")

    if not args.yes:
        ok = confirm("是否要继续删除操作？(y/N): ")
        if not ok:
            print("操作已取消。")
            return

    success = remove_images(ids, dry_run=args.dry_run)
    if not success:
        print("一些镜像无法删除（可能正在被使用），将继续尝试进行 prune")

    if not args.no_prune:
        prune_images(dry_run=args.dry_run)

    show_docker_df()

    print("\n✅ 镜像清理完成!")
    print("结束时间:", time.strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == "__main__":
    main()

