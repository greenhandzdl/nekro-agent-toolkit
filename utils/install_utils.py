"""
Nekro Agent 安装脚本的辅助函数模块。

包含所有与安装流程相关的具体步骤函数。
"""
import os
import shutil
import sys

from .helpers import (
    command_exists, get_docker_compose_cmd, run_sudo_command, get_remote_file,
    update_env_file, get_env_value, populate_env_secrets
)
from utils.i18n import get_message as _



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
    run_sudo_command(f"chmod -R 777 {nekro_data_dir}", _("setting_directory_permissions"))

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

    print(_("updating_nekro_data_dir"))
    update_env_file(env_path, "NEKRO_DATA_DIR", nekro_data_dir)
    
    populate_env_secrets(env_path)

    return env_path

def confirm_installation():
    """向用户显示提示，请求确认是否继续安装。

    如果用户输入 'n' 或 'no'，脚本将中止。
    """
    print(f"\n{_('check_env_config')}")
    try:
        yn = input(_('confirm_installation'))
        if yn.lower() not in ['', 'y', 'yes']:
            print(_('installation_cancelled'))
            sys.exit(0)
    except (EOFError, KeyboardInterrupt):
        print(f"\n{_('installation_cancelled')}")
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
            yn = input(_('use_napcat_service'))
            if yn.lower() in ['', 'y', 'yes']:
                with_napcat = True
        except (EOFError, KeyboardInterrupt):
            print(f"\n{_('default_no_napcat')}")  

    compose_filename = "docker-compose-x-napcat.yml" if with_napcat else "docker-compose.yml"
    print(_("getting_compose_file", compose_filename))
    if not get_remote_file(compose_filename, "docker-compose.yml"):
        print(_("error_cannot_pull_compose_file"), file=sys.stderr)
        sys.exit(1)
    return with_napcat

def run_docker_operations(docker_compose_cmd, env_path):
    """执行 Docker 操作，包括拉取镜像和启动服务。

    参数:
        docker_compose_cmd (str): 要使用的 docker-compose 命令。
        env_path (str): .env 文件的路径，用于 docker-compose 的 --env-file 参数。
    """
    env_file_arg = f"--env-file {env_path}"
    
    # 准备 Docker 环境
    docker_env = {}
    docker_host = os.environ.get('DOCKER_HOST')
    if docker_host and docker_host.startswith('/'):
        print(_("detected_docker_host_correcting", docker_host, docker_host))
        docker_env['DOCKER_HOST'] = f"unix://{docker_host}"

    run_sudo_command(f"{docker_compose_cmd} {env_file_arg} pull", _("pulling_service_images"), env=docker_env)
    run_sudo_command(f"{docker_compose_cmd} {env_file_arg} up -d", _("starting_main_service"), env=docker_env)
    run_sudo_command("docker pull kromiose/nekro-agent-sandbox", _("pulling_sandbox_image"), env=docker_env)

def configure_firewall(env_path, with_napcat):
    """如果 ufw 防火墙存在，则为其配置端口转发规则。

    参数:
        env_path (str): .env 文件的路径，用于获取端口号。
        with_napcat (bool): 是否为 NapCat 服务也配置端口。
    """
    if not command_exists("ufw"):
        return

    nekro_port = get_env_value(env_path, "NEKRO_EXPOSE_PORT") or "8021"
    print(f"\n{_('nekro_agent_needs_port', nekro_port)}")
    if with_napcat:
        napcat_port = get_env_value(env_path, "NAPCAT_EXPOSE_PORT") or "6099"
        print(_("napcat_needs_port", napcat_port))

    print(_("configuring_firewall_ufw"))
    run_sudo_command(f"ufw allow {nekro_port}/tcp", _("allow_port", nekro_port))
    if with_napcat:
        napcat_port = get_env_value(env_path, "NAPCAT_EXPOSE_PORT") or "6099"
        run_sudo_command(f"ufw allow {napcat_port}/tcp", _("allow_port", napcat_port))

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

    print(f"\n{_('deployment_complete')}")
    print(_('view_logs_instruction'))
    print(_('nekro_agent_logs', instance_name))
    if with_napcat:
        napcat_port = get_env_value(env_path, "NAPCAT_EXPOSE_PORT") or "6099"
        print(_('napcat_logs', instance_name))

    print(f"\n{_('important_config_info')}")
    print(_('onebot_access_token', onebot_token))
    print(_('admin_account', admin_pass))

    print(f"\n{_('service_access_info')}")
    print(_('nekro_agent_port', nekro_port))
    print(_('nekro_agent_web_access', nekro_port))
    if with_napcat:
        napcat_port = get_env_value(env_path, "NAPCAT_EXPOSE_PORT") or "6099"
        print(_('napcat_service_port', napcat_port))
    else:
        print(_('onebot_websocket_address', nekro_port))
    
    print(f"\n{_('important_notes')}")
    print(_('cloud_server_note'))
    print(_('external_access_note'))
    if with_napcat:
        print(_('napcat_qr_code_note', instance_name))

    print(f"\n{_('installation_complete')}")
