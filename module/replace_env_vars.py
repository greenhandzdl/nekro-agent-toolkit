#!/usr/bin/env python3
"""
读取.env文件并替换docker-compose.yml中的环境变量
"""

import re
from pathlib import Path


def load_env_file(env_path):
    """加载.env文件并返回环境变量字典"""
    env_vars = {}
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # 跳过注释和空行
            if not line or line.startswith('#'):
                continue
            
            # 解析键值对
            if '=' in line:
                key, value = line.split('=', 1)
                env_vars[key.strip()] = value.strip()
    
    return env_vars


def resolve_env_variables(env_vars):
    """解析环境变量中的嵌套引用"""
    resolved_vars = env_vars.copy()
    
    # 多次迭代以处理嵌套引用
    for _ in range(10):  # 最多迭代10次以防止无限循环
        changed = False
        for key, value in resolved_vars.items():
            # 查找 ${VAR_NAME} 模式
            pattern = r'\$\{([^}]+)\}'
            matches = re.findall(pattern, value)
            
            for var_name in matches:
                if var_name in resolved_vars:
                    old_value = value
                    value = value.replace(f'${{{var_name}}}', resolved_vars[var_name])
                    resolved_vars[key] = value
                    if old_value != value:
                        changed = True
                elif ':-' in var_name:
                    # 处理 ${VAR_NAME:-default} 模式
                    var_parts = var_name.split(':-')
                    var_name_clean = var_parts[0]
                    default_value = var_parts[1] if len(var_parts) > 1 else ''
                    
                    if var_name_clean in resolved_vars and resolved_vars[var_name_clean]:
                        old_value = value
                        value = value.replace(f'${{{var_name}}}', resolved_vars[var_name_clean])
                        resolved_vars[key] = value
                        if old_value != value:
                            changed = True
                    else:
                        old_value = value
                        value = value.replace(f'${{{var_name}}}', default_value)
                        resolved_vars[key] = value
                        if old_value != value:
                            changed = True
        
        if not changed:
            break
    
    return resolved_vars


def replace_variables_in_compose(compose_path, env_vars):
    """在docker-compose.yml中替换环境变量"""
    with open(compose_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换 ${VAR_NAME} 和 ${VAR_NAME:-default} 模式
    def replace_var(match):
        var_expression = match.group(1)
        var_name = var_expression
        default_value = ""

        # 处理 ${VAR_NAME:-default} 模式
        if ':-' in var_expression:
            var_parts = var_expression.split(':-')
            var_name = var_parts[0]
            default_value = var_parts[1] if len(var_parts) > 1 else ""

        # 替换变量
        if var_name in env_vars and env_vars[var_name]:
            return env_vars[var_name]
        else:
            return default_value

    # 使用正则表达式替换所有变量
    pattern = r'\$\{([^}]+)\}'
    resolved_content = re.sub(pattern, replace_var, content)

    return resolved_content


def main():
    # 获取当前目录
    current_dir = Path(__file__).parent

    # 定义文件路径
    env_path = current_dir / '.env'
    compose_path = current_dir / 'docker-compose.yml'
    output_path = current_dir / 'docker-compose-resolved.yml'

    # 检查文件是否存在
    if not env_path.exists():
        print(f"错误: 找不到 .env 文件: {env_path}")
        return

    if not compose_path.exists():
        print(f"错误: 找不到 docker-compose.yml 文件: {compose_path}")
        return

    # 加载环境变量
    print("正在加载 .env 文件...")
    env_vars = load_env_file(env_path)

    # 解析嵌套的环境变量
    print("正在解析环境变量...")
    resolved_env_vars = resolve_env_variables(env_vars)

    # 显示解析后的环境变量
    print("\n解析后的环境变量:")
    for key, value in resolved_env_vars.items():
        print(f"  {key}={value}")

    # 替换docker-compose.yml中的变量
    print("\n正在替换 docker-compose.yml 中的变量...")
    resolved_content = replace_variables_in_compose(compose_path, resolved_env_vars)

    # 写入新文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(resolved_content)

    print(f"\n已生成文件: {output_path}")
    print("现在可以使用以下命令运行 docker-compose:")
    print("  docker-compose -f docker-compose-resolved.yml up -d")


if __name__ == '__main__':
    main()