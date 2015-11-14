"""
Unit tests of todoist_settings
"""

import unittest
import sys

from todoist_settings import validate_coordinates, main, wf

class TestTodoistSettings(unittest.TestCase):

    def test_validate_coordinates(self):
        self.assertTrue(validate_coordinates('12'))
        self.assertTrue(validate_coordinates('12;'))
        self.assertTrue(validate_coordinates('12.3;1234.4'))
        self.assertFalse(validate_coordinates('a'))
        self.assertFalse(validate_coordinates('1a'))
        self.assertFalse(validate_coordinates('1;a'))

    def test_options(self):
        sys.argv = ['todoist_settings.py','']
        main(None)
        self.assertEqual(len(wf._items), 4)
        self.assertEqual(wf._items[0].title, 'Add Account')
        self.assertEqual(wf._items[1].title, 'Remove Account')
        self.assertEqual(wf._items[2].title, 'Set Home Location [long,lat]')
        self.assertEqual(wf._items[3].title, 'Set Work Location [long,lat]')
        wf._items = []


        sys.argv = ['todoist_settings.py','a']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, 'Add Account')
        wf._items = []

        sys.argv = ['todoist_settings.py','A']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, 'Add Account')
        wf._items = []

        sys.argv = ['todoist_settings.py','r']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, 'Remove Account')
        wf._items = []

        sys.argv = ['todoist_settings.py','s']
        main(None)
        self.assertEqual(len(wf._items), 2)
        self.assertEqual(wf._items[0].title, 'Set Home Location [long,lat]')
        self.assertEqual(wf._items[1].title, 'Set Work Location [long,lat]')
        wf._items = []

    def test_invalid_options(self):
        sys.argv = ['todoist_settings.py','not here']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, 'Invalid Option')
        self.assertFalse(wf._items[0].valid)
        self.assertFalse(wf._items[0].arg)
        wf._items = []

    def test_add_account(self):
        sys.argv = ['todoist_settings.py','add']
        main(None)
        self.assertEqual(len(wf._items), 1)
        self.assertEqual(wf._items[0].title, 'Add Account')
        self.assertTrue(wf._items[0].valid)
        self.assertTrue(wf._items[0].arg)
        wf._items = []

if __name__ == '__main__':
    unittest.main()