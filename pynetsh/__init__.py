#!python
# -*- coding: UTF-8 -*-

import subprocess
import sys

class Network:
    def __init__(self, name, bssid_number=None, network_type = None):
        self.name = name
        self.bssid_number = bssid_number
        self.network_type = network_type

    def show_infos(self):
        attrs = vars(self)
        
        for a in attrs.items():
            print(a)
        

    def __repr__(self):
        return "{}({})".format(self.name, self.bssid_number)

class NetshWLAN:
    def __init__(self):
        self.networks = []

    def get_networks(self, interface=None, mode=None, show=False):
        if (mode not in ["bssid", "ssid", None]):
            raise Exception("Wrong mode parameter is specified.")
        cmd = "netsh wlan show networks"
        if interface is not None:
            cmd = "{} interface={}".format(cmd, interface)
        if mode is not None:
            cmd = "{} mode={}".format(cmd, mode)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out_raw, err_raw = p.communicate()

        out_decoded = out_raw.decode(sys.stdout.encoding)
        out = out_decoded.split('\r\n')
        if (len(out)==2):
            raise Exception("The command ({}) failed :(".format(cmd))

        number_of_networks = [int(s) for s in out[2].split() if s.isdigit()][0]

        list_of_raw_networks = []
        raw_network = []
        for line in out[4:]:
            if (line == ''):
                list_of_raw_networks.append(raw_network)
                raw_network = []
            else:
                raw_network.append(line)

        list_of_raw_networks = list_of_raw_networks[0:-1]
        
        #print(number_of_networks)
        

        for i in list_of_raw_networks:
            network_name = i[0].split(" : ")[1]
            network_type = i[1].split(": ")[1]
            if (mode=="bssid"):
                network_ssid = i[4].split(": ")[1].replace(" ", "")
            else:
                network_ssid = None
            self.networks.append(Network(network_name, network_ssid, network_type=network_type))




        if show:
            return out_raw


        
        
        #for i in xrange(4, len(out), )

        return self.networks

    def show_networks(self, interface=None, mode=None):
        print(self.get_networks(interface, mode, show=True))
