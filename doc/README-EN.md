[以中文阅读](../README.md)

# Nekro Agent Toolkit

A professional toolkit for rapid deployment of Nekro Agent and related services, simplifying Docker-based QQ bot deployment.

## ✨ Features

- **Unified Management**: Single script for all operations with smart environment detection
- **Multi-language**: Auto-switching Chinese/English interface
- **Default Directory**: Simplified commands with auto-fill preset directories
- **Smart Backup**: Cross-platform Docker volume backup with dynamic discovery
- **Version Display**: Git SHA for source, version number for pip installs

## 🚀 Installation & Usage

### Installation

```bash
# pip install (recommended)
pip install nekro-agent-toolkit

# Source code
git clone https://github.com/your-repo/nekro-agent-toolkit.git
cd nekro-agent-toolkit
```

### Default Directory Management

```bash
# Set default directory
nekro-agent-toolkit -sd ./na_data

# View current setting (enter 'clear' to clear)
nekro-agent-toolkit -sd
```

### Common Commands

```bash
# Install (can auto-use default directory)
nekro-agent-toolkit -i [PATH]

# Update/Upgrade (can auto-use default directory)
nekro-agent-toolkit -u [PATH]    # Partial update
nekro-agent-toolkit -ua [PATH]   # Full upgrade

# Backup & Recovery (can auto-use default directory)
nekro-agent-toolkit -b [DATA_DIR] BACKUP_DIR
nekro-agent-toolkit -r BACKUP_FILE [DATA_DIR]
nekro-agent-toolkit -ri BACKUP_FILE [INSTALL_DIR]

# Options
--with-napcat    # Deploy NapCat service
--dry-run        # Preview mode
-y               # Auto confirm
```

## 📝 Additional Info

**Requirements**: Python 3.6+, Docker, Docker Compose

**Optional**: zstd (fast compression), ufw (firewall)

**Contributing**: See [`doc/REGULATE-EN.md`](./REGULATE-EN.md)

**License**: See [Nekro Agent Project](https://github.com/KroMiose/nekro-agent) and [LICENSE](../LICENSE)
