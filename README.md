[Read this in English](./doc/README-EN.md)

# Nekro Agent Toolkit

Nekro Agent Toolkit 是一款用于一站式部署、备份、恢复 Nekro Agent 及相关服务的工具，支持 Docker 环境下的自动化管理。

## ✨ 主要功能

- 一键安装、升级、备份与恢复 Nekro Agent
- 智能检测与多语言支持
- 支持 Docker 卷自动备份与恢复

## 🚀 快速使用

### 安装

```bash
pip install nekro-agent-toolkit
# 或源码运行
git clone https://github.com/your-repo/nekro-agent-toolkit.git
cd nekro-agent-toolkit
```

### 常用命令

```bash
# 安装/升级/备份/恢复
nekro-agent-toolkit -i [PATH]
nekro-agent-toolkit -u [PATH]
nekro-agent-toolkit -b [DATA_DIR] BACKUP_DIR
nekro-agent-toolkit -r BACKUP_FILE [DATA_DIR]
```

### 使用 uv 管理依赖（推荐）

本项目现在支持使用 `uv` 来管理依赖与生成可重现的锁文件 `uv.lock`。


## 附加信息

- 系统要求：Python 3.6+，Docker，Docker Compose
- 许可证：见 [LICENSE](./LICENSE)
