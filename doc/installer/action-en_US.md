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
5. Click **Run workflow** to start execution

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| with_napcat | boolean | true | Whether to include NapCat service |

## Download Files

After workflow execution, a ZIP package containing the installer files will be generated:

1. Find the **Artifacts** section on the workflow run page
2. Download the **installer-files** file
3. After extraction, you will get:
   - `.env` - Environment configuration file (contains randomly generated secrets)
   - `docker-compose.yml` - Docker Compose configuration file

## Related Links

- [中文文档](./action-zh_CN.md)
- [Installation Module Documentation](../README)
- [Development Documentation](../DEVELOP-EN.md)