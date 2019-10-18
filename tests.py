import unittest
import subprocess
import os
import re

class PstTestCase(unittest.TestCase):
    """This class represents the pst test case"""
    def test_installation_file_exists(self):
        self.assertEqual(os.path.exists("pst"),True)

    def test_version_string(self):
        output = subprocess.Popen(["pst", "-v"], 
                          stdout=subprocess.PIPE).communicate()[0]
        REGEX = re.compile('version')
        self.assertTrue(REGEX.search('version'))

if __name__ == "__main__":
    unittest.main()
