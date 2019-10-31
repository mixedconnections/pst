#!/usr/bin/env python

from setuptools import setup

_locals = {}
with open('pst/_version.py') as src:
    exec(src.read(), None, _locals)
version = _locals['__version__']

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pst",
    author="mixed.connections",
    version=version,
    author_email="mixed.connections2@gmail.com",
    description="A reproduction of pstree",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mixedconnections/pst",
    packages=["pst"],
    data_files=[("/usr/local/bin",["bin/pst"])],
    use_incremental=True,
    setup_requires=['incremental'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Topic :: Utilities",
    ],
    keywords = "shell pstree",
    license = "MIT"
)
