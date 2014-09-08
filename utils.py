#!/usr/bin/env python

from __future__ import print_function

import math

def deg2rad(deg):
    """Convert degrees to radians

    :param deg: angle in degrees
    :type deg: <float>

    :return: angle in radians
    :rtype: <float>
    """

    return deg / (180 / math.pi)

def euclidean(lon1, lat1, lon2, lat2):
    """
    Calculate the euclidean distance between two points 
    and return distance in meter

    :param lon1: longitude of first point  
    :type lon1: <float> 
    :param lat1: lattitude of first point  
    :type lat1: <float> 
    :param lon2: longitude of second point  
    :type lon2: <float> 
    :param lat2: lattitude of second point  
    :type lat2: <float> 

    :return: distance in meters
    :rtype: <float>
    """



    ONE_DEGREE = 1000. * 10000.8 / 90.    
    coef = math.cos(lat1 / 180. * math.pi)
    x = lat2 - lat1
    y = (lon2 - lon1) * coef
    distance = math.sqrt(x * x + y * y) * ONE_DEGREE

    return distance


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees) and return distance
    in meter

    :param lon1: longitude of first point  
    :type lon1: <float> 
    :param lat1: lattitude of first point  
    :type lat1: <float> 
    :param lon2: longitude of second point  
    :type lon2: <float> 
    :param lat2: lattitude of second point  
    :type lat2: <float> 

    :return: distance in meters
    :rtype: <float>
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(deg2rad, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 

    # 63710000 m is the radius of the Earth
    dist = 6371000 * c

    # r = 6371000
    # dist = r * math.acos(math.sin(deg2rad(lat1)) *
    #                      math.sin(deg2rad(lat2)) + 
    #                      math.cos(deg2rad(lat1)) *
    #                      math.cos(deg2rad(lat2)) * 
    #                      math.cos(deg2rad(lon1 - lon2)))
    return dist


