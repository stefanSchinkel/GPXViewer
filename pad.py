#!/usr/bin/env python

from __future__ import print_function,with_statement
import json
from GPXParser import GPXParser

def parseFile(gpxFile):
    
    print(gpxFile) 
    
    # init parser, reads XML and finds points
    gp = GPXParser(source=gpxFile)

    # read the data
    gp.readTrack()

    for k,v in gp.summary.iteritems():
        print("{}\t{}".format(k,v))

    # # total distances
    # print("Total distance is {:.2f} meters".format(sum(gp.track["distances"])))

    # # total time
    # print("Total duration is {:.1f} seconds".format(sum(gp.track["durations"])))
    
    # # average speed
    # print("Average speed is {:.1f} km/h".format(sum(gp.track["speed"])/len(gp.track["speed"])))

    return (gp.summary)

def main():

    # storage list
    catalogue = []

    # read track 01
    track01 = parseFile(gpxFile='./data/Training01.gpx')
    catalogue.append(track01)

    track02 = parseFile(gpxFile='./data/Training02.gpx')
    catalogue.append(track02)

    with open('./catalogue.json','wb') as fp:
        json.dump(catalogue,fp)
        fp.close()



if __name__ == '__main__':
    main()