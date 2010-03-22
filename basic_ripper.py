#!/usr/bin/env python
import sys
from subprocess import call,PIPE,Popen

alang="en"
chan="6"
msglevel="-1" #see the mplayer man page for "-msglevel all="

def build_commands(args):
    cmds=[]
    while len(args) >1:
        cmd=[]
        track = args.pop(0)
        name = args.pop(0)
        cmd.extend(["mencoder", "-alang", alang, "-channels", chan])
        cmd.extend(["-msglevel", "all=" + msglevel,])
        cmd.extend(["dvd://" + track, "-oac", "copy", "-ovc", "copy"])
        cmd.extend(["-of", "mpeg"])
        cmd.extend(["-o", name + ".mpeg"])
        #print " ".join(cmd)
        cmds.append(cmd)
    return cmds

def print_help():
    print "usage: ripper.py $track1 $title1 $track2 $title2 $trackN $titleN"
    sys.exit(1)

args = sys.argv[:]
args.pop(0)

if "--help" in args:
    print_help()
if "-h" in args:
    print_help()

cmds = build_commands(args)
for cmd in cmds:
    print "Starting: " + cmd[-1]
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    #p = Popen(cmd, stdout=None, stderr=None)
    p.wait()
    if p.returncode == 0:
        print "Sucess: " + cmd[-1]

call(["eject"])
