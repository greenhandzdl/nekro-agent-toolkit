###############################################################
# 使用须知：
# 1. 请将 /app/nekro-agent 挂载为主机目录，避免数据丢失。
# 2. 建议将容器内 Docker 数据目录（如 /var/lib/docker，存放 images 和 volumes）也映射到主机目录。
# 3. 该容器仅仅内置了 nekro-agent-toolkit，当你需要快速搭建nekro-agent-toolkit时，请使用 nekro-agent-toolkit -i。
#    当你需要快速恢复数据时，请上传数据包并使用 nekro-agent-toolkit -ri。
#    示例：
#    docker run -d \
#   --privileged \
#   --restart unless-stopped \
#   -e DOCKER_TLS_CERTDIR="" \
#   --name nekro-agent-toolkit \
#   -v /lib/modules:/lib/modules:ro \
#   -v ./data/nekro-agent:/app/nekro-agent \
#   -v ./data/docker-data:/var/lib/docker \
#   -p 8021:8021 -p 6099:6099 \
#   greenhandzdl/nekro-agent-toolkit:v1.4.19
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
RUN nekro-agent-toolkit -sd /app/nekro-agent -y

# 开放容器端口，便于端口映射
EXPOSE 8021 6099

# 启动 dockerd 并保持容器前台运行（使用 tail 持续占位），以便容器不自动退出，方便使用 docker exec 进入
ENTRYPOINT ["/bin/sh", "-c", "dockerd-entrypoint.sh & tail -f /dev/null"]