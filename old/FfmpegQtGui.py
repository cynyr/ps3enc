#!/usr/bin/env python

import sys
from Ffmpeg_Base import Ffmpeg
try:
    from PyQt4 import QtGui, QtCore
except:
    print "you need pyqt4 installed for this gui"
    print "Unexpected error:", sys.exc_info()

class FfmpegQtGui(Ffmpeg,QtGui.QWidget):
    def __init__(self,args,abr="256kb",crf="20",parent=None):
        Ffmpeg.__init__(self,abr,crf)
        QtGui.QWidget.__init__(self, parent)
        
        self.files_count=len(args)
        self.files = args

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Ps3Enc3')

        self.l_fname = QtGui.QLabel("File Name")
        self.l_progress = QtGui.QLabel("On File 0 of 0")
        self.l_eta = QtGui.QLabel("ETA: 00:00:00")
        self.l_previous = QtGui.QLabel("")

        self.pbar = QtGui.QProgressBar()
        self.pbar.setGeometry(30, 40, 200, 25)

        self.button = QtGui.QPushButton('Start')
        self.button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button.move(40, 80)

        self.reset = QtGui.QPushButton("restart")
        self.reset.setFocusPolicy(QtCore.Qt.NoFocus)
        
        hbox_pbar = QtGui.QHBoxLayout()
        hbox_pbar.addWidget(self.button)
        hbox_pbar.addWidget(self.reset)
        hbox_pbar.addStretch(0)
        
        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self.l_fname)
        vbox.addWidget(self.l_progress)
        vbox.addWidget(self.l_eta)
        vbox.addWidget(self.pbar)

        vbox.addLayout(hbox_pbar)
        vbox.addStretch(1)
        self.setLayout(vbox)

        self.connect(self.button, QtCore.SIGNAL('clicked()'), self.onStart)
        self.connect(self.reset, QtCore.SIGNAL('clicked()'), self.resetProgress)

        #self.timer = QtCore.QBasicTimer()
        self.started = False
        self.step = 0
        self.lastfile = ""

    def output(self,eta, percent, file, filenum=1, total_files=1):
        #self.l_fname = QtGui.QLabel("File Name")
        #self.l_progress = QtGui.QLabel("On File 0 of 0")
        #self.l_eta = QtGui.QLabel("ETA: 00:00:00")
        print "updating"

        self.l_eta.setText("ETA: " + str(eta))
        self.pbar.setValue(percent)
        self.l_fname.setText(file)
        self.l_progress.setText("File " + str(filenum) + " of "
                                + str(total_files))
        self.update()

    def output_totals(self, file, total_time):
        self.l_previous.setText("File " + file + "completed in " + total_time)

    def resetProgress(self):
        self.pbar.reset()

    def onStart(self):
        print self.updatesEnabled()
        self.Main(self.files)
