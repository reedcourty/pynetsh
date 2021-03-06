#!python
# -*- coding: UTF-8 -*-

import logging
import subprocess
import sys

logger = logging.getLogger(__name__)

def decode_console(out_raw):
    try:
        out_decoded = out_raw.decode(sys.stdout.encoding)
    except UnicodeDecodeError:
        out_decoded = out_raw.decode('iso-8859-2')
    return out_decoded
    

class NetshParser:
    def __init__(self):
        pass

    @staticmethod
    def parse_wlan_show_networks(netsh_output, mode):
        list_of_raw_networks = []
        raw_network = []
        for line in netsh_output[4:]:
            if (line == ''):
                list_of_raw_networks.append(raw_network)
                raw_network = []
            else:
                raw_network.append(line)

        list_of_raw_networks = list_of_raw_networks[0:-1]

        networks = []

        for i in list_of_raw_networks:
            network_name = i[0].split(" : ")[1]
            network_type = i[1].split(": ")[1]
            authentication = i[2].split(": ")[1]
            encryption_method = i[3].split(": ")[1].replace(" ", "")
            signal_strenght = int(i[5].split(": ")[1].replace(" ", "").replace("%", ""))
            radio_type = i[6].split(": ")[1].replace(" ", "")
            channel = int(i[7].split(": ")[1].replace(" ", ""))
            basic_rates = [float(x) for x in i[8].split(": ")[1].split(" ")]
            other_rates = [float(x) for x in i[9].split(": ")[1].split(" ")]
            if (mode=="bssid"):
                try:
                    network_ssid = i[4].split(": ")[1].replace(" ", "")
                except IndexError:
                    network_ssid = None
            else:
                network_ssid = None
            networks.append(Network(
                network_name,
                network_ssid,
                network_type=network_type,
                authentication=authentication,
                encryption_method=encryption_method,
                signal_strenght=signal_strenght,
                radio_type=radio_type,
                channel=channel,
                basic_rates=basic_rates,
                other_rates=other_rates))

        return networks


    @staticmethod
    def parse_wlan_show_profiles(netsh_output):

        profiles = []
        section_id = 0

        content = [[],[],[]]

        for line in netsh_output:
            if "--" in line:
                section_id = section_id + 1
            else:
                content[section_id].append(line)

        # TODO: add group policy support!
        
        # Parse Current User Profiles:
        for line in content[2]:
            if (line!=''):
                p = Profile(name=line.split(": ")[1].strip(), profile_type="Current User Profile")
                profiles.append(p)

        return profiles


    @staticmethod
    def parse_wlan_show_profiles_name(netsh_output):

        section_id = 0

        content = [[],[],[],[]]

        for line in netsh_output:
            if "--" in line:
                section_id = section_id + 1
            else:
                content[section_id].append(line)

        name = content[1][2].split(": ")[1]
        p = Profile(name)

        return [p]





class Network:
    def __init__(self, name, bssid_number=None, network_type = None, authentication=None, encryption_method = None,
        signal_strenght=None, radio_type=None, channel=None, basic_rates=None, other_rates=None):
        self.name = name
        self.bssid_number = bssid_number
        self.network_type = network_type
        self.authentication = authentication
        self.encryption_method = encryption_method
        self.signal_strenght = signal_strenght
        self.radio_type = radio_type
        self.channel = channel
        self.basic_rates = basic_rates
        self.other_rates = other_rates


    def show_infos(self):
        attrs = vars(self)
        
        for a in attrs.items():
            print(a)
        

    def __repr__(self):
        return "{}({})".format(self.name, self.bssid_number)


class Profile:
    def __init__(self, name, profile_type=None, authentication=None):
        self.name = name
        self.profile_type = profile_type
        self.authentication = authentication

    def show_infos(self):
        attrs = vars(self)
        
        for a in attrs.items():
            print(a)

    def __repr__(self):
        return "{}".format(self.name)


class NetshWLAN:
    def __init__(self):
        self.networks = []
        self.profiles = []

    def get_networks(self, interface=None, mode=None, show=False, signal_limit=0):
        logger.debug("interface={}, mode={}, show={}, signal_limit={}".format(interface, mode, show, signal_limit))
        if (mode not in ["bssid", "ssid", None]):
            raise Exception("Wrong mode parameter is specified.")
        cmd = "netsh wlan show networks"
        if interface is not None:
            cmd = "{} interface={}".format(cmd, interface)
        if mode is not None:
            cmd = "{} mode={}".format(cmd, mode)
        logger.debug(cmd)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out_raw, _ = p.communicate()

        if show:
            return out_raw

        out_decoded = decode_console(out_raw)
        out = out_decoded.split('\r\n')
        if (len(out)==2):
            raise Exception("The command ({}) failed :(".format(cmd))

        #number_of_networks = [int(s) for s in out[2].split() if s.isdigit()][0]

        networks = NetshParser.parse_wlan_show_networks(out, mode)

        self.networks = []
        for n in networks:
            if (n.signal_strenght >= signal_limit):
                logger.debug(n)
                self.networks.append(n)

        return self.networks

    def show_networks(self, interface=None, mode=None):
        print(self.get_networks(interface, mode, show=True))

    def get_profiles(self, name=None, interface=None, key=None, show=False):
        """
        Szintaxis: show profiles [[name=]<karakterlánc>] [[interface=]<karakterlánc>]
           [key=<karakterlánc>]
        """

        if name is not None:
            cmd = 'netsh wlan show profiles name="{}" key=clear'.format(name)
            logger.debug(cmd)
        else:
            cmd = "netsh wlan show profiles"
            logger.debug(cmd)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out_raw, err_raw = p.communicate()

        if show:
            return out_raw
        
        out_decoded = decode_console(out_raw)
        out = out_decoded.split('\r\n')
        
        if name is not None:
            profiles = NetshParser.parse_wlan_show_profiles_name(out)
        else:
            profiles = NetshParser.parse_wlan_show_profiles(out)

        self.profiles = []
        for p in profiles:
            self.profiles.append(p)

        return self.profiles

    def show_profiles(self, name=None, interface=None, key=None):
        print(self.get_profiles(name, interface, key, show=True))
        
        


