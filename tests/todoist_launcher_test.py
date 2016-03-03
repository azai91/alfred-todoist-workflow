"""
Unit tests of todoist_launcher
"""

import unittest
import sys

from src.todoist_launcher import main
import todoist_api
import todoist_api as todoist_api_back

class TestTodoistAPI(unittest.TestCase):

    def test_validate_login(self):
        sys.argv = ['todoist_launcher.py','']
        # main(None)
        # self.assert

    def test_validate_logout(self):
        sys.argv = ['todoist_launcher.py','']
        main(None)

        # self.assert

    def setUp

if __name__ == '__main__':
    unittest.main()