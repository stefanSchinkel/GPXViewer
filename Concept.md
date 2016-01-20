GPXViewer - Concept
===================

The GUI layout is clear. QTListView left,
stats on the top right, map below.

Listview is bound to a *CatalogeModel* that holds the lists of dictionaries.
The dictionaries are taken from GPXParser:

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

The meta data is stored as a json file in /daat.
Another question is where the actual files should go.
Either in the package or in $HOME or so. Not sure.

The map is a QTWebview using leafletjs.
