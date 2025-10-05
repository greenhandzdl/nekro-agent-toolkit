{
  description = "Nekro Agent Toolkit NixOS flake";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.05";
  inputs.nixos-generators.url = "github:nix-community/nixos-generators";

  outputs = { self, nixpkgs, nixos-generators }:
    let
      system = "x86_64-linux";
    in {
      nixosConfigurations.nekro-agent-toolkit = nixpkgs.lib.nixosSystem {
        system = system;
        modules = [
          ./nekro-agent-toolkit.nix
        ];
      };
    };
}
