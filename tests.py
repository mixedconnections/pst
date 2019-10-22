import unittest
import os
import re
from subprocess import Popen, PIPE
from distutils.spawn import find_executable


class PstTestCase(unittest.TestCase):
    """This class represents the pst test case"""
    
    @classmethod
    def tearDownClass(cls):
        filePath = "trees.txt"
        try:
            os.remove(filePath)
        except BaseException:
            print("Error while deleting file ", filePath)

    def test_file_exists(self):
        self.assertTrue(find_executable("pst"))

    def test_file_access(self):
        self.assertEqual(os.access(find_executable("pst"), os.X_OK), True)

    def test_compare_file_size(self):
        self.assertEqual( os.path.getsize( find_executable("pst")), os.path.getsize('bin/pst'))

    def test_help_string(self):
        proc = Popen(["pst", "-h"], stdout=PIPE, stderr=PIPE)
        output, error = proc.communicate()
        if error:
            self.fail("Failed with %s" % error)
        REGEX = re.compile('usage')
        self.assertTrue(REGEX.search(output))

    def test_user_and_output_file(self):
        proc = Popen(["pst", "-u", "root", "-o", "trees.txt"], stdout=PIPE, stderr=PIPE)
        output, error = proc.communicate()
        if error:
            self.fail("Failed with %s" % error)
        self.assertTrue(os.path.isfile("trees.txt"))
        self.assertTrue(os.path.getsize("trees.txt") > 0)
    

if __name__ == "__main__":
    unittest.main()
