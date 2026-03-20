# GitHub Action - Generate Installer Files

This project provides a GitHub Action workflow for automatically generating and updating installation configuration files.

## Overview

The `Generate Installer Files` workflow automatically performs the following tasks:

1. **Generate .env configuration file** - Runs the install module in dry-run mode to create a configuration file with random secrets
2. **Download docker-compose file** - Fetches docker-compose.yml or docker-compose-x-napcat.yml from the remote repository
3. **Auto-commit updates** - Automatically commits the generated files to the `installer/` directory in the repository

## Usage

### Manual Trigger

1. Go to the project's **Actions** page
2. Select the **Generate Installer Files** workflow
3. Click the **Run workflow** button
4. Configure options:
   - **Include NapCat service**: Whether to include NapCat service (enabled by default)
   - **Language**: Commit message language (zh_CN / en_US)
5. Click **Run workflow** to start execution

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| with_napcat | boolean | true | Whether to include NapCat service |
| language | choice | en_US | Commit message language |

## Output Files

After workflow execution, the following files will be generated in the `installer/` directory:

```
installer/
├── .env                 # Environment configuration file (with randomly generated secrets)
└── docker-compose.yml   # Docker Compose configuration file
```

## Related Links

- [中文文档](./action-zh_CN.md)
- [Installation Module Documentation](../README)
- [Development Documentation](../DEVELOP-EN.md)