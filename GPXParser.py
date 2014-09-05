#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GPXParser
=========
``GPXParser``  class provides the functionality to read .gpx files 

Public functions
----------------
-later

Private functions
----------------
 - self._parseXML()         : runs inital XML parse
 - self._findAllPoints()    : find all <trkpt> elements

Public Attributes
-------------------
The following are list with 1 val per trackpoint

<float> lat     : lattiude
<float> lon     : longitude
<float> ele        : elevation
<datetime> t     : time

GPX Dataformat:
===============
namespace: http://www.topografix.com/GPX/1/1

Format of CascaRun export is below. There can be
multiple <trkseg> but for the first implementation
we just collect all <trkpt> ::

    </gpx>
        <metadata>
            <name>Training - Do. Jun 12 07:32:28 2014</name>
            <desc>5k</desc>
            <author>
                <name>BlackBerry 10</name>
            </author>
            <extensions>
                <meerun uid="7cd94e5e" activity="running" filtered="true" interval="1" elevationCorrected="true" manualPause="true" autoPause="false" autoPauseSensitivity="medium" gpsPause="false" createLapOnPause="false">
                    <filter smoothing="12" maxSpeed="30" badSignals="55.5556" smallMoves="52"/>
                    <hrm used="false"/>
                </meerun>
            </extensions>
        </metadata>
        <trk>
            <trkseg>
                <trkpt lat="52.4098063200" lon="12.9869185200">
                    <ele>47.9</ele>
                    <time>2014-06-12T05:32:28.900</time>
                </trkpt>
            </trkseg>
        </trk>
    </gpx>    
"""

# imports
import xml.etree.cElementTree as ET # XML parser
import dateutil.parser
from utils import  haversine,distance
import math
class GPXParser(object):
    """ GPXParser - reads a gpx file and



    """


    def __init__(self,source='', namespaces=None):
        """ Instantiates an GPXParser object

        :param source: name of the GPX file
        :type source: <string>

        :param namespaces: namespace t
        :type namespaces: {dict}

        :returns: nothing
        """
        if namespaces is None:
            # all the NS we are currently dealing with
            self.namespaces = {'gpx':'http://www.topografix.com/GPX/1/1'}
        else: 
            self.namespaces = namespaces

        # empty list for all the vars needed
        self.N = 0;
        self.lat = []
        self.lon = []
        self.ele = []
        self.time = []
        self.distances = []     # steps in space
        self.durations = []    # steps in time (sec)

        # setup data file
        print source
        # if source is None:
        self.dataFile = './data/Training.gpx'

        # run inital parse
        self._parseXML()
        self._findAllPoints()


    def _parseXML(self):
        """ Prepares file for reading
        """
        self.tree = ET.parse(self.dataFile)
        self.root = self.tree.getroot()

    def _findAllPoints(self):
        """ Goes over the ET tree and finds all <trkpt> elements
        those are currently not sorted. Also waypoints and routes
        are ignored.

        :returns: self.allPoints
        :rtype: list of ET.<trkpt> elements
        """

        # find all tracks
        # the cElementTree implementation does not accept named parameters, 
        # but it works w/  ordered ones
        # allTracks = self.root.findall('gpx:trk',namespaces=self.namespaces) 
        allTracks = self.root.findall('gpx:trk',self.namespaces) 

        # then find all segs
        allSegs = []
        for track in allTracks:
            # allSegs.extend( track.findall('gpx:trkseg',namespaces=self.namespaces))
            allSegs.extend( track.findall('gpx:trkseg',self.namespaces))

        # and find all points
        self.allPoints = []

        for seg in allSegs:
            # allPoints.extend(seg.findall('gpx:trkpt', namespaces=self.namespaces))        
            self.allPoints.extend(seg.findall('gpx:trkpt', self.namespaces))

        self.N = len(self.allPoints)
        print "I found %d trackpoints" % self.N

    def readTrack(self):
        # extract original lat/lon and cast as float
        for point in self.allPoints:
            
            # lat/lon/ele are just list of floats
            self.lat.append(float(point.attrib['lat']))
            self.lon.append(float(point.attrib['lon']))
            self.ele.append(float(point.find('gpx:ele',self.namespaces).text))
            
            # times are datetime instances
            self.time.append(dateutil.parser.parse(
                point.find('gpx:time',self.namespaces).text
                ))

        # here we already compute individual steps between trackpoints
        
        # 1) haversine distance
        # list comprehension is fancy but a tad unreadable
        self.distances = [haversine(y0,x0,y1,x1)  for x0,x1,y0,y1 in zip(
                            self.lat[:-1],self.lat[1:],self.lon[:-1], self.lon[1:])]
        print sum(self.distances)    
        self.distances = [distance(y0,x0,y1,x1) for x0,x1,y0,y1 in zip(
                            self.lat[:-1],self.lat[1:],self.lon[:-1], self.lon[1:])]
        print sum(self.distances)
        # 2) time 
        self.durations = [(t1-t0).total_seconds() for t0,t1 in zip(self.time[:-1],self.time[1:])]

        # 3) speed in segments
        # d/t * 3.6 since we are in m/s but want km/h
        self.speed = [(d/t)*3.6 if t>0.0 else 0.0 for d,t in
                         zip(self.distances,self.durations)]

