"""
Program for showing the hierarchy of processes on a Linux computer
"""

__author__ = "Mike Accardo"
__copyright__ = "Copyright 2019, Mike Accardo"
__license__ = "MIT"

#!/usr/bin/python

# imports
import processparser as pp 

ps_command = 'ps -e l'
column_header, processes  = pp.get_processes(ps_command)

# Find the index of the headings that we are interested in (PID,PPID,COMMAND)
heading_indexes = pp.get_indexes(column_header)

# Next, using the indexes, extract the process data 
process_info = pp.extract_process_data( heading_indexes, processes )

# We have all the essential information that we need. Time to build the process trees.
process_trees = pp.build_process_trees( process_info )
pp.display_process_trees( process_info, process_trees )
