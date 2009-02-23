#!/usr/bin/env python

import sys
import os

try:
    from PyQt4 import QtGui, QtCore
except:
    print "Please install PyQT4"
    sys.exit(1)

class OpenFileButton(QtGui.QPushButton):
    def __init__(self, text):
        QtGui.QPushButton.__init__(text)

    def Clicked(self,event):
        print "nothing"

class MainWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.setWindowTitle("PS3Enc")
        self.doLayout()
        #self.connect(quit, QtCore.SIGNAL('clicked()'),
            #QtGui.qApp, QtCore.SLOT('quit()'))
        

    def doLayout(self):
        """Creates the UI layout"""
        
        #create a button
        self.b_source = QtGui.QPushButton("Open")
        #create a lineedit, textedit is multiline thingy
        self.e_source = QtGui.QLineEdit()
        self.e_source.setMaxLength(244)
        #set a tooltip on the lineedit
        self.e_source.setToolTip(
            "If DVD is checked, this is the path to the device")
        self.connect(self.b_source, QtCore.SIGNAL('clicked()'),
                        self.bSourceClicked)
        #create a check box, with a label, really all this is
        #is a button with the toggle property and a different pixmap
        self.cb_source = QtGui.QCheckBox("DVD")
        #another button
        self.b_dest = QtGui.QPushButton("Open")
        #you guessed it a lineedit.
        self.e_dest = QtGui.QLineEdit()
        self.connect(self.b_dest, QtCore.SIGNAL('clicked()'), self.bDestClicked)
        
        #create the main vbox
        vbox= QtGui.QVBoxLayout()

        #create the source section
        self.g_source = QtGui.QGroupBox("Source")

        hbox= QtGui.QHBoxLayout()
        hbox.addWidget(self.cb_source)
        hbox.addWidget(self.e_source)
        hbox.addWidget(self.b_source)
        
        self.g_source.setLayout(hbox)
        vbox.addWidget(self.g_source)

        
        #title section
        self.g_title = QtGui.QGroupBox("Title")
        hbox = QtGui.QHBoxLayout()

        self.e_title = QtGui.QLineEdit()
        hbox.addWidget(self.e_title)

        self.g_title.setLayout(hbox)
        vbox.addWidget(self.g_title)
        
        
        #dest Section
        self.g_dest = QtGui.QGroupBox("Destinition")
        #label = QtGui.QLabel("Destinition")
        #label.setAlignment(QtCore.Qt.AlignHCenter)
        #vbox.addWidget(label)

        hbox= QtGui.QHBoxLayout()
        hbox.addWidget(self.e_dest)
        hbox.addWidget(self.b_dest)
        self.g_dest.setLayout(hbox)

        vbox.addWidget(self.g_dest)
        
        self.status_vbox =QtGui.QVBoxLayout()
        
        self.status_group = QtGui.QGroupBox("Status - Pass: 0 - ETA: Never")
        self.status_group.setLayout(self.status_vbox)
        vbox.addWidget(self.status_group)
        self.status_group.setVisible(False)

        self.pbar = QtGui.QProgressBar()
        self.status_vbox.addWidget(self.pbar)



        self.b_start = QtGui.QPushButton("Start")
        self.connect(self.b_start, QtCore.SIGNAL('clicked()'), self.doStart)
        vbox.addWidget(self.b_start)
        #self.

        vbox.addStretch(-1) #position to add the flexable space
        self.setLayout(vbox)        

    def bSourceClicked(self):
        print "Clicked"
        self.openFileDia(self.e_source)
    def bDestClicked(self):
        self.openFileDia(self.e_dest)
    def openFileDia(self, lineedit):
        #lineedit.setText("a file name would go here")
        print "open a dia here"
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                    os.environ["HOME"])
        if filename != '':
            lineedit.setText(filename)
    def doStart(self):
        self.status_group.setVisible(True)
        if self.e_source.text() == "":
            print "you fail, enter a source"
        print "Check values and start the encode here"

app = QtGui.QApplication(sys.argv)
Window = MainWindow()
Window.show()
sys.exit(app.exec_())

