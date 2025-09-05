[Read this in English](./REGULATE-EN.md)

# 项目开发规范

本文档定义了 nekro-agent-toolkit 项目的开发规范，包括代码编写、命名约定、注释标准等。所有贡献者都应遵循这些规范以确保代码质量和一致性。

## 代码编写规范

### Python 代码标准

1. **遵循 PEP 8**：所有 Python 代码应遵循 PEP 8 编码规范
2. **缩进**：使用 4 个空格缩进，不使用 Tab
3. **行长度**：每行代码不超过 88 个字符（兼容 Black 格式化工具）
4. **编码声明**：所有 Python 文件开头应包含 UTF-8 编码声明

```python
# -*- coding: utf-8 -*-
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

```
utils/
├── backup_utils.py
├── install_utils.py
├── helpers.py
└── i18n.py
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

### 消息键命名

- 使用小写字母和下划线
- 具有描述性，包含模块上下文
- 遵循层次结构

```python
# 正确示例
"backup_docker_volume_complete"
"error_create_docker_volume"
"excluding_logs_directory"
"restoring_via_container_starting"

# 错误示例
"msg1"  # 无意义
"BackupComplete"  # 驼峰命名
"docker_complete"  # 缺乏上下文
```

### 使用规范

1. **所有用户可见的消息必须多语言化**：

```python
# 正确
print(_('backup_success'))
print(_('error_directory_not_exist', dir_path))

# 错误
print("备份成功！")  # 硬编码中文
print(f"目录 {dir_path} 不存在")  # 硬编码格式
```

2. **同时更新中英文语言包**：

```python
# data/zh_CN/messages.py
"backup_success": "备份成功！备份文件已保存至:",

# data/en_US/messages.py
"backup_success": "Backup successful! Backup file saved to:",
```

### 备份过滤消息规范

备份过滤消息应明确区分不同类型的排除项：

```python
# 具体的过滤类型消息
"excluding_logs_directory": "排除日志目录: {}",
"excluding_uploads_directory": "排除上传目录: {}",
"excluding_env_template": "排除配置模板: {}",
"excluding_temp_file": "排除临时文件: {}",

# 避免使用通用消息
"excluding_from_archive": "正在排除: {}",  # 过于模糊
```

## 错误处理规范

### 异常处理

- 使用具体的异常类型而非通用的 `Exception`
- 提供有意义的错误消息
- 适当使用多语言支持

```python
try:
    subprocess.run(cmd, check=True, capture_output=True)
except subprocess.CalledProcessError as e:
    print(_('backup_docker_volume_failed', volume_name, e), file=sys.stderr)
    return False
except FileNotFoundError:
    print(_('error_command_not_found', 'docker'), file=sys.stderr)
    return False
```

### 返回值约定

- 布尔函数：成功返回 `True`，失败返回 `False`
- 路径函数：成功返回路径字符串，失败返回 `None`
- 列表/字典函数：成功返回数据，失败返回空容器

## 文件操作规范

### 路径处理

- 始终使用 `os.path` 进行路径操作
- 使用绝对路径进行文件操作
- 适当处理跨平台路径差异

```python
# 正确
backup_path = os.path.join(backup_dir, filename)
if os.path.exists(backup_path):
    pass

# 错误
backup_path = backup_dir + "/" + filename  # 硬编码分隔符
```

### 临时文件处理

- 使用 `tempfile` 模块创建临时文件
- 确保临时文件在操作完成后被清理

```python
import tempfile
import shutil

temp_dir = tempfile.mkdtemp()
try:
    # 使用临时目录
    pass
finally:
    shutil.rmtree(temp_dir)
```

## 特殊文件过滤规范

### 备份过滤规则

遵循 `特殊文件模式过滤规范`：

1. **精确匹配**：使用路径层级匹配而非简单字符串包含
2. **临时文件过滤**：所有以 `._` 开头的文件应被过滤
3. **目录保留**：包含被过滤文件的目录本身应被保留

```python
def exclude_filter(tarinfo: tarfile.TarInfo) -> Optional[tarfile.TarInfo]:
    """过滤规则实现示例"""
    path_parts = tarinfo.name.split('/')
    filename = os.path.basename(tarinfo.name)
    
    # 过滤临时文件
    if filename.startswith('._'):
        print(f"  - {_('excluding_temp_file', tarinfo.name)}")
        return None
    
    # 过滤特定目录
    if len(path_parts) >= 2 and path_parts[1] == 'logs':
        print(f"  - {_('excluding_logs_directory', tarinfo.name)}")
        return None
        
    return tarinfo
```

## 版本管理规范

### 版本信息显示格式

- 源码版本：`nekro-agent-toolkit (源码) abc12345`
- 包版本：`nekro-agent-toolkit 1.0.3`
- 脏版本：`nekro-agent-toolkit (源码) abc12345 (dirty)`

### 版本更新脚本

版本更新脚本应：
- 专注于版本信息更新
- 不包含与版本无关的功能
- 确保可维护性和目的明确性

## 测试规范

### 单元测试

- 为关键功能编写单元测试
- 测试文件命名：`test_*.py`
- 使用描述性的测试函数名

```python
def test_create_docker_volume_success():
    """测试成功创建 Docker 卷"""
    pass

def test_backup_with_invalid_path():
    """测试无效路径的备份行为"""
    pass
```

### 跨平台测试

- 在多个操作系统上验证功能
- 特别关注路径处理和命令执行
- 使用 `platform.system()` 进行系统检测

## 文档规范

### 开发文档

- 保持 Mermaid 架构图简洁明了
- 仅展示关键模块依赖关系
- 具有技术参考价值

### 用户文档

- 英文版文档保持精简
- 重点突出新功能
- 描述简洁明了

## 代码审查清单

提交代码前应检查：

- [ ] 遵循命名规范
- [ ] 包含适当的注释和文档字符串
- [ ] 所有用户消息已多语言化
- [ ] 错误处理得当
- [ ] 通过基本测试验证
- [ ] 符合项目整体架构

## 工具推荐

### 代码格式化

- **Black**：Python 代码自动格式化
- **isort**：导入语句排序

### 代码检查

- **flake8**：代码风格检查
- **mypy**：类型检查

### 使用示例

```bash
# 格式化代码
black --line-length 88 .

# 排序导入
isort .

# 代码检查
flake8 --max-line-length=88 .

# 类型检查
mypy --ignore-missing-imports .
```

遵循这些规范将有助于维护代码质量，提高代码可读性和可维护性，确保项目的长期健康发展。