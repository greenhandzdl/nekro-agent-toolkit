# Quick Start

## Requirements
- Docker
- Docker Compose

## Usage

### 1. Start Services
```bash
docker compose --env-file ./.env pull
docker compose --env-file ./.env up -d
```

### 2. Stop Services
```bash
docker compose --env-file ./.env down
```

## .env File Path

If `.env` is not in the current directory, use `--env-file` to specify the full path:

```bash
docker compose --env-file /path/to/.env up -d
```

### Windows Path Conversion
Convert Windows paths to Linux-compatible format:
- `C:\path\to\.env` → `/c/path/to/.env`
- `D:\data\.env` → `/d/data/.env`