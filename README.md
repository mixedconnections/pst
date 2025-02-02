pst: a reproduction of pstree
=============================


[![Python versions](https://img.shields.io/pypi/v/pst.svg)](https://pypi.org/project/pst/)
[![Codecov](https://codecov.io/github/mixedconnections/pst/coverage.svg?branch=master)](https://codecov.io/gh/mixedconnections/pst)

pst is a command-line utility that creates visual trees of your running processes on Unix-like systems. 

![pstexample](https://user-images.githubusercontent.com/833824/68803703-40952580-062e-11ea-9ea6-2a506316cafb.png)

pst is a reproduction of [pstree](https://en.wikipedia.org/wiki/Pstree), written in Python.

# Installation

pst currently supports Python 2.x-3.x.

#### PyPI

    $ sudo pip install pst

#### Manual

First clone the pst repository and go into the directory.

    $ git clone git://github.com/topunix/pst.git
    $ cd pst

Then run the command below.

    $ sudo python setup.py install

If you don't have root permission (or don't want to install pst with sudo), try:

    $ python setup.py install --prefix=~/.local
    $ export PATH=~/.local/bin:$PATH

# Usage

 __pst__ shows running processes as a tree.  The tree is rooted at
 either _pid_ or __init__ if _pid_ is omitted.  If a user name is specified,
 all process trees rooted at processes owned by that user are shown
 
#### Command Line Options

##### -h, --help

Display a help message

##### -v, --version

Display the version of pst

##### -o, --output `string`
    
Directs the output to a file name of your choice

##### -w, --write

When specified, pst writes to stdout. By default, pst uses less to page the output. 

##### -u, --user `string`
    
Show only trees rooted at processes of this user

##### -p, --pid `integer`
    
Start at this pid; default is 1 (init)

# Demo
Demos speak more than a thousand words! Here's me running pst on ubuntu. As you can see, you can select a pid and see its child processes:

![pst-demo](https://user-images.githubusercontent.com/833824/68803841-7df9b300-062e-11ea-97bf-0aef1f264abd.gif)

#### More Examples

    shell> 
    shell> pst
    shell> pst --help
    shell> pst -o trees.txt 
    shell> pst --user postgres
