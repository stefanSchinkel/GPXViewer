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

def main():

    # storage list
    catalogue = []

    # read track 01
    track01 = parseFile(gpxFile='./data/Training01.gpx')
    catalogue.append(track01)

    track02 = parseFile(gpxFile='./data/Training02.gpx')
    catalogue.append(track02)
    
    track03 = parseFile(gpxFile='./sampleGPX/Herzberg.gpx')
    catalogue.append(track03)

    with open('./catalogue.json','wb') as fp:
        json.dump(catalogue,fp)
        fp.close()



if __name__ == '__main__':
    main()