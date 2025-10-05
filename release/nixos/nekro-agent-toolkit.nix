{ config, pkgs, ... }:
{
  # 创建 nekro-agent 用户，密码为 nekro-agent，属于 wheel 组（root 权限）
  users.users.nekro-agent = {
    isNormalUser = true;
    description = "Nekro Agent Toolkit User";
    extraGroups = [ "wheel" "docker" ];
    password = "nekro-agent";
    shell = pkgs.zsh;
  };

  # 安装所需软件包
  environment.systemPackages = with pkgs; [
    python3
    pipx
    nekro-agent-toolkit
    docker
    docker-compose
    ufw
    zstd
  ];

  # 启用 docker 服务
  services.docker.enable = true;

  # 启用 ufw 防火墙（如需自定义规则可扩展）
  services.ufw.enable = true;
  services.ufw.defaultInputPolicy = "accept";
  services.ufw.defaultOutputPolicy = "accept";

  # 允许 wheel 组用户 sudo
  security.sudo.wheelNeedsPassword = false;

  # 最小化系统配置
  networking.firewall.enable = false;
  system.stateVersion = "23.05"; # 根据实际 NixOS 版本调整
}

