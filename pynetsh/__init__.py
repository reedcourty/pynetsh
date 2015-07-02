#!python
# -*- coding: UTF-8 -*-

import subprocess
import sys

class NetshWLAN:
    def __init__(self):
        pass

    def get_networks(self, interface=None, mode=None):
        cmd = "netsh wlan show networks"
        if interface is not None:
            cmd = "{} interface={}".format(cmd, interface)
        if mode is not None:
            cmd = "{} mode={}".format(cmd, mode)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out_raw, err_raw = p.communicate()
        out_decoded = out_raw.decode(sys.stdout.encoding)
        out = out_decoded.split('\r\n')
        return out

    def show_networks(self, interface=None, mode=None):
        cmd = "netsh wlan show networks"
        if interface is not None:
            cmd = "{} interface={}".format(cmd, interface)
        if mode is not None:
            cmd = "{} mode={}".format(cmd, mode)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out_raw, err_raw = p.communicate()
        out_decoded = out_raw.decode(sys.stdout.encoding)
        out = out_decoded.split('\r\n')
        print(out_decoded)
