#!/usr/bin/env python

from __future__ import print_function,with_statement
import json

def main():
    from GPXParser import GPXParser

    # init parser, reads XML and finds points
    gp = GPXParser()

    # read the data
    gp.readTrack()

    # total distances
    print("Total distance is {:.2f} meters".format(sum(gp.track["distances"])))

    # total time
    print("Total duration is {:.1f} seconds".format(sum(gp.track["durations"])))
    
    # average speed
    print("Average speed is {:.1f} km/h".format(sum(gp.track["speed"])/len(gp.track["speed"])))


    # storage of 2 copies in list (just to be sure)
    catalogue = []
    catalogue.append(gp.track)
    catalogue.append(gp.track)

    with open('./catalogue.json','wb') as fp:
        json.dump(catalogue,fp)
        fp.close()

if __name__ == '__main__':
    main()