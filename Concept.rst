GPXViewer - Concept
===================

The GUI layout is clear. QTListView left, 
stats on the top right, map below. 

Listview is bound to a *CatalogeModel* that holds the lists:
 * titles (def: Training)
 * dates
 * speed
 * duration
 * distance
 * name of gpx file

The meta data is stored either pickled or as a json file. Not sure yet. 
Another question is where the actual files should go. Either in the package
or in $HOME or so. Not sure. 

The map will be a QTWebview using pygmaps for starters. 
