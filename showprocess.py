#!/usr/bin/env python
# showprocess.py
#
# Program for showing the hierarchy of processes on a Linux computer
# Usage: python <program name>
############################
import sys,re,shlex,subprocess,pprint

############### sub declarations come here ######################

def get_processes(sys_command):

    sys_command = shlex.split(sys_command)

    try:
        output = subprocess.check_output(sys_command)
    except subprocess.CalledProcessError as e:
        sys.exit("Unexpected error: " + e.output)

    lines = output.decode().split('\n')

    return lines[0], lines[1:]

def get_indexes(headers):

    indexes = {}
    index = 0

    for header in headers:
               
        header = header.lower()
        if re.match("^pid$",header):
            indexes['pid'] = index
        elif re.match("^ppid$", header):
            indexes['ppid'] = index
        elif re.match("^command$", header):
            indexes['command'] = index
        index += 1

    return indexes
    
def extract_row_data(row_indexes, processes):

    process_info = []

    for row in processes:
        row = row.rstrip()
        row_values = row.split()
        if len(row_values) <= 2:
            continue

        pid     = row_values[ row_indexes['pid'] ];
        ppid    = row_values[ row_indexes['ppid'] ];
        command = row_values[ row_indexes['command'] ];

        process_info.append({ 'pid':pid,'ppid':ppid,'command':command})

    return process_info

def build_process_trees(processes):

# %trees is a hash ( key => value )
# keys are the ids of processes that "may" have children
# values are array references which hold the children (and children of children)
#
# Empty array references indicate that the process has no children
#
# Children processes are a hash reference
# [ { 'pid' => $pid, 'command' => $command } ]
#
# These structures are pushed to the values (array refs)
# So values can be array refs of array refs of hash refs
#
# The multi-levelness is needed to indicate parentage
# Children of child processes have their hash ref appended to the hash ref of their nearest parent

    trees, seen_ppids = {},{}

    for row in processes:

        pid = row['pid']
        ppid = row['ppid']
        command = row['command']

        seen_ppids[pid] = 1

        if ppid == 0:
            trees[pid] = []
        elif ppid in seen_ppids:
            new_process = {'pid':pid,'command':command}
            if ppid in trees:
                trees[ppid].append([new_process])
            else:
                for root in trees:
                    for node in trees[root]:
                        # node should be an array holding a dict
                        counter = 0
                        for process in node:
                            counter += 1
                            process_pid = process['pid']
                            if ppid == process_pid:
                             # https://stackoverflow.com/questions/509211/understanding-slice-notation
                             # Success. We found the parent of the child process
                             # Append child to parent to indicate relatioship
                                node[counter:0] = [new_process]                        
        else: 
            # Most likely a zombie
            trees[pid] = []
    # End of for loop
    return trees

def format_line(pid,command,counter=None,pipeline=None):

    pid_length  = len(pid)
    num         = 5 - pid_length
    pid_padding = " " * num

    formatted_pid = pid_padding + pid

    formatted_command = "  {0}".format(command)

    if None not in (counter,pipeline):

        # 3 spaces is the min
        num = 3;

        if counter > 1: 
            num = ( counter * 4 ) + 3

        command_padding = " " * num

        if pipeline:
            # add pipe
            command_padding = re.sub(r'^\s{4}','   |',command_padding)

        formatted_command = "{0}\_ {1}".format(command_padding, command)
    

    return formatted_pid + formatted_command

def print_process_trees(processes, trees):

    # Print the header
    print(format_line( 'PID', 'COMMAND' ))

    for row in processes:

        pid     = row['pid']
        ppid    = row['ppid']
        command = row['command']

        # Parent always comes before child
        if pid in trees:

            print(format_line( pid, command ))

            num_children = len(trees[pid]) 

            for child in trees[pid]:

                # child is an array ref that will contain one or more hash refs
                # The hash refs hold the process info (pid,command)
                # Each hash ref is a child of the one before it

                counter = 0
                num_children-=1
                for process in child:

# IF counter is one here (meaning that the array ref has more than one hash ref)
# AND there is another array ref (sibling of the parent process) behind us
# THEN we need to draw a pipe to indicate the relationship to the parent

                    pipe_line = 0
                    if counter >= 1 and num_children >= 1:
                        pipe_line = 1

                    stored_pid     = process['pid']
                    stored_command = process['command']

                    print(format_line( stored_pid, stored_command, counter,
                        pipe_line ))

                    counter+=1

##########################################################
sys_command = 'ps -e l';

column_header, process_rows  = get_processes(sys_command)

# Are there processes? We should never die here.
if not process_rows:
    sys.exit("There are no processes available")

# Find the index of the processes that we are interested in (PID,PPID,COMMAND)
all_headers = column_header.split()
row_indexes = get_indexes(all_headers)

if len(row_indexes) != 3:
    sys.exit("Unable to find the right headers (PID PPID COMMAND) with process command")

# Next, using the indexes, extract the row data for each process
process_info = extract_row_data( row_indexes, process_rows )

# We have all the essential information that we need. Time to build the process trees.
#################################################################

process_tree = build_process_trees( process_info )

print_process_trees( process_info, process_tree )

sys.exit()
