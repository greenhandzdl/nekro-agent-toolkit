"""
多语言支持配置文件
"""
import os

# 获取项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

# 支持的语言列表
SUPPORTED_LANGUAGES = ["zh_CN", "en_US"]
DEFAULT_LANGUAGE = "zh_CN"