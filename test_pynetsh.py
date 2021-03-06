#!python
# -*- coding: UTF-8 -*-

import unittest

import pynetsh

class NetshWLANTestCase(unittest.TestCase):

    #@unittest.skip(None)
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
        for network in netshwlan.get_networks(mode="bssid"):
            network.show_infos()
        # Act
        
        expected = True
        actual = True
        
        # Assert
        self.assertEqual(expected, actual, msg='Expected "{}", but get "{}"'.format(expected, actual))

    #@unittest.skip(None)
    def test_show_profiles(self):
        # Arrange
        netshwlan = pynetsh.NetshWLAN()
        netshwlan.show_profiles()

        # Act
        expected = True
        actual = True

        # Assert
        self.assertEqual(expected, actual, msg='Expected "{}", but get "{}"'.format(expected, actual))

    #@unittest.skip(None)
    def test_get_profiles(self):
        # Arrange
        netshwlan = pynetsh.NetshWLAN()
        for profile in netshwlan.get_profiles():
            profile.show_infos()

        # Act
        expected = True
        actual = True

        # Assert
        self.assertEqual(expected, actual, msg='Expected "{}", but get "{}"'.format(expected, actual))

    #@unittest.skip(None)
    def test_show_profiles_name(self):
        # Arrange
        netshwlan = pynetsh.NetshWLAN()
        netshwlan.show_profiles(name="quanopt")

        # Act
        expected = True
        actual = True

        # Assert
        self.assertEqual(expected, actual, msg='Expected "{}", but get "{}"'.format(expected, actual))

    #@unittest.skip(None)
    def test_get_profiles_name(self):
        # Arrange
        netshwlan = pynetsh.NetshWLAN()
        for profile in netshwlan.get_profiles(name="quanopt"):
            profile.show_infos()

        # Act
        expected = True
        actual = True

        # Assert
        self.assertEqual(expected, actual, msg='Expected "{}", but get "{}"'.format(expected, actual))

if __name__ == '__main__':
    unittest.main()
