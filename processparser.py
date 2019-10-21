"""
Process parser for currently-running processes
"""

__author__ = "Mike Accardo"
__copyright__ = "Copyright 2019, Mike Accardo"
__license__ = "MIT"

# imports
import sys
import re
import shlex
import subprocess


def get_ps_output(ps_command):
    """ Gets the output from the process status command.

    Args:
        ps_command: the ps command that displays the currently-running processes

    Returns:
        column_header: string of column headings above the processes
        processes: array of the currently-running processes
    """

    ps_command = shlex.split(ps_command)

    proc = subprocess.Popen(
        ps_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    output, error = proc.communicate()
    if error:
        errors = error.decode().split('\n')
        sys.exit(errors[0])

    lines = output.decode().split('\n')
    column_header = lines[0]
    processes = lines[1:]

    # Are there processes? We should never exit here.
    if not processes:
        sys.exit("There are no processes available")

    return column_header, processes


def get_heading_indexes(column_header):
    """ Gets the position (indexes) of the PID, PPID, and COMMAND|CMD headings in the column header.

        PID: Process ID number
        PPID: ID number of the process's parent process
        COMMAND: Name of the process, including arguments, if any

    Args:
        column_header: the column header from the ps command output

    Returns:
        indexes: dictionary with the indexes of the PID, PPID, and COMMAND|CMD headings in the column header
    """

    indexes = {}
    index = 0

    for heading in column_header.split():

        heading = heading.lower()
        if re.match("^pid$", heading):
            indexes['pid'] = index
        elif re.match("^ppid$", heading):
            indexes['ppid'] = index
        elif re.match("^(command|cmd)$", heading):
            indexes['command'] = index
        index += 1

    if len(indexes) != 3:
        print("Unable to find the required headings (PID PPID COMMAND|CMD) with the ps command")
        print("Column header: " + column_header)
        sys.exit()

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

        pid = process_values[indexes['pid']]
        ppid = process_values[indexes['ppid']]
        command = process_values[indexes['command']]

        process_data.append({'pid': pid, 'ppid': ppid, 'command': command})

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
    trees, seen_ppids = {}, {}

    for row in processes:

        pid = row['pid']
        ppid = row['ppid']
        command = row['command']

        seen_ppids[pid] = 1

        if ppid == 0 or ppid not in seen_ppids:
            trees[pid] = []
        else:
            # Describe the child and find its parent process (ppid)
            new_process = {'pid': pid, 'command': command}
            try:
                trees[ppid].append([new_process])
            except KeyError:
                for root in trees:
                    for node in trees[root]:
                        # node should be an array holding a dict
                        for counter, process in enumerate(node, start=1):
                            if ppid == process['pid']:
                             # Success. We found the parent of the child process
                             # Append child to parent to indicate relationship
                                node[counter:0] = [new_process]
    # End of for loop
    return trees


def format_line(pid, command, counter=None, pipeline=None):
    """Add the correct spacing and pipes to processes"""
    pid_length = len(pid)
    num = 5 - pid_length
    pid_padding = " " * num

    formatted_pid = pid_padding + pid

    formatted_command = "  {0}".format(command)

    if None not in (counter, pipeline):

        # 3 spaces is the min
        num = 3

        if counter > 1:
            num = (counter * 4) + 3

        command_padding = " " * num

        if pipeline:
            # add pipe
            command_padding = re.sub(r'^\s{4}', '   |', command_padding)

        formatted_command = r"{0}\_ {1}".format(command_padding, command)

    return formatted_pid + formatted_command + "\n"


def format_process_trees(processes, trees):
    """ Format the process trees """

    tree_text = format_line('PID', 'COMMAND')

    for row in processes:

        pid = row['pid']
        command = row['command']

        # Parent always comes before child
        if pid in trees:

            tree_text += format_line(pid, command)

            num_children = len(trees[pid])

            for child in trees[pid]:

                # child is an array that will contain one or more dicts
                # The dicts hold the process info (pid,command)
                # Each dict is a child of the one before it

                num_children -= 1
                for counter, process in enumerate(child):

                    # IF counter is one here (meaning that the array has more than one dict)
                    # AND there is another array (sibling of the parent process) behind us
                    # THEN we need to draw a pipe to indicate the relationship
                    # to the parent

                    pipe_line = 0
                    if counter >= 1 and num_children >= 1:
                        pipe_line = 1

                    stored_pid = process['pid']
                    stored_command = process['command']

                    tree_text += format_line(stored_pid,
                                             stored_command, counter, pipe_line)
    return tree_text
