[以中文阅读](./REGULATE.md)

# Project Development Standards

This document defines the coding style standards for the nekro-agent-toolkit project, including project structure, code conventions, and naming conventions.

## Project Architecture Overview

### Directory Structure

```
nekro-agent-toolkit/
├── app.py                  # Main entry point
├── conf/                   # Configuration files
│   ├── backup_settings.py  # Backup configuration
│   ├── i18n_settings.py   # I18n configuration
│   └── install_settings.py # Install configuration
├── data/                   # Multi-language data
│   ├── zh_CN/             # Chinese language pack
│   │   └── messages.py
│   └── en_US/             # English language pack
│       └── messages.py
├── module/                 # Feature modules
│   ├── backup.py          # Backup & recovery module
│   ├── install.py         # Install module
│   └── update.py          # Update module
├── utils/                  # Utility functions
│   ├── backup_utils.py    # Backup utilities
│   ├── helpers.py         # General utilities
│   └── i18n.py           # Multi-language support
└── doc/                   # Documentation
    ├── REGULATE.md        # Development standards (Chinese)
    └── REGULATE-EN.md     # Development standards (English)
```

### Component Description

- **app.py**: Main entry point
- **conf/**: Configuration files directory, using `xxx_settings.py` naming format
- **data/**: Multi-language data directory
- **module/**: Feature modules directory
- **utils/**: Utility functions directory

## Coding Standards

### Python Code Standards

1. **Follow PEP 8**: All Python code should follow PEP 8 coding standards
2. **Indentation**: Use 4 spaces for indentation, no tabs
3. **Line Length**: Each line should not exceed 88 characters (compatible with Black formatter)
4. **Encoding Declaration**: All Python files should include UTF-8 encoding declaration
5. **Type Annotations**: Support Python 3.6+ using typing module for type annotations

```python
# -*- coding: utf-8 -*-
"""
Module description
"""
from typing import Optional, Dict, List, Union
```

### Type Annotation Standards

For Python 3.6+ compatibility, use typing module instead of new-style type annotations:

```python
# Correct (Python 3.6+ compatible)
from typing import Optional, Dict, List, Union

def process_volumes(volume_names: List[str]) -> Dict[str, str]:
    pass

def get_backup_path(base_path: str) -> Optional[str]:
    pass

# Incorrect (Python 3.10+ only)
def process_volumes(volume_names: list[str]) -> dict[str, str]:
    pass

def get_backup_path(base_path: str) -> str | None:
    pass
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
from conf.backup_settings import DOCKER_VOLUME_SUFFIXES
```

## Configuration File Standards

### Configuration File Naming

Configuration files use `xxx_settings.py` format (using underscores, not hyphens) to comply with Python import standards:

```python
# Correct
from conf.backup_settings import DOCKER_VOLUME_SUFFIXES
from conf.i18n_settings import SUPPORTED_LANGUAGES

# Incorrect (cannot import)
from conf.backup-settings import DOCKER_VOLUME_SUFFIXES  # Hyphens cannot be used in Python module names
```

### Configuration File Structure

```python
# conf/backup_settings.py
"""
Backup functionality configuration file
"""

# Docker volume suffix matching patterns
DOCKER_VOLUME_SUFFIXES = ["nekro_postgres_data", "nekro_qdrant_data"]

# Compatibility: static configuration list
DOCKER_VOLUMES_TO_BACKUP: List[str] = ["nekro_postgres_data", "nekro_qdrant_data"]
```

## Naming Conventions

### Function Naming

- Use lowercase letters with underscores (snake_case)
- Function names should be descriptive and clearly express functionality

```python
# Correct examples
def create_docker_volume_if_not_exists(volume_name: str) -> bool:
    pass

def discover_docker_volumes_by_pattern(suffixes: Optional[List[str]] = None) -> List[str]:
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
- Configuration files use `xxx_settings.py` format

```
utils/
├── backup_utils.py      # Backup utilities
├── helpers.py          # General utilities
└── i18n.py            # Multi-language support

conf/
├── backup_settings.py  # Backup configuration
├── i18n_settings.py   # I18n configuration
└── install_settings.py # Install configuration
```

## Multi-language Support Standards

### Usage Standards

1. **Import multi-language function**:
```python
from utils.i18n import get_message as _
```

2. **Message calls**:
```python
# Correct way
print(_('backup_success'))
print(_('error_directory_not_exist', dir_path))

# Incorrect way (no hardcoding)
print("Backup successful!")  # Hardcoded English
```

3. **Message key naming**: Use snake_case, descriptive

## Development Tools

```bash
# Format code
black --line-length 88 .

# Sort imports
isort .

# Code check
flake8 --max-line-length=88 .
```

## Error Handling Standards

### Exception Handling

- Use specific exception types rather than generic `Exception`
- Provide meaningful error messages
- Properly use multi-language support
- Docker commands require special handling (tar warnings not treated as errors)

```python
try:
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Special handling for Docker/tar commands
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, cmd)
    
    # tar normal warnings not treated as errors
    if result.stderr and "Removing leading" in result.stderr:
        print(f"  - {_('tar_normal_warning', result.stderr.strip())}")
        
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

## Backup Filtering Standards

### Filter Rule Adjustments

**Current Rules**: Only filter files starting with `._` at root directory level, such files in subdirectories are no longer filtered.

```python
def exclude_filter(tarinfo: tarfile.TarInfo) -> Optional[tarfile.TarInfo]:
    """Backup filter function implementation"""
    path_parts = tarinfo.name.split('/')
    filename = os.path.basename(tarinfo.name)
    
    # Only filter ._ files at root directory level
    if len(path_parts) == 2 and filename.startswith('._'):
        print(f"  - {_('excluding_temp_file', tarinfo.name)}")
        return None
    
    # Filter specific directories
    if len(path_parts) >= 2 and path_parts[1] == 'logs':
        print(f"  - {_('excluding_logs_directory', tarinfo.name)}")
        return None
    
    if len(path_parts) >= 2 and path_parts[1] == 'uploads':
        print(f"  - {_('excluding_uploads_directory', tarinfo.name)}")
        return None
        
    # Filter .env.example files
    if len(path_parts) == 2 and path_parts[1] == '.env.example':
        print(f"  - {_('excluding_env_template', tarinfo.name)}")
        return None
        
    return tarinfo
```

### Filter Message Standards

Use specific filter type messages, avoid vague generic descriptions:

```python
# Correct: specific descriptions
"excluding_logs_directory": "Excluding logs directory: {}",
"excluding_uploads_directory": "Excluding uploads directory: {}",
"excluding_env_template": "Excluding config template: {}",
"excluding_temp_file": "Excluding temporary file: {}",

# Incorrect: vague descriptions
"excluding_from_archive": "Excluding: {}",  # Too vague
```

## Runtime Environment Detection Standards

### Detection Mechanism

Implement multiple detection mechanisms to determine runtime environment:

1. **Command Name Detection**: Check if `sys.argv[0]` contains project files
2. **Script Path Detection**: Check if script path is in project directory
3. **Source File Detection**: Check if current directory contains project source files
4. **Default Strategy**: Default to installed version when uncertain

```python
def is_running_from_source() -> bool:
    """Determine if running from source code"""
    # 1. Check command name
    if 'app.py' in sys.argv[0]:
        return True
    
    # 2. Check script path
    script_path = os.path.abspath(sys.argv[0])
    if 'nekro-agent-toolkit' in script_path and script_path.endswith('app.py'):
        return True
    
    # 3. Check source files
    current_dir = os.getcwd()
    source_files = ['app.py', 'utils', 'module', 'conf']
    if all(os.path.exists(os.path.join(current_dir, f)) for f in source_files):
        return True
    
    # 4. Default to installed version
    return False

def get_command_prefix() -> str:
    """Get command prefix"""
    if is_running_from_source():
        return 'python3 app.py'
    else:
        return 'nekro-agent-toolkit'
```

### Dynamic Help Information Display

Use dynamic command prefix in ArgumentParser's epilog:

```python
from utils.helpers import get_command_prefix

parser = argparse.ArgumentParser(
    description=_('app_description'),
    epilog=_('app_examples', 
             get_command_prefix(), get_command_prefix(), 
             get_command_prefix(), get_command_prefix(),
             get_command_prefix(), get_command_prefix()),
    formatter_class=argparse.RawDescriptionHelpFormatter
)
```

## Version Management Standards

### Version Information Display Format

- **Source Version**: `nekro-agent-toolkit (source) abc12345`
- **Package Version**: `nekro-agent-toolkit 1.0.3`
- **Dirty Version**: `nekro-agent-toolkit (source) abc12345 (dirty)`

### Version Detection Mechanism

```python
def get_version_info() -> str:
    """Get version information"""
    if is_running_from_source():
        # Source running: display Git SHA
        try:
            git_sha = subprocess.check_output(
                ['git', 'rev-parse', '--short', 'HEAD'],
                cwd=project_root, text=True
            ).strip()
            
            # Check for uncommitted changes
            try:
                subprocess.check_output(
                    ['git', 'diff-index', '--quiet', 'HEAD'],
                    cwd=project_root
                )
                dirty = ""
            except subprocess.CalledProcessError:
                dirty = " (dirty)"
                
            return f"nekro-agent-toolkit (source) {git_sha}{dirty}"
        except:
            return "nekro-agent-toolkit (source) unknown"
    else:
        # Installed version: display package version
        return f"nekro-agent-toolkit {__version__}"
```

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
- Validate test files individually, ensuring compilation success

```python
def test_docker_volume_suffix_matching():
    """Test Docker volume suffix matching functionality"""
    suffixes = ["nekro_postgres_data", "nekro_qdrant_data"]
    
    # Test correct matching
    assert "my_app-nekro_postgres_data".endswith("nekro_postgres_data")
    assert "production-nekro_qdrant_data".endswith("nekro_qdrant_data")
    
    # Test non-matching
    assert not "nekro_postgres_data_backup".endswith("nekro_postgres_data")
    assert not "postgres_data".endswith("nekro_postgres_data")

def test_backup_with_invalid_path():
    """Test backup behavior with invalid path"""
    pass
```

### Test Execution Standards

1. **Individual Validation**: Validate immediately after generating one test file
2. **Compilation Check**: Fix any compilation issues
3. **Sequential Process**: Only proceed to next file after current file succeeds
4. **Immediate Execution**: Must execute immediately after writing tests and report results

### Cross-platform Testing

- Verify functionality on multiple operating systems
- Pay special attention to path handling and command execution
- Use `platform.system()` for system detection

## Code Review Checklist

Before submitting code, check:

- [ ] Follow naming conventions (snake_case, config files use xxx_settings.py)
- [ ] Include appropriate comments and docstrings
- [ ] All user messages are internationalized (using _() function)
- [ ] Error handling is appropriate (especially for Docker/tar commands)
- [ ] Type annotations compatible with Python 3.6+ (using typing module)
- [ ] Docker volume matching logic correct (suffix matching only)
- [ ] Backup filter rules correct (only filter ._ files at root directory)
- [ ] Pass basic test verification
- [ ] Conform to overall project architecture
- [ ] Use get_problems to validate code syntax

## Development Tools Recommendations

### Code Formatting

- **Black**: Python code auto-formatting
- **isort**: Import statement sorting

### Code Checking

- **flake8**: Code style checking
- **mypy**: Type checking (optional)

### Usage Examples

```bash
# Format code
black --line-length 88 .

# Sort imports
isort .

# Code checking
flake8 --max-line-length=88 .

# Type checking (optional)
mypy --ignore-missing-imports .

# Syntax checking
python3 -m py_compile file.py
```

## Summary

Following these standards will help:

1. **Improve Code Quality**: Through unified coding style and standards
2. **Enhance Readability**: Clear naming and commenting standards
3. **Ensure Compatibility**: Support Python 3.6+ and cross-platform operation
4. **Improve User Experience**: Complete multi-language support
5. **Ensure Stability**: Comprehensive error handling and testing mechanisms
6. **Facilitate Maintenance**: Clear module division and documentation standards

These standards are formulated based on the actual situation of the nekro-agent-toolkit project, aiming to ensure the long-term healthy development of the project.

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