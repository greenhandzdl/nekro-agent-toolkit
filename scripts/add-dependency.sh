#!/bin/bash
# add-dependency.sh - 向 requirements.txt 和 pyproject.toml 添加依赖
# 用法: ./scripts/add-dependency.sh <package_name>

set -e

if [[ $# -ne 1 ]]; then
    echo "用法: $0 <package_name>"
    exit 1
fi

PKG_NAME="$1"

# 自动查找项目根目录（含 pyproject.toml）
find_project_root() {
    local dir="$PWD"
    while [[ "$dir" != "/" ]]; do
        if [[ -f "$dir/pyproject.toml" ]]; then
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    return 1
}

PROJECT_ROOT="$(find_project_root)"
if [[ -z "$PROJECT_ROOT" ]]; then
    echo "未找到 pyproject.toml，无法确定项目根目录。"
    exit 1
fi
cd "$PROJECT_ROOT"

REQ_FILE="requirements.txt"
PYPROJECT_FILE="pyproject.toml"

# 添加到 requirements.txt
if [[ ! -f "$REQ_FILE" ]]; then
    echo "$PKG_NAME" > "$REQ_FILE"
    echo "已创建 $REQ_FILE 并添加 $PKG_NAME"
else
    if grep -q -E "^$PKG_NAME([=<>!~]|$)" "$REQ_FILE"; then
        echo "$REQ_FILE 已包含 $PKG_NAME"
    else
        echo "$PKG_NAME" >> "$REQ_FILE"
        echo "已将 $PKG_NAME 添加到 $REQ_FILE"
    fi
fi

# 添加到 pyproject.toml [tool.poetry.dependencies]
if grep -q "\[tool.poetry.dependencies\]" "$PYPROJECT_FILE"; then
    if awk '/\[tool.poetry.dependencies\]/{flag=1;next}/\[.*\]/{flag=0}flag' "$PYPROJECT_FILE" | grep -q "^$PKG_NAME"; then
        echo "pyproject.toml 的 dependencies 已包含 $PKG_NAME"
    else
        awk -v pkg="$PKG_NAME" '/\[tool.poetry.dependencies\]/{print;flag=1;next}/\[.*\]/{flag=0}flag{last=NR}1;END{if(flag) print pkg " = \"*\""}' "$PYPROJECT_FILE" > "$PYPROJECT_FILE.tmp" && mv "$PYPROJECT_FILE.tmp" "$PYPROJECT_FILE"
        echo "已将 $PKG_NAME = \"*\" 添加到 pyproject.toml 的 dependencies 区块"
    fi
else
    echo "[tool.poetry.dependencies]" >> "$PYPROJECT_FILE"
    echo "$PKG_NAME = \"*\"" >> "$PYPROJECT_FILE"
    echo "已创建 dependencies 区块并添加 $PKG_NAME 到 pyproject.toml"
fi

