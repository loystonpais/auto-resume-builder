{ pkgs ? import <nixpkgs> {} }:

let

  inherit (import ./derivations.nix { inherit pkgs; }) groq linkedin-api;

in

pkgs.mkShell {
  buildInputs = with pkgs; [
    python3
    python3Packages.reportlab
    python3Packages.weasyprint
    python3Packages.pygithub
    linkedin-api
    groq
  ];
}
