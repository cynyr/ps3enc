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
        self.b_dest = QtGui.QPushButton("Open dest")
        #you guessed it a lineedit.
        self.e_dest = QtGui.QLineEdit()
        self.connect(self.b_dest, QtCore.SIGNAL('clicked()'), self.bDestClicked)
        
        #create the main vbox
        vbox= QtGui.QVBoxLayout()
        #this makes it grow in blank space, if you want widgets to grow,
        #don't use it

        #create a label and set it's alignment
        label = QtGui.QLabel("Source")
        label.setAlignment(QtCore.Qt.AlignHCenter)
        #pack it in the vbox, wonder how you set something to 
        #not show on the main show() method, see 2 lines down.
        vbox.addWidget(label)
        #label.setVisible(False)

        hbox= QtGui.QHBoxLayout()
        hbox.addWidget(self.cb_source)
        hbox.addWidget(self.e_source)
        hbox.addWidget(self.b_source)
        vbox.addLayout(hbox)

        label = QtGui.QLabel("Title")
        label.setAlignment(QtCore.Qt.AlignHCenter)
        vbox.addWidget(label)
        self.e_title = QtGui.QLineEdit()
        vbox.addWidget(self.e_title)
        
        label = QtGui.QLabel("Destinition")
        label.setAlignment(QtCore.Qt.AlignHCenter)
        vbox.addWidget(label)

        hbox= QtGui.QHBoxLayout()
        hbox.addWidget(self.e_dest)
        hbox.addWidget(self.b_dest)
        vbox.addLayout(hbox)
        
        self.status_vbox =QtGui.QVBoxLayout()
        #self.status_vbox.addStretch(0)
        vbox.addLayout(self.status_vbox)

        self.l_pass = QtGui.QLabel("Pass: 0")
        self.l_pass.setAlignment(QtCore.Qt.AlignHCenter)
        self.l_eta = QtGui.QLabel("ETA: Never")
        self.l_eta.setAlignment(QtCore.Qt.AlignHCenter)
        hbox = QtGui.QHBoxLayout()
        hbox.setAlignment(QtCore.Qt.AlignHCenter)
        hbox.addWidget(self.l_pass)
        hbox.addWidget(self.l_eta)
        self.status_vbox.addLayout(hbox)
        self.pbar = QtGui.QProgressBar()
        self.status_vbox.addWidget(self.pbar)

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
                    '/home')
        if filename != '':
            lineedit.setText(filename)

app = QtGui.QApplication(sys.argv)
Window = MainWindow()
Window.show()
sys.exit(app.exec_())

