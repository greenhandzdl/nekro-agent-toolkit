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
from typing import Optional

from conf.install_settings import BASE_URLS
from utils.i18n import get_message as _

import platform

# --- 默认数据目录管理 ---

def get_default_data_dir_config_path():
    """获取默认数据目录配置文件的路径。
    
    返回:
        str: 配置文件的绝对路径
    """
    # 使用XDG Base Directory规范，将配置存放在~/.config/.nekro-agent-toolkit目录
    config_dir = os.path.expanduser("~/.config/.nekro-agent-toolkit")
    if not os.path.exists(config_dir):
        os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, "default_data_dir")

def set_default_data_dir(path: Optional[str] = None):
    """设置或清除默认数据目录。
    
    参数:
        path (Optional[str]): 要设置的默认数据目录路径。如果为 None 或空字符串，则清除默认设置。
    """
    config_path = get_default_data_dir_config_path()
    
    if not path or path.strip() == "":
        # 清除默认目录
        if os.path.exists(config_path):
            os.remove(config_path)
        print(_("default_data_dir_cleared"))
    else:
        # 设置默认目录
        abs_path = os.path.abspath(path.strip())
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(abs_path + '\n')
        print(_("default_data_dir_set", abs_path))

def get_default_data_dir() -> Optional[str]:
    """获取当前设置的默认数据目录。
    
    返回:
        Optional[str]: 如果已设置默认数据目录，返回其路径；否则返回 None。
    """
    config_path = get_default_data_dir_config_path()
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            path = f.read().strip()
            if path:
                return path
    return None

def show_default_data_dir():
    """显示当前的默认数据目录设置。"""
    default_dir = get_default_data_dir()
    if default_dir:
        print(_("current_default_data_dir", default_dir))
        # 提供交互式清除选项
        try:
            response = input(_("clear_default_data_dir_prompt"))
            if response.lower() == 'clear':
                set_default_data_dir('')
            else:
                print(_("clear_cancelled"))
        except (KeyboardInterrupt, EOFError):
            print("\n" + _("clear_cancelled"))
    else:
        print(_("no_default_data_dir"))

def confirm_use_default_data_dir(command_name: str, equivalent_command: str) -> bool:
    """询问用户是否使用默认数据目录。
    
    参数:
        command_name (str): 命令名称（如 "install", "backup", "recovery"）
        equivalent_command (str): 等效的完整命令
        
    返回:
        bool: 如果用户确认使用默认目录返回 True，否则返回 False。
    """
    default_dir = get_default_data_dir()
    if not default_dir:
        return False
        
    response = input(_("confirm_use_default_data_dir", default_dir, equivalent_command))
    return response.lower() in ['y', 'yes', '是', '确认']


# --- 系统与命令 ---

def is_running_from_source():
    """检查当前是否从源码运行还是从已安装的包运行。
    
    返回:
        bool: 如果从源码运行返回 True，如果从已安装的包运行返回 False。
    """
    # 获取当前脚本的绝对路径
    current_script = os.path.abspath(sys.argv[0])
    script_name = os.path.basename(current_script)
    
    # 1. 最直接的判断：如果命令名称就是 nekro-agent-toolkit，肯定是安装版本
    if script_name == 'nekro-agent-toolkit':
        return False
    
    # 2. 检查脚本路径是否包含典型的安装路径
    installed_indicators = [
        '.local/bin/',        # pipx 安装路径
        'site-packages/',     # pip 安装路径
        '/usr/bin/',         # 系统安装路径
        '/usr/local/bin/',   # 本地安装路径
    ]
    for indicator in installed_indicators:
        if indicator in current_script:
            return False
    
    # 3. 如果脚本名称为 app.py，很可能是从源码运行
    if script_name == 'app.py':
        return True
    
    # 4. 检查当前工作目录是否包含项目源码文件
    current_dir = os.getcwd()
    source_indicators = [
        'setup.py',        # Python 包设置文件
        'pyproject.toml',  # 现代 Python 包配置
        'app.py',          # 主入口文件
        'module',          # 项目模块目录
        'utils',           # 工具目录
        'conf'             # 配置目录
    ]
    
    source_file_count = sum(1 for indicator in source_indicators 
                           if os.path.exists(os.path.join(current_dir, indicator)))
    
    # 如果有4个或以上的源码指标文件，很可能是从源码运行
    if source_file_count >= 4:
        return True
    
    # 5. 检查脚本所在目录是否包含源码文件
    script_dir = os.path.dirname(current_script)
    if script_dir and script_dir != '/usr/bin' and script_dir != '/usr/local/bin':
        script_dir_source_count = sum(1 for indicator in source_indicators 
                                     if os.path.exists(os.path.join(script_dir, indicator)))
        if script_dir_source_count >= 3:
            return True
    
    # 6. 特殊情况：交互式运行或测试（sys.argv[0] 为 '-c' 或类似）
    if script_name in ['-c', '<stdin>', '<string>']:
        # 基于当前工作目录判断
        return source_file_count >= 3
    
    # 默认假设是安装版本（更保守的判断）
    return False

def get_version_info():
    """获取版本信息。
    
    根据运行环境返回不同的版本信息：
    - 源码运行：显示 Git SHA
    - 包安装运行：显示版本号
    
    返回:
        str: 版本信息字符串
    """
    if is_running_from_source():
        # 从源码运行，尝试获取 Git SHA
        try:
            # 尝试获取当前的 Git commit SHA
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"], 
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                universal_newlines=True,
                cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            )
            if result.returncode == 0:
                sha = result.stdout.strip()[:8]  # 只取前8位
                
                # 检查是否有未提交的更改
                status_result = subprocess.run(
                    ["git", "status", "--porcelain"],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    universal_newlines=True,
                    cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                )
                dirty = " (dirty)" if status_result.stdout.strip() else ""
                
                return f"nekro-agent-toolkit (源码) {sha}{dirty}"
            else:
                return "nekro-agent-toolkit (源码) unknown"
        except (subprocess.CalledProcessError, FileNotFoundError):
            return "nekro-agent-toolkit (源码) unknown"
    else:
        # 从包安装运行，返回版本号
        try:
            # 尝试从已安装的包获取版本（Python 3.8+ 优先使用 importlib.metadata）
            try:
                from importlib.metadata import version
                pkg_version = version("nekro-agent-toolkit")
                return f"nekro-agent-toolkit {pkg_version}"
            except ImportError:
                # 兼容 Python 3.7 及以下版本
                import pkg_resources
                pkg_version = pkg_resources.get_distribution("nekro-agent-toolkit").version
                return f"nekro-agent-toolkit {pkg_version}"
        except Exception:
            # 如果无法获取已安装版本，回退到硬编码版本
            return "nekro-agent-toolkit 1.0.3"

def get_command_prefix():
    """获取当前运行环境的命令前缀。
    
    返回:
        str: 'python3 app.py' (源码运行) 或 'nekro-agent-toolkit' (包安装)
    """
    if is_running_from_source():
        return "python3 app.py"
    else:
        return "nekro-agent-toolkit"

def command_exists(command):
    """检查指定命令是否存在于系统的 PATH 中。

    参数:
        command (str): 需要检查的命令名称。

    返回:
        bool: 如果命令存在则返回 True，否则返回 False。
    """
    return shutil.which(command) is not None

def get_docker_compose_cmd() -> Optional[str]:
    """确定要使用的正确 docker-compose 命令（v1 或 v2）。

    检查系统中是否存在 'docker-compose' (v1) 或 'docker compose' (v2)，
    并返回可用的命令。

    返回:
        Optional[str]: 如果找到，返回 'docker-compose' 或 'docker compose' 字符串；
                    如果两者都未找到，则返回 None。
    """
    # 1. 检测 `docker compose` (v2)
    try:
        result = subprocess.run(
            "docker compose --version", 
            shell=True, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.DEVNULL
        )
        if result.returncode == 0:
            return "docker compose"
    except Exception:
        pass  # 忽略异常，继续检测下一个命令

    # 2. 检测 `docker-compose` (v1)
    if command_exists("docker-compose"):
        return "docker-compose"

    # 3. 如果两者都未找到，返回 None
    print(_('no_docker_compose_command_found'))
    return None

def run_sudo_command(command, description, env=None):
    """
    执行需要提升权限的命令，自动处理权限不足的情况，提供提权选项
    
    Args:
        command (str): 要执行的命令
        description (str): 命令的描述，用于用户界面显示
        env (dict, optional): 要添加到环境变量中的键值对，默认为 None
    
    Returns:
        None: 该函数在成功执行时返回，失败时退出程序
    
    Logic:
        1. 首先在当前用户权限下尝试执行命令
        2. 如果执行失败（权限不足），询问用户是否使用sudo提权
        3. 用户可以选择重试、提权或退出
        4. 如果命令不存在，直接报错退出
    """
    # 打印正在执行的操作描述
    print(_("executing_command", description))
    
    # 创建环境变量副本，如果提供了额外环境变量则合并
    cmd_env = os.environ.copy()
    if env:
        cmd_env.update(env)

    # 标记是否已经尝试过sudo，用于控制重试逻辑
    tried_sudo = False
    
    # 主循环：处理命令执行和可能的权限提升
    while True:
        try:
            # 根据是否已尝试sudo决定是否添加sudo前缀
            cmd_to_run = command if not tried_sudo else f"sudo -E {command}"
            
            # 执行命令，使用shell=True以支持管道等shell特性
            # 捕获stderr以便在出错时显示详细信息
            result = subprocess.run(
                cmd_to_run,
                shell=True,
                check=True,                    # 非零退出码时抛出异常
                stdout=subprocess.DEVNULL,     # 不输出标准输出
                stderr=subprocess.PIPE,        # 捕获错误输出
                env=cmd_env                    # 使用合并后的环境变量
            )
            
            # 执行成功，根据是否使用了sudo显示不同成功信息
            print(_("sudo_elevation_success") if tried_sudo else _('execute_with_current_user_success'))
            return  # 成功执行后返回
        except subprocess.CalledProcessError as e:
            # 命令执行失败（非零退出码）
            if not tried_sudo:
                # 首次失败，提示权限不足，建议提权
                print(_('insufficient_permissions_try_sudo'))
            else:
                # 已经使用sudo但仍失败，显示详细错误信息
                print(_('error_sudo_failed', description), file=sys.stderr)
                print(f"Return code: {e.returncode}")
                if e.stderr:
                    print(f"Error output: {e.stderr.decode() if hasattr(e.stderr, 'decode') else e.stderr}")
            
            # 进入交互模式，让用户选择如何处理失败
            while True:
                # 根据是否已尝试sudo显示不同的提示信息
                choice = input(_("command_failed_retry_sudo_exit" if not tried_sudo else "sudo_failed_retry_exit")).strip().lower()
                if choice == 'r':
                    break  # 重试当前模式（不提权或已提权）
                elif choice == 'y':
                    if not tried_sudo:
                        tried_sudo = True  # 首次失败后，下次尝试使用sudo
                        break
                    else:
                        break  # 已经sudo后仍然失败，继续重试sudo模式
                elif choice == 'n':
                    print(_("exited"))  # 用户选择退出
                    sys.exit(1)
                else:
                    print(_("invalid_input_retry"))  # 无效输入，重新提示
        except FileNotFoundError:
            # 命令不存在的情况
            cmd_name = command.split()[0]
            print(_("error_command_not_found", cmd_name), file=sys.stderr)
            sys.exit(1)


def check_dependencies():
    """检查并确认所有必需的系统依赖（如 docker, docker-compose）都已安装。

    如果缺少依赖，则打印错误信息并退出脚本。

    返回:
        str: 可用的 docker-compose 命令（'docker-compose' 或 'docker compose'）。
    """
    print(_("checking_dependencies"))
    if not command_exists("docker"):
        print(_("error_docker_not_found"), file=sys.stderr)
        sys.exit(1)

    docker_compose_cmd = get_docker_compose_cmd()
    if not docker_compose_cmd:
        print(_("error_docker_compose_not_found"), file=sys.stderr)
        sys.exit(1)
    
    print(_("dependencies_check_passed"))
    print(_("using_docker_compose_cmd", docker_compose_cmd))
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
            print(_('downloading_from', url))
            urllib.request.urlretrieve(url, output_path)
            print(_('download_success', filename))
            return True
        except Exception as e:
            print(_('download_failed_try_other', e))
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
    import platform
    system = platform.system()
    
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

    # 在 Windows 上使用临时文件写入策略，避免文件锁定问题
    if system == "Windows":
        import tempfile
        import stat
        
        # 先尝试移除只读属性
        try:
            os.chmod(env_path, stat.S_IWRITE | stat.S_IREAD)
        except Exception:
            pass  # 如果无法更改属性，继续尝试写入
        
        # 创建临时文件
        temp_fd, temp_path = tempfile.mkstemp(dir=os.path.dirname(env_path), suffix='.tmp')
        try:
            with os.fdopen(temp_fd, 'w', encoding='utf-8') as tmp_file:
                tmp_file.writelines(lines)
            
            # 将临时文件移动到目标位置
            # Windows 上使用 os.replace 替换原文件
            os.replace(temp_path, env_path)
        except PermissionError:
            # 如果还是失败，则尝试使用重试机制
            max_retries = 2
            for attempt in range(max_retries):
                try:
                    with open(env_path, 'w', encoding='utf-8') as f:
                        f.writelines(lines)
                    break  # 成功则跳出循环
                except PermissionError:
                    if attempt < max_retries - 1:  # 如果不是最后一次尝试
                        import time
                        time.sleep(1)  # 等待一秒后重试
                    else:
                        raise  # 重试次数用完，抛出异常
    else:
        # 非 Windows 系统，直接写入文件
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
    print(_("checking_generating_credentials"))
    for key, length in [("ONEBOT_ACCESS_TOKEN", 32), ("NEKRO_ADMIN_PASSWORD", 16), ("QDRANT_API_KEY", 32)]:
        if not get_env_value(env_path, key):
            print(_("generating_random_key", key))
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