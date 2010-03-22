#!/usr/bin/env python
from __future__ import print_function

try:
    import sys
    import os
    from optparse import OptionParser
    import ConfigParser
    from ffmpegbase2 import Ffmpeg
    from socket import socket, AF_NET, SOCK_DGRAM
    from socket import error as sock_err
except ImportError as ierr:
    print(ierr[0])
    sys.exit(1)

class Options:
    def __init__(self):
        self.gui = "term"
        self.destination = "./"
        self.scale = None


class FfmpegQTGui(QtGui.QWidget):
    def __init__(self,host="localhost", port=36134, socket_=None, parent=None):
        Ffmpeg.__init__(self,abr,crf)
        QtGui.QWidget.__init__(self, parent)
        
        self.addr=(str(host),int(port))
        if sockect_:
            self._socket = socket_
        else:
            self._socket = socket(AF_NET, SOCK_DGRAM)
            try:
                self._socket.bind(self.addr)
            except 

        
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
        self.run()
    
    def run(self):
        #setup socket
        #get socket data w/timeout
        #call output with socket data
        #repeat
    
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

def merge_options(cloptions, cfoptions):
    """merge_option(commandline_options, configfile_options)

        Merges the commandline options into the file options with the
        commandline ones taking precedence"""
    ops = Options()
    if not cloptions and not cfoptions:
        return ops
    #merge the configfile options first.
    for key,value in [list(x) for x in list(cfoptions)]:
        setattr(ops,key,value)
    #then merge in the commandline options.
    for attr in [x for x in dir(cloptions) if not x.startswith("_")]:
        val=getattr(cloptions, attr)
        #print(val)
        if val:
            setattr(ops,attr,val)
    return ops
        
def get_socket_pair(port,host,auto=True):
    s1 = socket(AF_INET, SOCK_DGRAM)
    s2 = socket(AF_INET, SOCK_DGRAM)
    if port and host and not auto:
        try:
            s1.bind((str(host),int(port)))
        except sock_err as err:
            print("error binding to address: " + str(port))
            sys.exit(3)
    else:
        

op = OptionParser()
op.add_option("-g", "--gui", dest="gui", type="string",
             help="Which output to use. term or qt.")
op.add_option("-c", "--config", dest="configfile", type="string",
             help="Use the specified config file instead of the default ones.")
op.add_option("-d", "--destination", dest="destination", type="string", 
             help="The directory to store all of the output files.")
op.add_option("-s", "--scale", dest="scale", 
              help="Scale the sources to this size. Any size that FFmpeg will"\
                    + " accept.")
(cloptions,clargs) = op.parse_args()
#print(dir(cloptions))
#print(cloptions.configfile)

cp = ConfigParser.ConfigParser()
if cloptions.configfile:
    configfiles = [cloptions.configfile,]
else:
    configfiles = ["/etc/ps3enc/ps3enc.conf"]
    if os.environ["HOME"]:
        configfiles.append(os.environ["HOME"] + "/.config/ps3enc/ps3enc.conf")
cp.read(configfiles)
try:
    cfoptions = cp.items("Main")
except ConfigParser.NoSectionError:
    cfoptions = None
#print([list(x) for x in list(cfoptions)])

options = merge_options(cloptions, cfoptions)
#for key in [x for x in dir(options) if not x.startswith("_")]:
for key in ["scale","gui","destination"]:
    print([key,getattr(options,key)])

if options.gui.lower() == "qt":
    try:
        from PyQt4 import QtGui, QtCore
    except ImportError as err:
        print(err.args)
        sys.exit(1)
    else:
        #get qt application object
        app = QtGui.QApplicationa(sys.argv)
        #get an ffmpeg object
        ff = ffmpeg()
        #get a new gui object
        gui = FfmpegQTGui()
        #start up ffmpeg object
        ff.start()
        #start up app
        sys.exit(app.exec_())
