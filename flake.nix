{
  description = "A tool to build resumes";

  inputs = { nixpkgs.url = "nixpkgs/nixos-24.11"; };

  outputs = { self, nixpkgs }: 
  let 
    forAllSystems = nixpkgs.lib.genAttrs nixpkgs.lib.systems.flakeExposed;

    nixpkgsFor = forAllSystems (system: import nixpkgs { inherit system; });
  in
  {


    packages = forAllSystems (system: {
      default = import ./default.nix { pkgs = nixpkgsFor.${system}; };
    });

    devShells = forAllSystems (system: {
      default = import ./shell.nix { pkgs = nixpkgsFor.${system}; };
    });

    nixosModules.default = { lib, config, pkgs, ... }: {
      options = {
        services.auto-resume-builder = {
          enable = lib.mkEnableOption "enables auto resume builder";
          envFilePath = lib.mkOption {
            type = lib.types.str;
          };
        };
      };

      config =
      let
          pkg = pkgs.callPackage ./default.nix { inherit pkgs; };
      in lib.mkIf config.services.auto-resume-builder.enable {
        systemd.services.auto-resume-builder = {
          enable = true;
          serviceConfig = {
            ExecStart = "${pkg}/bin/build-resume";
            EnvironmentFile = config.services.auto-resume-builder.envFilePath;
            Type = "oneshot";
          };
        };
        systemd.timers.auto-resume-builder = {
          enable = true;
          wantedBy = [ "timers.target" ];
          timerConfig = {
            OnBootSec = "5m";
            OnUnitActiveSec = "5m";
            Unit = "auto-resume-builder.service";
          };
        };
      };
    };

  };
}
