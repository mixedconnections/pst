#!/usr/bin/env python

import os
import sys
from setuptools import setup
file_dir = os.path.dirname(os.path.realpath(__file__))
pst_dir = os.path.join(file_dir, './pst')
sys.path.insert(0, pst_dir)
from _version import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pst",
    author="mixed.connections",
    version=__version__,
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
