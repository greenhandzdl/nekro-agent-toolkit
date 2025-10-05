{ config, pkgs, ... }:
let
  nekroAgentToolkit = import ../nix/nekro-agent-toolkit.nix { pkgs = pkgs; };
in
{
  # 创建 nekro-agent 用户，密码为 nekro-agent，属于 wheel 组（root 权限）
  users.users.nekro-agent = {
    isNormalUser = true;
    description = "Nekro Agent Toolkit User";
    extraGroups = [ "wheel" "docker" ];
    password = "nekro-agent";
    shell = pkgs.zsh;
    home = "/home/nekro-agent";
  };

  # 安装所需软件包（包含本地 Nix 包）
  environment.systemPackages = with pkgs; [
    python3
    pipx
    docker
    docker-compose
    ufw
    zstd
    nekroAgentToolkit
  ];

  # 启用 docker 服务
  virtualisation.docker.enable = true;

  # 启用 ufw 防火墙（如需自定义规则可扩展）
  services.ufw.enable = true;
  services.ufw.defaultInputPolicy = "accept";
  services.ufw.defaultOutputPolicy = "accept";

  # 允许 wheel 组用户 sudo
  security.sudo.wheelNeedsPassword = false;

  # 最小化系统配置
  networking.firewall.enable = false;
  system.stateVersion = "23.05"; # 根据实际 NixOS 版本调整

  # 构建后自动以 nekro-agent 用户在 /home/nekro-agent 执行初始化命令
  systemd.services.nekro-agent-toolkit-init = {
    description = "Initialize nekro-agent-toolkit for nekro-agent user";
    after = [ "network.target" ];
    wantedBy = [ "multi-user.target" ];
    serviceConfig = {
      Type = "oneshot";
      User = "nekro-agent";
      WorkingDirectory = "/home/nekro-agent";
      Environment = "PATH=/home/nekro-agent/.local/bin:/run/wrappers/bin:/usr/bin:/bin";
      ExecStartPre = "/run/current-system/sw/bin/pipx install nekro-agent-toolkit";
      ExecStart = "/home/nekro-agent/.local/bin/nekro-agent-toolkit -sd /home/nekro-agent";
      ExecStartPost = "yes | /home/nekro-agent/.local/bin/nekro-agent-toolkit -i ";
    };
  };
}
