#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
"""

# for accessing json
from __future__ import with_statement
import json

# QT stuff
from PySide import QtCore,QtGui
from layout import Ui_MainWindow

# for fiddlings w/ ISO8601 and <datetime>s
from dateutil import parser
import time

import os,sys


class CatalogueModel(QtGui.QStandardItemModel):
    """ A simple model to tie to our list view 
    """
    def __init__(self,parent=None):

        #init parent
        super(CatalogueModel,self).__init__(parent)

        # modelSetup
        # the information contained here should go in a class
        # that has the relevant lists or rather dicts

        #read the catalogue file
        print "reading json"
        with open('./catalogue.json') as fp:
            catalogue = json.load(fp)

        print "init lists"
        self._dates = []
        self._speed = []
        self._files = []
        self._duration = []
        self._distance = []

        print "filling lists"
        # loop over catalogue and fill
        for training in catalogue:
                    
            # the dates as datetime instances      
            date = parser.parse(training['date'])           # <unicode>
            self._dates.append(date)
            self._duration.append(training["duration"])     # <float>
            self._distance.append(training["distance"])     # <float>
            self._speed.append(training["speed"])           # <float>
            self._files.append(training["file"])             # <unicode>


        #the model needs rows to make the view happy
        for item in self._dates:
            # Create an item with a caption
            listItem = QtGui.QStandardItem(item.strftime("%d. %b %Y - %H:%M"))
            # Add the item to the model
            self.appendRow(listItem)
        
        # once everything is read-in we can sum up
        # and fill summary dict that the view than can query
        self._summary={}
        self._summary["totalDistance"] = sum(self._distance)
        self._summary["totalDuration"] = sum(self._duration)
        self._summary["totalSpeed"] = sum(self._speed)/len(self._speed)


    def data(self, index, role = QtCore.Qt.DisplayRole):
        """ data function is required to names, icons etc
        for the QListView to acutally render nicely 

        :arg index: currently selected index
        :type index: PySide.QtCore.QModelIndex

        :arg role: what kind of DisplayRole
        :type role: QtCore.Qt.DisplayRole
        """
        # check if we have a valid index
        if not index.isValid():
            return None

        # and return a nicely formated <str> for the listview
        if role == QtCore.Qt.DisplayRole:
            return self._dates[index.row()].strftime("%d. %b %Y - %H:%M")

        # as well as an icon
        elif role == QtCore.Qt.DecorationRole:
            return QtGui.QIcon(QtGui.QPixmap('icons/running.png'))

        return None

    ###
    ### Various callbacks to query the model with the pattern
    ### getVarname(self,index) that returns the proper time from _varname[]
    ###
    def getDate(self,index):
        """ returns date from summary 
        """
        if not index.isValid():
            return None
        return self._dates[index.row()]

    def getSpeed(self,index):
        """ returns speed  from summary
        """
        if not index.isValid():
            return None
        return self._speed[index.row()]

    def getDuration(self,index):
        """ returns duration  from summary
        """
        if not index.isValid():
            return None
        return self._duration[index.row()]

    def getDistance(self,index):
        """ returns distance  from summary
        """
        if not index.isValid():
            return None
        return self._distance[index.row()]

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):

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
        # # enable multiple selection ? 
        # # rather not for now since the we'd have to plot 
        # # more than one track on the maps
        # self.listView.setSelectionMode(
        #     QtGui.QAbstractItemView.ExtendedSelection
        #     )

        # instantiate the CatalogueModel and tie to view
        self.model = CatalogueModel()
        self.listView.setModel(self.model)

        # and populate summary
        self.updateSummary()


        # and connect callbacks
        self.listView.doubleClicked.connect(self.itemDoubleClicked)
        self.listView.clicked.connect(self.itemClicked)

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
                    self.model._summary["totalSpeed"]*3.6))

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
        speed =  "{:.1f} km/h".format(self.model.getSpeed(idx)*3.6)
        self.textSpeed.setText(speed)

        # and update statusbar
        self.statusbar.showMessage("Selected Training from " + date.strftime("%d.%m.%Y"))

    def itemDoubleClicked(self):
        """ On double click the map should be rendered
        """
        idx = self.listView.currentIndex()
        print "Would render training " + self.model.data(idx)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    win.raise_()
    sys.exit(app.exec_())