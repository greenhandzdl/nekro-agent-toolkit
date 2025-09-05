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
}