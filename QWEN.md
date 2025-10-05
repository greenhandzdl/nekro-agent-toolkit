# Nekro Agent Toolkit - Project Documentation

## Overview
Nekro Agent Toolkit is a comprehensive installation, update, and backup management tool for the Nekro Agent (a QQ bot service) that uses Docker for deployment.

## Key Features
1. **Unified Management**: Single script handles all operations with intelligent environment detection
2. **Multi-language Support**: Automatic Chinese/English interface switching
3. **Default Data Directory**: Simplified command operations with preset directories
4. **Smart Backup**: Cross-platform Docker volume backup with dynamic discovery
5. **Version Display**: Shows Git SHA for source runs or version number for package installs

## Architecture
- **Main Entry Point**: `app.py` - handles command-line arguments and dispatches to modules
- **Core Modules**:
  - `install.py` - handles Nekro Agent installation with optional NapCat service
  - `update.py` - manages partial or complete updates of services
  - `backup.py` - creates and restores backups including Docker volumes
- **Utility Modules**:
  - `helpers.py` - common functions for system operations, Docker handling, permissions
  - `install_utils.py`, `update_utils.py`, `backup_utils.py` - specific utility functions
- **Configuration**: `conf/` directory with settings for installation, backup, and i18n
- **Internationalization**: `data/` directory with Chinese and English message files

## Key Functionality
- Installation with automatic .env file generation and credential setup
- Support for both standard Docker and Docker Desktop (macOS/Windows)
- Cross-platform Docker volume backup using container method for non-Linux systems
- Smart update mechanisms (partial vs. complete updates)
- Backup with filtering of logs/uploads directories and compression with zstd if available
- Automatic firewall configuration when ufw is present

## Command-Line Interface
The toolkit supports various operations:
- Install: `nekro-agent-toolkit -i [PATH]`
- Update: `nekro-agent-toolkit -u [PATH]`
- Upgrade: `nekro-agent-toolkit -ua [PATH]`
- Backup: `nekro-agent-toolkit -b [DATA_DIR] [BACKUP_DIR]`
- Recovery: `nekro-agent-toolkit -r [BACKUP_FILE] [DATA_DIR]`
- Recover and Install: `nekro-agent-toolkit -ri [BACKUP_FILE] [INSTALL_DIR]`
- Set default data directory: `nekro-agent-toolkit -sd [PATH]`

## Build Process
- `build.sh` - creates a single executable using PyInstaller
- `build_to_wheel.sh` - builds and uploads Python wheels to PyPI
- `setup.py` and `pyproject.toml` for package configuration

## Design Principles
- Uses only Python standard libraries (no external dependencies)
- Cross-platform compatibility with special handling for Docker volumes on different OS
- Comprehensive error handling and user confirmation prompts
- Automatic credential generation for security
- Smart backup filtering to exclude unnecessary files/directories

This toolkit is designed to make the deployment and management of Nekro Agent services straightforward for users with varying technical backgrounds.