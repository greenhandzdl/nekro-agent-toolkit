[Read this in English](./doc/README-EN.md)

# Nekro Agent Toolkit

Nekro Agent Toolkit 是一个用于快速部署 Nekro Agent 及其相关服务的专业安装工具。它简化了基于 Docker 的 QQ 机器人服务部署流程，提供完整的安装、更新、备份和恢复解决方案。

## ✨ 核心特性

- **统一管理**：单一脚本处理所有操作，智能环境检测
- **多语言支持**：中英文界面自动切换
- **默认数据目录**：简化命令操作，自动填充预设目录
- **智能备份**：跨平台Docker卷备份，动态发现，精确过滤
- **版本显示**：源码运行显示Git SHA，包安装显示版本号

## 🚀 安装与使用

### 安装

```bash
# pip 安装（推荐）
pip install nekro-agent-toolkit

# 源码运行
git clone https://github.com/your-repo/nekro-agent-toolkit.git
cd nekro-agent-toolkit
```

> [!NOTE]
> 安装完后请看[协议端配置](https://doc.nekro.ai/docs/02_quick_start/config/protocol),[系统配置](https://doc.nekro.ai/docs/02_quick_start/config/system)注意改密码。

### 默认数据目录管理

```bash
# 设置默认目录
nekro-agent-toolkit -sd ./na_data

# 查看当前设置（输入 clear 可清除）
nekro-agent-toolkit -sd
```

### 常用命令

```bash
# 安装（可自动使用默认目录）
nekro-agent-toolkit -i [PATH]

# 更新/升级（可自动使用默认目录）
nekro-agent-toolkit -u [PATH]    # 部分更新
nekro-agent-toolkit -ua [PATH]   # 完整升级

# 备份与恢复（可自动使用默认目录）
nekro-agent-toolkit -b [DATA_DIR] BACKUP_DIR
nekro-agent-toolkit -r BACKUP_FILE [DATA_DIR]
nekro-agent-toolkit -ri BACKUP_FILE [INSTALL_DIR]

# 选项
--with-napcat    # 部署 NapCat 服务
--dry-run        # 预演模式
-y               # 自动确认
```

## 📝 附加信息

**系统要求**：Python 3.6+、Docker、Docker Compose

**可选软件**：zstd（快速压缩）、ufw（防火墙）

**贡献指南**：参考 [`doc/REGULATE.md`](./doc/REGULATE.md)

**许可证**：参考 [Nekro Agent 项目](https://github.com/KroMiose/nekro-agent) 和 [LICENSE](./LICENSE)