#!/usr/bin/env python
import os,sys
from time import time
from subprocess import Popen,PIPE,STDOUT
import re
from optparse import OptionParser

class Ffmpeg():
    def __init__(self,abr="256kb",crf="22"):
        self.audio_bitrate = abr
        self.crf = crf

    def Main(self,files, sizeopts = None):
        filesn = len(files)
        for filenum in range(filesn):
            file = files[filenum]
            sys.stderr.write("Starting: " + file + "\n")
            nfn = self.gen_output_filename(file)
            sinfo = self.GetSourceInfo(file)
            tframes =  self.ToFrames(self.get_source_length(sinfo))
            ffmpeg_cmd = self.build_command_list(sinfo,file, nfn)
            #print ffmpeg_cmd
            #sys.stderr.write(" ".join(ffmpeg_cmd))
            self.proc = Popen(ffmpeg_cmd, stdout=PIPE,stderr=STDOUT,\
                        shell=False,universal_newlines=True)
            t1 = time()
            while self.proc.poll() == None:
                oline = self.proc.stdout.readline()
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
                    self.output(eta, percent, file, filenum +1, filesn)
            t2=time()
            #sys.stdout.write(" "*79 + "\r")
            #sys.stdout.write(file + " compleated in: " + sec_to_hms(str(t2-t1)))
            #print proc.poll()
            self.output_total(file,t2-t1)
    
    def output_totals(self,file, total_time):
        """output_totals(file,seconds)"""
        pass
    
    def output(self, eta, percent, file, filenum=1, total_files=1):
        """output(eta, percent, file, filenum, total_files)
        "eta" in seconds, 
        "file" as a string, The name of the file
        "filenum" as an int, The current position in the list of files
        "total_files" as an int, The total number of files in the run
    
        To provide a different output type override this function.
        """
        pass
    
    def sec_to_hms(self, seconds):
        """returns a string that is in HH:MM:SS from the seconds passed"""
        seconds = int(float(seconds))
        hours = seconds/3600
        minutes = (seconds%3600)/60
        secs = (seconds%3600)%60
        return "%0*d:%0*d:%0*d" % (2, hours, 2, minutes, 2, secs)
    
    
    def debug_print_output_line(self, line):
        if line != "":
            print line.strip("\n")
    
    def build_command_list(self, sinfo,src,dest):
        cmd = []
        cmd.extend(["nice", "-n", "20"])
        cmd.extend(["ffmpeg", "-i", src])
        maps = self.GetAudioMap(sinfo)
        #print maps
        cmd.extend(["-map", "0:0", "-map",maps[0]])
        cmd.extend(["-deinterlace", "-vcodec", "libx264", "-vpre"])
        cmd.extend(["normal", "-crf", self.crf, "-threads", "0", "-level", "41"])
        cmd.extend(["-acodec", "libfaac", "-ac", "6", "-ab",])
        cmd.extend([self.audio_bitrate])
        #comment this line after testing
        #cmd.extend(["-vframes", "3000", "-f", "rawvideo", "-y", "/dev/null"])
        #uncomment after testing
        cmd.append(dest)
        if maps[1] != "stereo" and maps[2] != "aac":
            cmd.extend(["-map", maps[0]])
            cmd.extend(["-acodec", "libfaac", "-ac", "2", "-ab",])
            cmd.extend([self.audio_bitrate, "-newaudio",])
    
        return cmd
    
    def gen_output_filename(self, inname):
        """Generate an output file name, checking for collisions"""
    
        fname = os.path.split(inname)[1]
        nfn = fname.split(".")[0] + ".mp4"
        if not os.access("./" + nfn, os.F_OK):
            return nfn
        else:
            return nfn.split(".")[0] + "".join(str(time()).split(".")) + ".mp4"
    
    def ToSeconds(self, s):
        """ToSeconds(string), "01:23:78.8" and converts it to seconds"""
        time=s.split(':')
        seconds=int(time[0])*3600
        seconds+= int(time[1])*60 
        seconds+= float(time[2])
        return seconds
    
    def ToFrames(self, f):
        """ToFrames(f), converts the "time" to a number of frames.
    
        ToFrames(float/int), returns float * 29.97
        ToFrames(str), passes str to ToSeconds(str) and finds the
            the total frames from that."""
        if type(f) == type(2.2):
            #return f*29.97
            #framrate is hardcoded at the moment, this needs to fixed
            #The framerate should be found on a per file basis.
            return f*59.94
        elif type(f) == type(""):
            #return ToSeconds(f)*29.97
            return self.ToSeconds(f)*29.97
    
    def GetSourceInfo(self, fn):
        """Returns ffmpegs info about the file"""
    
        c = ["ffmpeg", "-i", fn]
        p = Popen(c,stdout=PIPE,stderr=STDOUT,
                shell=False,universal_newlines=True)
        return p.communicate()[0]
    
    def GetAudioMap(self, info, track="0x80"):
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
        print [s2,t,c]
        return [s2,t,c]
    
    def GetMapStrings(self, info, track="0x80"):
        [map,type] = self.GetAudioMap(info)
        r = ["-map 0:0 -map %s" % (map,),]
        if type != "stereo":
            r.append("-map %s" % (map,))
        else:
            r.append("")
        return r
    
    def get_source_length(self, info):
        s = None
        for line in info.split("\n"):
            m = re.search(r"(?<=Duration:\s)([0-9]+:)+[0-9]+\.[0-9]+", line)
            if m != None:
                s = m.group(0)
        if s == None:
            #try using mplayer to get the length
            pass
        return s
    

