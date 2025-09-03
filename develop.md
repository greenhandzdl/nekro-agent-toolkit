[Read this in English](./DEVELOP-EN.md)

# 开发者指南

本文档概述了项目的内部结构和模块关系，以帮助未来开发。

## 项目结构

项目被组织为以下几个主要目录：

- `app.py`: 项目的统一命令行入口，负责调度安装、更新和备份恢复任务。
- `module/`: 封装了核心功能的模块，可被外部调用。
  - `install.py`: 提供 `install_agent` 函数。
  - `update.py`: 提供 `update_agent` 函数。
  - `backup.py`: 提供 `backup_agent`、`recover_agent` 和 `recover_and_install_agent` 函数。
- `utils/`: 存放辅助函数。
  - `helpers.py`: 底层的、跨模块共享的工具函数（如系统命令、文件操作）。
  - `install_utils.py`: 服务于安装流程的高级函数。
  - `update_utils.py`: 服务于更新流程的高级函数。
  - `backup_utils.py`: 服务于备份恢复的底层函数（如打包、解压、分析归档）。
- `conf/`: 存放静态配置文件。
  - `settings.py`: 共享的配置，如远程仓库 URL。

## 模块关系图

下图展示了不同模块之间的导入和依赖关系。

```mermaid
graph TD
    subgraph "主入口 (Main Entry Point)"
        APP["app.py"];
    end

    subgraph "高级 API 模块"
        INSTALL["module/install.py"];
        UPDATE["module/update.py"];
        BACKUP["module/backup.py"];
    end

    subgraph "业务逻辑 (Business Logic)"
        INSTALL_UTILS["utils/install_utils.py"];
        UPDATE_UTILS["utils/update_utils.py"];
        BACKUP_UTILS["utils/backup_utils.py"];
    end

    subgraph "共享库 (Shared Libraries)"
        HELPERS["utils/helpers.py"];
        CONF["conf/settings.py"];
    end

    APP -- 调用 --> INSTALL;
    APP -- 调用 --> UPDATE;
    APP -- 调用 --> BACKUP;

    INSTALL -- 调用 --> INSTALL_UTILS;
    UPDATE -- 调用 --> UPDATE_UTILS;
    BACKUP -- 调用 --> BACKUP_UTILS;
    BACKUP -- 调用 --> INSTALL;
    
    INSTALL_UTILS -- 导入 --> HELPERS;
    UPDATE_UTILS -- 导入 --> HELPERS;
    BACKUP_UTILS -- 导入 --> HELPERS;

    HELPERS -- 导入 --> CONF;
```
