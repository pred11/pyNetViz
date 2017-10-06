'''
Created on Dec 17, 2014

@author: kiel
'''

from pynetviz.IOSParser import IOSParser
from pynetviz.NmapParser import NmapParser
from pynetviz.NetObjects import *
from pynetviz.NetGraph import NetGraph
from glob import glob


#from pynetviz.Parser import IOSParser

if __name__ == '__main__':
    '''    
    n = NetGraph()
    
    iParse = IOSParser()
    for i in glob("*.txt"):
        iParse.nvParse(i, n)

    print ("var nodes = " + n.toVis_JS()+ ";")
    print ("var edges = " + str(n.links)+ ";")
    '''    
    
    p = NmapParser()
    n = NetGraph()
    
    for i in glob("*.xml"):
        print("main: " + i)
        p.nvParse(i, n)
    print ("var nodes = " + n.toVis_JS()+ ";")
    print ("var edges = " + str(n.links)+ ";")