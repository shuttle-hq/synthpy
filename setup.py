from setuptools import setup
import os

__version__ = "0.2.1"

with open('README.md', encoding='utf-8') as readme_file:
    readme = readme_file.read()

setup(
    name="getsynthpy",
    version=__version__,
    author="Damien Broka",
    author_email="damien@getsynth.com",
    description="A Python-native synthd client library",
    long_description=readme,
    long_description_content_type='text/markdown',
    scripts=["bin/synthpy"],
    packages=["synthpy", "synthpy/client"],
    tests_require=["pytest", "pytest-asyncio"],
    setup_requires=["pytest-runner"],
    install_requires=[
        "setuptools",
        "aiohttp>=3.6.2,<4.1.0",
        "yarl>=1.4.2,<1.7.0",
        "click>=7.0,<8.0",
        "colored>=1.4.2,<1.5.0",
        "coloredlogs>=10.0,<16.0",
    ],
    python_requires=">=3.7",
)
