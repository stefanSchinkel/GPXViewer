
###GPXViewer

``GPXViewer`` is a python gui to view .gpx files. The basic facilities are
a catalog for trainings and a map to trace the individual track.


###Screenshot
![GPXviewer demo](screenshot.png "Sample training")

### Installation

A simple `pip install -r requirements.txt` should do the trick. If you want to run the app in a venv you might face some issues (see below).



####Running on OSX w/ virtualenv

When running on OSX and inside a venv runngin the app might fail w/ sth like this:

>  ImportError: dlopen($VENV/lib/python2.7/site-packages/PySide/QtCore.so, 2): Library not loaded: @rpath/libpyside-python2.7.1.2.dylib
  Referenced from: $VENV/lib/python2.7/site-packages/PySide/QtCore.so

In this case, you need to set the environment variable `DYLD_LIBRARY_PATH` to point to the correct place (in my case to systemwide availabel pyside that came from MacPorts). This can be found using:
```sh
$> locate QtCore.so
```

> /opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/PySide/QtCore.so
/opt/local/Library/Frameworks/Python.framework/Versions/3.3/lib/python3.3/site-packages/PySide/QtCore.so

For Python 2.7 we use the first hit and run the app as:
```sh
DYLD_LIBRARY_PATH=/opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/PySide/ \
python GPXViewer.py

```

###Todo

 - Better handling of data files eg. copying to some directory etc
 - nicer summary statistics (some barcharts maybe)
