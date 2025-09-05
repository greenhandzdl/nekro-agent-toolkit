# Python 版本兼容性说明

## 修复内容

修复了 Python 3.9 兼容性问题，将 Python 3.10+ 的联合类型注解改为向后兼容的格式。

### 修复的类型注解

#### 1. utils/backup_utils.py

**修复前 (Python 3.10+ 语法):**
```python
def create_archive(source_paths: dict[str, str], dest_path_base: str) -> str | None:
def get_docker_volumes(volume_names: list[str]) -> dict[str, str]:
def extract_archive(archive_path: str, dest_dir: str, volume_mountpoints: dict[str, str] | None = None) -> bool:
def exclude_filter(tarinfo: tarfile.TarInfo) -> tarfile.TarInfo | None:
def get_archive_root_dir(archive_path: str, inspect_path: str | None = None) -> str | None:
```

**修复后 (Python 3.6+ 兼容):**
```python
from typing import Union, Optional, Dict, List

def create_archive(source_paths: Dict[str, str], dest_path_base: str) -> Optional[str]:
def get_docker_volumes(volume_names: List[str]) -> Dict[str, str]:
def extract_archive(archive_path: str, dest_dir: str, volume_mountpoints: Optional[Dict[str, str]] = None) -> bool:
def exclude_filter(tarinfo: tarfile.TarInfo) -> Optional[tarfile.TarInfo]:
def get_archive_root_dir(archive_path: str, inspect_path: Optional[str] = None) -> Optional[str]:
```

#### 2. utils/helpers.py

**修复前:**
```python
def get_docker_compose_cmd():
    """
    返回:
        str | None: 如果找到，返回 'docker-compose' 或 'docker compose' 字符串；
    """
```

**修复后:**
```python
from typing import Optional

def get_docker_compose_cmd() -> Optional[str]:
    """
    返回:
        Optional[str]: 如果找到，返回 'docker-compose' 或 'docker compose' 字符串；
    """
```

## 兼容性支持

现在项目支持以下Python版本：
- ✅ Python 3.6+
- ✅ Python 3.7
- ✅ Python 3.8  
- ✅ Python 3.9 (修复后)
- ✅ Python 3.10+
- ✅ Python 3.11

## 类型注解映射表

| Python 3.10+ 语法 | Python 3.6+ 兼容语法 | 说明 |
|------------------|-------------------|------|
| `str \| None` | `Optional[str]` | 可选字符串 |
| `list[str]` | `List[str]` | 字符串列表 |
| `dict[str, str]` | `Dict[str, str]` | 字典类型 |
| `A \| B` | `Union[A, B]` | 联合类型 |

## 最佳实践

1. **向后兼容**: 使用 `typing` 模块的类型注解确保向后兼容
2. **导入管理**: 统一从 `typing` 导入类型注解
3. **文档一致性**: 确保函数文档字符串中的类型描述与注解一致

## 验证方法

可以使用以下命令验证语法正确性：

```bash
# 编译检查
python3 -m py_compile utils/backup_utils.py
python3 -m py_compile utils/helpers.py

# 导入测试
python3 -c "from utils.backup_utils import create_archive; print('导入成功')"
```