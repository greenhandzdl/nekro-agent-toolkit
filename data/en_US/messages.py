# -*- coding: utf-8 -*-
"""
English language pack
"""

MESSAGES = {
    # Common messages
    "checking_dependencies": "Checking dependencies...",
    "dependencies_check_passed": "Dependencies check passed.",
    "using_docker_compose_cmd": "Using '{}' as docker-compose command.",
    
    # Error messages
    "error_prefix": "Error:",
    "error_docker_not_found": "Command 'docker' not found, please install it first.",
    "error_docker_compose_not_found": "'docker-compose' or 'docker compose' not found, please install it first.",
    "error_directory_not_exist": "Directory '{}' does not exist.",
    "error_data_dir_not_exist": "Specified data directory '{}' does not exist or is not a directory.",
    "error_backup_file_not_exist": "Specified backup file '{}' does not exist or is not a file.",
    "error_invalid_backup_format": "Invalid backup file format. Only '.tar' and '.tar.zstd' are supported.",
    "error_env_file_not_exist": ".env file does not exist, please check if Nekro Agent is properly installed.",
    "error_cannot_pull_compose_file": "Cannot pull docker-compose.yml file.",
    "error_command_not_found": "Command '{}' not found.",
    "error_sudo_not_found": "'sudo' command not found. Please ensure you have administrator privileges.",
    
    # Warning messages
    "warning_prefix": "Warning:",
    "warning_data_dir_not_empty": "Target data directory '{}' is not empty. Recovery operation may overwrite existing files.",
    "warning_docker_volumes_will_overwrite": "The following Docker volumes will be restored, which will overwrite existing content in the volumes:",
    "warning_compose_file_not_found": "docker-compose.yml file not found in directory '{}'.",
    "warning_cannot_determine_data_dir": "Cannot determine main data directory from backup file, or backup only contains Docker volumes.",
    "warning_skip_data_restore": "Will only restore data directory, skip Docker volume recovery.",
    
    # Success messages
    "backup_success": "Backup successful! Backup file saved to:",
    "recovery_success": "Recovery successful! Data restored to: {}",
    "docker_volumes_restored": "Docker volumes have also been restored.",
    "update_complete": "Update complete!",
    "installation_complete": "Installation complete! Enjoy using it!",
    "version_update_complete": "Version update complete!",
    "sudo_elevation_success": "Sudo elevation successful.",
    
    # Operation progress messages
    "starting_backup": "Starting backup of Nekro Agent, data directory: {}",
    "finding_docker_volumes_backup": "Finding Docker volumes to backup...",
    "finding_docker_volumes_recovery": "Finding Docker volumes to restore...",
    "creating_archive": "Starting to create archive file...",
    "starting_extraction": "Starting extraction and recovery...",
    "analyzing_backup_file": "Analyzing backup file...",
    "creating_tar_archive": "Creating tar archive: {}...",
    "adding_to_archive": "Adding: {} (archived as: {})",
    "adding_docker_volume_backup": "Adding Docker volume backup: {} (archived as: {})",
    "restoring_docker_volume": "Restoring Docker volume '{}' to: {}",
    "restoring_docker_volume_via_container": "Restoring Docker volume '{}' (via container method)",
    "backup_docker_volume_complete": "Docker volume '{}' backup complete: {}",
    "getting_compose_file": "Getting {}...",
    
    # Confirmation operations
    "confirm_installation": "Confirm to continue installation? [Y/n] ",
    "confirm_continue": "Continue? (y/N): ",
    "confirm_update": "Continue with update? (y/N): ",
    "confirm_version_update": "Confirm version update? (y/N): ",
    "use_napcat_service": "Use napcat service as well? [Y/n] ",
    
    # Cancellation operations
    "installation_cancelled": "Installation cancelled.",
    "operation_cancelled": "Operation cancelled.",
    "update_cancelled": "Update cancelled.",
    "version_update_cancelled": "Operation cancelled",
    
    # Mode messages
    "dry_run_complete": "--dry-run complete.\n.env file generated at {}.\nNo actual installation operations performed.",
    "dry_run_mode_start": "--- Starting recovery and installation process (Dry Run mode) ---",
    "dry_run_mode_end": "--- Dry Run ended ---",
    "dry_run_not_executed": "(No actual file operations performed)",
    "recovery_install_start": "--- Starting recovery and installation process ---",
    "recovery_install_end": "--- Recovery and installation process ended ---",
    "recovery_install_data_restored": "--- Data restored, starting installation process on {} ---",
    "recovery_install_no_data_dir": "--- No specific data directory restored, will run installation process on target install directory ---",
    "default_no_napcat": "Default to not use napcat.",
    
    # Update related
    "update_method_one": "Executing update method one: Update only Nekro Agent and sandbox image",
    "update_method_two": "Executing update method two: Update all images and restart containers",
    "pulling_latest_sandbox": "Pulling latest kromiose/nekro-agent-sandbox image",
    "pulling_latest_nekro_agent": "Pulling latest nekro_agent image",
    "rebuilding_nekro_agent": "Rebuilding and starting nekro_agent container",
    "pulling_all_services": "Pulling latest images for all services",
    "restarting_all_services": "Restarting all service containers",
    
    # Installation configuration check
    "check_env_config": "Please check and modify the configuration in the .env file as needed.",
    
    # Deployment complete messages
    "deployment_complete": "=== Deployment Complete! ===",
    "view_logs_instruction": "You can view service logs with the following commands:",
    "nekro_agent_logs": "NekroAgent: 'sudo docker logs -f {}{}'",
    "napcat_logs": "NapCat: 'sudo docker logs -f {}{}'",
    "important_config_info": "=== Important Configuration Information ===",
    "onebot_access_token": "OneBot Access Token: {}",
    "admin_account": "Admin Account: admin | Password: {}",
    "service_access_info": "=== Service Access Information ===",
    "nekro_agent_port": "NekroAgent Main Service Port: {}",
    "nekro_agent_web_access": "NekroAgent Web Access URL: http://127.0.0.1:{}",
    "napcat_service_port": "NapCat Service Port: {}",
    "onebot_websocket_address": "OneBot WebSocket Connection URL: ws://127.0.0.1:{}/onebot/v11/ws",
    "important_notes": "=== Important Notes ===",
    "cloud_server_note": "1. If you are using a cloud server, please allow the corresponding ports in your cloud provider's security group console.",
    "external_access_note": "2. If you need external access, replace 127.0.0.1 in the above URLs with your server's public IP.",
    "napcat_qr_code_note": "3. Use 'sudo docker logs {}{}' to view the QR code for robot QQ account login.",
    
    # Firewall configuration
    "configuring_firewall": "Configuring firewall rules...",
    "firewall_rule_added": "Firewall rule added: {}",
    "firewall_config_complete": "Firewall configuration complete.",
    
    # Version information
    "current_version": "Current version: {}",
    "target_version": "Target version: {}",
    "updated_version": "Updated version: {}",
    "backup_file_created": "Backup file created: {}",
    "starting_version_update": "Starting version update...",
    "checking_install_file": "Checking {} (no version information needs updating currently)",
    
    # tar related
    "tar_normal_warning": "Note: tar output normal warning: {}",
    "tar_warning": "Warning: {}",
    
    # Docker volume related
    "backup_docker_volume_failed": "Failed to backup Docker volume '{}': {}",
    "backup_docker_volume_exception": "Exception occurred while backing up Docker volume '{}': {}",
    "backup_file_not_created": "Backup file {} was not successfully created or is empty",
    "volume_backup_skipped": "Backup contains volume '{}', but no recovery path provided, will skip.",
    "expected_directory_not_found": "Expected directory '{}' not found after recovery.",
    "recovery_failed": "Recovery failed.",
    "restoring_via_container_complete": "Docker volume '{}' restoration complete",
    "restore_docker_volume_failed": "Error: Failed to restore Docker volume '{}': {}",
    "backup_via_container_complete": "Docker volume '{}' backup complete: {}",
    
    # Help and usage related
    "install_description": "Install Nekro Agent to the specified path.",
    "update_description": "Perform partial update on the installation at the specified path.",
    "upgrade_description": "Perform complete update (upgrade) on the installation at the specified path.",
    "backup_description": "Backup data directory to the specified folder.",
    "recovery_description": "Restore from backup file to the specified data directory.",
    "recover_install_description": "Recover and install. This will extract the backup file to the target directory, then run the installation process on top of it.",
    "version_description": "Display version information.",
    "with_napcat_description": "Use with --install or --recover-install to deploy NapCat service.",
    "dry_run_description": "Use with --install or --recover-install to perform a dry run.",
    "yes_description": "Automatically confirm all prompts to run in non-interactive mode.",
    "all_description": "Update all services, not just Nekro Agent",
    
    # Main program description
    "app_description": "Nekro Agent installation, update and backup unified management tool.",
    "app_examples": "Usage examples:\n  {} --install ./na_data\n    # Install Nekro Agent in ./na_data directory\n\n  {} --update ./na_data\n    # Perform partial update on installation in specified directory\n\n  {} --upgrade ./na_data\n    # Perform complete update (upgrade) on installation in specified directory\n\n  {} --backup ./na_data ./backups\n    # Backup na_data directory to backups folder\n\n  {} --recovery ./backups/na_backup_123.tar.zstd ./na_data_new\n    # Restore from backup file to na_data_new directory\n\n  {} --recover-install ./backup.tar.zst ./restored_install\n    # Restore data from backup and run installation on top of it",
    
    # Installation related messages
    "app_data_directory": "Application data directory (NEKRO_DATA_DIR): {}",
    "error_create_app_directory": "Error: Cannot create application directory {}. Please check permissions.\n{}",
    "warning_chmod_777": "Warning: Setting application directory permissions to 777, this may not be secure.",
    "setting_directory_permissions": "Setting directory permissions",
    "switched_to_directory": "Switched to directory: {}",
    "env_file_found_copying": "Found .env file in {}, copying to {}...",
    "copy_success": "Copy successful.",
    "env_file_not_found_downloading": ".env file not found, downloading .env.example from repository...",
    "error_cannot_get_env_example": "Error: Cannot get .env.example file.",
    "env_file_created": ".env file created.",
    "updating_nekro_data_dir": "Updating NEKRO_DATA_DIR in .env file...",
    "checking_generating_credentials": "Checking and generating necessary access credentials...",
    "generating_random_key": "Generating random {}...",
    "default_no_napcat": "Default to not use napcat.",
    "getting_compose_file": "Getting {}...",
    "error_cannot_pull_compose_file": "Error: Cannot pull docker-compose.yml file.",
    "pulling_service_images": "Pulling service images",
    "starting_main_service": "Starting main service",
    "pulling_sandbox_image": "Pulling sandbox image",
    "detected_docker_host_correcting": "Detected DOCKER_HOST='{}', will automatically correct to 'unix://{}'",
    "nekro_agent_needs_port": "NekroAgent main service needs to allow port {}/tcp...",
    "napcat_needs_port": "NapCat service needs to allow port {}/tcp...",
    "configuring_firewall_ufw": "Configuring firewall (ufw)...",
    "allow_port": "Allow port {}",
    
    # Backup related messages
    "docker_volume_exists": "Docker volume '{}' already exists",
    "creating_docker_volume": "Creating Docker volume '{}'...",
    "docker_volume_created": "Docker volume '{}' created successfully",
    "error_create_docker_volume": "Error: Failed to create Docker volume '{}': {}",
    "warning_docker_not_found_skip_recovery": "Warning: 'docker' command not found, will skip Docker volume recovery.",
    "warning_docker_not_found_skip_backup": "Warning: 'docker' command not found, will skip Docker volume backup.",
    "will_restore_docker_volume_to_path": "Will restore Docker volume '{}' to path: {}",
    "will_restore_docker_volume_via_container": "Will restore Docker volume '{}' via container method",
    "warning_cannot_get_volume_mountpoint": "Warning: Cannot get mountpoint for Docker volume '{}', will skip. Error: {}",
    "found_docker_volume_path": "Found Docker volume '{}' path: {}",
    "found_docker_volume_container_backup": "Found Docker volume '{}' (will backup via container method)",
    "warning_docker_volume_invalid_path": "Warning: Docker volume '{}' path '{}' is invalid or not a directory, will skip.",
    "warning_cannot_get_volume_info": "Warning: Cannot get information for Docker volume '{}', will skip. Error: {}",
    "backup_via_container_starting": "Backing up Docker volume '{}' via container...",
    "restoring_via_container_starting": "Restoring Docker volume '{}' via container...",
    "restoring_via_container_complete": "Docker volume '{}' restoration complete",
    "backup_via_container_complete": "Docker volume '{}' backup complete: {}",
    "excluding_from_archive": "Excluding: {}",
    "detected_zstd_compressing": "Detected zstd, compressing to: {}...",
    "zstd_not_detected_tar_only": "zstd not detected, creating .tar archive only.",
    "error_archive_creation_failed": "Error: Archive creation failed.\n{}",
    "error_archive_extraction_failed": "Error: Archive extraction failed.\n{}",
    "error_zstd_required_for_recovery": "Error: Recovery requires 'zstd' command.",
    "error_unsupported_file_format": "Error: Unsupported file format: {}",
    
    # Docker volume container backup/recovery related
    "backup_via_container_starting": "Backing up Docker volume '{}' via container...",
    "restoring_via_container_starting": "Restoring Docker volume '{}' via container...",
    "restoring_via_container_complete": "Docker volume '{}' restoration complete",
    "backup_via_container_complete": "Docker volume '{}' backup complete: {}",
    
    # Backup creation related
    "archiving_current_directory": "Archiving current directory '.' as '{}'",
    "excluding_from_archive": "Excluding: {}",
    "detected_zstd_compressing": "Detected zstd, compressing to: {}...",
    "zstd_not_detected_tar_only": "zstd not detected, creating .tar archive only.",
    
    # Backup recovery related
    "restoring_data_to": "Restoring data to: {}",
    "multiple_root_directories_warning": "Warning: Backup contains multiple possible root directories: {}. Cannot automatically determine main data directory.",
    
    # General recovery related
    "preparing_recovery_from_backup": "Preparing recovery from backup file: {}",
    "dry_run_will_restore_from": "[Dry Run] Will restore from backup file: {}",
    "dry_run_data_extract_to": "[Dry Run] Data will be extracted to: {}",
    "dry_run_docker_volumes_restore": "[Dry Run] Docker volumes will be restored (if present in backup).",
    "dry_run_install_on_extracted": "[Dry Run] Will run installation process on extracted data.",
    "recovery_step_failed": "Recovery step failed, aborting operation.",
    "restoring_backup_to": "Restoring backup to: {}",
    
    # Command execution related
    "execute_with_current_user_success": "Executed successfully with current user permissions.",
    "insufficient_permissions_try_sudo": "Insufficient current user permissions, trying sudo elevation...",
    "error_sudo_failed": "Error: Even after sudo elevation, {} still failed.\n{}",
    
    # File download related
    "downloading_from": "Downloading from {}...",
    "download_success": "Download successful: {}",
    "download_failed_try_other": "Download failed, trying other sources... (Error: {})",
    "error_details": "Error details: {}",
    
    # Backup filtering related
    "excluding_logs_directory": "Excluding logs directory: {}",
    "excluding_uploads_directory": "Excluding uploads directory: {}",
    "excluding_env_template": "Excluding config template: {}",
    "excluding_temp_file": "Excluding AppleDouble encoded Macintosh file file: {}",
    
    # Docker volume dynamic discovery related messages
    "discovered_docker_volumes": "Dynamically discovered {} matching Docker volumes",
    "no_matching_volumes_using_static": "No matching volumes found, using static configuration: {}",
    "found_matching_docker_volume": "Found matching Docker volume: {} (suffix match: {})",
    "warning_cannot_get_volume_list": "Warning: Cannot get Docker volume list: {}",
    "error_docker_volume_discovery_exception": "Error: Exception occurred during Docker volume discovery: {}",
    
    # Module standalone help information
    "backup_module_description": "Nekro Agent backup and recovery tool.",
    "backup_module_help": "Backup specified data directory and related Docker volumes to target backup directory.",
    "recovery_module_help": "Restore data and Docker volumes from specified backup file to target directory.",
    "install_module_description": "Nekro Agent installation and management script",
    "install_module_data_dir_help": "Nekro Agent application data directory.\nDefaults to \"na_data/\" folder in the script directory.",
    "install_module_with_napcat_help": "Deploy NapCat service as well.",
    "install_module_dry_run_help": "Dry run mode: only generate .env file, do not perform actual installation.",
    "install_module_yes_help": "Automatically confirm all prompts to run in non-interactive mode.",
    "install_module_examples": "Usage examples:\n  python install.py\n    # Create na_data/ in script directory and install\n\n  python install.py /srv/nekro\n    # Install in specified directory /srv/nekro\n\n  python install.py --with-napcat\n    # Install in default directory and enable NapCat service\n\n  python install.py /srv/nekro --dry-run\n    # Dry run in specified directory, only generate .env file\n",
    "update_module_description": "Nekro Agent update tool",
    "update_module_data_dir_help": "Nekro Agent data directory (defaults to current directory)",
    "update_module_all_help": "Update all services, not just Nekro Agent",
    "update_module_yes_help": "Automatically confirm all prompts to run in non-interactive mode.",
    "update_module_examples": "Usage examples:\n  python update.py\n    # Update Nekro Agent in current directory (recommended)\n\n  python update.py /srv/nekro\n    # Update Nekro Agent located at /srv/nekro\n\n  python update.py --all\n    # Update all services in default directory (including databases)\n\n  python update.py /srv/nekro --all\n    # Combined usage: update all services in specified directory",
    
    # helpers.py related messages
    "executing_command": "Executing: {}",
    
    # Default data directory related messages
    "set_data_description": "Set or clear the default data directory.",
    "default_data_dir_set": "Default data directory set to: {}",
    "default_data_dir_cleared": "Default data directory cleared.",
    "current_default_data_dir": "Current default data directory: {}",
    "no_default_data_dir": "No default data directory set.",
    "confirm_use_default_data_dir": "Detected default data directory: {}\nUse default directory? This is equivalent to running: {}\nContinue? (y/N): ",
    "clear_default_data_dir_prompt": "Enter 'clear' to clear default data directory setting: ",
    "clear_cancelled": "Clear operation cancelled.",
}