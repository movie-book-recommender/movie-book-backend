"""
This module implements unit and integration tests for 
routes related to application usage.
"""

import unittest
import main.extentions as extentions

class TestExtentions(unittest.TestCase):
    def setUp(self):
        print("Set up goes here")

    def test_hello_world(self):
        self.assertEqual("Hello world", "Hello world")

if __name__ == '__main__':
    unittest.main()
