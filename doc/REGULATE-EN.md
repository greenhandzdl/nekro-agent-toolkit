[以中文阅读](./REGULATE.md)

# Project Development Standards

This document defines the development standards for the nekro-agent-toolkit project, including coding practices, naming conventions, commenting standards, etc. All contributors should follow these standards to ensure code quality and consistency.

## Coding Standards

### Python Code Standards

1. **Follow PEP 8**: All Python code should follow PEP 8 coding standards
2. **Indentation**: Use 4 spaces for indentation, no tabs
3. **Line Length**: Each line should not exceed 88 characters (compatible with Black formatter)
4. **Encoding Declaration**: All Python files should include UTF-8 encoding declaration at the beginning

```python
# -*- coding: utf-8 -*-
```

### Import Standards

Import statements should be organized in the following order, with blank lines between groups:

1. Standard library imports
2. Third-party library imports
3. Local module imports

```python
# Standard library
import os
import sys
import subprocess
from typing import Optional, Dict, List

# Third-party libraries
import requests

# Local modules
from utils.helpers import command_exists
from utils.i18n import get_message as _
```

## Naming Conventions

### Function Naming

- Use lowercase letters with underscores (snake_case)
- Function names should be descriptive and clearly express functionality

```python
# Correct examples
def create_docker_volume_if_not_exists(volume_name: str) -> bool:
    pass

def get_docker_volumes_for_recovery(volume_names: List[str]) -> Dict[str, str]:
    pass

# Incorrect examples
def createVol(name):  # CamelCase + abbreviation
    pass
```

### Variable Naming

- Use lowercase letters with underscores (snake_case)
- Constants use all uppercase letters with underscores

```python
# Variables
volume_name = "nekro_postgres_data"
backup_file_path = "/path/to/backup.tar.zstd"

# Constants
DOCKER_VOLUMES_TO_BACKUP = ["nekro_postgres_data", "nekro_qdrant_data"]
DEFAULT_TIMEOUT = 30
```

### Class Naming

- Use PascalCase
- Class names should be nouns and descriptive

```python
class BackupManager:
    pass

class DockerVolumeHandler:
    pass
```

### File and Directory Naming

- Use lowercase letters with underscores
- Python module files use `.py` extension
- Directory names should be concise and clear

```
utils/
├── backup_utils.py
├── install_utils.py
├── helpers.py
└── i18n.py
```

## Comment Standards

### Module-level Comments

Each Python file should start with a module docstring:

```python
# -*- coding: utf-8 -*-
"""
Low-level utility functions for backup and recovery features.

This module provides cross-platform Docker volume backup and recovery functionality, supporting:
- Linux system direct filesystem access
- macOS/Windows system containerized backup
- Intelligent volume management and automatic creation
"""
```

### Function Comments

Use Google-style docstrings:

```python
def create_docker_volume_if_not_exists(volume_name: str) -> bool:
    """Create Docker volume if it doesn't exist.
    
    Args:
        volume_name (str): Name of the Docker volume to create.
        
    Returns:
        bool: True if volume exists or creation successful, False on failure.
        
    Raises:
        subprocess.CalledProcessError: When Docker command execution fails.
    """
    pass
```

### Inline Comments

- Used to explain complex logic or non-obvious code
- Comments should be kept in sync with code updates

```python
# Check if volume already exists
result = subprocess.run(
    ["docker", "volume", "inspect", volume_name],
    capture_output=True,
    text=True,
    check=True
)

# tar command may output warning "Removing leading `/' from member names"
# This is normal behavior, success is indicated by return code 0
if result.returncode != 0:
    raise subprocess.CalledProcessError(result.returncode, cmd)
```

## Multi-language Support Standards

### Message Key Naming

- Use lowercase letters with underscores
- Descriptive, include module context
- Follow hierarchical structure

```python
# Correct examples
"backup_docker_volume_complete"
"error_create_docker_volume"
"excluding_logs_directory"
"restoring_via_container_starting"

# Incorrect examples
"msg1"  # Meaningless
"BackupComplete"  # CamelCase
"docker_complete"  # Lacks context
```

### Usage Standards

1. **All user-visible messages must be internationalized**:

```python
# Correct
print(_('backup_success'))
print(_('error_directory_not_exist', dir_path))

# Incorrect
print("Backup successful!")  # Hardcoded English
print(f"Directory {dir_path} does not exist")  # Hardcoded format
```

2. **Update both Chinese and English language packs**:

```python
# data/zh_CN/messages.py
"backup_success": "备份成功！备份文件已保存至:",

# data/en_US/messages.py
"backup_success": "Backup successful! Backup file saved to:",
```

### Backup Filter Message Standards

Backup filter messages should clearly distinguish different types of exclusions:

```python
# Specific filter type messages
"excluding_logs_directory": "Excluding logs directory: {}",
"excluding_uploads_directory": "Excluding uploads directory: {}",
"excluding_env_template": "Excluding config template: {}",
"excluding_temp_file": "Excluding temporary file: {}",

# Avoid generic messages
"excluding_from_archive": "Excluding: {}",  # Too vague
```

## Error Handling Standards

### Exception Handling

- Use specific exception types rather than generic `Exception`
- Provide meaningful error messages
- Properly use multi-language support

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

### Return Value Conventions

- Boolean functions: Return `True` on success, `False` on failure
- Path functions: Return path string on success, `None` on failure
- List/dict functions: Return data on success, empty container on failure

## File Operation Standards

### Path Handling

- Always use `os.path` for path operations
- Use absolute paths for file operations
- Properly handle cross-platform path differences

```python
# Correct
backup_path = os.path.join(backup_dir, filename)
if os.path.exists(backup_path):
    pass

# Incorrect
backup_path = backup_dir + "/" + filename  # Hardcoded separator
```

### Temporary File Handling

- Use `tempfile` module to create temporary files
- Ensure temporary files are cleaned up after operations

```python
import tempfile
import shutil

temp_dir = tempfile.mkdtemp()
try:
    # Use temporary directory
    pass
finally:
    shutil.rmtree(temp_dir)
```

## Special File Filtering Standards

### Backup Filter Rules

Follow `Special File Pattern Filtering Standards`:

1. **Exact Matching**: Use path hierarchy matching rather than simple string containment
2. **Temporary File Filtering**: All files starting with `._` should be filtered
3. **Directory Preservation**: Directories containing filtered files should themselves be preserved

```python
def exclude_filter(tarinfo: tarfile.TarInfo) -> Optional[tarfile.TarInfo]:
    """Filter rule implementation example"""
    path_parts = tarinfo.name.split('/')
    filename = os.path.basename(tarinfo.name)
    
    # Filter temporary files
    if filename.startswith('._'):
        print(f"  - {_('excluding_temp_file', tarinfo.name)}")
        return None
    
    # Filter specific directories
    if len(path_parts) >= 2 and path_parts[1] == 'logs':
        print(f"  - {_('excluding_logs_directory', tarinfo.name)}")
        return None
        
    return tarinfo
```

## Version Management Standards

### Version Information Display Format

- Source version: `nekro-agent-toolkit (源码) abc12345`
- Package version: `nekro-agent-toolkit 1.0.3`
- Dirty version: `nekro-agent-toolkit (源码) abc12345 (dirty)`

### Version Update Scripts

Version update scripts should:
- Focus on version information updates
- Not include version-unrelated functionality
- Ensure maintainability and clear purpose

## Testing Standards

### Unit Testing

- Write unit tests for key functionality
- Test file naming: `test_*.py`
- Use descriptive test function names

```python
def test_create_docker_volume_success():
    """Test successful Docker volume creation"""
    pass

def test_backup_with_invalid_path():
    """Test backup behavior with invalid path"""
    pass
```

### Cross-platform Testing

- Verify functionality on multiple operating systems
- Pay special attention to path handling and command execution
- Use `platform.system()` for system detection

## Documentation Standards

### Development Documentation

- Keep Mermaid architecture diagrams simple and clear
- Only show key module dependencies
- Provide technical reference value

### User Documentation

- Keep English documentation concise
- Highlight new features
- Keep descriptions brief and clear

## Code Review Checklist

Check before submitting code:

- [ ] Follows naming conventions
- [ ] Includes appropriate comments and docstrings
- [ ] All user messages are internationalized
- [ ] Proper error handling
- [ ] Passes basic test verification
- [ ] Conforms to overall project architecture

## Recommended Tools

### Code Formatting

- **Black**: Python code auto-formatting
- **isort**: Import statement sorting

### Code Checking

- **flake8**: Code style checking
- **mypy**: Type checking

### Usage Examples

```bash
# Format code
black --line-length 88 .

# Sort imports
isort .

# Code checking
flake8 --max-line-length=88 .

# Type checking
mypy --ignore-missing-imports .
```

Following these standards will help maintain code quality, improve code readability and maintainability, and ensure the long-term healthy development of the project.