# -*- coding: utf-8 -*-
"""
多语言支持模块
Internationalization (i18n) support module
"""

import os
import sys
import locale

from conf.i18n_settings import PROJECT_ROOT, DATA_DIR, SUPPORTED_LANGUAGES, DEFAULT_LANGUAGE

# 全局语言配置
_current_language = None
_messages = None


def detect_system_language():
    """
    检测系统语言环境
    
    Returns:
        str: 语言代码 (如 zh_CN, en_US)
    """
    # 优先检查 LANG 或 LANGUAGE 环境变量（更通用的解析）
    lang_env = os.environ.get('LANG', '') or os.environ.get('LANGUAGE', '')
    if lang_env:
        # 处理常见格式，如 zh_CN.UTF-8, en-US, es_ES.UTF-8
        code = lang_env.split('.')[0]
        code = code.replace('-', '_')
        # 直接返回已支持的语言代码
        if code in SUPPORTED_LANGUAGES:
            return code
        # 更宽松的前缀匹配（例如 zh -> zh_CN, en -> en_US, es -> es_ES 等）
        prefix_map = {
            'zh': 'zh_CN',
            'en': 'en_US',
            'es': 'es_ES',
            'fr': 'fr_FR',
            'ja': 'ja_JP',
            'ru': 'ru_RU',
            'ar': 'ar_SA',
        }
        for pfx, target in prefix_map.items():
            if code.startswith(pfx):
                return target if target in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE
    
    # 回退到 locale 检测（同样采用更通用的处理）
    try:
        system_locale = locale.getdefaultlocale()[0]
        if system_locale:
            sys_code = system_locale.split('.')[0].replace('-', '_')
            if sys_code in SUPPORTED_LANGUAGES:
                return sys_code
            # 宽松前缀匹配（回退）
            for pfx, target in prefix_map.items():
                if sys_code.startswith(pfx):
                    return target if target in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE
    except Exception:
        pass
    
    # 最后的回退
    return DEFAULT_LANGUAGE


def load_language(language_code=None):
    """
    加载指定语言的消息
    
    Args:
        language_code (str): 语言代码，如果为 None 则自动检测
        
    Returns:
        dict: 消息字典
    """
    global _current_language, _messages
    
    if language_code is None:
        language_code = detect_system_language()
    
    # 如果不在支持的语言列表中，使用默认语言
    if language_code not in SUPPORTED_LANGUAGES:
        language_code = DEFAULT_LANGUAGE
    
    # 如果已经加载了相同语言，直接返回
    if _current_language == language_code and _messages is not None:
        return _messages
    
    # 加载语言文件
    try:
        language_file_path = os.path.join(DATA_DIR, language_code, "messages.py")
        
        if not os.path.exists(language_file_path):
            # 如果语言文件不存在，使用默认语言
            if language_code != DEFAULT_LANGUAGE:
                return load_language(DEFAULT_LANGUAGE)
            else:
                raise FileNotFoundError(f"Default language file not found: {language_file_path}")
        
        # 动态加载语言模块
        # Python 3.5+ 方式
        if sys.version_info >= (3, 5):
            import importlib.util
            spec = importlib.util.spec_from_file_location(f"messages_{language_code}", language_file_path)
            if spec is None or spec.loader is None:
                raise ImportError(f"Cannot load module spec for {language_file_path}")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        else:
            # 兼容旧版本
            import imp
            module = imp.load_source(f"messages_{language_code}", language_file_path)
        
        _messages = module.MESSAGES
        _current_language = language_code
        
        return _messages
    
    except Exception as e:
        # 如果加载失败且不是默认语言，尝试加载默认语言
        if language_code != DEFAULT_LANGUAGE:
            return load_language(DEFAULT_LANGUAGE)
        else:
            # 如果连默认语言都加载失败，返回空字典避免程序崩溃
            print(f"Warning: Failed to load language pack: {e}", file=sys.stderr)
            return {}


def get_message(key, *args, **kwargs):
    """
    获取本地化消息
    
    Args:
        key (str): 消息键
        *args: 格式化参数
        **kwargs: 关键字参数，支持 language 指定语言
        
    Returns:
        str: 本地化消息
    """
    language = kwargs.pop('language', None)
    messages = load_language(language)
    
    message = messages.get(key, key)  # 如果找不到消息，返回键本身
    
    # 格式化消息
    if args:
        try:
            return message.format(*args)
        except (IndexError, ValueError):
            # 如果格式化失败，返回原消息
            return message
    
    return message


def get_current_language():
    """
    获取当前语言代码
    
    Returns:
        str: 当前语言代码
    """
    global _current_language
    if _current_language is None:
        load_language()
    return _current_language


def set_language(language_code):
    """
    设置语言
    
    Args:
        language_code (str): 语言代码
    """
    load_language(language_code)


# 便捷函数
def _(key, *args, **kwargs):
    """
    获取本地化消息的简写函数
    
    Args:
        key (str): 消息键
        *args: 格式化参数
        **kwargs: 关键字参数
        
    Returns:
        str: 本地化消息
    """
    return get_message(key, *args, **kwargs)


# 初始化时自动加载默认语言
load_language()