#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
"""

# for accessing json
from __future__ import with_statement
import json
import time
import sys

# QT stuff
from PySide import QtCore,QtGui

# tools
from GPXParser import GPXParser
from utils import writeTrackFile

#import model
from model.catalogue import CatalogueModel

#view
from views.layoutGPXParser import Ui_MainWindow


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    """ A QTMain Window, the whole thing
    """
    def __init__(self, parent = None):


        # this has to be stored in some config file
        #dataDir = unicode(os.path.expanduser("~"))
        dataDir = QtCore.QDir.currentPath() + '/data'
        print dataDir

        # init super and load layout
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        # disable editable feature in list view
        self.listView.setEditTriggers(
                QtGui.QAbstractItemView.NoEditTriggers
                )

        # instantiate the CatalogueModel and tie to view
        self.model = CatalogueModel()
        self.listView.setModel(self.model)

        # and populate summary
        self.updateSummary()

        # and connect callbacks
        self.listView.doubleClicked.connect(self.itemDoubleClicked)
        self.listView.clicked.connect(self.itemClicked)
        self.actionOpen.activated.connect(self.addTraining)

        # Statusbar
        self.statusbar.showMessage('READY ...')

    def updateSummary(self):
        """ Queries the model for the summary of all trainings and sets
        the corresponding texts
        """
        self.textTotalDistance.setText("{:.1f} km".format(
                    self.model._summary["totalDistance"]/1000.0))
        self.textTotalDuration.setText(time.strftime('%H:%M:%S',
                    time.gmtime(self.model._summary["totalDuration"])))
        self.textTotalSpeed.setText("{:.1f} km/h".format(
                    self.model._summary["totalSpeed"]))

    def itemClicked(self):
        """ Callback when just pointing at a  list item
        """
        # get selected item as Qt ModelIndex *not* <int>
        idx = self.listView.currentIndex()
        # item =  self.model.data(idx)

        # fill in the track statistics
        # date & time
        date = self.model.getDate(idx)
        self.textDate.setText(date.strftime("%d. %b %Y"))
        self.textTime.setText(date.strftime("%H:%M"))

        # distance formated as km (is in m)
        distance = "{:.1f} km".format(self.model.getDistance(idx) /1000.0)
        self.textDistance.setText(distance)

        # duration is in secs, so this has to be formated too
        duration = self.model.getDuration(idx)
        self.textDuration.setText(time.strftime('%H:%M:%S', time.gmtime(duration)))

        # speed is in m/s so we have to multiply
        speed =  "{:.1f} km/h".format(self.model.getSpeed(idx))
        self.textSpeed.setText(speed)

        # and update statusbar
        self.statusbar.showMessage("Selected Training from " + date.strftime("%d.%m.%Y"))

        # acquire the filename
        gpxFile = self.model.getFile(idx)
        writeTrackFile(gpxFile)
        self.webView.reload()

    def itemDoubleClicked(self):
        """ On double click the map should be rendered
        """
        idx = self.listView.currentIndex()
        print "Would render training " + self.model.data(idx)

    def addTraining(self):
        """Callback to add a new training to the catalogue
        """

        print "Hit callback"
        fileName, _ = QtGui.QFileDialog.getOpenFileName(parent=self,
                    caption = 'Select file to be added',
                    dir = QtCore.QDir.homePath(),
                    filter = '*.gpx')



        with open('./catalogue.json','r') as fp:
            catalogue = json.load(fp)

        gpx = GPXParser(source=fileName)
        gpx.trackSummary()
        newTrack  = gpx.summary;
        catalogue.append(newTrack)

        with open('./catalogue.json', 'wb') as f:
            json.dump(catalogue, f)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    win.raise_()
    sys.exit(app.exec_())















