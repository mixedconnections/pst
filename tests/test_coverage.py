import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..')) 
import processparser as pp


class PstTestCase(unittest.TestCase):
    """This class represents the pst test case"""

    def test_ps_output(self):
	ps_command = 'ps -e l'
	column_header, processes = pp.get_ps_output(ps_command)
	heading_indexes = pp.get_heading_indexes(column_header)
	process_info = pp.get_process_data(heading_indexes, processes)
	process_trees = pp.build_process_trees(process_info)
	tree_output = pp.format_process_trees(process_info, process_trees)
	self.assertTrue(len(tree_output) > 0)

if __name__ == "__main__":
    unittest.main(failfast=True)
