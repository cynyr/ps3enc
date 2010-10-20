#!/usr/bin/env python
from __future__ import print_function
from guis.terminal import do_terminal_gui
from ffmpegbase2 import Ffmpeg
from optparse import OptionParser,OptionGroup
from configfileparser import parse_file
import sys
import os

def get_parser_instance(defaults=None):
    p = OptionParser()
    unimp_group=OptionGroup(p, "Unimplimented options",
        "These options do NOT work yet, they will be accepted and ignored.")

    p.add_option("--outputdir", "-d", dest="outputdir", type="string",
                help="Directory to put the encoded file in")
    p.add_option("--config", "-c", dest="configfile", type="string")
    p.add_option("--audiobitrate", "-a", dest="abr", type="string")
    unimp_group.add_option("--hostname", "-H", dest="hostname", type="string",
                help="hostname for the backend to connect to. This is"+
                     " being ignored for the moment")
    unimp_group.add_option("--port", "-p", dest="portnumber", type="int",
                help="Port to connect or listen on")
    unimp_group.add_option("--debug", "-D", dest="debug", action="count")
    #long only options
    #p.add_option("--ignore-defaults", dest="config", type="string")
    p.add_option("--crf", dest="crf", type="string",
                 help="which x264 CRF number to use. default:22")
    unimp_group.add_option("--threads", dest="threads", type="string",
                           help="number of threads to use. default auto")
    p.add_option_group(unimp_group)
    if not defaults is None:
        if type(defaults) == type(dict()):
            p.set_defaults(**defaults)
    return p

def handle_config():
    """This gathers config data and returns it as an object."""
    if os.name == "posix":
        from defaults import posix
        files=posix.files[:]
    parser=get_parser_instance(defaults=None)
    (options, args) = parser.parse_args(sys.argv)
    files.append(os.path.join(os.getenv("HOME"),".config/ps3enc.config"))
    print(options.configfile)
    if options.configfile:
        files.append(os.path.normpath(options.configfile))
    print(files)
    default_options=dict(outputdir=os.getcwd(),
                         abr="256KB",
                         hostname="localhost",
                         portnumber=36134,
                         crf="22",
                         threads="0")
    for file in files:
        default_options=parse_file(file, default_options)
    parser2=get_parser_instance(defaults=default_options)
    return parser2.parse_args(sys.argv)


if __name__ == "__main__":
    (options,args) = handle_config()
    #print(options.outputdir)
    #print(args)
    ff=Ffmpeg(args[1:], output_dir=options.outputdir, printcmd=True)
    ff.start()
    do_terminal_gui()
