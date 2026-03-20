# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Nekro Agent Toolkit is a unified management tool for installing, updating, and backing up Nekro Agent and related services in Docker environments. It provides one-click deployment, intelligent system detection, multi-language support (7 languages), and automated Docker volume backup and restore.

## Common Commands

### Development
```bash
# Install dependencies with uv (recommended)
uv sync

# Or with pip
pip install -r requirements.txt

# Run the CLI tool directly
python app.py -i [PATH]          # Install
python app.py -u [PATH]          # Update
python app.py -b [DATA_DIR] [BACKUP_DIR]   # Backup
python app.py -r [BACKUP_FILE] [DATA_DIR]  # Restore
```

### Building Executables
```bash
# Build standalone executable with PyInstaller
bash scripts/build.sh

# Build wheel package
bash scripts/build_to_wheel.sh
```

### Internationalization
```bash
# Sort translation messages
python scripts/sort_messages.py
```

## Architecture

### Core Modules (`module/`)
- `install.py` - Installation logic: directory setup, env config, compose file download, image pull, service start
- `update.py` - Update logic: handles both Nekro Agent only and all services update modes
- `backup.py` - Backup/restore logic: creates tar/tar.zstd archives, Docker volume backup via containers

### Utilities (`utils/`)
- `helpers.py` - Core utilities: dependency checks, Docker compose detection, env file operations, sudo handling
- `docker_helpers.py` - Docker image pulling with automatic mirror fallback for Chinese users
- `backup_utils.py` - Archive creation/extraction, Docker volume backup
- `i18n.py` - Language detection and message loading

### Configuration (`conf/`)
- `install_settings.py` - Installation URLs and config (BASE_URLS for compose files)
- `backup_settings.py` - Docker volumes and helper images
- `docker_mirrors.py` - Docker registry mirrors
- `i18n_settings.py` - Supported languages (zh_CN, en_US, es_ES, fr_FR, ja_JP, ru_RU, ar_SA)

### Language Packs (`data/`)
Each language has a `messages.py` file with translation keys. The system auto-detects locale and falls back to zh_CN.

### Remote File Downloads
The project downloads `docker-compose.yml`, `docker-compose-x-napcat.yml`, and `.env.example` from BASE_URLS defined in `conf/install_settings.py`. The URLs are tried in order until one succeeds.

## GitHub Actions

- `.github/workflows/generate-installer.yml` - Generates installer files (.env and docker-compose.yml) via workflow_dispatch, commits to `installer/` directory
- `.github/workflows/pypi-release.yml` - Publishes to PyPI on release
- `.github/workflows/docker-build.yml` - Builds Docker images