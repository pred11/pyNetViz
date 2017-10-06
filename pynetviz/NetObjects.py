'''
Created on Dec 16, 2014

@author: kiel
'''

#import ipaddress
from ipaddress import IPv4Interface, IPv4Network

class NetworkObj(object):
    '''
    classdocs
    '''
    numObjs = 0

    def __init__(self):
        '''
        Constructor
        '''
        self.id = NetworkObj.numObjs
        NetworkObj.numObjs += 1
        
'''
class Firewall(NetworkObj):

    def __init__(self):
        super().__init__()
        self.type = 'firewall'
'''        
        
class Firewall(NetworkObj):

    def __init__(self):
        NetworkObj.__init__(self)
        self.type = 'firewall'
        
class Switch(NetworkObj):

    def __init__(self):
        NetworkObj.__init__(self)
        self.type = 'switch'
        
class Host(NetworkObj):

    def __init__(self):
        NetworkObj.__init__(self)
        self.type = 'host'
        self.ips = []
        self.hostname = []
        self.interfaces = []
        self.domainname = ""
        self.filename = ""
        self.routes = []
        
    def __repr__(self):
        retVal = {}
        retVal["id"] = self.id
        retVal["group"] = self.type
#        retVal["ips"] = self.ips
        retVal["hostname"] = self.hostname
        retVal["group"] = self.type
#        retVal["interfaces"] = self.interfaces
        retVal["domainname"] = self.domainname
        retVal["label"] = self.filename
#        retVal["routes"] = self.routes
        return str(retVal)
    
    def getInterfaceByName(self, inf):
        for i in self.interfaces:
            if i.name == inf:
                return i
        return 0
        
    def __str__(self):
        return "HOST(" + self.type + "): " + str(self.ips) + str(self.hostname)
      
class Interface(NetworkObj):
    
    def __init__(self):
        NetworkObj.__init__(self)
        self.type = 'interface'
        self.addresses = []
        self.name = ""
        self.hwname = ""
        
    def __repr__(self):
        retVal = {}
        retVal["id"] = self.id
        retVal["group"] = self.type
        retVal["label"] = self.name + "\n" + self.hwname
        return str(retVal)
        
class Vlan(NetworkObj):
    
    def __init__(self):
        NetworkObj.__init__(self)
        self.type = 'vlan'
        self.tag = 0
        
    def __str__(self, *args, **kwargs):
        return "VLAN: " + self.tag
    
    def __repr__(self):
        retVal = {}
        retVal["id"] = self.id
        retVal["group"] = self.type
        retVal["tag"] = self.tag
        return str(retVal)
    
class Subnet(NetworkObj, IPv4Network):

    def __init__(self, address):
        NetworkObj.__init__(self)
        IPv4Network.__init__(self, address)
        self.type = 'subnet'
        self.network = address
        self.ips = []
        
    def __repr__(self):
        retVal = {}
        retVal["id"] = self.id
        retVal["label"] = str(self.with_netmask).replace("/", "\n")
        #retVal["mask"] = 
        retVal["group"] = self.type
        return str(retVal)
        
class IP(NetworkObj, IPv4Interface):

    def __init__(self, address):
        NetworkObj.__init__(self)
        IPv4Interface.__init__(self, address)
        self.type = 'ip'
        self.subnet = 0
        self.address = address
        self.hostname = ""
        self.openPorts = []
        self.os = ""
        
    def __repr__(self):
        retVal = {}
        retVal["id"] = self.id
        retVal["label"] = str(self.ip)
        if self.os != "":
            retVal["group"] = self.os
        else:
            retVal["group"] = self.type
        retVal["title"] = self.hostname
        return str(retVal)
        
class Hostname(NetworkObj):

    def __init__(self):
        super().__init__()
        self.type = 'hostname'
        self.hostname = ""

