"""
Process parser for currently-running processes
"""

__author__ = "Mike Accardo"
__copyright__ = "Copyright 2019, Mike Accardo"
__license__ = "MIT"

# imports
import sys,re,shlex,subprocess

def get_ps_output(ps_command):
    """ Gets the output from the process status command.

    Args:
        ps_command: the ps command that displays the currently-running processes

    Returns:
        column_header: string of column headings above the processes 
        processes: array of the currently-running processes
    """

    ps_command = shlex.split(ps_command)

    try:
        output = subprocess.check_output(ps_command)
    except subprocess.CalledProcessError as e:
        sys.exit("Unexpected error: " + e.output)

    lines = output.decode().split('\n')
    column_header = lines[0]
    processes = lines[1:]

    # Are there processes? We should never exit here.
    if not processes:
        sys.exit("There are no processes available")

    return column_header, processes

def get_heading_indexes(column_header):
    """ Gets the position (indexes) of the PID, PPID, and COMMAND headings in the column header.

        PID: Process ID number
        PPID: ID number of the process's parent process
        COMMAND: Name of the process, including arguments, if any

    Args:
        column_header: the column header from the ps command output

    Returns:
        indexes: dictionary with the indexes of the PID, PPID, and COMMAND headings in the column header
    """

    indexes = {}
    index = 0

    for heading in column_header.split():
               
        heading = heading.lower()
        if re.match("^pid$",heading):
            indexes['pid'] = index
        elif re.match("^ppid$", heading):
            indexes['ppid'] = index
        elif re.match("^command$", heading):
            indexes['command'] = index
        index += 1

    if len(indexes) != 3:
        sys.exit("Unable to find the right headings (PID PPID COMMAND) with the ps command")

    return indexes
    
def get_process_data(indexes, processes):
    """Extract and label the process data from the ps command output.

    Args:
        indexes: dictionary with the indexes of the PID, PPID, and COMMAND headings in the column header
        processes: array of the currently-running processes
    
    Returns:
        process_data: array of dictionarys where each dict has the process data for the PID, PPID, and COMMAND headings

    """

    process_data = []

    for process in processes:
        process = process.rstrip()
        process_values = process.split()
        if len(process_values) <= 2:
            continue

        pid     = process_values[ indexes['pid'] ]
        ppid    = process_values[ indexes['ppid'] ]
        command = process_values[ indexes['command'] ]

        process_data.append({ 'pid':pid,'ppid':ppid,'command':command})

    return process_data

def build_process_trees(processes):
    """ 
    Build a nested dictionary, based on the relationships between processes.

    Args:
        processes: array of the currently-running processes

    Returns:
        trees: a multi-level dictionary. 

    The keys are the ids of processes that "may" have children
    Values are arrays which hold the children (and children of children)

    Empty arrays indicate that the process has no children
    """
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
                             # Success. We found the parent of the child process
                             # Append child to parent to indicate relatioship
                                node[counter:0] = [new_process]                        
        else: 
            # Most likely a zombie process
            trees[pid] = []
    # End of for loop
    return trees

def format_line(pid,command,counter=None,pipeline=None):
    """Add the correct spacing and pipes to processes"""
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
    
    return formatted_pid + formatted_command + "\n" 


def format_process_trees(processes, trees):
    """ Format the process trees """
    
    tree_text = format_line( 'PID', 'COMMAND' )

    for row in processes:

        pid     = row['pid']
        ppid    = row['ppid']
        command = row['command']

        # Parent always comes before child
        if pid in trees:

            tree_text += format_line( pid, command )

            num_children = len(trees[pid]) 

            for child in trees[pid]:

                # child is an array that will contain one or more dicts
                # The dicts hold the process info (pid,command)
                # Each dict is a child of the one before it

                counter = 0
                num_children-=1
                for process in child:

                # IF counter is one here (meaning that the array has more than one dict)
                # AND there is another array (sibling of the parent process) behind us
                # THEN we need to draw a pipe to indicate the relationship to the parent

                    pipe_line = 0
                    if counter >= 1 and num_children >= 1:
                        pipe_line = 1

                    stored_pid     = process['pid']
                    stored_command = process['command']

                    tree_text += format_line( stored_pid, stored_command, counter,
                        pipe_line )

                    counter+=1
    return tree_text
