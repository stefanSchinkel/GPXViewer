#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GPXParser
=========
:GPXParser: class provides the functionality to read .gpx files 

Public functions
----------------
 - readTrack()  : reads the track and fills <track> dict

Public attributes
-------------------
 - allPoints    : [<ET.element>]  list of ET elements (<trkpt>)
A dictionary `track` with the following keys:

    =========   ============    ============================================
    key         type            desc
    =========   ============    ============================================
    N           <int>           number of trackpoints
    lon         [<float>]       list with longitudes
    lat         [<float>]       list with lattitudes
    ele         [<float>]       list with elevations
    time        [<datetime>]    list with timestamps as datetime instances
    distances   [<float>]       distance between succesive points (in meter)
    durations   [<float>]       time difference between points (in secs)
    speed       [<float>]       list of current speeds (in km/h)
    =========   ============    ============================================

Private functions
-----------------
 - self._parseXML()         : runs inital XML parse
 - self._findAllPoints()    : find all <trkpt> elements, sets **allPoints**

Private attributes
------------------
 - _source          : source file 
 -                  : find all <trkpt> elements


GPX Dataformat reference/sample:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
from utils import  haversine,euclidean

class GPXParser(object):
    """ GPXParser - reads a gpx file and

    :ivar allPoints: collection of all trackpoints <trkpt>
    :type allPoints: list of ET.elements

    :ivar track: dictionary describing track details
    :type track: <dict>

    """


    def __init__(self,source='', namespaces=None):
        """ Instantiates an GPXParser object

        :param source: name of the GPX file
        :type source: <string>

        :param namespaces: namespace dictionary
        :type namespaces: {dict}

        """
        if namespaces is None:
            # all the NS we are currently dealing with
            self.namespaces = {'gpx':'http://www.topografix.com/GPX/1/1'}
        else: 
            self.namespaces = namespaces

        # empty list for all the vars needed
        self.track = {}
        self.track["N"] = 0;
        self.track["lat"] = []
        self.track["lon"] = []
        self.track["ele"] = []
        self.track["time"] = []
        self.track["distances"] = []    # steps in space
        self.track["durations"] = []    # steps in time (sec)
        self.track["speed"] = []        # speed in km/h

        # setup data file
        print source
        # if source is None:
        self._source = './data/Training.gpx'

        # run inital parse
        self._parseXML()
        self._findAllPoints()

    def _parseXML(self):
        """ Prepares file for reading
        """
        self.tree = ET.parse(self._source)
        self.root = self.tree.getroot()

    def _findAllPoints(self):
        """ Goes over the ET tree and finds all <trkpt> elements.
        These are read-in by order and not further sorted.

        Waypoints and routes are currently ignored.

        Sets the following public attributes:

        :ivar allPoints: collection of all trackpoints <trkpt>
        :type allPoints: list of ET.elements

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

        self.track["N"] = len(self.allPoints)
        print "I found %d trackpoints" % self.track["N"]

    def readTrack(self):
        """Read the track in the GPX file and populate the `track` dictionary. 
        The time is read twice once local (as datetime so we can easily compute
        offsets) and once as an ISO 8601 string (as it is written) to be stored
        in the `track` dict. 


        """
        # locate time version for datetime objects
        times = []

        # extract original lat/lon and cast as float
        for point in self.allPoints:
            
            # lat/lon/ele are just list of floats
            self.track["lat"].append(float(point.attrib['lat']))
            self.track["lon"].append(float(point.attrib['lon']))
            self.track["ele"].append(float(point.find('gpx:ele',self.namespaces).text))
            
            # self.time  are datetime instances whereas track["time"] are
            # ISO strings (so the can be serialized)
            times.append(dateutil.parser.parse(
                point.find('gpx:time',self.namespaces).text
                ))
            self.track["time"].append(point.find('gpx:time',self.namespaces).text                )

        # here we already compute individual steps between trackpoints
        
        # 1) distance (haversine)
        # list comprehension is fancy but a tad unreadable
        # also decide wether we need haversion or if euclidean is enough
        self.track["distances"] = [haversine(y0,x0,y1,x1)  for x0,x1,y0,y1 in zip(
                            self.track["lat"][:-1],self.track["lat"][1:],
                            self.track["lon"][:-1],self.track["lon"][1:])]

        # the euclidean should work for small distances too and is less demanding    
        self.track["distances"] = [euclidean(y0,x0,y1,x1)  for x0,x1,y0,y1 in zip(
                            self.track["lat"][:-1],self.track["lat"][1:],
                            self.track["lon"][:-1],self.track["lon"][1:])]

        # 2) durations (these have to be converted to datatime object)
        # actually we could just substract the seconds since the GPS *should* be 
        # sampled every few secs but you never know
        self.track["durations"] = [(t1-t0).total_seconds() for t0,t1 in zip(
                            times[:-1],times[1:])]

        # 3) speed in segments
        # d/t * 3.6 since we are in m/s but want km/h
        self.track["speed"] = [(d/t)*3.6 if t>0.0 else 0.0 for d,t in
                         zip(self.track["distances"],self.track["durations"])]

