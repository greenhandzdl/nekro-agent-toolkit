#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Dependencies are managed by `uv` and listed in `requirements.txt` generated from `uv.lock`.
# Avoid reading requirements here to prevent duplication; use uv to manage dependencies.

setup(
    name="nekro-agent-toolkit",
    version="1.5.5",
    author="greenhandzdl",
    author_email="greenhandzdl@greenhandzdl.moe",
    description="Nekro Agent 安装、更新与备份的统一管理工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/greenhandzdl/nekro-agent-toolkit",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "nekro-agent-toolkit=app:main",
        ],
    },
    package_data={
        "conf": ["*.py"],
    },
    include_package_data=True,
)