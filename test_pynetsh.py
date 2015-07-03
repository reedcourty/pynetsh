#!python
# -*- coding: UTF-8 -*-

import unittest

import pynetsh

class NetshWLANTestCase(unittest.TestCase):

    @unittest.skip(None)
    def test_show_networks(self):
        # Arrange
        netshwlan = pynetsh.NetshWLAN()
        netshwlan.show_networks(mode="bssid")

        # Act
        
        expected = True
        actual = True
        
        # Assert
        self.assertEqual(expected, actual, msg='Expected "{}", but get "{}"'.format(expected, actual))

    #@unittest.skip(None)
    def test_get_networks(self):
        # Arrange
        netshwlan = pynetsh.NetshWLAN()
        print(netshwlan.get_networks(mode="bssid"))
        # Act
        
        expected = True
        actual = True
        
        # Assert
        self.assertEqual(expected, actual, msg='Expected "{}", but get "{}"'.format(expected, actual))

if __name__ == '__main__':
    unittest.main()
