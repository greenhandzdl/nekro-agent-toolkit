# Developer Guide

This document outlines the project's internal structure and module relationships to aid in future development.

## Project Structure

The project is organized into the following main directories:

- `module/`: Contains the main entry point scripts (`install.py`, `update.py`).
- `utils/`: Contains helper functions.
  - `helpers.py`: Low-level, shared utility functions (e.g., system commands, file operations).
  - `install_utils.py`: High-level functions specific to the installation process.
  - `update_utils.py`: High-level functions specific to the update process.
- `conf/`: Contains static configuration files.
  - `settings.py`: Shared settings like remote repository URLs.

## Module Relationship Diagram

The following diagram illustrates how the different modules import and depend on each other.

```mermaid
graph TD
    subgraph "Entry Points"
        A["module/install.py"];
        B["module/update.py"];
    end

    subgraph "Business Logic"
        C["utils/install_utils.py"];
        D["utils/update_utils.py"];
    end

    subgraph "Shared Libraries"
        E["utils/helpers.py"];
        F["conf/settings.py"];
    end

    A -- calls --> C;
    A -- calls --> E;
    B -- calls --> D;
    B -- calls --> E;

    C -- imports --> E;
    D -- imports --> E;

    E -- imports --> F;
```
