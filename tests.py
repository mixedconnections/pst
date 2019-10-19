import unittest
import subprocess
import os
import re

class PstTestCase(unittest.TestCase):
    """This class represents the pst test case"""
    def test_installation_file_exists(self):
        self.assertEqual(os.path.exists("pst"),True)

    def test_help_string(self):
        proc = subprocess.Popen(["pst","-h"], stdout=subprocess.PIPE)
        output = proc.stdout.read()
        REGEX = re.compile('usage')
        self.assertTrue(REGEX.search(output))

if __name__ == "__main__":
    unittest.main()
