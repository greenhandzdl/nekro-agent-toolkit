"""
Nekro Agent 安装脚本的辅助函数模块。

包含所有与安装流程相关的具体步骤函数。
"""
import os
import shutil
import sys
import platform
import subprocess
from .helpers import (
    command_exists, run_sudo_command, get_remote_file,
    update_env_file, get_env_value, populate_env_secrets
)
from utils.i18n import get_message as _


def set_directory_permissions(path):
    """
    根据项目约定和平台设置目录权限，支持跨语言/平台适配。
    优先读取 conf/install_settings.DATA_DIR_MODE 配置项。
    遇到权限问题时自动尝试 sudo 提权（仅类 Unix 系统）。
    Windows 下尝试 icacls 提权。
    """
    system = platform.system()
    
    if system == "Windows":
        # Windows 系统权限设置
        try:
            subprocess.run(["icacls", path, "/grant", "Everyone:(OI)(CI)F", "/T", "/C"], check=True,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(_("windows_icacls_permission_success", path))
        except Exception as icacls_e:
            print(_("windows_icacls_permission_failed", path, icacls_e))
    elif system in ["Linux", "Darwin", "FreeBSD", "OpenBSD", "NetBSD"]:
        # 获取权限模式配置
        try:
            from conf import install_settings
            mode = getattr(install_settings, 'DATA_DIR_MODE', None)
        except Exception:
            mode = None
        
        if mode is None:
            mode = 0o777  # rwxrwxrwx
        
        # 应用 POSIX 权限到目录和文件
        _apply_posix_permissions(path, mode)
    else:
        print(_("unknown_system_permission", system))


def _apply_posix_permissions(path, mode):
    """
    内部函数：应用 POSIX 权限到路径中的所有文件和目录
    """
    try:
        for root, dirs, files in os.walk(path):
            for d in dirs:
                os.chmod(os.path.join(root, d), mode)
            for f in files:
                os.chmod(os.path.join(root, f), mode)
        os.chmod(path, mode)
    except PermissionError as e:
        print(_("setting_directory_permissions"))
        print(_("error_create_app_directory", path, e))
        # 自动尝试 sudo 提权
        run_sudo_command(f"chmod -R {oct(mode)[2:]} {path}", _("setting_directory_permissions"))


def setup_directories(nekro_data_dir):
    """创建应用数据目录，设置权限，并切换当前工作目录到该目录。

    参数:
        nekro_data_dir (str): 要设置和进入的应用数据目录的绝对路径。

    返回:
        str: 传入的应用数据目录路径。
    """
    print(_("app_data_directory", nekro_data_dir))

    try:
        os.makedirs(nekro_data_dir, exist_ok=True)
    except OSError as e:
        print(_("error_create_app_directory", nekro_data_dir, e), file=sys.stderr)
        sys.exit(1)

    print(_("warning_chmod_777"))

    set_directory_permissions(nekro_data_dir)
    print(_("setting_directory_permissions"))

    os.chdir(nekro_data_dir)
    print(_("switched_to_directory", os.getcwd()))
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
            print(_("env_file_found_copying", original_cwd, nekro_data_dir))
            shutil.copy(source_env_in_cwd, env_path)
            print(_("copy_success"))
        else:
            print(_("env_file_not_found_downloading"))
            env_example_path = os.path.join(nekro_data_dir, ".env.example")
            if not get_remote_file(".env.example", env_example_path):
                print(_("error_cannot_get_env_example"), file=sys.stderr)
                sys.exit(1)
            shutil.copy(env_example_path, env_path)
            print(_("env_file_created"))
        
        # 在 Windows 上，为新创建的 .env 文件设置适当的权限
        import platform
        if platform.system() == "Windows":
            try:
                import subprocess
                subprocess.run(["icacls", env_path, "/grant", "Everyone:F", "/C"], check=True,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as e:
                # 记录权限设置失败，但继续执行
                print(_("windows_icacls_permission_failed", env_path, e))

    print(_("updating_nekro_data_dir"))
    update_env_file(env_path, "NEKRO_DATA_DIR", nekro_data_dir)
    
    populate_env_secrets(env_path)

    return env_path

def confirm_installation():
    """向用户显示提示，请求确认是否继续安装。

    如果用户输入 'n' 或 'no'，脚本将中止。
    """
    print(_('check_env_config'))
    try:
        yn = input(_('confirm_installation'))
        if yn.lower() not in ['', 'y', 'yes']:
            print(_('installation_cancelled'))
            sys.exit(0)
    except (EOFError, KeyboardInterrupt):
        print('\n' + _('installation_cancelled'))
        sys.exit(0)

def download_compose_file(with_napcat_arg, non_interactive=False):
    """根据用户选择，下载合适的 docker-compose.yml 文件。

    如果用户未通过命令行参数指定，则会交互式地询问是否需要 NapCat 版本。

    参数:
        with_napcat_arg (bool): 从命令行参数传入的是否使用 NapCat 的标志。
        non_interactive (bool): 是否跳过交互式确认步骤，默认为 False。

    返回:
        bool: 最终确认的是否使用 NapCat 的状态。
    """
    import platform
    system = platform.system()
    
    with_napcat = with_napcat_arg
    if not with_napcat and not non_interactive:
        try:
            yn = input(_('use_napcat_service'))
            if yn.lower() in ['', 'y', 'yes']:
                with_napcat = True
        except (EOFError, KeyboardInterrupt):
            print('\n' + _('default_no_napcat'))
    elif not with_napcat and non_interactive:
        # 在非交互模式下，默认不使用 NapCat
        print('\n' + _('default_no_napcat'))
        with_napcat = False

    compose_filename = "docker-compose-x-napcat.yml" if with_napcat else "docker-compose.yml"
    target_file = "docker-compose.yml"
    
    print(_('getting_compose_file', compose_filename))
    
    if not _download_compose_file_with_backup(compose_filename, target_file, system):
        print(_('error_cannot_pull_compose_file'), file=sys.stderr)
        sys.exit(1)
    
    return with_napcat


def _download_compose_file_with_backup(compose_filename, target_file, system):
    """
    内部函数：安全下载 compose 文件，处理可能的权限问题
    
    参数:
        compose_filename (str): 要下载的 compose 文件名
        target_file (str): 目标文件路径
        system (str): 系统类型（"Windows", "Linux", "Darwin", 等）
    
    返回:
        bool: 下载是否成功
    """
    import stat
    import shutil
    
    # 如果目标文件存在，先处理权限问题
    if os.path.exists(target_file):
        try:
            # 移除只读属性，确保文件可以被覆盖
            os.chmod(target_file, stat.S_IWRITE | stat.S_IREAD)
            os.remove(target_file)
        except Exception:
            # 如果无法删除，重命名为备份文件
            backup_name = target_file + ".bak"
            try:
                shutil.move(target_file, backup_name)
            except Exception:
                # 如果连备份都失败，则无法继续
                return False
    
    # 在 Windows 系统上使用临时文件方式，避免文件锁定问题
    if system == "Windows":
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            # 创建临时文件进行下载
            temp_file = os.path.join(temp_dir, "temp_compose.yml")
            # 从远程获取文件到临时文件
            success = get_remote_file(compose_filename, temp_file)
            if success:
                # 将临时文件移动到目标位置（Windows 上的原子操作）
                shutil.move(temp_file, target_file)
            return success
    else:
        # 非 Windows 系统（Linux、macOS、BSD）直接下载到目标文件
        success = get_remote_file(compose_filename, target_file)
        if not success:
            # 下载失败，尝试恢复备份文件
            backup_name = target_file + ".bak"
            if os.path.exists(backup_name):
                shutil.move(backup_name, target_file)
        else:
            # 下载成功，删除备份文件（如果存在）
            backup_name = target_file + ".bak"
            try:
                if os.path.exists(backup_name):
                    os.remove(backup_name)
            except:
                pass  # 忽略删除备份文件时的错误
        return success

def run_docker_operations(docker_compose_cmd, env_path):
    """执行 Docker 操作，包括拉取镜像和启动服务。

    参数:
        docker_compose_cmd (str): 要使用的 docker-compose 命令。
        env_path (str): .env 文件的路径，用于 docker-compose 的 --env-file 参数。
    """
    env_file_arg = "--env-file {}".format(env_path)
    # 准备 Docker 环境
    docker_env = {}
    docker_host = os.environ.get('DOCKER_HOST')
    if docker_host and docker_host.startswith('/'):
        print(_('detected_docker_host_correcting', docker_host, docker_host))
        docker_env['DOCKER_HOST'] = "unix://{}".format(docker_host)
    run_sudo_command("{} {} pull".format(docker_compose_cmd, env_file_arg), _('pulling_service_images'), env=docker_env)
    run_sudo_command("{} {} up -d".format(docker_compose_cmd, env_file_arg), _('starting_main_service'), env=docker_env)
    run_sudo_command("docker pull kromiose/nekro-agent-sandbox", _('pulling_sandbox_image'), env=docker_env)

def configure_firewall(env_path, with_napcat):
    """如果 ufw 防火墙存在，则为其配置端口转发规则。

    参数:
        env_path (str): .env 文件的路径，用于获取端口号。
        with_napcat (bool): 是否为 NapCat 服务也配置端口。
    """
    if not command_exists("ufw"):
        return

    nekro_port = get_env_value(env_path, "NEKRO_EXPOSE_PORT") or "8021"
    print('\n' + _('nekro_agent_needs_port', nekro_port))
    if with_napcat:
        napcat_port = get_env_value(env_path, "NAPCAT_EXPOSE_PORT") or "6099"
        print(_('napcat_needs_port', napcat_port))
    print(_('configuring_firewall_ufw'))
    run_sudo_command("ufw allow {}/tcp".format(nekro_port), _('allow_port', nekro_port))
    if with_napcat:
        napcat_port = get_env_value(env_path, "NAPCAT_EXPOSE_PORT") or "6099"
        run_sudo_command("ufw allow {}/tcp".format(napcat_port), _('allow_port', napcat_port))

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

    print('\n' + _('deployment_complete'))
    print(_('view_logs_instruction'))
    print(_('nekro_agent_logs', instance_name))
    if with_napcat:
        napcat_port = get_env_value(env_path, "NAPCAT_EXPOSE_PORT") or "6099"
        print(_('napcat_logs', instance_name))

    print('\n' + _('important_config_info'))
    print(_('onebot_access_token', onebot_token))
    print(_('admin_account', admin_pass))

    print('\n' + _('service_access_info'))
    print(_('nekro_agent_port', nekro_port))
    print(_('nekro_agent_web_access', nekro_port))
    if with_napcat:
        napcat_port = get_env_value(env_path, "NAPCAT_EXPOSE_PORT") or "6099"
        print(_('napcat_service_port', napcat_port))
    else:
        print(_('onebot_websocket_address', nekro_port))
    
    print('\n' + _('important_notes'))
    print(_('cloud_server_note'))
    print(_('external_access_note'))
    if with_napcat:
        print(_('napcat_qr_code_note', instance_name))

    print('\n' + _('installation_complete'))
