import unittest
import filecmp
import os
import re
from subprocess import Popen, PIPE

class PstTestCase(unittest.TestCase):
    """This class represents the pst test case"""

    @classmethod
    def tearDownClass(cls):
        files = ["trees-root.txt", "trees-pid.txt", "trees-pst.txt"]
        for f in files:
	    if os.path.isfile(f):
                try:
                    os.remove(f)
                except BaseException:
                    print("Error while deleting file ", f)

    def test_file_exists(self):
        self.assertTrue(os.path.isfile("../pst.py"))

    def test_file_access(self):
        self.assertEqual(os.access("../pst.py", os.X_OK), True)

    def test_help_string(self):
        proc = Popen(["../pst.py", "-h"], stdout=PIPE, stderr=PIPE)
        output, error = proc.communicate()
        if error:
            self.fail("Failed with %s" % error)
        REGEX = re.compile('usage')
        self.assertTrue(REGEX.search(output.decode('utf-8')))

    def test_user_and_output_file(self):
        proc = Popen(["../pst.py", "-u", "root", "-o", "trees-root.txt"], stdout=PIPE, stderr=PIPE)
        output, error = proc.communicate()
        if error:
            self.fail("Failed with %s" % error)
        self.assertTrue(os.path.isfile("trees-root.txt"))
        self.assertTrue(os.path.getsize("trees-root.txt") > 0)
    
    def test_compare_output_file_sizes(self):
        proc = Popen(["../pst.py", "-p", "1", "-o", "trees-pid.txt"], stdout=PIPE, stderr=PIPE)
        output, error = proc.communicate()
        if error:
            self.fail("Failed with %s" % error)
        proc = Popen(["../pst.py", "-o", "trees-pst.txt"], stdout=PIPE, stderr=PIPE)
        output, error = proc.communicate()
        if error:
            self.fail("Failed with %s" % error)
        self.assertTrue(os.path.getsize('trees-pst.txt') > os.path.getsize('trees-pid.txt')) 

if __name__ == "__main__":
    unittest.main(failfast=True)
