from conf.docker_mirrors import DOCKER_MIRRORS as DOCKER_MIRRORS  # noqa: F401


# 帮我写一个测试docker官方是否连通的函数，不连通返回false
def is_docker_official_reachable(timeout: int = 3) -> bool:
    """
    测试 Docker 官方 registry 是否可访问。
    对 https://registry-1.docker.io/v2/ 发起 HEAD 请求：
      - 网络异常或超时 -> 返回 False
      - 受到 5xx 响应 -> 返回 False
      - 其它响应（包括 200, 301, 302, 401, 403, 429 等） -> 返回 True
    如果环境中未安装 requests，则函数也返回 False（安全失败）。
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
