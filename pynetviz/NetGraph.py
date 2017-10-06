'''
Created on Jun 13, 2016

@author: kiel
'''
from pynetviz.NetObjects import *
import pynetviz
from ipaddress import IPv4Address, IPv4Network



class NetGraph(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        # IP objects
        self.ips = []
        # Strings
        self.hostnames = []
        self.interfaces = []
        self.netDevices = []
        # Subnet objects
        self.ipsubnet = []
        # VLAN objects
        self.vlans = []
        self.links = []
    
    #
    # Takes care of adding interfaces and making connections
    #
    def addHost(self, h):
        self.netDevices.append(h)
        for i in h.interfaces:
            if len(i.addresses) > 0:
                self.setLink(h, i)
                self.interfaces.append(i)
                for addr in i.addresses:
                    self.setLink(i, addr)
        for r in h.routes:
            self.setLink(r["gw"], r["net"])
        
    def  getHostname(self, hostname):
        for h in self.hostnames:
            if hostname in h.hostname:
                return h
        h = Hostname()
        self.hostnames.append(h)
        return h
        
    def  getVLAN(self, vlan):
        for v in self.vlans:
            if v.tag == vlan:
                return v
        v = Vlan()
        v.tag = vlan
        self.vlans.append(v)
        return v
    
        # Pass a IPv4Network object
    def  getSubnet(self, snet):
        if not isinstance(snet, IPv4Network):
            raise TypeError
        if str(snet) != "0.0.0.0/0":
            for s in self.ipsubnet:
                if s.network.compare_networks(snet) == 0:
                    return s
        subnet = Subnet(snet)
        self.ipsubnet.append(subnet)
        return subnet
    
    # Pass a string ipaddr
    def  getIP(self, ipaddr):
        if not isinstance(ipaddr, str):
            raise TypeError
        #print(str(ipaddr))
        if str(ipaddr != "0.0.0.0"):
            for ip in self.ips:
                if ipaddr == str(ip.address):
                    #print ("returning ip")
                    return ip

        ip = IP(IPv4Address(ipaddr))
        self.ips.append(ip)
        return ip
    
    # Pass an IPv4Interface object
    def  getIPInterface(self, ipinf):
        if not isinstance(ipinf, IPv4Interface):
            raise TypeError
#        return self.getIP(ipinf.ip)
        ipaddr = ipinf.ip
        for ip in self.ips:
            if str(ipaddr) == str(ip.address):
                return ip
        ip = self.getIP(str(ipinf.ip))
        self.getSubnet(ipinf.network)
        return ip
    
    def __str__(self, *args, **kwargs):
        return "NETGRAPH:\n  " + str(self.ips) +"\n  " + str(self.netDevices)  +"\n  "+ str(self.vlans)+"\n  "+ str(self.ipsubnet)
    
    def setIPLinks(self):
        for i in self.ips:
            for s in self.ipsubnet:
                if i in s and str(s) != "0.0.0.0/0":
                    if i.subnet == 0 or i.subnet.num_addresses > s.num_addresses:
                        i.subnet = s
                        self.setLink(i, s)
    
    def setLink(self, n1, n2):
        if not isinstance(n1, NetworkObj):
            raise TypeError
        if not isinstance(n2, NetworkObj):
            raise TypeError
        lnk = {}
        lnk["from"] = n1.id
        lnk["to"] = n2.id
        self.links.append(lnk)
        
               
    def toVis_JS(self):
        self.setIPLinks()
        retVal = {}
        nodes = []
        nodes = self.ips
        nodes += self.ipsubnet
        nodes += self.interfaces
        nodes += self.netDevices
        retVal["nodes"] = str(nodes)
        retVal["edges"] = str(self.links)
        return str(nodes)
        #return retVal
                  
