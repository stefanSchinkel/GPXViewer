#!/usr/bin/env python

from __future__ import print_function

def main():
    from GPXParser import GPXParser

    # init parser, reads XML and finds points
    gp = GPXParser()

    # read the data
    gp.readTrack()

    # total distances
    print("Total distance is {:.2f} meters".format(sum(gp.distances)))

    # total time
    print("Total duration is {:.1f} seconds".format(sum(gp.durations)))
    
    # average speed
    print("Average speed is {:.1f}".format(sum(gp.speed)/len(gp.speed)))


if __name__ == '__main__':
    main()