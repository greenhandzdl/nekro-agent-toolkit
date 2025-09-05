# 多语言支持实现总结

## 已完成的功能

### 1. 核心多语言系统
- ✅ 创建了 `utils/i18n.py` 多语言管理模块
- ✅ 支持环境变量 `$LANG` 自动检测语言
- ✅ 实现了语言文件动态加载机制
- ✅ 提供了便捷的 `_()` 函数用于消息获取

### 2. 语言文件
- ✅ 创建了 `data/zh_CN/messages.py` 中文语言包
- ✅ 创建了 `data/en_US/messages.py` 英文语言包
- ✅ 涵盖了所有系统消息（错误、警告、成功、进度等）

### 3. 应用集成
- ✅ 更新了 `app.py` 主程序支持多语言参数描述
- ✅ 更新了 `utils/helpers.py` 核心函数支持多语言
- ✅ 错误消息和系统提示已国际化

### 4. 配置更新
- ✅ 更新了 `pyproject.toml` 包含语言文件
- ✅ 创建了使用文档和示例

## 使用方式

### 基本语法
```python
from utils.i18n import get_message as _

# 简单消息
print(_("checking_dependencies"))

# 带参数消息  
print(_("error_directory_not_exist", "/path"))
```

### 环境控制
```bash
# 中文环境
LANG=zh_CN.UTF-8 nekro-agent-toolkit --help

# 英文环境
LANG=en_US.UTF-8 nekro-agent-toolkit --help
```

## 特性

1. **自动检测**: 根据 `$LANG` 环境变量自动选择语言
2. **智能回退**: 不支持的语言自动回退到中文
3. **错误处理**: 缺失消息键时返回键名本身
4. **格式化支持**: 支持参数格式化
5. **运行时切换**: 支持程序运行时切换语言

## 语言检测优先级

1. 环境变量 `LANG`
2. 系统默认 locale
3. 默认语言 (zh_CN)

## 支持的语言

- `zh_CN` - 中文简体（默认）
- `en_US` - 英文

## 扩展方法

要添加新语言（如日文）：

1. 创建目录 `data/ja_JP/`
2. 创建 `data/ja_JP/messages.py` 文件
3. 复制消息键并翻译为日文
4. 在 `utils/i18n.py` 的 `SUPPORTED_LANGUAGES` 中添加 `"ja_JP"`

## 待完善的模块

以下模块还需要完成多语言集成：

- [ ] `utils/install_utils.py`
- [ ] `utils/update_utils.py` 
- [ ] `utils/backup_utils.py`
- [ ] `module/install.py`
- [ ] `module/update.py`
- [ ] `module/backup.py`

这些模块的多语言化可以按需逐步进行，核心框架已经建立完成。