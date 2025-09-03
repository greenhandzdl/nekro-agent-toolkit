#!/bin/bash
# You should enter the virtual environment before running this script
python3 -m pip install --upgrade build
python3 -m build

# Force reinstall the package
pip install --force-reinstall dist/

# You need twine to build a wheel
python3 -m pip install --upgrade twine

# For Testing
twine upload --repository testpypi dist/*

# For Production
twine upload dist/*