import unittest
import subprocess
import os
import re
from distutils.spawn import find_executable


class PstTestCase(unittest.TestCase):
    """This class represents the pst test case"""

    def test_file_exists(self):
        self.assertTrue(find_executable("pst"))

    def test_file_access(self):
        self.assertEqual(os.access(find_executable("pst"), os.X_OK), True)

    def test_file_size(self):
        self.assertEqual(
            os.path.getsize(
                find_executable("pst")),
            os.path.getsize('bin/pst'))

    def test_help_string(self):
        proc = subprocess.Popen(["pst", "-h"], stdout=subprocess.PIPE)
        output = proc.stdout.read()
        REGEX = re.compile('usage')
        self.assertTrue(REGEX.search(output))


if __name__ == "__main__":
    unittest.main()
