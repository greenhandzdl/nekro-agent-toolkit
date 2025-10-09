###############################################################
# 使用须知：
# 1. 请将 /app/nekro-agent 挂载为主机目录，避免数据丢失。
# 2. 建议将容器内 Docker 数据目录（如 /var/lib/docker，存放 images 和 volumes）也映射到主机目录。
#    示例：
#    docker run -v /主机/nekro-agent:/app/nekro-agent -v /主机/docker-data:/var/lib/docker ...
# 3. 安全提示：请在启动后执行修改/app/nekro-agent/.env文件。
# 4. 恢复提示：可以上传你的文件夹用-ri回复。
###############################################################
FROM docker:dind

WORKDIR /app
USER root
ENV PATH=/root/.local/bin:$PATH

# 安装 python3、pip、pipx、bash、git
RUN apk update && apk upgrade \
    && apk add --no-cache python3 py3-pip bash git \
    && apk add --no-cache py3-pipx || true \
    && if apk info py3-pipx >/dev/null 2>&1; then \
        echo "pipx installed via apk"; \
    else \
        echo "py3-pipx not available via apk, installing via pip3 with --break-system-packages"; \
        pip3 install --no-cache-dir --break-system-packages pipx; \
    fi \
    && pipx ensurepath \
    && /bin/sh -c 'pipx install nekro-agent-toolkit'

# 进入工作目录后执行初始化命令
RUN nekro-agent-toolkit -sd /app/nekro-agent -y \
    && yes r | nekro-agent-toolkit -i /app/nekro-agent -y

# 启动 dockerd 并进入 bash
ENTRYPOINT ["/bin/sh", "-c", "dockerd-entrypoint.sh & exec bash"]
