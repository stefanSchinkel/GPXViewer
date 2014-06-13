#!/usr/bin/python
# -*- coding: utf-8 -*-
#
"""
GPXParser -
Simple class to read the XML in .gpx files and d
"""
# imports
import sys
import time


try:
    import xml.etree.ElementTree as ET
except ImportError:
    print """
    Fatal Error: Could not import XML Parser"
    Make sure you have the python XML module installed. 
    """
    sys.exit(0)



class GPXParser(object):
    """The GPXParser class, inheriting from object only
    """

    def __init__(self):

        print "OSMParser: ready"
        self.debug = True

    def setSource(self,src):
        """ Sets the source, for now only a file
        
        :arg src: source (for now a file) 
        :type src: string
   
        :rtype: None 
        """
        self.source = src;

    def parseXML(self):
        """
        Runs an inital parsing of the XML tree, 
        to the pass around the root and tree objects
        """
        # open and parse XML fils
        # store in root
        self.tree = ET.parse(self.source)
        self.root = self.tree.getroot()

        # find all nodes and ways
        self.allNodes = self.root.findall('node') 
        self.allWays = self.root.findall('way')

    @staticmethod
    def _parseTime(dstr):
        """Parse ISO8601+UTC String and return datetime object
        """
        d,t = dstr.strip().split('T')
        return dt.datetime( *map(int, d.split('-') + t.split(':')) )  

    #==========================================================================
    def debugMessage(self,mesgID):
        """ Prints a message identified by mesgID, given the global 
        debug state is enabled (debug=True)
        """
        messages = {
            1: "",
            2: "",
            3: "",
            4: ""
       }

        if self.debug:
            print messages[mesgID]
            print "========================================"
