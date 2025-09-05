[Read this in English](./REGULATE-EN.md)

# 项目开发规范

本文档定义了 nekro-agent-toolkit 项目的编码风格规范，包括项目结构、代码规范、命名约定等。

## 项目架构概览

### 目录结构

```
nekro-agent-toolkit/
├── app.py                  # 主入口文件
├── conf/                   # 配置文件目录
│   ├── backup_settings.py  # 备份功能配置
│   ├── i18n_settings.py   # 多语言配置
│   └── install_settings.py # 安装功能配置
├── data/                   # 多语言数据目录
│   ├── zh_CN/             # 中文语言包
│   │   └── messages.py
│   └── en_US/             # 英文语言包
│       └── messages.py
├── module/                 # 功能模块目录
│   ├── backup.py          # 备份与恢复模块
│   ├── install.py         # 安装模块
│   └── update.py          # 更新模块
├── utils/                  # 工具函数目录
│   ├── backup_utils.py    # 备份工具函数
│   ├── helpers.py         # 通用工具函数
│   └── i18n.py           # 多语言支持
└── doc/                   # 文档目录
    ├── REGULATE.md        # 开发规范(中文)
    └── REGULATE-EN.md     # 开发规范(英文)
```

### 组件说明

- **app.py**: 主入口文件
- **conf/**: 配置文件目录，使用 `xxx_settings.py` 命名格式
- **data/**: 多语言数据目录
- **module/**: 功能模块目录
- **utils/**: 工具函数目录

## 代码编写规范

### Python 代码标准

1. **遵循 PEP 8**：所有 Python 代码应遵循 PEP 8 编码规范
2. **缩进**：使用 4 个空格缩进，不使用 Tab
3. **行长度**：每行代码不超过 88 个字符（兼容 Black 格式化工具）
4. **编码声明**：所有 Python 文件开头应包含 UTF-8 编码声明
5. **类型注解**：支持 Python 3.6+，使用 typing 模块进行类型注解

```python
# -*- coding: utf-8 -*-
"""
模块描述
"""
from typing import Optional, Dict, List, Union
```

### 类型注解规范

为了兼容 Python 3.6+，使用 typing 模块而不是新式类型注解：

```python
# 正确（兼容 Python 3.6+）
from typing import Optional, Dict, List, Union

def process_volumes(volume_names: List[str]) -> Dict[str, str]:
    pass

def get_backup_path(base_path: str) -> Optional[str]:
    pass

# 错误（仅 Python 3.10+ 支持）
def process_volumes(volume_names: list[str]) -> dict[str, str]:
    pass

def get_backup_path(base_path: str) -> str | None:
    pass
```

### 导入规范

导入语句应按以下顺序组织，各组之间用空行分隔：

1. 标准库导入
2. 第三方库导入
3. 本地模块导入

```python
# 标准库
import os
import sys
import subprocess
from typing import Optional, Dict, List

# 第三方库
import requests

# 本地模块
from utils.helpers import command_exists
from utils.i18n import get_message as _
from conf.backup_settings import DOCKER_VOLUME_SUFFIXES
```

## 配置文件规范

### 配置文件命名

配置文件使用 `xxx_settings.py` 格式（使用下划线而非破折号），以符合 Python 导入规范：

```python
# 正确
from conf.backup_settings import DOCKER_VOLUME_SUFFIXES
from conf.i18n_settings import SUPPORTED_LANGUAGES

# 错误（无法导入）
from conf.backup-settings import DOCKER_VOLUME_SUFFIXES  # 破折号不能用于 Python 模块名
```

### 配置文件结构

```python
# conf/backup_settings.py
"""
备份功能配置文件
"""

# Docker 卷后缀匹配模式
DOCKER_VOLUME_SUFFIXES = ["nekro_postgres_data", "nekro_qdrant_data"]

# 兼容性：静态配置列表
DOCKER_VOLUMES_TO_BACKUP: List[str] = ["nekro_postgres_data", "nekro_qdrant_data"]
```

## 命名规范

### 函数命名

- 使用小写字母和下划线（snake_case）
- 函数名应具有描述性，清楚表达功能

```python
# 正确示例
def create_docker_volume_if_not_exists(volume_name: str) -> bool:
    pass

def get_docker_volumes_for_recovery(volume_names: List[str]) -> Dict[str, str]:
    pass

# 错误示例
def createVol(name):  # 驼峰命名 + 缩写
    pass
```

### 变量命名

- 使用小写字母和下划线（snake_case）
- 常量使用全大写字母和下划线

```python
# 变量
volume_name = "nekro_postgres_data"
backup_file_path = "/path/to/backup.tar.zstd"

# 常量
DOCKER_VOLUMES_TO_BACKUP = ["nekro_postgres_data", "nekro_qdrant_data"]
DEFAULT_TIMEOUT = 30
```

### 类命名

- 使用帕斯卡命名法（PascalCase）
- 类名应为名词，具有描述性

```python
class BackupManager:
    pass

class DockerVolumeHandler:
    pass
```

### 文件和目录命名

- 使用小写字母和下划线
- Python 模块文件使用 `.py` 扩展名
- 目录名简洁明了
- 配置文件使用 `xxx_settings.py` 格式

```
utils/
├── backup_utils.py      # 备份工具函数
├── helpers.py          # 通用工具函数
└── i18n.py            # 多语言支持

conf/
├── backup_settings.py  # 备份配置
├── i18n_settings.py   # 多语言配置
└── install_settings.py # 安装配置
```

## 注释规范

### 模块级注释

每个 Python 文件开头应包含模块文档字符串：

```python
# -*- coding: utf-8 -*-
"""
备份与恢复功能的底层辅助函数。

本模块提供跨平台的 Docker 卷备份和恢复功能，支持：
- Linux 系统直接文件系统访问
- macOS/Windows 系统容器化备份
- 智能卷管理和自动创建
"""
```

### 函数注释

使用 Google 风格的文档字符串：

```python
def create_docker_volume_if_not_exists(volume_name: str) -> bool:
    """如果 Docker 卷不存在，则创建它。
    
    Args:
        volume_name (str): 要创建的 Docker 卷名称。
        
    Returns:
        bool: 卷存在或创建成功返回 True，失败返回 False。
        
    Raises:
        subprocess.CalledProcessError: 当 Docker 命令执行失败时。
    """
    pass
```

### 行内注释

- 用于解释复杂逻辑或不明显的代码
- 注释应与代码保持同步更新

```python
# 检查卷是否已经存在
result = subprocess.run(
    ["docker", "volume", "inspect", volume_name],
    capture_output=True,
    text=True,
    check=True
)

# tar 命令可能会输出警告 "Removing leading `/' from member names"
# 这是正常行为，只要返回码为 0 就表示成功
if result.returncode != 0:
    raise subprocess.CalledProcessError(result.returncode, cmd)
```

## 多语言支持规范

### 使用规范

1. **导入多语言函数**：
```python
from utils.i18n import get_message as _
```

2. **消息调用**：
```python
# 正确方式
print(_('backup_success'))
print(_('error_directory_not_exist', dir_path))

# 错误方式（禁止硬编码）
print("备份成功！")  # 硬编码中文
```

3. **消息键命名**：使用 snake_case，具有描述性

















## 开发工具推荐

```bash
# 格式化代码
black --line-length 88 .

# 排序导入
isort .

# 代码检查
flake8 --max-line-length=88 .
```