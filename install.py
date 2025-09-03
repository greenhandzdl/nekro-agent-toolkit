#!/usr/bin/env python3
import argparse
import os
import secrets
import shutil
import string
import subprocess
import sys
import time
import urllib.request

# --- 配置 ---
BASE_URLS = [
    "https://raw.githubusercontent.com/KroMiose/nekro-agent/main/docker",
    "https://raw.gitcode.com/gh_mirrors/ne/nekro-agent/raw/main/docker",
    "http://hk-yd-proxy.gitwarp.com:6699/https://raw.githubusercontent.com/KroMiose/nekro-agent/main/docker"
]
NEKRO_DATA_DIR = os.getcwd()  # 默认的应用数据目录，使用当前工作目录

# --- 辅助函数 ---

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
    """使用 sudo 运行一个 shell 命令，并提供操作描述。

    如果命令执行失败或 'sudo' 命令不存在，将打印错误信息并退出脚本。

    参数:
        command (str): 需要以 root 权限执行的命令。
        description (str): 对正在执行的操作的简短描述。
    """
    print(f"正在执行: {description}")
    try:
        subprocess.run(f"sudo {command}", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"错误: {description} 失败。\n{e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("错误: 'sudo' 命令未找到。请确保您有管理员权限。", file=sys.stderr)
        sys.exit(1)

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

def generate_random_string(length):
    """生成指定长度的随机字母数字字符串。

    参数:
        length (int): 要生成的字符串的长度。

    返回:
        str: 生成的随机字符串。
    """
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))

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

# --- 安装步骤 ---

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

def setup_directories(nekro_data_dir):
    """创建应用数据目录，设置权限，并切换当前工作目录到该目录。

    参数:
        nekro_data_dir (str): 要设置和进入的应用数据目录的绝对路径。

    返回:
        str: 传入的应用数据目录路径。
    """
    print(f"应用数据目录 (NEKRO_DATA_DIR): {nekro_data_dir}")

    try:
        os.makedirs(nekro_data_dir, exist_ok=True)
    except OSError as e:
        print(f"错误: 无法创建应用目录 {nekro_data_dir}。请检查权限。\n{e}", file=sys.stderr)
        sys.exit(1)
    
    print("警告: 正在设置应用目录权限为 777，这可能不安全。")
    run_sudo_command(f"chmod -R 777 {nekro_data_dir}", "设置目录权限")

    os.chdir(nekro_data_dir)
    print(f"已切换到目录: {os.getcwd()}")
    return nekro_data_dir

def configure_env_file(nekro_data_dir, original_cwd):
    """准备并配置 .env 环境文件。

    如果目标目录中没有 .env 文件，会尝试从脚本的原始运行目录复制一个。
    如果原始目录也没有，则从远程仓库下载 .env.example 并创建 .env。
    最后，确保文件中有必要的随机生成值。

    参数:
        nekro_data_dir (str): 应用数据目录的绝对路径。
        original_cwd (str): 脚本开始执行时的原始工作目录路径。

    返回:
        str: 配置好的 .env 文件的绝对路径。
    """
    env_path = os.path.join(nekro_data_dir, ".env")
    
    if not os.path.exists(env_path):
        source_env_in_cwd = os.path.join(original_cwd, ".env")
        if os.path.normpath(original_cwd) != os.path.normpath(nekro_data_dir) and os.path.exists(source_env_in_cwd):
            print(f"在 {original_cwd} 中找到 .env 文件，正在复制到 {nekro_data_dir}...")
            shutil.copy(source_env_in_cwd, env_path)
            print("复制成功。")
        else:
            print("未找到 .env 文件，正在从仓库获取 .env.example...")
            env_example_path = os.path.join(nekro_data_dir, ".env.example")
            if not get_remote_file(".env.example", env_example_path):
                print("错误: 无法获取 .env.example 文件。", file=sys.stderr)
                sys.exit(1)
            shutil.copy(env_example_path, env_path)
            print("已创建 .env 文件。")

    print("正在更新 .env 文件...")
    update_env_file(env_path, "NEKRO_DATA_DIR", nekro_data_dir)

    for key, length in [("ONEBOT_ACCESS_TOKEN", 32), ("NEKRO_ADMIN_PASSWORD", 16), ("QDRANT_API_KEY", 32)]:
        if not get_env_value(env_path, key):
            print(f"正在生成随机 {key}...")
            update_env_file(env_path, key, generate_random_string(length))
    return env_path

def confirm_installation():
    """向用户显示提示，请求确认是否继续安装。

    如果用户输入 'n' 或 'no'，脚本将中止。
    """
    print("\n请检查并按需修改 .env 文件中的配置。")
    try:
        yn = input("确认是否继续安装？[Y/n] ")
        if yn.lower() not in ['', 'y', 'yes']:
            print("安装已取消。")
            sys.exit(0)
    except (EOFError, KeyboardInterrupt):
        print("\n安装已取消。")
        sys.exit(0)

def download_compose_file(with_napcat_arg):
    """根据用户选择，下载合适的 docker-compose.yml 文件。

    如果用户未通过命令行参数指定，则会交互式地询问是否需要 NapCat 版本。

    参数:
        with_napcat_arg (bool): 从命令行参数传入的是否使用 NapCat 的标志。

    返回:
        bool: 最终确认的是否使用 NapCat 的状态。
    """
    with_napcat = with_napcat_arg
    if not with_napcat:
        try:
            yn = input("是否同时使用 napcat 服务？[Y/n] ")
            if yn.lower() in ['', 'y', 'yes']:
                with_napcat = True
        except (EOFError, KeyboardInterrupt):
            print("\n默认不使用 napcat。")

    compose_filename = "docker-compose-x-napcat.yml" if with_napcat else "docker-compose.yml"
    print(f"正在获取 {compose_filename}...")
    if not get_remote_file(compose_filename, "docker-compose.yml"):
        print("错误: 无法拉取 docker-compose.yml 文件。", file=sys.stderr)
        sys.exit(1)
    return with_napcat

def run_docker_operations(docker_compose_cmd, env_path):
    """执行 Docker 操作，包括拉取镜像和启动服务。

    参数:
        docker_compose_cmd (str): 要使用的 docker-compose 命令。
        env_path (str): .env 文件的路径，用于 docker-compose 的 --env-file 参数。
    """
    env_file_arg = f"--env-file {env_path}"
    run_sudo_command(f"{docker_compose_cmd} {env_file_arg} pull", "拉取服务镜像")
    run_sudo_command(f"{docker_compose_cmd} {env_file_arg} up -d", "启动主服务")
    run_sudo_command("docker pull kromiose/nekro-agent-sandbox", "拉取沙盒镜像")

def configure_firewall(env_path, with_napcat):
    """如果 ufw 防火墙存在，则为其配置端口转发规则。

    参数:
        env_path (str): .env 文件的路径，用于获取端口号。
        with_napcat (bool): 是否为 NapCat 服务也配置端口。
    """
    if not command_exists("ufw"):
        return

    nekro_port = get_env_value(env_path, "NEKRO_EXPOSE_PORT") or "8021"
    print(f"\nNekroAgent 主服务需放行端口 {nekro_port}/tcp...")
    if with_napcat:
        napcat_port = get_env_value(env_path, "NAPCAT_EXPOSE_PORT") or "6099"
        print(f"NapCat 服务需放行端口 {napcat_port}/tcp...")

    print("正在配置防火墙 (ufw)...")
    run_sudo_command(f"ufw allow {nekro_port}/tcp", f"放行端口 {nekro_port}")
    if with_napcat:
        run_sudo_command(f"ufw allow {napcat_port}/tcp", f"放行端口 {napcat_port}")

def print_summary(env_path, with_napcat):
    """在安装结束后，打印包含重要访问信息和下一步操作的摘要。

    参数:
        env_path (str): .env 文件的路径，用于获取访问凭证和端口。
        with_napcat (bool): 是否也显示 NapCat 相关的信息。
    """
    instance_name = get_env_value(env_path, "INSTANCE_NAME")
    onebot_token = get_env_value(env_path, "ONEBOT_ACCESS_TOKEN")
    admin_pass = get_env_value(env_path, "NEKRO_ADMIN_PASSWORD")
    nekro_port = get_env_value(env_path, "NEKRO_EXPOSE_PORT") or "8021"

    print("\n=== 部署完成！ ===")
    print("你可以通过以下命令查看服务日志：")
    print(f"  NekroAgent: 'sudo docker logs -f {instance_name}nekro_agent'")
    if with_napcat:
        napcat_port = get_env_value(env_path, "NAPCAT_EXPOSE_PORT") or "6099"
        print(f"  NapCat: 'sudo docker logs -f {instance_name}napcat'")

    print("\n=== 重要配置信息 ===")
    print(f"OneBot 访问令牌: {onebot_token}")
    print(f"管理员账号: admin | 密码: {admin_pass}")

    print("\n=== 服务访问信息 ===")
    print(f"NekroAgent 主服务端口: {nekro_port}")
    print(f"NekroAgent Web 访问地址: http://127.0.0.1:{nekro_port}")
    if with_napcat:
        napcat_port = get_env_value(env_path, "NAPCAT_EXPOSE_PORT") or "6099"
        print(f"NapCat 服务端口: {napcat_port}")
    else:
        print(f"OneBot WebSocket 连接地址: ws://127.0.0.1:{nekro_port}/onebot/v11/ws")
    
    print("\n=== 注意事项 ===")
    print("1. 如果您使用的是云服务器，请在云服务商控制台的安全组中放行相应端口。")
    print("2. 如果需要从外部访问，请将上述地址中的 127.0.0.1 替换为您的服务器公网IP。")
    if with_napcat:
        print(f"3. 请使用 'sudo docker logs {instance_name}napcat' 查看机器人 QQ 账号二维码进行登录。")

    print("\n安装完成！祝您使用愉快！")

# --- 主执行函数 ---

def main():
    """主安装脚本的协调器，负责按顺序调用所有安装步骤。"""
    original_cwd = os.getcwd()
    parser = argparse.ArgumentParser(description="Nekro Agent Installer")
    parser.add_argument('nekro_data_dir', nargs='?', default=NEKRO_DATA_DIR, help='The directory to install Nekro Agent. Defaults to the current directory.')
    parser.add_argument('--with-napcat', action='store_true', help="Enable NapCat service.")
    args = parser.parse_args()

    # 确定最终的应用数据目录
    nekro_data_dir = os.path.abspath(args.nekro_data_dir)

    docker_compose_cmd = check_dependencies()
    setup_directories(nekro_data_dir)
    env_path = configure_env_file(nekro_data_dir, original_cwd)
    
    confirm_installation()
    
    with_napcat = download_compose_file(args.with_napcat)
    run_docker_operations(docker_compose_cmd, env_path)
    configure_firewall(env_path, with_napcat)
    print_summary(env_path, with_napcat)

if __name__ == "__main__":
    main()
