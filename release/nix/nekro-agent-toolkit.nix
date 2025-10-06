{ pkgs ? import <nixpkgs> {} }:

pkgs.stdenv.mkDerivation {
  pname = "nekro-agent-toolkit";
  version = "1.4.9";

  src = null;

  buildInputs = [
    pkgs.python3
    pkgs.pipx
  ];

  # 可选依赖（用户可按需添加到环境中）
  meta = {
    description = "Nekro Agent Toolkit installed via pipx.";
    homepage = "https://pypi.org/project/nekro-agent-toolkit";
    license = pkgs.lib.licenses.mit;
    optionalDeps = [
      pkgs.docker
      pkgs.docker-compose
      pkgs.zstd
      pkgs.ufw
    ];
  };

  installPhase = ''
    mkdir -p $out/bin
    export PIPX_HOME="$out/pipx"
    export PIPX_BIN_DIR="$out/bin"
    pipx install nekro-agent-toolkit
  '';

  shellHook = ''
    export PIPX_HOME="$PWD/pipx"
    export PIPX_BIN_DIR="$PWD/bin"
    pipx install nekro-agent-toolkit || true
    echo "Optional dependencies: docker, docker-compose, zstd, ufw"
  '';
}

