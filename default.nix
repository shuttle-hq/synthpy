{
  python
}:
python.pkgs.buildPythonPackage {
  name = "synthpy";
  version = "0.2.1";

  src = ./.;

  buildInputs = with python.pkgs; [
    pytest
    pytest-asyncio
    pytestrunner
  ];

  propagatedBuildInputs = with python.pkgs; [
    setuptools
    click
    yarl
    colored
    coloredlogs
    aiohttp
    ipython
  ];
}
