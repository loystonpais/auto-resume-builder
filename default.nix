{ pkgs ? import <nixpkgs> {} }:

let 

  inherit (import ./derivations.nix { inherit pkgs; }) groq linkedin-api; 

  srcDir = with pkgs.lib.fileset; toSource {
    root = ./.;
    fileset =
    let
      # IIRC cleanSource removes .git
      cleaned = fromSource (pkgs.lib.cleanSource ./.);

      nixFiles = fileFilter (f: f.hasExt "nix") ./.;

      gitignores = fileFilter (f: f.name == ".gitignore") ./.;

      other = unions ( map maybeMissing [
        ./result
        ./.direnv
        ./.github
        ./.idea
        ./.vscode
        ./.envrc

        ./resume.pdf
        ./__pycache__
        ./build

        ./flake.lock

        ./README.md
      ] );

      fileset = difference cleaned ( unions [
        nixFiles
        gitignores
        other
      ] );
    in fileset;
  };

in

pkgs.python3Packages.buildPythonPackage rec {
  name = "auto-resume-builder";
  src = srcDir;
  dependencies = with pkgs.python3Packages; [ 
    reportlab
    weasyprint
    pygithub
    groq
    linkedin-api
  ];

  installPhase = ''
    mkdir -p $out/bin
    cp build-resume.py $out/bin/build-resume
    substituteInPlace $out/bin/build-resume --replace-fail "/usr/bin/env python" "${pkgs.python3}/bin/python3"
    chmod +x $out/bin/build-resume
  '';
}