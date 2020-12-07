from setuptools import setup

setup(
    name="synthpy",
    version="0.1.0",
    author="Damien Broka",
    author_email="damien@getsynth.com",
    description="A Python-native synthd client library",
    packages=["synthpy"],
    tests_require=["pytest", "pytest-asyncio"],
    setup_requires=["pytest-runner"],
    install_requires=["aiohttp", "yarl"],
    python_requires=">=3.7",
)
