#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

"""
GPXParser
=========

``GPXParser``  class provides the functionality to read .gpx files 

Public functions
--------------------
-later

Public Attributes
-------------------
The following are list with 1 val per trackpoint

<float> lat 	: lattiude
<float> lon 	: longitude
<float> ele		: elevation
<datetime> t 	: time

GPX Dataformat:
===============
namespace: http://www.topografix.com/GPX/1/1

Format of CascaRun export is below. There can be
multiple <trkseg> but for the first implementation
we just collect all <trkpt> 
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
# usual
import os,sys,time

# imports
import xml.etree.ElementTree as ET # XML parser


class GPXParser(object):
	""" GPXParser the actual thing

	"""
	# all the NS we are currently dealing with
	namespaces = {'gpx':'http://www.topografix.com/GPX/1/1'}

	def __init__(self,namespaces=None):
		""" Instantiates an GPXParser object
		
		:param namespaces: namespace t
		:type namespaces: {dict}
		
		:returns: nothing
		"""

		# empty list for all the vars needed
		self.N = 0;
		self.lat = []
		self.lon = []
		self.ele = []
		self.ts = []

		# setup data file
		self.dataFile = './data/Training.gpx'

		self.parseXML()
		self.findAllPoints()


	def parseXML(self):
		""" Prepares file for reading
		"""
		self.tree = ET.parse(self.dataFile)
		self.root = self.tree.getroot()

	def findAllPoints(self):
		""" Find all <trk> elements

		:returns: self.allTracks
		:rtype: list of ET.Elements
		"""

		# find all tracks
		allTracks = self.root.findall('gpx:trk',namespaces=self.namespaces) 
		
		# then find all segs
		allSegs = []
		for track in allTracks:
			allSegs.extend( track.findall('gpx:trkseg',namespaces=self.namespaces))

		# and find all points
		allPoints = []
		
		for seg in allSegs:
			allPoints.extend(seg.findall('gpx:trkpt', namespaces=self.namespaces))
		
		self.N = len(allPoints)
		print "I found %d trackpoints" % self.N
	
		# extract original lat/lon and cast as float
		for point in allPoints:
		    self.lat.append(float(point.attrib['lat']))
		    self.lon.append(float(point.attrib['lon']))