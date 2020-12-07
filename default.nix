{
  pkgs ? import <nixpkgs> {}
, python ? pkgs.python38
}:
python.pkgs.buildPythonPackage {
  name = "synthpy";
  version = "0.1.0";

  src = ./.;

  buildInputs = with python.pkgs; [
    pytest
    pytest-asyncio
    pytestrunner
  ];

  propagatedBuildInputs = with python.pkgs; [
    aiohttp
    yarl
  ];
}
