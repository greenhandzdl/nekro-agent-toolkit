# GitHub Action 生成安装文件

本项目提供了一个 GitHub Action 工作流，用于自动生成和更新安装所需的配置文件。

## 功能概述

`Generate Installer Files` 工作流可以自动完成以下任务：

1. **生成 .env 配置文件** - 运行 install 模块的 dry-run 模式，生成包含随机密钥的配置文件
2. **下载 docker-compose 文件** - 从远程仓库获取 docker-compose.yml 或 docker-compose-x-napcat.yml
3. **自动提交更新** - 将生成的文件自动提交到仓库的 `installer/` 目录

## 使用方法

### 手动触发

1. 转到项目的 **Actions** 页面
2. 选择 **Generate Installer Files** 工作流
3. 点击 **Run workflow** 按钮
4. 配置选项：
   - **Include NapCat service**: 是否包含 NapCat 服务（默认启用）
   - **Language**: 提交信息的语言（zh_CN / en_US）
5. 点击 **Run workflow** 开始执行

### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| with_napcat | boolean | true | 是否包含 NapCat 服务 |
| language | choice | en_US | 提交信息的语言 |

## 输出文件

工作流执行完成后，会在 `installer/` 目录下生成以下文件：

```
installer/
├── .env                 # 环境配置文件（包含随机生成的密钥）
└── docker-compose.yml   # Docker Compose 配置文件
```

## 相关链接

- [English Documentation](./action-en_US.md)
- [安装模块文档](../README)
- [开发文档](../DEVELOP.md)