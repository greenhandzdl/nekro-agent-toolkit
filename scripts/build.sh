#!/bin/bash

# ==============================================================================
# Nekro Agent Installer - Build Script
# ==============================================================================
#
# This script packages the application into a single executable using PyInstaller.
# It creates a local Python virtual environment to avoid conflicts with system
# packages, which is the recommended way to handle PEP 668.
#
# All script output will be logged to ./build_log.txt for easy review and cleanup.
#
# Usage:
#   bash build.sh
#
# ==============================================================================

set -e # Exit immediately if a command exits with a non-zero status.

# --- Log Setup ---
LOG_FILE="./build_log.txt"
# Ensure the log file is clean for a new run
> "$LOG_FILE"
echo "Script output is being logged to: $LOG_FILE"
# Redirect all subsequent stdout and stderr to tee, which writes to console and log file
exec > >(tee -a "$LOG_FILE") 2>&1


# --- 1. Set up Virtual Environment ---
VENV_DIR=".venv"
echo "---> Setting up Python virtual environment in '$VENV_DIR'..."
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi

# Activate the virtual environment
# This works for bash/zsh. For other shells, this might need adjustment.
source "$VENV_DIR/bin/activate"

echo "---> Virtual environment activated."


# --- 2. Install Dependencies ---
echo "---> Installing/Updating PyInstaller in virtual environment from official PyPI..."

pip install --upgrade pyinstaller --index-url https://pypi.org/simple/


# --- 3. Determine OS and Output Name ---
OS_NAME=$(uname -s)
case "$OS_NAME" in
    Linux*) 
        TARGET_OS="Linux"
        OUTPUT_NAME="na_installer_linux"
        ;;
    Darwin*) 
        TARGET_OS="macOS"
        OUTPUT_NAME="na_installer_darwin"
        ;;
    CYGWIN*|MINGW*|MSYS*) 
        TARGET_OS="Windows"
        OUTPUT_NAME="na_installer"
        ;;
    *)
        echo "Error: Unsupported operating system '$OS_NAME'" >&2
        # Deactivate before exiting on error
        deactivate
        exit 1
        ;;
esac

echo "---> Detected Target OS: $TARGET_OS"


# --- 4. Clean previous builds and Run PyInstaller ---
echo "---> Cleaning up previous build artifacts..."
rm -rf build/ dist/
rm -f build # In case 'build' is a file from previous log redirection

echo "---> Starting PyInstaller build process..."

pyinstaller \
    --name "$OUTPUT_NAME" \
    --onefile \
    --clean \
    --add-data "module:module" \
    --add-data "utils:utils" \
    --add-data "conf:conf" \
    app.py


# --- 5. Final Message & Cleanup ---
echo "
---> Build complete!"
echo "The executable can be found in the 'dist/' directory:"

ls -l dist/

# Deactivate the virtual environment
deactivate
echo "
---> Virtual environment deactivated."