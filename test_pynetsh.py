#!python
# -*- coding: UTF-8 -*-

import unittest

import pynetsh

class NetshWLANTestCase(unittest.TestCase):

    def test_show_networks(self):
        # Arrange
        netshwlan = pynetsh.NetshWLAN()
        
        # Act
        
        expected = True
        actual = netshwlan.show_networks(mode="gssid")
        
        # Assert
        self.assertEqual(expected, actual, msg='Expected "{}", but get "{}"'.format(expected, actual))

if __name__ == '__main__':
    unittest.main()