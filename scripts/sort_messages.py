#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对 data/*/messages.py 中的 MESSAGES 字典按 key 首字母 A-Z 排序，且不保留注释，输出合法 Python 字典格式。
"""
import glob
import os
import re
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATTERN = os.path.join(ROOT, 'data', '*', 'messages.py')

MESSAGES_RE = re.compile(r"^MESSAGES\s*=\s*{", re.MULTILINE)


def extract_messages_dict(lines):
    start, end = None, None
    for i, line in enumerate(lines):
        if MESSAGES_RE.match(line):
            start = i
            break
    if start is None:
        return None, None, None
    brace_count = 0
    for j in range(start, len(lines)):
        brace_count += lines[j].count('{')
        brace_count -= lines[j].count('}')
        if brace_count == 0:
            end = j
            break
    if end is None:
        return None, None, None
    return start, end, lines[start:end+1]


def parse_messages_items(dict_lines):
    """
    解析 MESSAGES 字典内容，返回 (key, value) 列表，支持多行字符串。
    对于重复 key，收集所有 value。
    """
    body = dict_lines[1:-1]
    items = []
    key = None
    value_lines = []
    entry_re = re.compile(r'\s*("[^"]+"|\'[^\"]+\')\s*:\s*(.*?)(,?)\s*$')
    for line in body:
        if not line.strip() or line.strip().startswith('#'):
            continue
        m = entry_re.match(line)
        if m:
            # 保存上一个 key-value
            if key is not None:
                value = '\n'.join(value_lines).rstrip(',')
                items.append((key, value))
            key = m.group(1)
            value = m.group(2)
            # 判断 value 是否以引号结尾（单行字符串）
            if value.count('"') % 2 == 0 and value.count("'") % 2 == 0:
                items.append((key, value))
                key = None
                value_lines = []
            else:
                value_lines = [value]
        else:
            # 多行字符串
            if key is not None:
                value_lines.append(line.rstrip())
    if key is not None:
        value = '\n'.join(value_lines).rstrip(',')
        items.append((key, value))
    # 对于重复 key，收集所有 value
    key_to_values = {}
    for k, v in items:
        key_to_values.setdefault(k, []).append(v)
    return key_to_values


def sort_messages_dict(dict_lines):
    key_to_values = parse_messages_items(dict_lines)
    # 对于每个 key，随机选取一个 value
    unique_items = [(k, random.choice(vs)) for k, vs in key_to_values.items()]
    unique_items.sort(key=lambda x: x[0].lower())
    sorted_lines = [dict_lines[0]]
    for idx, (key, value) in enumerate(unique_items):
        is_last = idx == len(unique_items) - 1
        # 多行字符串保持缩进
        if '\n' in value:
            value_lines = value.split('\n')
            # 第一行
            sorted_lines.append(f"    {key}: {value_lines[0]}\n")
            # 中间行
            for vline in value_lines[1:-1]:
                sorted_lines.append(f"        {vline}\n")
            # 最后一行
            last_line = value_lines[-1].rstrip()
            if not is_last:
                last_line = last_line.rstrip(',')  # 移除多余逗号
                sorted_lines.append(f"        {last_line},\n")
            else:
                last_line = last_line.rstrip(',')
                sorted_lines.append(f"        {last_line}\n")
        else:
            value = value.rstrip(',')
            comma = ',' if not is_last else ''
            sorted_lines.append(f"    {key}: {value}{comma}\n")
    sorted_lines.append(dict_lines[-1])
    return sorted_lines


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    start, end, dict_lines = extract_messages_dict(lines)
    if dict_lines is None:
        print(f"No MESSAGES found in {filepath}")
        return
    sorted_dict_lines = sort_messages_dict(dict_lines)
    new_lines = lines[:start] + sorted_dict_lines + lines[end+1:]
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print(f"Sorted MESSAGES in {filepath}")


def main():
    for path in glob.glob(PATTERN):
        process_file(path)

if __name__ == '__main__':
    main()
