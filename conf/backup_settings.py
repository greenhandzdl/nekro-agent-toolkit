"""
备份功能配置文件
"""
from typing import List

# 定义需要备份的 Docker 卷后缀模式（卷名必须以这些字符串结尾）
# 例如：会匹配 "xxx-nekro_postgres_data", "nekro_postgres_data", "my_app-nekro_qdrant_data" 等
DOCKER_VOLUME_SUFFIXES: List[str] = ["nekro_postgres_data", "nekro_qdrant_data"]

# 兼容性：保留原有的具体卷名列表（优先级较低）
DOCKER_VOLUMES_TO_BACKUP: List[str] = ["nekro_postgres_data", "nekro_qdrant_data"]

# 备份/恢复过程中使用的临时容器镜像和 tag
# 默认使用 Ubuntu 基础镜像及指定的 tag（可根据需要改为 alpine、debian 等更小的镜像）
BACKUP_HELPER_IMAGE: str = "alpine"
BACKUP_HELPER_TAG: str = "3.22"