# 快速开始

## 环境要求
- Docker
- Docker Compose

## 使用方法

### 1. 启动服务
```bash
docker compose --env-file ./.env pull
docker compose --env-file ./.env up -d

# 拉取沙箱镜像（必须）
docker pull kromiose/nekro-agent-sandbox
```

### 2. 停止服务
```bash
docker compose --env-file ./.env down
```

## .env 文件路径说明

如果 `.env` 文件不在当前目录，使用 `--env-file` 参数指定完整路径：

```bash
docker compose --env-file /path/to/.env up -d
```

### Windows 路径转换
Windows 路径需要转换为 Linux 兼容格式：
- `C:\path\to\.env` → `/c/path/to/.env`
- `D:\data\.env` → `/d/data/.env`