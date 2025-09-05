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
}