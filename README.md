# <font size =5 color=green>**pst**</font>

**pst** is a command-line utility that creates visual trees of your running processes. Works best on Unix-like systems. 

**pst** is a light-weight version of [pstree](https://en.wikipedia.org/wiki/Pstree), written in Python. 

## Installation

percol currently supports only Python 2.x.

### PyPI

    $ sudo pip install percol

### Manual

First, clone percol repository and go into the directory.

    $ git clone git://github.com/mooz/percol.git
    $ cd percol

Then, run a command below.

    $ sudo python setup.py install

If you don't have a root permission (or don't wanna install percol with sudo), try next one.

    $ python setup.py install --prefix=~/.local
    $ export PATH=~/.local/bin:$PATH

## Usage

    shell> 
    shell> pst
    shell> pst --help
    shell> pst -o trees.txt

