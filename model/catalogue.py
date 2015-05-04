#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
""" A model for the  training catalogue
"""
# for accessing json
import json

# QT stuff
from PySide import QtCore,QtGui

# for fiddlings w/ ISO8601 and <datetime>s
from dateutil import parser


class CatalogueModel(QtGui.QStandardItemModel):
    """ A simple model to tie to our list view
    """
    def __init__(self,parent=None):

        #init parent
        super(CatalogueModel,self).__init__(parent)

        # modelSetup
        # the information contained here should go in a class
        # that has the relevant lists or rather dicts

        # the whole init thing can be abstracted to
        # create a list that is name as the key and fill it!

        #read the catalogue file
        print "reading json"
        with open('./catalogue.json') as fp:
            catalogue = json.load(fp)

        print "init lists"
        self._date = []
        self._speed = []
        self._files = []
        self._duration = []
        self._distance = []

        print "filling lists"
        # loop over catalogue and fill
        for training in catalogue:

            # the dates as datetime instances
            date = parser.parse(training['date'])           # <unicode>
            self._date.append(date)                         # <datetime>
            self._duration.append(training["duration"])     # <float>
            self._distance.append(training["distance"])     # <float>
            self._speed.append(training["speed"])           # <float> km/h
            self._files.append(training["file"])            # <unicode>


        #the model needs rows to make the view happy
        for item in self._date:
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
            return self._date[index.row()].strftime("%d. %b %Y - %H:%M")

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
        return self._date[index.row()]

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

    def getFile(self,index):
        """ returns distance  from summary
        """
        if not index.isValid():
            return None
        return self._files[index.row()]