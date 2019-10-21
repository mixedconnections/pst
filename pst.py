#!/usr/bin/env python

"""
Program for showing the hierarchy of processes on a Linux computer
"""

__author__ = "Mike Accardo"
__copyright__ = "Copyright 2019, Mike Accardo"
__license__ = "MIT"


# imports
import traceback
import os
import sys
import subprocess
import argparse
import processparser as pp
file_dir = os.path.dirname(os.path.realpath(__file__))
pst_dir = os.path.join(file_dir, './pst')
sys.path.insert(0, pst_dir)
from _version import __version__


def less(data):
    process = subprocess.Popen(["less"], stdin=subprocess.PIPE)

    try:
        process.stdin.write(data.encode('utf-8'))
        process.communicate()
    except Exception:
        process.terminate()
        print(traceback.format_exc())
        sys.exit(0)


def my_parse_args():
    parser = argparse.ArgumentParser(
        description='Show the hierarchy of processes on a Linux computer.')
    parser.add_argument(
        "-o",
        "--output",
        action='store',
        type=str,
        dest='output',
        help="directs the output to a file name of your choice")
    parser.add_argument(
        "-c",
        "--command",
        action='store',
        type=str,
        dest='command',
        help="use custom ps command")
    parser.add_argument(
        "-w",
        "--write",
        action='store_true',
        dest='stdout',
        help="write to stdout")
    parser.add_argument(
        "-v",
        "--version",
        action='version',
        version='{version}'.format(version=__version__),
        dest='stdout',
        help="display version information")
    parser.add_argument(
        "-u",
        "--user",
        action='store',
        type=str,
        dest='user',
        help="show only trees rooted at processes of this user")
    parser.add_argument(
        "-p",
        "--pid",
        action='store',
        type=int,
        dest='pid',
        help="start at this PID; default is 1 (init)")
    args = vars(parser.parse_args())
    return args


def main(args):

    ps_command = 'ps -e l'
    if args['command']:
        ps_command = args['command']
    elif args['user']:
        ps_command = 'ps -fu {}'.format(args['user'])
    elif args['pid']:
        ps_command = 'ps -p {pid} --ppid {pid} -o pid,ppid,cmd'.format(
            pid=args['pid'])

    column_header, processes = pp.get_ps_output(ps_command)

    # Find the index of the headings that we are interested in
    # (PID,PPID,COMMAND)
    heading_indexes = pp.get_heading_indexes(column_header)

    # Next, using the indexes, extract the process data
    process_info = pp.get_process_data(heading_indexes, processes)

    # We have all the essential information that we need. Time to build the
    # process trees.
    process_trees = pp.build_process_trees(process_info)

    tree_output = pp.format_process_trees(process_info, process_trees)

    if args['output']:
        with open(args['output'], 'w') as f:
            sys.stdout = f
            sys.stdout.write(tree_output)
    elif args['stdout']:
        sys.stdout.write(tree_output)
    else:
        less(tree_output)


if __name__ == '__main__':
    args = my_parse_args()
    main(args)
