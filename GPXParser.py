#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=c0103

""" The ``GPXParser`` class encapsulates parsing of .gpx files.

Public functions
^^^^^^^^^^^^^^^^
 - trackSummary()   : reads track summary and fills {summary}
 - trackDetails()   : reads  track details and fills {track}

Public attributes
^^^^^^^^^^^^^^^^^

 - allPoints    : [<ET.element>]  list of ET elements (<trkpt>)
 - track        : dictionary with the following keys:
    =========   =========       ============================================
    key         type            description
    =========   =========       ============================================
    N           <int>           number of trackpoints
    lon         [<float>]       list with longitudes
    lat         [<float>]       list with lattitudes
    ele         [<float>]       list with elevations
    time        [<str>]         list with timestamps as ISO8601 strings
    distances   [<float>]       distance between succesive points (in meter)
    durations   [<float>]       time difference between points (in secs)
    speed       [<float>]       list of current speeds (in km/h)
    file        <str>           string w/ file name
    =========   =========       ============================================

 - summary     : dictionary with the following keys:
    ========    =======     =====================
    key         type        description
    ========    =======     =====================
    date        <str>       time of track ISO8601
    duration    <float>     duration in s
    distance    <float>     distance in m
    speed       <float>     avg speed in m/s
    ========    =======     =====================

Private functions
^^^^^^^^^^^^^^^^^
 - self._findAllPoints()    : find all <trkpt> elements, sets **allPoints**

Private attributes
^^^^^^^^^^^^^^^^^^
 - _source          : source file
"""


# imports
import xml.etree.cElementTree as ET # XML parser
import dateutil.parser
from utils import haversine
# from utils import euclidean

debug = False

class GPXParser(object):
    """ GPXParser - reads a gpx file and an by default assumes the
    namespace: http://www.topografix.com/GPX/1/1.
    While there can be multiple <trkseg> but for the first implementation
    we just collect all <trkpt> and continue.


    :arg source: name of the GPX file
    :type source: <string>

    :arg namespaces: namespace dictionary
    :type namespaces: {dict}

    The class has the following instance variables once the respective
    methods have been called.

    :ivar allPoints: collection of all trackpoints <trkpt>
    :type allPoints: list of ET.elements

    :ivar summary: dictionary with summary of the training
    :type summary: <dict>

    :ivar track: dictionary with track details
    :type track: <dict>
    """

    def __init__(self, source='', namespaces=None):
        """ Instantiates an GPXParser object

       """
        # setup data file
        if source is None:
            #only for testing
            self._source = './data/Training01.gpx'
        else:
            self._source = source

        if namespaces is None:
            # all the NS we are currently dealing with
            self.namespaces = {'gpx':'http://www.topografix.com/GPX/1/1'}
        else:
            self.namespaces = namespaces

        # init dicts
        self.summary = dict()
        self.track = dict()

        #  and run inital parse
        self._tree = ET.parse(self._source)
        self._root = self._tree.getroot()

        # and find all <trkpts>
        self._findAllPoints()

    def _findAllPoints(self):
        """ Goes over the ET tree and finds all <trkpt> elements.
        These are read-in by order and not further sorted.

        Waypoints and routes are currently ignored.

        Sets the following public attributes:

        :attrib allPoints: collection of all trackpoints <trkpt>
        :type allPoints: list of ET.elements

        """

        # find all tracks
        # the cElementTree implementation does not accept named parameters,
        # but it works w/  ordered ones
        allTracks = self._root.findall('gpx:trk', self.namespaces)

        # then find all segs
        allSegs = []
        for track in allTracks:
            allSegs.extend(track.findall('gpx:trkseg', self.namespaces))

        # and find all points
        self.allPoints = []

        for seg in allSegs:
            self.allPoints.extend(seg.findall('gpx:trkpt', self.namespaces))

        self.track["N"] = len(self.allPoints)
        if debug:
            print "I found %d trackpoints" % self.track["N"]

    def trackSummary(self):
        """ Parse only the key data needed for the model in GPXViewer. Details will
        only be read on demand.

        This function populates the summary dictionary.

        """
        # populate the summary dict w/ the filename
        self.summary["file"] = self._source

        # date as ISO string
        # with some sources the date is only in the metadata and not each track point
        # self.summary["date"] = self.allPoints[0].find('gpx:time', self.namespaces).text
        metaData = self._root.findall('gpx:metadata', self.namespaces)
        for md in metaData:
            time = md.findall('gpx:time', self.namespaces)

        self.summary["date"] = time[0].text

        # duration
        t0 = dateutil.parser.parse(self.allPoints[0].find('gpx:time', self.namespaces).text)
        t1 = dateutil.parser.parse(self.allPoints[-1].find('gpx:time', self.namespaces).text)
        self.summary["duration"] = (t1-t0).total_seconds()

        # distance
        lat = []
        lon = []
        for point in self.allPoints:
            lat.append(float(point.attrib['lat']))
            lon.append(float(point.attrib['lon']))
        _dist = sum([haversine(y0, x0, y1, x1)  for x0, x1, y0, y1 in zip(
            lat[:-1], lat[1:], lon[:-1], lon[1:])])
        self.summary["distance"] = _dist

        # and average speed in km/h
        self.summary["speed"] = 3.6 * self.summary["distance"]/self.summary["duration"]

    def trackDetails(self):
        """Read the track in the GPX file and populate the `track` dictionary.
        The time is read twice once local (as datetime so we can easily compute
        offsets) and once as an ISO 8601 string (as it is written) to be stored
        in the `track` dict.

        """
        # empty list for all the vars for the details
        self.track["source"] = self._source
        self.track["lat"] = []
        self.track["lon"] = []
        self.track["ele"] = []
        self.track["time"] = []
        self.track["distances"] = []    # steps in space
        self.track["durations"] = []    # steps in time (sec)
        self.track["speed"] = []        # speed in km/h

        # locate time version for datetime objects
        times = []

        # extract original lat/lon and cast as float
        for point in self.allPoints:

            # lat/lon/ele are just list of floats
            self.track["lat"].append(float(point.attrib['lat']))
            self.track["lon"].append(float(point.attrib['lon']))
            self.track["ele"].append(float(point.find('gpx:ele', self.namespaces).text))

            # self.time  are datetime instances whereas track["time"] are
            # ISO strings (so the can be serialized)
            times.append(dateutil.parser.parse(
                point.find('gpx:time', self.namespaces).text
                ))
            self.track["time"].append(point.find('gpx:time', self.namespaces).text)

        # here we already compute individual steps between trackpoints

        # 1) distance (haversine)
        # list comprehension is fancy but a tad unreadable
        # also decide wether we need haversion or if euclidean is enough
        self.track["distances"] = [haversine(y0, x0, y1, x1)  for x0, x1, y0, y1 in zip(
            self.track["lat"][:-1], self.track["lat"][1:],
            self.track["lon"][:-1], self.track["lon"][1:])]

        # # the euclidean should work for small distances too and is less demanding
        # self.track["distances"] = [euclidean(y0,x0,y1,x1)  for x0,x1,y0,y1 in zip(
        #                     self.track["lat"][:-1],self.track["lat"][1:],
        #                     self.track["lon"][:-1],self.track["lon"][1:])]

        # 2) durations (these have to be converted to datatime object)
        # actually we could just substract the seconds since the GPS *should* be
        # sampled every few secs but you never know
        self.track["durations"] = [(t1-t0).total_seconds() for t0, t1 in zip(
            times[:-1], times[1:])]

        # 3) speed in segments
        # d/t * 3.6 since we are in m/s but want km/h
        self.track["speed"] = [(d/t)*3.6 if t > 0.0 else 0.0 for d, t in zip(
            self.track["distances"], self.track["durations"])]

        # distance, duration and speed can be computer for n=2 only and thus
        # are too short
        self.track["distances"] = [0] + self.track["distances"]
        self.track["durations"] = [0] + self.track["durations"]
        self.track["speed"] = [0] + self.track["speed"]

        # sum distances consecutively
        self.track["distances"] = [sum(self.track["distances"][:i+1]) for i in
                                    range(len(self.track["distances"]))]

