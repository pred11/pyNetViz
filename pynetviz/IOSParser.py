'''
Created on Jun 13, 2016

@author: kiel
'''

from pynetviz.NetVizParser import NetVizParser
from pynetviz.NetObjects import *
from pynetviz.NetGraph import NetGraph

class IOSParser(NetVizParser):
    
    def __init__(self):
        '''
        Constructor
        '''
        super(IOSParser, self).__init__()
       
        
    def nvParse(self, filename, ng):
        if not isinstance(ng, NetGraph):
            raise TypeError
        nvfw = Host()
        nvfw.type = "switch"
        nvfw.filename = filename
        f = open(filename, 'r')
#        asa_fw = {'interfaces': [], 'ip': "", 'hostname': "", 'routes': [], 'domainname': ""}
        for line in f:
            line = line.strip()
            words = line.split(' ')
            if "ASA Version" in line:
                nvfw.type = "firewall"
            elif(words[0] == 'interface'):
                shutdown = False;
                asa_int = {}
                nvInf = Interface()
 #               asa_int['intf'] = words[1]
                nvInf.hwname = words[1]
                for line1 in f:
                    line1 = line1.strip()
                    words1 = line1.split(' ')
                    if(line1 == '!'): break
                    elif(words1[0] == 'nameif'): nvInf.name = words1[1] #asa_int['name'] = words1[1]
                    elif(words1[0] == 'ip' and words1[1] == "address"):
                        nvip = IPv4Interface(words1[2]+'/'+words1[3])
                        ip = ng.getIPInterface(nvip)
                        nvInf.addresses.append(ip)
                        #nvip = ipaddress.ip_interface(words1[2]+'/'+words1[3])
                        asa_int['ip'] = words1[2]
                        asa_int['netmask'] = words1[3]
                    elif(words1[0] == "shutdown"): shutdown = True
                if(not shutdown):
                    nvfw.interfaces.append(nvInf)
#                asa_fw['interfaces'].append(asa_int)
                #print (asa_int)
                #print (nvInf)
            elif(words[0] == 'ip'):
                pass
            elif(words[0] == 'hostname'):
#                asa_fw['hostname'] = words[1]
                nvfw.hostname.append(words[1])
            elif(words[0] == 'domain-name'):
#                asa_fw['domainname'] = words[1]
                nvfw.domainname = words[1]
            elif(words[0] == 'route'):
                rte = {}
                rte['intf'] = nvfw.getInterfaceByName(words[1])
                rte['net'] = ng.getSubnet(IPv4Network(words[2]+"/"+words[3]))
                #rte['mask'] = words[3]
                rte['gw'] = ng.getIP(words[4])
#                asa_fw['routes'].append(rte)  
                nvfw.routes.append(rte)
            elif(words[0] == 'end' or line == ': end'):
                break
#        print (nvfw.toDict())
#        ng.netDevices.append(nvfw)
        ng.addHost(nvfw)