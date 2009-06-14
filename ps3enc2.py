#!/usr/bin/env python
import os,sys
from time import time
from subprocess import Popen,PIPE,STDOUT
import re

def Main(files):
    audbitrate = "128kb"
    for file in files:
        print file
        global nfn = gen_output_filename(file)
        global sinfo = GetSourceInfo(file)
        global tframes =  ToFrames(get_source_length(sinfo))
        global audio_bitrate = "128kb"
        global video_options = "-deinterlace -vcodec libx264 -vpre " +\
                            "hq -crf 22 -threads 0 -level 41"
        global [audio_options,audio_options2] = GetAudioOptions(info)
        print [nfn, tframes, audio_options, audio_options2]

def gen_output_filename(inname):
    """Generate an output file name, checking for collisions"""

    fname = os.path.split(inname)[1]
    nfn = fname.split(".")[0] + ".mp4"
    if not os.access("./" + nfn, os.F_OK):
        return nfn
    else:
        return nfn.split(".")[0] + "".join(str(time()).split(".")) + ".mp4"

def ToSeconds(s):
    """ToSeconds(string), "01:23:78.8" and converts it to seconds"""
    time=length.split(':')
    seconds=int(time[0])*3600
    seconds+= int(time[1])*60 
    seconds+= float(time[2])
    return seconds

def ToFrames(f):
    """ToFrames(f), converts the "time" to a number of frames.

    ToFrames(float/int), returns float * 29.97
    ToFrames(str), passes str to ToSeconds(str) and finds the
        the total frames from that."""
    if type(f) == type(2.2):
        return f*29.97
    elif type(f) == type(""):
        return ToSeconds(f)*29.97

def GetSourceInfo(fn):
    """Returns ffmpegs info about the file"""

    c = "ffmpeg -i %s" % (fn,)
    p = Popen(c.split(),stdout=PIPE,stderr=STDOUT,
              shell=False,universal_newlines=True)
    return p.communicate()[0]

def GetAudioMap(info, track="0x80"):
    """GetAudioMap(info), Returns [file:stream, type] from the info)"""

    regex = '^\s*Stream.*\[' + track + '\].*$'
    ptr = re.compile(regex, re.MULTILINE)
    s = ptr.search(info)
    s2 = None
    if s != None:
        s = s.group(0)
        m = re.search('(?<=#)([0-9]\.[0-9])', s)
        t = re.search('(?<!#)([0-9]\.[0-9])|(stereo)', s)
        if m != None:
            s2 = m.group(0).replace(".",":")
            print s2
        if t != None:
            t = t.group(0)
    return [s2,t]

def GetAudioMapStrings(info, track="0x80"):
    [map,type] = GetAudioMap(info)
    r = ["-map 0:0 -map %s" % (map,),]
    if type != "stereo":
        r.append("-map %s" % (map,))
    else:
        r.append("")
    return r

def get_source_length(info):
    #c = "ffmpeg -i %s" % (fn,)
    #p = Popen(c.split(),stdout=PIPE,stderr=STDOUT,
    #          shell=False,universal_newlines=True)
    #out = p.communicate()[0]
    #print type(out)
    #print out
    s = None
    for line in info.split("\n"):
        m = re.search(r"(?<=Duration:\s)([0-9]+:)+[0-9]+\.[0-9]+", line)
        if m != None:
            s = m.group(0)
    if s == None:
        #try using mplayer to get the length
        pass
    return s

if __name__ == "__main__":
    for file in sys.argv[1:]:
        print file
        global nfn = gen_output_filename(sys.argv[1])
        global sinfo = GetSourceInfo(file)
        global tframes =  ToFrames(get_source_length(sinfo))
        global audbitrate = "128kb"
        #print length
        #seconds = ToSeconds(length)
        #print seconds
        #frames = ToFrames(length)
        #print frames
        #maps = GetAudioMapStrings(sinfo)
        #print maps

        #f = open(nfn, "w+")
        #f.write("test")
        #f.close()


