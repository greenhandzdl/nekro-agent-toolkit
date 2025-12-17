# Nekro Agent Toolkit

<p align="center">
	<img src="https://cdn.jsdelivr.net/gh/greenhandzdl/nekro-agent-toolkit@main/icons/nekro-agent-toolkit-icons.png" alt="Nekro Agent Toolkit mascot">
</p>

Nekro Agent Toolkit is an all-in-one tool for deploying, backing up and restoring Nekro Agent and related services, with automation support for Docker environments.

## 🌐 Other languages

| [Read in English](https://cdn.jsdelivr.net/gh/greenhandzdl/nekro-agent-toolkit@main/doc/README/README-EN.md) | [اقرأ باللغة العربية](https://cdn.jsdelivr.net/gh/greenhandzdl/nekro-agent-toolkit@main/doc/README/README-AR.md) | [Lire en français](https://cdn.jsdelivr.net/gh/greenhandzdl/nekro-agent-toolkit@main/doc/README/README-FR.md) | [Читать на русском](https://cdn.jsdelivr.net/gh/greenhandzdl/nekro-agent-toolkit@main/doc/README/README-RU.md) | [Leer en español](https://cdn.jsdelivr.net/gh/greenhandzdl/nekro-agent-toolkit@main/doc/README/README-ES.md) | [日本語で読む](https://cdn.jsdelivr.net/gh/greenhandzdl/nekro-agent-toolkit@main/doc/README/README-JP.md) |

## ✨ Key features

- One-click install, upgrade, backup and restore for Nekro Agent
- Smart detection and multi-language support
- Automatic backup/restore support for Docker volumes

## 🚀 Quick start

### Install

```bash
pip install nekro-agent-toolkit
# Or run from source
git clone https://github.com/greenhandzdl/nekro-agent-toolkit.git
cd nekro-agent-toolkit
```

### Common commands

```bash
# install/upgrade/backup/restore
nekro-agent-toolkit -i [PATH]
nekro-agent-toolkit -u [PATH]
nekro-agent-toolkit -b [DATA_DIR] BACKUP_DIR
nekro-agent-toolkit -r BACKUP_FILE [DATA_DIR]
```

### Manage dependencies with `uv` (recommended)

This project now supports using `uv` to manage dependencies and produce a reproducible `uv.lock` file.

## Additional information

- Requirements: Python 3.6+, Docker, Docker Compose
- License: see [LICENSE](https://cdn.jsdelivr.net/gh/greenhandzdl/nekro-agent-toolkit@main/LICENSE)
