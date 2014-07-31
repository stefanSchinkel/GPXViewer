#!/usr/bin/python
# -*- coding: utf-8 -*-
#
"""
"""
from PySide import QtCore,QtGui
#from PySide.QtGui import QDirModel
from layout import Ui_MainWindow
import os,sys


class ListModel(QtGui.QStandardItemModel):
    """ A simple model to tie to our list view 
    """
    def __init__(self,parent=None):

        #init parent
        super(ListModel,self).__init__(parent)
        #self.model = QtGui.QStandardItemModel()
        #==============
        # modelSetup
        self._theList = ['Monday','Tuesday','Wednesday','Thursday']
        
        for item in self._theList:
            # Create an item with a caption
            listItem = QtGui.QStandardItem(item)
        
            # Add the item to the model
            self.appendRow(listItem)


    def data(self, index, role = QtCore.Qt.DisplayRole):
        """ Data function is required to return sth. 

        :arg index: currently selected index
        :type index:    PySide.QtCore.QModelIndex

        :arg role: what kind of 
        :type role:
        """
        # check in
        if not index.isValid():
            return None
        if role == QtCore.Qt.DisplayRole:
            s =  self._theList[index.row()]
            return s + "\n12km\t1:10h\n1240kCal"
            #return "001"
        elif role == QtCore.Qt.DecorationRole:
            return QtGui.QIcon(QtGui.QPixmap('icons/running.png'))

        return None

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
        #==============================================================
        # this works, but only with FileSystem model
        # setup model for the file system
        # self.model = QtGui.QFileSystemModel()
        # self.model.setRootPath(dataDir)
        # self.listView.setRootIndex(self.model.index(dataDir))
        #==============================================================
        # instead of the path, we use our own list
        # try to instantiate own class
        self.model = ListModel()
        self.listView.setModel(self.model)
 
 

        #connect callbacks
        self.listView.doubleClicked.connect(self.itemDoubleClicked)
        self.listView.clicked.connect(self.itemClicked)

        # Statusbar
        self.statusbar.showMessage('')

    def itemClicked(self):
        f = "dummy"#self.model.fileName(self.listView.currentIndex())
        print "highlighted: %s" % (f)

        self.textDate.setText(f)
        self.statusbar.showMessage(f)

    def itemDoubleClicked(self):
        self.textTotalDuration.setText('1:30h')
        self.textTotalDistance.setText('12 km')
        self.textTotalSpeed.setText('8.8 km/h')


        print "doubleClicked"
        idx = self.listView.currentIndex()
        print self.model.data(idx)
        #print self.model.filePath(self.listView.currentIndex())

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    win.raise_()
    sys.exit(app.exec_())