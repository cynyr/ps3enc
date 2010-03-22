#!/usr/bin/env python
from __future__ import print_function
from guis.terminal import do_terminal_gui
from ffmpegbase2 import Ffmpeg
from optparse import OptionParser
from configfileparser import parse_file
import os

if os.name == "posix":
    from defaults import posix
    files=posix.files[:]


p = OptionParser()
p.add_option("-d", dest="dir", default="./",
             help="Where to save the output files")
(options, args) = p.parse_args()

defaultoptions = {}
files.append(os.path.join(os.getenv("HOME"),".config/ps3enc.config"))
print(files)



p = OptionParser()
p.add_option("-d", dest="dir", default="./",
             help="Where to save the output files")
(options, args) = p.parse_args()
ff=Ffmpeg(args, output_dir=options.dir, printcmd=True)
#guis.terminal.hello_world()
ff.start()
#guis.terminal.do_terminal_gui()
do_terminal_gui()
