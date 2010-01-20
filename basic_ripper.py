#!/usr/bin/env python
import sys
from subprocess import call,PIPE

alang="en"
chan="6"

def build_commands(args):
    cmds=[]
    while len(args) >1:
        cmd=[]
        track = args.pop(0)
        name = args.pop(0)
        cmd.extend(["mencoder", "-alang", alang, "-channels", chan])
        cmd.extend(["dvd://" + track, "-oac", "copy", "-ovc", "copy"])
        cmd.extend(["-of", "mpeg"])
        cmd.extend(["-o", name + ".mpeg"])
        print " ".join(cmd)
        cmds.append(cmd)
    return cmds

def print_help():
    print "usage: ripper.py $track1 $title1 $track2 $title2 $trackN $titleN"
    sys.exit(1)

args = sys.argv
args.pop(0)

if "--help" in args:
    print_help()
if "-h" in args:
    print_help()

cmds = build_commands(args)
for cmd in cmds:
    ret = call(cmd, stdout=PIPE, stderr=PIPE)
    print ret

call(["eject"])
