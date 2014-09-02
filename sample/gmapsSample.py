import pygmaps

########## CONSTRUCTOR: pygmaps(latitude, longitude, zoom) ##############################
# DESC:     initialize a map  with latitude and longitude of center point
mymap = pygmaps.maps(52.3942,13.0727,16)

########## FUNCTION: setgrids(start-Lat, end-Lat, Lat-interval, start-Lng, end-Lng, Lng-interval) ######
# DESC:     set grids on map
#mymap.setgrids(37.42, 37.43, 0.001, -122.15, -122.14, 0.001)


########## FUNCTION:  addpoint(latitude, longitude, [color])#############################
# DESC:     add a point into a map and dispaly it, color is optional default is red
mymap.addpoint(52.3942,13.0727, "#0000FF")


# ########## FUNCTION:  addradpoint(latitude, longitude, radius, [color])##################
# # DESC:     add a point with a radius (Meter) - Draw cycle
mymap.addradpoint(52.3942,13.0727,100, "#FF0000")


########## FUNCTION:  addpath(path,[color])##############################################
# DESC:     add a path into map, the data struceture of Path is a list of points
path = [(52.3942,13.0734),(52.3942,13.0775),(52.4025,13.0775),(52.4025,13.0825)]
mymap.addpath(path,"#00FF00")

########## FUNCTION:  addpath(file)######################################################
# DESC:     create the html map file (.html)
mymap.draw('./map.html')



