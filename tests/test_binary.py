import unittest
import re
import os
import sys
from subprocess import Popen, PIPE
from distutils.spawn import find_executable
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from pst import __version__

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

    def test_help_string(self):
        proc = Popen(["pst", "-h"], stdout=PIPE, stderr=PIPE)
        output, error = proc.communicate()
        if error:
            self.fail("Failed with %s" % error)
        REGEX = re.compile('usage')
        self.assertTrue(REGEX.search(output.decode('utf-8')))

    def test_user_and_output_file(self):
        proc = Popen(["pst", "-u", "root", "-o", "trees-root.txt"], stdout=PIPE, stderr=PIPE)
        output, error = proc.communicate()
        if error:
            self.fail("Failed with %s" % error)
        self.assertTrue(os.path.isfile("trees-root.txt"))
        self.assertTrue(os.path.getsize("trees-root.txt") > 0)

    def test_file_sizes_comparison(self):
        proc = Popen(["pst", "-p", "1", "-o", "trees-pid.txt"], stdout=PIPE, stderr=PIPE)
        output, error = proc.communicate()
        if error:
            self.fail("Failed with %s" % error)
        proc = Popen(["pst", "-o", "trees-pst.txt"], stdout=PIPE, stderr=PIPE)
        output, error = proc.communicate()
        if error:
            self.fail("Failed with %s" % error)
        self.assertTrue(os.path.getsize('trees-pst.txt') > os.path.getsize('trees-pid.txt'))

    def test_version_comparison(self):
        proc = Popen(["pst", "-v"], stdout=PIPE, stderr=PIPE)
        version_bin = proc.communicate()[1]
        self.assertEqual(version_bin.rstrip(),str(__version__))

if __name__ == "__main__":
    unittest.main(failfast=True)
