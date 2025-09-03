[Read this in English](./doc/README-EN.md)

# Nekro Agent 安装器

Nekro Agent 是一个基于 Docker 的应用程序，可以与 QQ 机器人结合使用。本安装器可以帮助您快速部署 Nekro Agent 及其相关服务。

## 功能特性

- 统一的 `app.py` 脚本入口，用于安装、更新和备份恢复
- 自动检查系统依赖（Docker 和 Docker Compose）
- 自动下载和配置所需的配置文件
- 支持一键部署 Nekro Agent 主服务
- 可选集成 NapCat QQ 机器人服务
- 自动生成安全密钥和访问令牌
- 自动配置防火墙规则（如果使用 ufw）
- 内置备份与恢复工具

## 系统要求

- Linux 或类 Unix 操作系统
- Docker 已安装
- Docker Compose 已安装
- `zstd` 压缩工具（推荐，用于创建更小的备份文件）
- 管理员权限（sudo）

## 安装方式

### 方法一：使用 pip 安装（推荐）

```bash
pip install nekro-agent-toolkit
```

安装完成后，即可直接使用 `nekro-agent-toolkit` 命令：

```bash
# 在当前目录下创建一个名为 na_data 的文件夹，并安装服务
nekro-agent-toolkit --install ./na_data
```

### 方法二：从源码运行

使用 `-i` 或 `--install` 参数执行安装。你需要提供一个用于存放应用数据的目录路径。

```bash
# 在当前目录下创建一个名为 na_data 的文件夹，并安装服务
python3 app.py --install ./na_data
```

## 使用方法

### 安装选项

- **启用 NapCat 服务**：附加 `--with-napcat` 参数。
- **预演模式**：附加 `--dry-run` 参数，将只生成配置文件或打印计划，不执行实际操作。
- **自动确认**：附加 `-y` 或 `--yes` 参数，脚本将不会请求交互式确认。

### 更新

- **部分更新 (推荐)**：使用 `-u` 或 `--update` 参数，仅更新 Nekro Agent 核心服务。
  ```bash
  nekro-agent-toolkit --update ./na_data
  # 或者从源码运行:
  python3 app.py --update ./na_data
  ```

- **完全更新 (升级)**：使用 `-ua` 或 `--upgrade` 参数，更新所有 Docker 镜像（包括数据库等）。
  ```bash
  nekro-agent-toolkit --upgrade ./na_data
  # 或者从源码运行:
  python3 app.py --upgrade ./na_data
  ```

### 备份与恢复

- **备份**：使用 `-b` 或 `--backup` 参数。需要提供源数据目录和备份文件存放目录。
  ```bash
  # 将 ./na_data 目录备份到 ./backups 文件夹中
  nekro-agent-toolkit --backup ./na_data ./backups
  # 或者从源码运行:
  python3 app.py --backup ./na_data ./backups
  ```
  > 脚本会自动生成带时间戳的备份文件，如 `na_backup_1678886400.tar.zstd`。

- **恢复**：使用 `-r` 或 `--recovery` 参数。需要提供备份文件和要恢复到的目标目录。
  ```bash
  nekro-agent-toolkit --recovery ./backups/na_backup_1678886400.tar.zstd ./na_data_new
  # 或者从源码运行:
  python3 app.py --recovery ./backups/na_backup_1678886400.tar.zstd ./na_data_new
  ```
  > **注意**: 恢复操作会覆盖目标目录中的文件，如果目录非空，程序会请求确认。

- **恢复并安装**：使用 `-ri` 或 `--recover-install` 参数。此命令会先执行恢复，然后在恢复的数据之上继续执行安装流程（如下载 `docker-compose.yml`，拉取镜像等）。
  ```bash
  nekro-agent-toolkit --recover-install ./backups/na_backup_1678886400.tar.zstd ./na_data_new
  # 或者从源码运行:
  python3 app.py --recover-install ./backups/na_backup_1678886400.tar.zstd ./na_data_new
  ```

## 安装过程高级说明

1. **依赖检查**：脚本会自动检查系统中是否安装了 Docker 和 Docker Compose。
2. **目录设置**：在您指定的路径创建应用数据目录。
3. **配置文件生成**：
    - 如果您指定的目录下已存在 `.env` 文件，脚本会直接使用它。
    - 否则，脚本会从远程仓库下载最新的 `.env.example` 作为模板，并自动填充必要的随机密钥。
4. **服务部署**：下载并启动 Docker 容器。
5. **防火墙配置**：如果系统使用 ufw，会自动配置防火墙规则。

## 访问信息

安装完成后，您可以通过以下方式访问服务：

- Web 管理界面：`http://127.0.0.1:8021`
- OneBot WebSocket 地址：`ws://127.0.0.1:8021/onebot/v11/ws`

如果启用了 NapCat 服务，还会提供：
- NapCat 服务端口：默认为 `6099`

## 注意事项

1. 如果您使用云服务器，请在云服务商的安全组中放行相应端口。
2. 如果需要从外部访问，请将地址中的 `127.0.0.1` 替换为您的服务器公网 IP。
3. 如果启用了 NapCat 服务，请使用 `sudo docker logs [容器名]napcat` 查看机器人 QQ 登录二维码。

## 故障排除

如果安装过程中遇到问题，请检查：

1. 确保系统已正确安装 Docker 和 Docker Compose。
2. 确保当前用户具有 sudo 权限。
3. 检查网络连接是否正常（安装过程需要从 GitHub 下载配置文件）。
4. 检查防火墙设置是否阻止了必要的端口。

## 许可证

请参考 [Nekro Agent 项目](https://github.com/KroMiose/nekro-agent) 获取许可证信息和[本项目](./LICENSE)。