"""
安装功能配置文件
"""

# 用于下载文件的远程仓库基础 URL 列表
BASE_URLS = [
    "https://raw.githubusercontent.com/KroMiose/nekro-agent/main/docker",
    "https://ep.nekro.ai/e/KroMiose/nekro-agent/main/docker",
    "https://cdn.jsdelivr.net/gh/KroMiose/nekro-agent@main/docker", # 同步更改需要访问https://purge.jsdelivr.net/gh进行刷新
    # "https://gh.ddlc.top/https://raw.githubusercontent.com/KroMiose/nekro-agent/main/docker",
    # 不可用（保留）
    # "https://raw.gitcode.com/gh_mirrors/ne/nekro-agent/raw/main/docker",
    # "http://hk-yd-proxy.gitwarp.com:6699/https://raw.githubusercontent.com/KroMiose/nekro-agent/main/docker"
]

# 应用数据目录权限的项目约定
DATA_DIR_MODE = 0o777  # 可根据实际需要修改，推荐 0o777
