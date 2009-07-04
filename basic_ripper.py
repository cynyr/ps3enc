#!/usr/bin/env python
import sys
from subprocess import call,PIPE

alang="en"
chan="6"

args = sys.argv
args.pop(0)
print args

while len(args) > 1:
    track = args.pop(0)
    name = args.pop(0)
    cmd = []
    cmd.extend(["mencoder", "-alang", alang, "-channels", chan])
    cmd.extend(["dvd://" + track, "-oac", "copy", "-ovc", "copy"])
    cmd.extend(["-o", name + ".vob"])
    print " ".join(cmd)
    #ret = call(cmd, stdout=PIPE, stderr=PIPE)
    ret = call(cmd)
    print ret
