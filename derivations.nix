{ pkgs ? import <nixpkgs> { } }: {
  groq = pkgs.python3Packages.buildPythonPackage rec {
    pname = "groq";
    version = "0.13.0";
    format = "pyproject";
    src = pkgs.fetchPypi {
      inherit pname version;
      sha256 = "sha256-qqITghyU2JdOV7q1/lnLRciHGHXQzVPsF5r+2Si60Y4=";
    };
    nativeBuildInputs = with pkgs.python3Packages; [
      hatchling
      hatch-vcs
      hatch-fancy-pypi-readme
      anyio
      distro
      httpx
      pydantic
    ];

    propagatedBuildInputs = with pkgs.python3Packages; [
      anyio
      distro
      httpx
      pydantic
    ];
  };

  linkedin-api = pkgs.python3Packages.buildPythonPackage rec {
    pname = "linkedin_api";
    version = "2.3.1";
    format = "pyproject";
    src = pkgs.fetchPypi {
      inherit pname version;
      sha256 = "sha256-B6sCBECgSeSObFXWth+6sElIAiXsioLxTlwHeufsyYQ=";
    };

    propagatedBuildInputs = with pkgs.python3Packages; [
      poetry-core
      beautifulsoup4
      lxml
      requests
    ];
  };
}
