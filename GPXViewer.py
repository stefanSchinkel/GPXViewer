#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
"""
from PySide import QtCore,QtGui
#from PySide.QtGui import QDirModel
from layout import Ui_MainWindow
import os,sys


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    

    def __init__(self, parent = None):
        
        # this has to be stored in some config file
        #dataDir = unicode(os.path.expanduser("~"))
        dataDir = QtCore.QDir.currentPath() + '/data'
        print dataDir
        
        # init super and load layout
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        # setup model for the file system
        self.model = QtGui.QFileSystemModel()
        self.model.setRootPath(dataDir)

        # and a QTreeView to show it
        self.fileBrowser.setModel(self.model)
        self.fileBrowser.setRootIndex(self.model.index(dataDir))

        #connect callbacks
        self.fileBrowser.doubleClicked.connect(self.itemDoubleClicked)
        self.fileBrowser.clicked.connect(self.itemClicked)

        # Statusbar
        self.statusbar.showMessage('')

    def itemClicked(self):
        f = self.model.fileName(self.fileBrowser.currentIndex())
        print "highlighted: %s" % (f)

        self.textDate.setText(f)
        self.statusbar.showMessage(f)

    def itemDoubleClicked(self):
        self.textTotalDuration.setText('1:30h')
        self.textTotalDistance.setText('12 km')
        self.textTotalSpeed.setText('8.8 km/h')
        print "doubleClicked"
        print self.model.fileName(self.fileBrowser.currentIndex())
        print self.model.filePath(self.fileBrowser.currentIndex())

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    win.raise_()
    sys.exit(app.exec_())