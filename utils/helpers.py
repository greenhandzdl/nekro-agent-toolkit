"""
通用辅助函数模块

包含系统、网络、Docker、.env 文件操作等相关的可重用函数。
"""
import os
import secrets
import shutil
import string
import subprocess
import sys
import time
import urllib.request

from conf.settings import BASE_URLS

# --- 系统与命令 ---

def command_exists(command):
    """检查指定命令是否存在于系统的 PATH 中。

    参数:
        command (str): 需要检查的命令名称。

    返回:
        bool: 如果命令存在则返回 True，否则返回 False。
    """
    return shutil.which(command) is not None

def get_docker_compose_cmd():
    """确定要使用的正确 docker-compose 命令（v1 或 v2）。

    检查系统中是否存在 'docker-compose' (v1) 或 'docker compose' (v2)，
    并返回可用的命令。

    返回:
        str | None: 如果找到，返回 'docker-compose' 或 'docker compose' 字符串；
                    如果两者都未找到，则返回 None。
    """
    if command_exists("docker-compose"):
        return "docker-compose"
    try:
        subprocess.run("docker compose version", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return "docker compose"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

def run_sudo_command(command, description):
    """尝试以当前用户权限运行命令，如果失败则使用 sudo 提权后重试。

    首先会尝试直接执行命令。如果因为权限不足等问题失败，
    会自动在该命令前加上 'sudo' 并再次尝试。

    参数:
        command (str): 需要执行的命令。
        description (str): 对正在执行的操作的简短描述。
    """
    print(f"正在执行: {description}")
    try:
        # 1. 尝试直接运行
        # 使用 DEVNULL 来抑制成功执行时的输出，只在失败时关心错误
        subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("使用当前用户权限执行成功。")
        return
    except subprocess.CalledProcessError:
        # 2. 如果失败，则尝试 sudo
        print("当前用户权限不足，尝试使用 sudo 提权...")
        try:
            subprocess.run(f"sudo {command}", shell=True, check=True)
            print("使用 sudo 提权成功。")
        except subprocess.CalledProcessError as e:
            print(f"错误: 使用 sudo 提权后，{description} 仍然失败。\n{e}", file=sys.stderr)
            sys.exit(1)
        except FileNotFoundError:
            print("错误: 'sudo' 命令未找到。请确保您有管理员权限。", file=sys.stderr)
            sys.exit(1)
    except FileNotFoundError:
        # 如果原始命令就不存在
        cmd_name = command.split()[0]
        print(f"错误: 命令 '{cmd_name}' 未找到。", file=sys.stderr)
        sys.exit(1)

def check_dependencies():
    """检查并确认所有必需的系统依赖（如 docker, docker-compose）都已安装。

    如果缺少依赖，则打印错误信息并退出脚本。

    返回:
        str: 可用的 docker-compose 命令（'docker-compose' 或 'docker compose'）。
    """
    print("正在检查依赖...")
    if not command_exists("docker"):
        print("错误: 命令 'docker' 未找到，请先安装后再运行。", file=sys.stderr)
        sys.exit(1)

    docker_compose_cmd = get_docker_compose_cmd()
    if not docker_compose_cmd:
        print("错误: 'docker-compose' 或 'docker compose' 未找到，请先安装后再运行。", file=sys.stderr)
        sys.exit(1)
    
    print("依赖检查通过。")
    print(f"使用 '{docker_compose_cmd}' 作为 docker-compose 命令。")
    return docker_compose_cmd

# --- 网络 ---

def get_remote_file(filename, output_path):
    """从 BASE_URLS 列表中定义的远程源下载文件。

    会依次尝试每个 URL，直到成功下载文件或所有源都失败。

    参数:
        filename (str): 要下载的文件名。
        output_path (str): 文件在本地的保存路径。

    返回:
        bool: 如果成功下载则返回 True，否则返回 False。
    """
    for base_url in BASE_URLS:
        url = f"{base_url}/{filename}"
        try:
            print(f"正在从 {url} 下载...")
            urllib.request.urlretrieve(url, output_path)
            print(f"下载成功: {filename}")
            return True
        except Exception as e:
            print(f"下载失败，尝试其他源... (错误: {e})")
            time.sleep(1)
    return False

# --- .env 文件操作 ---

def update_env_file(env_path, key, value):
    """在 .env 文件中更新或添加一个键值对。

    如果键已存在，则更新其值；如果不存在，则在文件末尾添加新的键值对。

    参数:
        env_path (str): .env 文件的路径。
        key (str): 要更新或添加的配置项名称。
        value (str): 要设置的配置项的值。
    """
    lines = []
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

    found = False
    for i, line in enumerate(lines):
        if line.strip().startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            found = True
            break
    
    if not found:
        lines.append(f"{key}={value}\n")

    with open(env_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

def get_env_value(env_path, key):
    """从 .env 文件中获取指定键的值。

    参数:
        env_path (str): .env 文件的路径。
        key (str): 要获取的配置项的名称。

    返回:
        str: 找到的配置项的值，如果未找到或文件不存在则返回空字符串。
    """
    if not os.path.exists(env_path):
        return ""
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip().startswith(f"{key}="):
                return line.strip().split('=', 1)[1].strip()
    return ""

def populate_env_secrets(env_path):
    """确保 .env 文件中包含所有必需的随机生成值。

    如果 .env 文件中缺少 ONEBOT_ACCESS_TOKEN, NEKRO_ADMIN_PASSWORD, 或 QDRANT_API_KEY，
    此函数会为它们生成新的随机值并更新文件。

    参数:
        env_path (str): .env 文件的路径。
    """
    print("正在检查并生成必要的访问凭证...")
    for key, length in [("ONEBOT_ACCESS_TOKEN", 32), ("NEKRO_ADMIN_PASSWORD", 16), ("QDRANT_API_KEY", 32)]:
        if not get_env_value(env_path, key):
            print(f"正在生成随机 {key}...")
            update_env_file(env_path, key, generate_random_string(length))

# --- 其他 ---

def generate_random_string(length):
    """生成指定长度的随机字母数字字符串。

    参数:
        length (int): 要生成的字符串的长度。

    返回:
        str: 生成的随机字符串。
    """
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))