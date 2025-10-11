#!/usr/bin/env bash
set -euo pipefail

# Export requirements.txt from Poetry-managed pyproject.toml
# Usage: ./scripts/export_requirements.sh

TMP_VENV=".venv-poetry"

echo "Creating temporary venv: ${TMP_VENV}"
python3 -m venv "${TMP_VENV}"
# shellcheck source=/dev/null
. "${TMP_VENV}/bin/activate"

python -m pip install --upgrade pip
python -m pip install poetry
python -m pip install poetry-plugin-export

# Ensure pyproject.toml has [tool.poetry] section; export requirements
poetry export -f requirements.txt --without-hashes -o requirements.txt

# Clean up
deactivate
rm -rf "${TMP_VENV}"

echo "requirements.txt generated from pyproject.toml (tool.poetry)."
