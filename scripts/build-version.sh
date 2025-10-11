#!/bin/bash

# build-version.sh - 版本更新脚本
# 用于更新 pyproject.toml 和 Nix 包定义文件中的版本信息

set -e

# ============================================================================
# 颜色定义
# ============================================================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ============================================================================
# 初始化
# ============================================================================
# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 自动查找项目根目录（包含 pyproject.toml 的目录）
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
    print_error "未找到 pyproject.toml，无法确定项目根目录。"
    exit 1
fi
cd "$PROJECT_ROOT"

# 文件路径配置（基于项目根目录）
PYPROJECT_FILE="pyproject.toml"
INSTALL_FILE="module/install.py"
NIX_FILE="release/nix/nekro-agent-toolkit.nix"
SETUP_FILE="setup.py"

# ============================================================================
# 辅助函数
# ============================================================================
# 函数：打印带颜色的消息
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 函数：显示使用方法
show_usage() {
    echo "用法: $0 <new_version>"
    echo ""
    echo "示例:"
    echo "  $0 1.0.4          # 更新版本到 1.0.4"
    echo "  $0 2.0.0-beta1    # 更新版本到 2.0.0-beta1"
    echo ""
    echo "此脚本会更新以下文件中的版本信息:"
    echo "  - pyproject.toml"
    echo "  - setup.py"
    echo "  - release/nix/nekro-agent-toolkit.nix"
}

# 函数：验证版本格式
validate_version() {
    local version="$1"
    # 简单的版本格式验证 (支持 x.y.z, x.y.z-suffix 格式)
    if [[ ! $version =~ ^[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9]+)?$ ]]; then
        print_error "无效的版本格式: $version"
        print_error "版本格式应为: x.y.z 或 x.y.z-suffix (如: 1.0.4, 2.0.0-beta1)"
        return 1
    fi
    return 0
}

# ============================================================================
# 版本信息处理函数
# ============================================================================
# 函数：获取当前版本
get_current_version() {
    if [[ -f "$PYPROJECT_FILE" ]]; then
        grep '^version = ' "$PYPROJECT_FILE" | sed 's/version = "\(.*\)"/\1/'
    else
        echo "unknown"
    fi
}

# ============================================================================
# 文件更新函数
# ============================================================================
# 函数：更新 pyproject.toml
update_pyproject() {
    local new_version="$1"
    
    if [[ ! -f "$PYPROJECT_FILE" ]]; then
        print_error "文件不存在: $PYPROJECT_FILE"
        return 1
    fi
    
    # 备份原文件
    cp "$PYPROJECT_FILE" "$PYPROJECT_FILE.bak"
    
    # 更新版本
    sed -i.tmp "s/^version = \".*\"/version = \"$new_version\"/" "$PYPROJECT_FILE"
    rm "$PYPROJECT_FILE.tmp"
    
    print_info "已更新 $PYPROJECT_FILE 中的版本"
}

# 函数：检查 install.py（预留功能，当前无版本信息需要更新）
update_install() {
    local new_version="$1"
    
    if [[ ! -f "$INSTALL_FILE" ]]; then
        print_warn "文件不存在: $INSTALL_FILE，跳过"
        return 0
    fi
    
    # 目前 install.py 中没有硬编码的版本信息
    # 此函数保留以备将来可能需要更新版本相关内容
    print_info "已检查 $INSTALL_FILE（当前无版本信息需要更新）"
}

# 函数：更新 Nix 包定义文件中的版本号
update_nix_version() {
    local new_version="$1"
    if [[ ! -f "$NIX_FILE" ]]; then
        print_warn "文件不存在: $NIX_FILE，跳过 Nix 包版本更新"
        return 0
    fi
    cp "$NIX_FILE" "$NIX_FILE.bak"
    sed -i.tmp "s/^  version = \".*\";/  version = \"$new_version\";/" "$NIX_FILE"
    rm "$NIX_FILE.tmp"
    print_info "已更新 $NIX_FILE 中的版本"
}

# 函数：更新 setup.py
update_setup_py() {
    local new_version="$1"
    if [[ ! -f "$SETUP_FILE" ]]; then
        print_error "文件不存在: $SETUP_FILE"
        return 1
    fi
    cp "$SETUP_FILE" "$SETUP_FILE.bak"
    # 支持 version="x.y.z" 或 version='x.y.z'
    sed -i.tmp -E "s/(version\s*=\s*[\"\'])[0-9]+\.[0-9]+\.[0-9]+(-[a-zA-Z0-9]+)?([\"\'])/\1${new_version}\3/" "$SETUP_FILE"
    rm "$SETUP_FILE.tmp"
    print_info "已更新 $SETUP_FILE 中的版本"
}

# ============================================================================
# 验证函数
# ============================================================================
# 函数：验证文件存在
check_files() {
    local missing_files=()
    if [[ ! -f "$PYPROJECT_FILE" ]]; then
        missing_files+=("$PYPROJECT_FILE")
    fi
    if [[ ! -f "$SETUP_FILE" ]]; then
        missing_files+=("$SETUP_FILE")
    fi
    if [[ ${#missing_files[@]} -gt 0 ]]; then
        print_error "以下必需文件不存在:"
        for file in "${missing_files[@]}"; do
            echo "  - $file"
        done
        return 1
    fi
    return 0
}

# ============================================================================
# 主函数
# ============================================================================
# 主函数：执行版本更新流程
main() {
    # 1. 参数验证
    if [[ $# -ne 1 ]]; then
        show_usage
        exit 1
    fi
    
    local new_version="$1"
    
    # 2. 版本格式验证
    if ! validate_version "$new_version"; then
        exit 1
    fi
    
    # 3. 文件存在性检查
    if ! check_files; then
        exit 1
    fi
    
    # 4. 显示版本信息
    local current_version
    current_version=$(get_current_version)
    
    print_info "当前版本: $current_version"
    print_info "目标版本: $new_version"
    
    # 5. 用户确认
    echo ""
    read -p "确认更新版本吗? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "取消操作"
        exit 0
    fi
    
    # 6. 执行版本更新
    print_info "开始更新版本..."
    # 更新 pyproject.toml
    update_pyproject "$new_version"
    # 更新 setup.py
    update_setup_py "$new_version"
    # 检查 install.py（如有必要）
    update_install "$new_version"
    # 更新 Nix 包定义文件
    update_nix_version "$new_version"

    # 7. 完成提示
    print_info "版本更新完成!"
    print_info "已创建备份文件: $PYPROJECT_FILE.bak, $SETUP_FILE.bak"

    # 显示更新后的版本信息
    local updated_version
    updated_version=$(get_current_version)
    print_info "更新后版本: $updated_version"
}

# ============================================================================
# 脚本入口
# ============================================================================
# 执行主函数
main "$@"
