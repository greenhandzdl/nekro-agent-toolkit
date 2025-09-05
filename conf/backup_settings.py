"""
备份功能配置文件
"""

# 定义需要备份的 Docker 卷后缀模式（卷名必须以这些字符串结尾）
# 例如：会匹配 "xxx-nekro_postgres_data", "nekro_postgres_data", "my_app-nekro_qdrant_data" 等
DOCKER_VOLUME_SUFFIXES = ["nekro_postgres_data", "nekro_qdrant_data"]

# 兼容性：保留原有的具体卷名列表（优先级较低）
DOCKER_VOLUMES_TO_BACKUP: list[str] = ["nekro_postgres_data", "nekro_qdrant_data"]