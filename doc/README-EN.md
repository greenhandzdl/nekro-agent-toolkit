[以中文阅读](../README.md)

# Nekro Agent Installer

Nekro Agent is a Docker-based application that can be used with QQ bots. This installer helps you quickly deploy Nekro Agent and its related services.

## Features

- A unified `app.py` script entry point for installation, updates, and backups.
- Automatically checks for system dependencies (Docker and Docker Compose).
- Automatically downloads and configures the necessary configuration files.
- Supports one-click deployment of the main Nekro Agent service.
- Optional integration with the NapCat QQ bot service.
- Automatically generates security keys and access tokens.
- Automatically configures firewall rules (if ufw is used).
- Built-in backup and recovery tools.

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

- **Backup**: Use the `-b` or `--backup` parameter. You need to provide the source data directory and the directory where the backup file will be stored.
  ```bash
  # Back up the ./na_data directory to the ./backups folder
  nekro-agent-toolkit --backup ./na_data ./backups
  # Or run from source code:
  python3 app.py --backup ./na_data ./backups
  ```
  > The script automatically generates a timestamped backup file, such as `na_backup_1678886400.tar.zstd`.

- **Recovery**: Use the `-r` or `--recovery` parameter. You need to provide the backup file and the target directory to restore to.
  ```bash
  nekro-agent-toolkit --recovery ./backups/na_backup_1678886400.tar.zstd ./na_data_new
  # Or run from source code:
  python3 app.py --recovery ./backups/na_backup_1678886400.tar.zstd ./na_data_new
  ```
  > **Note**: The recovery operation will overwrite files in the target directory. If the directory is not empty, the program will ask for confirmation.

- **Recover and Install**: Use the `-ri` or `--recover-install` parameter. This command first performs a recovery and then continues with the installation process on the recovered data (e.g., downloading `docker-compose.yml`, pulling images, etc.).
  ```bash
  nekro-agent-toolkit --recover-install ./backups/na_backup_1678886400.tar.zstd ./na_data_new
  # Or run from source code:
  python3 app.py --recover-install ./backups/na_backup_1678886400.tar.zstd ./na_data_new
  ```

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
