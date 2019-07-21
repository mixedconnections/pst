#!/usr/bin/env python
# showprocess.py
#
# Program for showing the hierarchy of processes on a Linux computer
# Usage: python <program name>
############################
import trees as tr 

sys_command = 'ps -e l';

column_header, process_rows  = tr.get_processes(sys_command)

# Find the index of the processes that we are interested in (PID,PPID,COMMAND)
all_headers = column_header.split()
row_indexes = tr.get_indexes(all_headers)

# Next, using the indexes, extract the row data for each process
process_info = tr.extract_row_data( row_indexes, process_rows )

# We have all the essential information that we need. Time to build the process trees.
#################################################################

process_tree = tr.build_process_trees( process_info )

tr.print_process_trees( process_info, process_tree )
