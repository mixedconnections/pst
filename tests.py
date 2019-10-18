import unittest
import os

class PstTestCase(unittest.TestCase):
    """This class represents the pst test case"""
    def test_installation_file_exist(self):
        self.assertEqual(os.path.exists("pst"),True)

if __name__ == "__main__":
    unittest.main()
