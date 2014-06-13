#!/usr/bin/python
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
        
        homeDir = unicode(os.path.expanduser("~"))
        homeDir = QtCore.QDir.currentPath()
        # init super and load layout
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        # setup model for the file system
        self.model = QtGui.QFileSystemModel()
        self.model.setRootPath(homeDir)

        # and a QTreeView to show it
        self.fileBrowser.setModel(self.model)
        self.fileBrowser.setRootIndex(self.model.index(homeDir))

        #connect callbacks
        self.fileBrowser.doubleClicked.connect(self.itemDoubleClicked)
        self.fileBrowser.clicked.connect(self.itemClicked)

    def itemClicked(self):
        print "highlighted: %s" % (self.model.fileName(self.fileBrowser.currentIndex()))

    def itemDoubleClicked(self):
        print "doubleClicked"
        print self.model.fileName(self.fileBrowser.currentIndex())
        print self.model.filePath(self.fileBrowser.currentIndex())
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())