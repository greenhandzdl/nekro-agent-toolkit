[Read in Chinese](../README.md)

# Nekro Agent Toolkit

Nekro Agent Toolkit is an all-in-one tool for deploying, backing up, and restoring Nekro Agent and related services. It supports automated Docker management and provides a dependency management script for quickly adding dependencies.

## ✨ Main Features

- One-click install, upgrade, backup, and restore for Nekro Agent
- Smart detection and multi-language support
- Automated Docker volume backup and restore
- Dependency management script: easily add dependencies to requirements.txt and pyproject.toml

## 🚀 Quick Start

### Installation

```bash
pip install nekro-agent-toolkit
# Or run from source
git clone https://github.com/your-repo/nekro-agent-toolkit.git
cd nekro-agent-toolkit
```

### Common Commands

```bash
# Install/Upgrade/Backup/Restore
nekro-agent-toolkit -i [PATH]
nekro-agent-toolkit -u [PATH]
nekro-agent-toolkit -b [DATA_DIR] BACKUP_DIR
nekro-agent-toolkit -r BACKUP_FILE [DATA_DIR]

# Add dependency to requirements.txt and pyproject.toml
./scripts/add-dependency.sh <package_name>
```

## Additional Info

- Requirements: Python 3.6+, Docker, Docker Compose
- License: See [LICENSE](../LICENSE)
