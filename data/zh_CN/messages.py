# -*- coding: utf-8 -*-
"""
中文语言包
"""

MESSAGES = {
    # 通用信息
    "checking_dependencies": "正在检查依赖...",
    "dependencies_check_passed": "依赖检查通过。",
    "using_docker_compose_cmd": "使用 '{}' 作为 docker-compose 命令。",
    
    # 错误信息
    "error_prefix": "错误:",
    "error_docker_not_found": "命令 'docker' 未找到，请先安装后再运行。",
    "error_docker_compose_not_found": "'docker-compose' 或 'docker compose' 未找到，请先安装后再运行。",
    "error_directory_not_exist": "目录 '{}' 不存在。",
    "error_data_dir_not_exist": "指定的数据目录 '{}' 不存在或不是一个目录。",
    "error_backup_file_not_exist": "指定的备份文件 '{}' 不存在或不是一个文件。",
    "error_invalid_backup_format": "无效的备份文件格式。只支持 '.tar' 和 '.tar.zstd'。",
    "error_env_file_not_exist": ".env 文件不存在，请检查 Nekro Agent 是否已正确安装。",
    "error_cannot_pull_compose_file": "无法拉取 docker-compose.yml 文件。",
    "error_command_not_found": "命令 '{}' 未找到。",
    "error_sudo_not_found": "'sudo' 命令未找到。请确保您有管理员权限。",
    
    # 警告信息
    "warning_prefix": "警告:",
    "warning_data_dir_not_empty": "目标数据目录 '{}' 非空。恢复操作可能会覆盖现有文件。",
    "warning_docker_volumes_will_overwrite": "将恢复以下 Docker 卷，这会覆盖卷中的现有内容:",
    "warning_compose_file_not_found": "目录 '{}' 中未找到 docker-compose.yml 文件。",
    "warning_cannot_determine_data_dir": "无法在备份文件中确定主数据目录，或备份中只包含 Docker 卷。",
    "warning_skip_data_restore": "将仅恢复数据目录，跳过 Docker 卷的恢复。",
    
    # 成功信息
    "backup_success": "备份成功！备份文件已保存至:",
    "recovery_success": "恢复成功！数据已恢复至: {}",
    "docker_volumes_restored": "Docker 卷也已恢复。",
    "update_complete": "更新完成!",
    "installation_complete": "安装完成！祝您使用愉快！",
    "version_update_complete": "版本更新完成!",
    "sudo_elevation_success": "使用 sudo 提权成功。",
    
    # 操作进度信息
    "starting_backup": "开始备份 Nekro Agent, 数据目录: {}",
    "finding_docker_volumes_backup": "正在查找需要备份的 Docker 卷...",
    "finding_docker_volumes_recovery": "正在查找需要恢复的 Docker 卷...",
    "creating_archive": "开始创建归档文件...",
    "starting_extraction": "开始解压和恢复文件...",
    "analyzing_backup_file": "正在分析备份文件...",
    "creating_tar_archive": "正在创建 tar 归档: {}...",
    "adding_to_archive": "正在添加: {} (归档为: {})",
    "adding_docker_volume_backup": "正在添加 Docker 卷备份: {} (归档为: {})",
    "restoring_docker_volume": "正在恢复 Docker 卷 '{}' 到: {}",
    "restoring_docker_volume_via_container": "正在恢复 Docker 卷 '{}' (通过容器方式)",
    "backup_docker_volume_complete": "Docker 卷 '{}' 备份完成: {}",
    "getting_compose_file": "正在获取 {}...",
    
    # 确认操作
    "confirm_installation": "确认是否继续安装？[Y/n] ",
    "confirm_continue": "是否继续？ (y/N): ",
    "confirm_update": "是否继续更新? (y/N): ",
    "confirm_version_update": "确认更新版本吗? (y/N): ",
    "use_napcat_service": "是否同时使用 napcat 服务？[Y/n] ",
    
    # 取消操作
    "installation_cancelled": "安装已取消。",
    "operation_cancelled": "操作已取消。",
    "update_cancelled": "取消更新。",
    "version_update_cancelled": "取消操作",
    
    # 模式信息
    "dry_run_complete": "--dry-run 完成。\n.env 文件已在 {} 生成。\n未执行任何安装操作。",
    "dry_run_mode_start": "--- 开始恢复并安装流程 (Dry Run 模式) ---",
    "dry_run_mode_end": "--- Dry Run 结束 ---",
    "dry_run_not_executed": "(未执行任何实际文件操作)",
    "recovery_install_start": "--- 开始恢复并安装流程 ---",
    "recovery_install_end": "--- 恢复并安装流程结束 ---",
    "recovery_install_data_restored": "--- 数据已恢复，开始在 {} 上执行安装流程 ---",
    "recovery_install_no_data_dir": "--- 未恢复特定数据目录，将在目标安装目录上执行安装流程 ---",
    "default_no_napcat": "默认不使用 napcat。",
    
    # 更新相关
    "update_method_one": "正在执行更新方式一：仅更新 Nekro Agent 和沙盒镜像",
    "update_method_two": "正在执行更新方式二：更新所有镜像并重启容器",
    "pulling_latest_sandbox": "拉取最新的 kromiose/nekro-agent-sandbox 镜像",
    "pulling_latest_nekro_agent": "拉取最新的 nekro_agent 镜像",
    "rebuilding_nekro_agent": "重新构建并启动 nekro_agent 容器",
    "pulling_all_services": "拉取所有服务的最新镜像",
    "restarting_all_services": "重启所有服务容器",
    
    # 安装配置检查
    "check_env_config": "请检查并按需修改 .env 文件中的配置。",
    
    # 部署完成信息
    "deployment_complete": "=== 部署完成！ ===",
    "view_logs_instruction": "你可以通过以下命令查看服务日志：",
    "nekro_agent_logs": "NekroAgent: 'sudo docker logs -f {}{}'",
    "napcat_logs": "NapCat: 'sudo docker logs -f {}{}'",
    "important_config_info": "=== 重要配置信息 ===",
    "onebot_access_token": "OneBot 访问令牌: {}",
    "admin_account": "管理员账号: admin | 密码: {}",
    "service_access_info": "=== 服务访问信息 ===",
    "nekro_agent_port": "NekroAgent 主服务端口: {}",
    "nekro_agent_web_access": "NekroAgent Web 访问地址: http://127.0.0.1:{}",
    "napcat_service_port": "NapCat 服务端口: {}",
    "onebot_websocket_address": "OneBot WebSocket 连接地址: ws://127.0.0.1:{}/onebot/v11/ws",
    "important_notes": "=== 注意事项 ===",
    "cloud_server_note": "1. 如果您使用的是云服务器，请在云服务商控制台的安全组中放行相应端口。",
    "external_access_note": "2. 如果需要从外部访问，请将上述地址中的 127.0.0.1 替换为您的服务器公网IP。",
    "napcat_qr_code_note": "3. 请使用 'sudo docker logs {}{}' 查看机器人 QQ 账号二维码进行登录。",
    
    # 防火墙配置
    "configuring_firewall": "正在配置防火墙规则...",
    "firewall_rule_added": "防火墙规则已添加: {}",
    "firewall_config_complete": "防火墙配置完成。",
    
    # 版本信息
    "current_version": "当前版本: {}",
    "target_version": "目标版本: {}",
    "updated_version": "更新后版本: {}",
    "backup_file_created": "已创建备份文件: {}",
    "starting_version_update": "开始更新版本...",
    "checking_install_file": "检查 {} (当前无需更新版本信息)",
    
    # tar 相关
    "tar_normal_warning": "注意: tar 输出了正常警告: {}",
    "tar_warning": "警告: {}",
    
    # Docker 卷相关
    "backup_docker_volume_failed": "备份 Docker 卷 '{}' 失败: {}",
    "backup_docker_volume_exception": "备份 Docker 卷 '{}' 时发生异常: {}",
    "backup_file_not_created": "备份文件 {} 未成功创建或为空",
    "volume_backup_skipped": "备份中包含卷 '{}'，但未提供其恢复路径，将跳过。",
    "expected_directory_not_found": "恢复后未找到预期的目录 '{}'。",
    "recovery_failed": "恢复失败。",
    "restoring_via_container_complete": "Docker 卷 '{}' 恢复完成",
    "restore_docker_volume_failed": "错误: 恢复 Docker 卷 '{}' 失败: {}",
    "backup_via_container_complete": "Docker 卷 '{}' 备份完成: {}",
    
    # 帮助和使用说明相关
    "install_description": "安装 Nekro Agent 到指定路径。",
    "update_description": "对指定路径的安装执行部分更新。",
    "upgrade_description": "对指定路径的安装执行完全更新（升级）。",
    "backup_description": "备份数据目录到指定文件夹。",
    "recovery_description": "从备份文件恢复到指定数据目录。",
    "recover_install_description": "恢复并安装。这会解压备份文件到目标目录，然后在此之上运行安装流程。",
    "version_description": "显示版本信息。",
    "with_napcat_description": "与 --install 或 --recover-install 配合使用，部署 NapCat 服务。",
    "dry_run_description": "与 --install 或 --recover-install 配合使用，执行预演。",
    "yes_description": "自动确认所有提示，以非交互模式运行。",
    "all_description": "更新所有服务，而不仅仅是 Nekro Agent",
    
    # 主程序描述信息
    "app_description": "Nekro Agent 安装、更新与备份的统一管理工具。",
    "app_examples": "用法示例:\n  {} --install ./na_data\n    # 在 ./na_data 目录中安装 Nekro Agent\n\n  {} --update ./na_data\n    # 对指定目录的安装执行部分更新\n\n  {} --upgrade ./na_data\n    # 对指定目录的安装执行完全更新（升级）\n\n  {} --backup ./na_data ./backups\n    # 备份 na_data 目录到 backups 文件夹\n\n  {} --recovery ./backups/na_backup_123.tar.zstd ./na_data_new\n    # 从备份文件恢复到 na_data_new 目录\n\n  {} --recover-install ./backup.tar.zst ./restored_install\n    # 从备份恢复数据，并在此基础上执行安装",
    
    # 安装相关消息
    "app_data_directory": "应用数据目录 (NEKRO_DATA_DIR): {}",
    "error_create_app_directory": "错误: 无法创建应用目录 {}。请检查权限。\n{}",
    "warning_chmod_777": "警告: 正在设置应用目录权限为 777，这可能不安全。",
    "setting_directory_permissions": "设置目录权限",
    "switched_to_directory": "已切换到目录: {}",
    "env_file_found_copying": "在 {} 中找到 .env 文件，正在复制到 {}...",
    "copy_success": "复制成功。",
    "env_file_not_found_downloading": "未找到 .env 文件，正在从仓库获取 .env.example...",
    "error_cannot_get_env_example": "错误: 无法获取 .env.example 文件。",
    "env_file_created": "已创建 .env 文件。",
    "updating_nekro_data_dir": "正在更新 .env 文件中的 NEKRO_DATA_DIR...",
    "checking_generating_credentials": "正在检查并生成必要的访问凭证...",
    "generating_random_key": "正在生成随机 {}...",
    "default_no_napcat": "默认不使用 napcat。",
    "getting_compose_file": "正在获取 {}...",
    "error_cannot_pull_compose_file": "错误: 无法拉取 docker-compose.yml 文件。",
    "pulling_service_images": "拉取服务镜像",
    "starting_main_service": "启动主服务",
    "pulling_sandbox_image": "拉取沙盒镜像",
    "detected_docker_host_correcting": "检测到 DOCKER_HOST='{}'，将自动修正为 'unix://{}'",
    "nekro_agent_needs_port": "NekroAgent 主服务需放行端口 {}/tcp...",
    "napcat_needs_port": "NapCat 服务需放行端口 {}/tcp...",
    "configuring_firewall_ufw": "正在配置防火墙 (ufw)...",
    "allow_port": "放行端口 {}",
    
    # 备份相关消息
    "docker_volume_exists": "Docker 卷 '{}' 已存在",
    "creating_docker_volume": "正在创建 Docker 卷 '{}'...",
    "docker_volume_created": "Docker 卷 '{}' 创建成功",
    "error_create_docker_volume": "错误: 创建 Docker 卷 '{}' 失败: {}",
    "warning_docker_not_found_skip_recovery": "警告: 未找到 'docker' 命令，将跳过 Docker 卷的恢复。",
    "warning_docker_not_found_skip_backup": "警告: 未找到 'docker' 命令，将跳过 Docker 卷的备份。",
    "will_restore_docker_volume_to_path": "将恢复 Docker 卷 '{}' 到路径: {}",
    "will_restore_docker_volume_via_container": "将通过容器方式恢复 Docker 卷 '{}'",
    "warning_cannot_get_volume_mountpoint": "警告: 无法获取 Docker 卷 '{}' 的挂载点，将跳过。错误: {}",
    "found_docker_volume_path": "找到 Docker 卷 '{}' 的路径: {}",
    "found_docker_volume_container_backup": "找到 Docker 卷 '{}' (将通过容器方式备份)",
    "warning_docker_volume_invalid_path": "警告: Docker 卷 '{}' 的路径 '{}' 无效或不是一个目录，将跳过。",
    "warning_cannot_get_volume_info": "警告: 无法获取 Docker 卷 '{}' 的信息，将跳过。错误: {}",
    "backup_via_container_starting": "正在通过容器备份 Docker 卷 '{}'...",
    "restoring_via_container_starting": "正在通过容器恢复 Docker 卷 '{}'...",
    "restoring_via_container_complete": "Docker 卷 '{}' 恢复完成",
    "backup_via_container_complete": "Docker 卷 '{}' 备份完成: {}",
    "excluding_from_archive": "正在排除: {}",
    "detected_zstd_compressing": "检测到 zstd，正在压缩为: {}...",
    "zstd_not_detected_tar_only": "未检测到 zstd，仅创建 .tar 归档。",
    "error_archive_creation_failed": "错误：创建归档失败.\n{}",
    "error_archive_extraction_failed": "错误：解压归档失败.\n{}",
    "error_zstd_required_for_recovery": "错误: 恢复需要 'zstd' 命令。",
    "error_unsupported_file_format": "错误: 不支持的文件格式: {}",
    
    # Docker 卷容器备份/恢复相关
    "backup_via_container_starting": "正在通过容器备份 Docker 卷 '{}'...",
    "restoring_via_container_starting": "正在通过容器恢复 Docker 卷 '{}'...",
    "restoring_via_container_complete": "Docker 卷 '{}' 恢复完成",
    "backup_via_container_complete": "Docker 卷 '{}' 备份完成: {}",
    
    # 备份创建相关
    "archiving_current_directory": "将当前目录 '.' 归档为 '{}'",
    "excluding_from_archive": "正在排除: {}",
    "detected_zstd_compressing": "检测到 zstd，正在压缩为: {}...",
    "zstd_not_detected_tar_only": "未检测到 zstd，仅创建 .tar 归档。",
    
    # 备份恢复相关
    "restoring_data_to": "正在恢复数据到: {}",
    "multiple_root_directories_warning": "警告: 备份中包含多个可能的根目录: {}。无法自动确定主数据目录。",
    
    # 通用恢复相关
    "preparing_recovery_from_backup": "准备从备份文件恢复: {}",
    "dry_run_will_restore_from": "[Dry Run] 将从备份文件恢复: {}",
    "dry_run_data_extract_to": "[Dry Run] 数据将被解压到: {}",
    "dry_run_docker_volumes_restore": "[Dry Run] Docker 卷将被恢复（如果存在于备份中）。",
    "dry_run_install_on_extracted": "[Dry Run] 将在解压后的数据上运行安装流程。",
    "recovery_step_failed": "恢复步骤失败，中止操作。",
    "restoring_backup_to": "正在将备份恢复到: {}",
    
    # 命令执行相关
    "execute_with_current_user_success": "使用当前用户权限执行成功。",
    "insufficient_permissions_try_sudo": "当前用户权限不足，尝试使用 sudo 提权...",
    "error_sudo_failed": "错误: 使用 sudo 提权后，{} 仍然失败.\n{}",
    
    # 文件下载相关
    "downloading_from": "正在从 {} 下载...",
    "download_success": "下载成功: {}",
    "download_failed_try_other": "下载失败，尝试其他源... (错误: {})",
    "error_details": "错误详情: {}",
    
    # 备份过滤相关
    "excluding_logs_directory": "排除日志目录: {}",
    "excluding_uploads_directory": "排除上传目录: {}",
    "excluding_env_template": "排除配置模板: {}",
    "excluding_temp_file": "排除AppleDouble encoded Macintosh file文件: {}",
    
    # Docker 卷动态发现相关消息
    "discovered_docker_volumes": "动态发现了 {} 个符合条件的 Docker 卷",
    "no_matching_volumes_using_static": "未发现符合条件的 Docker 卷，使用静态配置: {}",
    "found_matching_docker_volume": "发现符合条件的 Docker 卷: {} (匹配后缀: {})",
    "warning_cannot_get_volume_list": "警告: 无法获取 Docker 卷列表: {}",
    "error_docker_volume_discovery_exception": "错误: 发现 Docker 卷时发生异常: {}",
    
    # 模块独立运行帮助信息
    "backup_module_description": "Nekro Agent 备份与恢复工具。",
    "backup_module_help": "备份指定的数据目录和相关 Docker 卷到目标备份目录。",
    "recovery_module_help": "从指定的备份文件恢复数据和 Docker 卷到目标目录。",
    "install_module_description": "Nekro Agent 安装与管理脚本",
    "install_module_data_dir_help": "Nekro Agent 的应用数据目录。\n默认为脚本所在目录下的 \"na_data/\" 文件夹。",
    "install_module_with_napcat_help": "同时部署 NapCat 服务。",
    "install_module_dry_run_help": "预演模式：仅生成 .env 文件，不执行实际安装。",
    "install_module_yes_help": "自动确认所有提示，以非交互模式运行。",
    "install_module_examples": "用法示例:\n  python install.py\n    # 在脚本目录下创建 na_data/ 并安装\n\n  python install.py /srv/nekro\n    # 在指定目录 /srv/nekro 安装\n\n  python install.py --with-napcat\n    # 在默认目录安装，并启用 NapCat 服务\n\n  python install.py /srv/nekro --dry-run\n    # 在指定目录预演，仅生成 .env 文件\n",
    "update_module_description": "Nekro Agent 更新工具",
    "update_module_data_dir_help": "Nekro Agent 数据目录 (默认为当前目录)",
    "update_module_all_help": "更新所有服务，而不仅仅是 Nekro Agent",
    "update_module_yes_help": "自动确认所有提示，以非交互模式运行。",
    "update_module_examples": "用法示例:\n  python update.py\n    # 在当前目录更新 Nekro Agent (推荐方式)\n\n  python update.py /srv/nekro\n    # 更新位于 /srv/nekro 的 Nekro Agent\n\n  python update.py --all\n    # 在默认目录更新所有服务 (包括数据库等)\n\n  python update.py /srv/nekro --all\n    # 组合使用：在指定目录更新所有服务",
    
    # helpers.py 相关消息
    "executing_command": "正在执行: {}",
    
    # 默认数据目录相关消息
    "set_data_description": "设置或清除默认数据目录。",
    "default_data_dir_set": "默认数据目录已设置为: {}",
    "default_data_dir_cleared": "默认数据目录已清除。",
    "current_default_data_dir": "当前默认数据目录: {}",
    "no_default_data_dir": "未设置默认数据目录。",
    "confirm_use_default_data_dir": "检测到默认数据目录: {}\n是否使用默认目录？这等效于运行: {}\n继续？ (y/N): ",
    "clear_default_data_dir_prompt": "输入 'clear' 以清除默认数据目录设置: ",
    "clear_cancelled": "清除操作已取消。",
}