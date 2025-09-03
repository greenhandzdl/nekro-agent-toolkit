[以中文阅读](./develop.md)

# Developer Guide

This document outlines the project's internal structure and module relationships to aid in future development.

## Project Structure

The project is organized into the following main directories:

- `app.py`: The unified command-line entry point for the project, responsible for dispatching installation, update, and backup/recovery tasks.
- `module/`: Modules that encapsulate core features and can be called externally.
  - `install.py`: Provides the `install_agent` function.
  - `update.py`: Provides the `update_agent` function.
  - `backup.py`: Provides `backup_agent`, `recover_agent`, and `recover_and_install_agent` functions.
- `utils/`: Contains helper functions.
  - `helpers.py`: Low-level, shared utility functions (e.g., system commands, file operations).
  - `install_utils.py`: High-level functions for the installation process.
  - `update_utils.py`: High-level functions for the update process.
  - `backup_utils.py`: Low-level functions for backup/recovery (e.g., archiving, extraction, analysis).
- `conf/`: Contains static configuration files.
  - `settings.py`: Shared settings, such as remote repository URLs.

## Module Relationship Diagram

The following diagram illustrates how the different modules import and depend on each other.

```mermaid
graph TD
    subgraph "Main Entry Point"
        APP["app.py"];
    end

    subgraph "High-level API Modules"
        INSTALL["module/install.py"];
        UPDATE["module/update.py"];
        BACKUP["module/backup.py"];
    end

    subgraph "Business Logic"
        INSTALL_UTILS["utils/install_utils.py"];
        UPDATE_UTILS["utils/update_utils.py"];
        BACKUP_UTILS["utils/backup_utils.py"];
    end

    subgraph "Shared Libraries"
        HELPERS["utils/helpers.py"];
        CONF["conf/settings.py"];
    end

    APP -- calls --> INSTALL;
    APP -- calls --> UPDATE;
    APP -- calls --> BACKUP;

    INSTALL -- calls --> INSTALL_UTILS;
    UPDATE -- calls --> UPDATE_UTILS;
    BACKUP -- calls --> BACKUP_UTILS;
    BACKUP -- calls --> INSTALL;
    
    INSTALL_UTILS -- imports --> HELPERS;
    UPDATE_UTILS -- imports --> HELPERS;
    BACKUP_UTILS -- imports --> HELPERS;

    HELPERS -- imports --> CONF;
```
