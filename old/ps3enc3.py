#!/usr/bin/env python
import sys
from optparse import OptionParser

p = OptionParser()
p.add_option("-g", "--gui", dest="gui", default="Term",
             help="Which gui to use, Term or QT")
p.add_option("-c", "--config", dest="configfile",
             help="Use this config file instead of the system ones.")

(options, args) = p.parse_args()

if options.gui.lower() == "qt":
    from FfmpegQtGui import FfmpegQtGui
    try:
        from PyQt4 import QtGui, QtCore
        #QtGui.QApplication
    except:
        print "PyQt4 is needed for this Gui"
    else:
        app = QtGui.QApplication(sys.argv)
        ff = FfmpegQtGui(args)
        ff.show()
        #ff.Main(args)
        sys.exit(app.exec_())

if options.gui.lower() == "term":
    from FfmpegTermGui import FfmpegTermGui
    ff = FfmpegTermGui()
    ff.Main(args)


