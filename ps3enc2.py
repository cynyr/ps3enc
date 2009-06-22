#!/usr/bin/env python
import os,sys
from time import time
from subprocess import Popen,PIPE,STDOUT
import re

global audio_bitrate
global crf
audio_bitrate = "256kb"
crf = "20"

def Main(files, sizeopts = None):
    filesn = len(files)
    for filenum in range(filesn):
        file = files[filenum]
        sys.stderr.write("Starting: " + file + "\n")
        nfn = gen_output_filename(file)
        sinfo = GetSourceInfo(file)
        tframes =  ToFrames(get_source_length(sinfo))
        ffmpeg_cmd = build_command_list(sinfo,file, nfn)
        #sys.stderr.write(" ".join(ffmpeg_cmd))
        proc = Popen(ffmpeg_cmd, stdout=PIPE,stderr=STDOUT,\
                     shell=False,universal_newlines=True)
        t1 = time()
        while proc.poll() == None:
            oline = proc.stdout.readline()
            #debug_print_output_line(oline)
            frame = re.search(r"(?<=frame=)\s*[0-9]+", oline)
            fps = re.search(r"(?<=fps=)\s*[0-9]+", oline)
            if frame != None and fps != None:
                frame = int(frame.group(0).strip())
                fps = int(fps.group(0).strip())
                #sys.stderr.write(fps)
                #sys.stderr.write(frame)
                if fps == 0:
                    fps = 1
                eta = int((tframes - frame)/ fps)
                percent = frame / tframes * 100
                #print [eta, percent]
                output(eta, percent, file, filenum +1, filesn)
        t2=time()
        sys.stdout.write(" "*79 + "\r")
        sys.stdout.write(file + " compleated in: " + sec_to_hms(str(t2-t1)))
        #print proc.poll()

def output(eta, percent, file, filenum=1, total_files=1):
    """output(eta, percent, file, filenum, total_files)
    "eta" in seconds, 
    "file" as a string, The name of the file
    "filenum" as an int, The current position in the list of files
    "total_files" as an int, The total number of files in the run

    To provide a different output type override this function.
    """
    sys.stdout.write("\r" + " " * 79 + "\r")
    sys.stdout.write("file " + str(filenum) + "/" + str(total_files))
    sys.stdout.write(" " + file)
    sys.stdout.write(" " + sec_to_hms(eta) + ", %3.2f%%" % (percent))

def sec_to_hms(seconds):
    """returns a string that is in HH:MM:SS from the seconds passed"""
    seconds = int(float(seconds))
    hours = seconds/3600
    minutes = (seconds%3600)/60
    secs = (seconds%3600)%60
    return "%0*d:%0*d:%0*d" % (2, hours, 2, minutes, 2, secs)


def debug_print_output_line(line):
    if line != "":
        print line.strip("\n")

def build_command_list(sinfo,src,dest):
    cmd = []
    cmd.extend(["nice", "-n", "20"])
    cmd.extend(["ffmpeg", "-i", src])
    maps = GetAudioMap(sinfo)
    #print maps
    cmd.extend(["-map", "0:0", "-map",maps[0]])
    cmd.extend(["-deinterlace", "-vcodec", "libx264", "-vpre"])
    cmd.extend(["hq", "-crf", crf, "-threads", "0", "-level", "41"])
    cmd.extend(["-acodec", "libfaac", "-ac", "6", "-ab", audio_bitrate])
    #comment this line after testing
    #cmd.extend(["-vframes", "3000", "-f", "rawvideo", "-y", "/dev/null"])
    #uncomment after testing
    cmd.append(dest)
    if maps[1] != "stereo" and maps[2] != "aac":
        cmd.extend(["-map", maps[0]])
        cmd.extend(["-acodec", "libfaac", "-ac", "2", "-ab", audio_bitrate])
        cmd.extend(["-newaudio",])

    return cmd

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
    time=s.split(':')
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
    """GetAudioMap(info), Returns [file:stream, type, codec] from the info)"""

    regex = '^\s*Stream.*\[' + track + '\].*$'
    ptr = re.compile(regex, re.MULTILINE)
    s = ptr.search(info)
    #print "Finding track 0x80 returned: %s" % (s,)
    s2 = None
    t=None
    c = None
    if s != None:
        s = s.group(0)
        m = re.search('(?<=#)([0-9]\.[0-9])', s)
        t = re.search('(?<!#)([0-9]\.[0-9])|(stereo)', s)
        c = re.search('(?<=Audio: )aac(?=,)', s)
        if m != None:
            s2 = m.group(0).replace(".",":")
        if t != None:
            t = t.group(0)
        if c != None:
            c = c.group(0)
    else:
        ptr = re.compile(r"^\s*Stream .*0.1.*:.*$", re.MULTILINE)
        s = ptr.search(info)
        if s != None:
            s2="0:1"
            t = re.search('(?<!#)([0-9]\.[0-9])|(stereo)', s.group(0))
            c = re.search('(?<=Audio: )aac(?=,)', s.group(0))
            if t != None:
                t = t.group(0)
            if c != None:
                c = c.group(0)
    return [s2,t,c]

def GetMapStrings(info, track="0x80"):
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
    Main(sys.argv[1:])
    #for file in sys.argv[1:]:
        #print file
        #global nfn = gen_output_filename(sys.argv[1])
        #global sinfo = GetSourceInfo(file)
        #global tframes =  ToFrames(get_source_length(sinfo))
        #global audbitrate = "128kb"
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


