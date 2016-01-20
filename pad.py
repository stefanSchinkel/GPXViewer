#!/usr/bin/env python

from __future__ import print_function,with_statement
import json
from GPXParser import GPXParser

def parseFile(gpxFile):

    print(gpxFile)

    # init parser, reads XML and finds points
    gp = GPXParser(source=gpxFile)

    # read the data
    # gp.readTrack()

    gp.trackSummary()
    for k,v in gp.summary.iteritems():
        print("{}\t{}".format(k,v))

    # print("readTrack")
    # # total distances
    print("Total distance is {:.2f} meters".format(gp.summary["distance"]))

    # # total time
    # print("Total duration is {:.1f} seconds".format(gp.summary["durations"]))

    # average speed
    # print("Average speed is {:.1f} km/h".format(3.6*sum(gp.track["distances"])/sum(gp.track["durations"])))

    return (gp.summary)

def writeTrack(gpxFile):
    """write leaflet compatible track array"""
    # init parser, reads XML and finds points
    gpx = GPXParser(source=gpxFile)

    # read track details
    gpx.trackDetails()

    trackHeader="""
    var map = L.map('map').setView([{},{}], 14);
    mapLink = '<a href="http://openstreetmap.org">OpenStreetMap</a>';
    L.tileLayer(
            'http://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: 'Map data &copy; ' + mapLink,
            maxZoom: 18,
            }}).addTo(map);
    track = ["""
    # open js file
    with open ('./src/track.js','wb') as fp:
        print(trackHeader.format(gpx.track['lat'][0],
                                gpx.track['lon'][0]),
                                file=fp)
        for idx in range(gpx.track['N']):
            print ("\t[{},{}],".format(gpx.track['lat'][idx],
                                    gpx.track['lon'][idx]),
                                    file=fp)
        print("];\nvar polyline = L.polyline(track).addTo(map);",file=fp)

def main():

    # storage list
    catalogue = []

    # # read track 01
    track01 = parseFile(gpxFile='./data/Training01.gpx')
    catalogue.append(track01)

    track02 = parseFile(gpxFile='./data/Training02.gpx')
    catalogue.append(track02)

    # # track03 = parseFile(gpxFile='./sampleGPX/Herzberg.gpx')
    # # catalogue.append(track03)


    # sort by date
    catalogue.sort(key=lambda item:item['date'], reverse=False)

    with open('data/catalogue.json','wb') as fp:
        json.dump(catalogue,fp)



if __name__ == '__main__':
    main()
