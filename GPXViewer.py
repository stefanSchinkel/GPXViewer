#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
"""
from PySide import QtCore,QtGui
#from PySide.QtGui import QDirModel
from layout import Ui_MainWindow
import os,sys


class CatalogueModel(QtGui.QStandardItemModel):
    """ A simple model to tie to our list view 
    """
    def __init__(self,parent=None):

        #init parent
        super(CatalogueModel,self).__init__(parent)
        #self.model = QtGui.QStandardItemModel()
        #==============
        # modelSetup
        # the information contained here should go in a class
        # that has the relevant lists
        self._theList = ['Monday','Tuesday','Wednesday','Thursday','Friday']
        self._speed = [10,11,10,11,12]
        self._duration = ['0:55','1:00','1:05','0:59','0:55']
        self._distance = [9,10,11,10,9]

        for item in self._theList:
            # Create an item with a caption
            listItem = QtGui.QStandardItem(item)

            # Add the item to the model
            self.appendRow(listItem)
        

    def data(self, index, role = QtCore.Qt.DisplayRole):
        """ data function is required to names, icons etc
        for the QListView to acutally render nicely 

        :arg index: currently selected index
        :type index: PySide.QtCore.QModelIndex

        :arg role: what kind of DisplayRole
        :type role: QtCore.Qt.DisplayRole
        """
        # check in
        if not index.isValid():
            return None
        if role == QtCore.Qt.DisplayRole:
            return self._theList[index.row()]
            #return "001"
        elif role == QtCore.Qt.DecorationRole:
            return QtGui.QIcon(QtGui.QPixmap('icons/running.png'))

        return None

    def getSpeed(self,index):
        """ returns speed 
        """
        if not index.isValid():
            return None
        return self._speed[index.row()]

    def getDuration(self,index):
        """ returns duration 
        """
        if not index.isValid():
            return None
        return self._duration[index.row()]

    def getDistance(self,index):
        """ returns distance 
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
        # enable multiple selection
        self.listView.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection
            )

        #==============================================================
        # this works, but only with FileSystem model
        # setup model for the file system
        # self.model = QtGui.QFileSystemModel()
        # self.model.setRootPath(dataDir)
        # self.listView.setRootIndex(self.model.index(dataDir))
        #==============================================================
        # instead of the path, we use our own list
        # try to instantiate own class
        self.model = CatalogueModel()
        self.listView.setModel(self.model)

        #connect callbacks
        self.listView.doubleClicked.connect(self.itemDoubleClicked)
        self.listView.clicked.connect(self.itemClicked)

        # Statusbar
        self.statusbar.showMessage('')

    def itemClicked(self):
        """ Callback when just pointing at a  list item
        """
        # get selected item as Qt ModelIndex *not* <int>
        idx = self.listView.currentIndex()

        item =  self.model.data(idx)

        self.textDate.setText(item)
        self.statusbar.showMessage("Selected Training " + item)
        
        speed =  str(self.model.getSpeed(idx))
        duration = self.model.getDuration(idx)
        distance = str(self.model.getDistance(idx))
        
        self.textDuration.setText(duration)
        self.textDistance.setText(distance)
        self.textSpeed.setText(speed)

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