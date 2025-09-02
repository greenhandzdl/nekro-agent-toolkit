# Nekro Agent 安装器

Nekro Agent 是一个基于 Docker 的应用程序，可以与 QQ 机器人结合使用。本安装器可以帮助您快速部署 Nekro Agent 及其相关服务。

## 功能特性

- 自动检查系统依赖（Docker 和 Docker Compose）
- 自动下载和配置所需的配置文件
> [!NOTE]
> 
> 如果存在'.env'文件，那么脚本会用你提供的文件。
> 
> 即使存在'docker-compose.yml'文件也会下，这可能会保证你一直在使用新的容器。
- 支持一键部署 Nekro Agent 主服务
- 可选集成 NapCat QQ 机器人服务
- 自动生成安全密钥和访问令牌
- 自动配置防火墙规则（如果使用 ufw）

## 系统要求

- Linux 或类 Unix 操作系统
- Docker 已安装
- Docker Compose 已安装
- 管理员权限（sudo）

## 安装方式

### 自动安装（推荐）

```bash
# 下载并运行安装脚本
curl -O https://raw.githubusercontent.com/greenhandzdl/nekro-agent-installer/main/install.py
chmod +x install.py
python3 install.py
```

### 使用参数安装

```bash
# 启用 NapCat 服务安装
python3 install.py --with-napcat
# 不启用 NapCat 服务安装（不受支持）
# 这玩意本来就要折腾，要么你自己看源代码改，要么你自己按照自动安装流程走。
```

## 安装过程说明

1. **依赖检查**：脚本会自动检查系统中是否安装了 Docker 和 Docker Compose
2. **目录设置**：创建应用数据目录，在**脚本运行目录**下。可以参考`setup_directories`函数，或者搜索`nekro_data_dir`变量，与原项目不同。
3. **配置文件生成**：自动下载 `.env` 配置文件并生成必要的安全密钥
> 你有'.env'，那么就用你自己的了。
4. **用户确认**：在正式安装前会提示用户确认配置
5. **服务部署**：下载并启动 Docker 容器
6. **防火墙配置**：如果系统使用 ufw，会自动配置防火墙规则

## 配置说明

安装过程中会自动生成以下配置项：

- `ONEBOT_ACCESS_TOKEN`：OneBot 访问令牌（32位随机字符串）
- `NEKRO_ADMIN_PASSWORD`：管理员密码（16位随机字符串）
- `QDRANT_API_KEY`：Qdrant API 密钥（32位随机字符串）

您可以在 `.env` 文件中修改这些配置以及其他选项。

## 访问信息

安装完成后，您可以通过以下方式访问服务：

- Web 管理界面：`http://127.0.0.1:8021`
- OneBot WebSocket 地址：`ws://127.0.0.1:8021/onebot/v11/ws`

如果启用了 NapCat 服务，还会提供：
- NapCat 服务端口：默认为 `6099`

## 注意事项

1. 如果您使用云服务器，请在云服务商的安全组中放行相应端口
2. 如果需要从外部访问，请将地址中的 `127.0.0.1` 替换为您的服务器公网 IP
3. 如果启用了 NapCat 服务，请使用 `sudo docker logs [容器名]napcat` 查看机器人 QQ 登录二维码

## 常用管理命令

```bash
# 查看 Nekro Agent 服务日志
sudo docker logs -f [实例名]nekro_agent

# 查看 NapCat 服务日志（如果启用）
sudo docker logs -f [实例名]napcat

# 停止服务
sudo docker-compose down

# 启动服务
sudo docker-compose up -d

# 更新服务
sudo docker-compose pull
```

## 故障排除

如果安装过程中遇到问题，请检查：

1. 确保系统已正确安装 Docker 和 Docker Compose
2. 确保当前用户具有 sudo 权限
3. 检查网络连接是否正常（安装过程需要从 GitHub 下载配置文件）
4. 检查防火墙设置是否阻止了必要的端口

## 许可证

请参考 [Nekro Agent 项目](https://github.com/KroMiose/nekro-agent) 获取许可证信息。