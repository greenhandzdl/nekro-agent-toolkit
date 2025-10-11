#!/usr/bin/env python3
import os
import sys

# 将项目根目录添加到 sys.path，确保可以正确导入本地模块
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from conf.docker_mirrors import DOCKER_MIRRORS
from utils.helpers import run_sudo_command
from utils.i18n import get_message as _


def parse_image_url(url):
    """
    解析 Docker 镜像 URL，分离出 tag 或 digest。
    支持格式：
      - repository:tag
      - repository@digest
      - registry/repository:tag
      - registry/repository@digest
    Args:
        url (str): 镜像地址
    Returns:
        tuple: (url_base, tag, digest)
    """
    tag = ''
    digest = ''
    if '@' in url:
        url, digest = url.split('@', 1)
        digest = '@' + digest
    elif ':' in url and '/' in url and url.rfind(':') > url.rfind('/'):
        # 只有最后的 : 是 tag
        url, tag = url.rsplit(':', 1)
        tag = ':' + tag
    return url, tag, digest

def has_registry(url):
    """
    判断镜像 URL 是否包含 registry 信息。
    规则：第一个 / 之前有 . 或 :，则认为有 registry。
    Args:
        url (str): 镜像地址
    Returns:
        bool: 是否包含 registry
    """
    parts = url.split('/', 1)
    return '.' in parts[0] or ':' in parts[0]

def is_docker_official_reachable(timeout: int = 3) -> bool:
    """
    测试 Docker 官方 registry 是否可访问。
    对 https://registry-1.docker.io/v2/ 发起 HEAD 请求：
      - 网络异常或超时 -> 返回 False
      - 5xx 响应 -> 返回 False
      - 其它响应（如 200, 301, 302, 401, 403, 429 等） -> 返回 True
    如果环境中未安装 requests，则函数也返回 False（安全失败）。
    Args:
        timeout (int): 请求超时时间（秒）
    Returns:
        bool: 官方 registry 是否可访问
    """
    try:
        import requests
    except Exception:
        # requests 未安装或不可用，返回 False（视为不可达）
        return False

    url = "https://registry-1.docker.io/v2/"
    try:
        resp = requests.head(url, timeout=timeout, allow_redirects=True)
    except requests.RequestException:
        return False
    return resp.status_code < 500

def docker_pull_image(image_url: str, description: str, env=None):
    """
    拉取 Docker 镜像，自动选择官方源或镜像源。
    优先尝试官方源，若不可达则依次尝试配置的镜像源，全部失败后再回退官方源。
    拉取过程中的每一步均有详细的本地化提示。
    Args:
        image_url (str): 镜像地址
        description (str): 操作描述（用于本地化消息）
        env (dict, optional): 传递给子进程的环境变量
    Returns:
        None
    Raises:
        Exception: 拉取镜像失败时抛出异常
    """
    if is_docker_official_reachable(timeout=5):
        print(_("pulling_image_official", description, image_url))
        run_sudo_command("docker pull {}".format(image_url), description, env=env)
        return
    print(_("pulling_image_mirrors", description, image_url))
    url_base, tag, digest = parse_image_url(image_url)
    for mirror in DOCKER_MIRRORS:
        if has_registry(image_url):
            # 已有 registry，直接用原始 image_url
            mirror_image = image_url
        else:
            # 拼接镜像源和 repo
            if '/' in url_base:
                repo = url_base
            else:
                repo = "library/{}".format(url_base)
            mirror_image = "{}/{}{}{}".format(mirror.rstrip('/'), repo, tag, digest)
        print(_("trying_mirror_pull", mirror, mirror_image))
        try:
            run_sudo_command("docker pull {}".format(mirror_image), description, env=env)
            print(_("mirror_pull_success", description, mirror, mirror_image))
            return
        except Exception as e:
            print(_("mirror_pull_failed", mirror, e))
    # 所有镜像源都失败，最后再尝试官方源一次
    print(_("all_mirrors_failed_try_official", image_url))
    try:
        run_sudo_command("docker pull {}".format(image_url), description, env=env)
        print(_("official_pull_success", description, image_url))
    except Exception as e:
        print(_("official_pull_failed", e))

if __name__ == "__main__":
    # 示例：拉取 hello-world 镜像
    docker_pull_image("hello-world", "测试拉取镜像")
