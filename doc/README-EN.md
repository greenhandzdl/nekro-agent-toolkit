[以中文阅读](../README.md)

# Nekro Agent Installer

Nekro Agent is a Docker-based application that can be used with QQ bots. This installer helps you quickly deploy Nekro Agent and its related services.

## Features

- A unified `app.py` script entry point for installation, updates, and backups
- Smart runtime environment detection with dynamic command display
- Automatically checks for system dependencies (Docker and Docker Compose)
- Automatically downloads and configures the necessary configuration files
- Supports one-click deployment of the main Nekro Agent service
- Optional integration with the NapCat QQ bot service
- Automatically generates security keys and access tokens
- Automatically configures firewall rules (if ufw is used)
- Cross-platform Docker volume backup and recovery (Linux/macOS/Windows)
- Automatic Docker volume creation in new environments
- Version information display (Git SHA for source, package version for pip installs)

## System Requirements

- Linux or Unix-like operating system.
- Docker installed.
- Docker Compose installed.
- `zstd` compression tool (recommended for smaller backups).
- Administrator privileges (sudo).

## Installation Methods

### Method 1: Install with pip (Recommended)

```bash
pip install nekro-agent-toolkit
```

After installation, you can directly use the `nekro-agent-toolkit` command:

```bash
# Create a folder named na_data in the current directory and install the service
nekro-agent-toolkit --install ./na_data
```

### Method 2: Run from source code

```bash
git clone https://github.com/greenhandzdl/nekro-agent-toolkit.git
cd nekro-agent-toolkit
python3 app.py --install ./na_data
```

### Basic Commands

#### Check Version

```bash
# Shows Git SHA when running from source
python3 app.py --version
# Example output: nekro-agent-toolkit (源码) a1b2c3d4

# Shows version number when installed via pip
nekro-agent-toolkit --version
# Example output: nekro-agent-toolkit 1.0.3
```

#### Help Information

```bash
# Smart display of correct command format
python3 app.py --help          # When running from source
nekro-agent-toolkit --help     # When installed via pip
```

### Installation Options

- **Enable NapCat Service**: Append the `--with-napcat` flag.
- **Dry Run Mode**: Append the `--dry-run` flag to only generate configuration files or print the plan without performing any actual operations.
- **Automatic Confirmation**: Append the `-y` or `--yes` flag, and the script will not ask for interactive confirmation.

### Updating

- **Partial Update (Recommended)**: Use the `-u` or `--update` parameter to update only the Nekro Agent core service.
  ```bash
  nekro-agent-toolkit --update ./na_data
  # Or run from source code:
  python3 app.py --update ./na_data
  ```

- **Full Update (Upgrade)**: Use the `-ua` or `--upgrade` parameter to update all Docker images (including the database, etc.).
  ```bash
  nekro-agent-toolkit --upgrade ./na_data
  # Or run from source code:
  python3 app.py --upgrade ./na_data
  ```

### Backup and Recovery

Cross-platform backup and recovery with intelligent strategy selection.

#### Smart Backup Strategy

- **Linux**: Direct filesystem access to Docker volumes
- **macOS/Windows**: Container-based backup via Docker
- **Auto-detection**: Automatically selects optimal strategy

#### Commands

- **Backup**: Use `-b` or `--backup` parameter
  ```bash
  nekro-agent-toolkit --backup ./na_data ./backups
  ```
  > Creates timestamped files like `na_backup_1678886400.tar.zstd`
  > Includes data directory and Docker volumes (nekro_postgres_data, nekro_qdrant_data)

- **Recovery**: Use `-r` or `--recovery` parameter
  ```bash
  nekro-agent-toolkit --recovery ./backups/na_backup_1678886400.tar.zstd ./na_data_new
  ```
  > **New Environment Support**: Automatically creates missing Docker volumes

- **Recover and Install**: Use `-ri` or `--recover-install` parameter
  ```bash
  nekro-agent-toolkit --recover-install ./backups/na_backup_1678886400.tar.zstd ./na_data_new
  ```

#### Advanced Features

- **Cross-platform compatibility**: Same backup works across different OS
- **Automatic volume management**: Creates missing Docker volumes in new environments
- **Smart error handling**: Distinguishes normal tar warnings from real errors
- **Compression optimization**: Prefers zstd, falls back to standard tar

## Advanced Installation Process Description

1. **Dependency Check**: The script automatically checks if Docker and Docker Compose are installed on the system.
2. **Directory Setup**: Creates the application data directory at your specified path.
3. **Configuration File Generation**:
    - If a `.env` file already exists in your specified directory, the script will use it directly.
    - Otherwise, the script will download the latest `.env.example` from the remote repository as a template and automatically fill in the necessary random keys.
4. **Service Deployment**: Downloads and starts the Docker containers.
5. **Firewall Configuration**: If the system uses ufw, it automatically configures the firewall rules.

## Access Information

After installation is complete, you can access the services in the following ways:

- Web Admin Interface: `http://127.0.0.1:8021`
- OneBot WebSocket Address: `ws://127.0.0.1:8021/onebot/v11/ws`

If the NapCat service is enabled, it will also provide:
- NapCat Service Port: Defaults to `6099`

## Important Notes

1. If you are using a cloud server, please allow the corresponding ports in the security group of your cloud provider's console.
2. If you need to access from outside, replace `127.0.0.1` in the addresses above with your server's public IP.
3. If the NapCat service is enabled, use `sudo docker logs [container_name]napcat` to view the robot's QQ login QR code.

## Troubleshooting

If you encounter problems during installation, please check:

1. Ensure that Docker and Docker Compose are correctly installed on your system.
2. Ensure that the current user has sudo privileges.
3. Check if the network connection is normal (the installation process needs to download configuration files from GitHub).
4. Check if firewall settings are blocking the necessary ports.

## License

Please refer to the [Nekro Agent Project](https://github.com/KroMiose/nekro-agent) and [this project](../LICENSE) for license information.
