"""
Program for showing the hierarchy of processes on a Linux computer
"""

__author__ = "Mike Accardo"
__copyright__ = "Copyright 2019, Mike Accardo"
__license__ = "MIT"

#!/usr/bin/python

# imports
import sys
import argparse
import processparser as pp 

def my_parse_args():
    parser = argparse.ArgumentParser(description='Show the hierarchy of processes on a Linux computer.')
    parser.add_argument("-o", "--output", action='store',
                     type=argparse.FileType('w'), dest='output', 
                     help="Directs the output to a file name of your choice")
    parser.add_argument("-c", "--command", action='store',
                     type=str, dest='command', 
                     help="Use custom ps command")
    args = vars(parser.parse_args())
    return args

def main(args):

    ps_command = args['command'] or 'ps -e l'
    column_header, processes  = pp.get_ps_output(ps_command)

    # Find the index of the headings that we are interested in (PID,PPID,COMMAND)
    heading_indexes = pp.get_heading_indexes(column_header)

    # Next, using the indexes, extract the process data 
    process_info = pp.get_process_data( heading_indexes, processes )

    # We have all the essential information that we need. Time to build the process trees.
    process_trees = pp.build_process_trees( process_info )

    if args['output']:
        with open(args['output'], 'w') as f:
            sys.stdout = f

    pp.display_process_trees( process_info, process_trees )

if __name__ == '__main__':
    args = my_parse_args()
    main(args)
