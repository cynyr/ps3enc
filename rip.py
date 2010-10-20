#!/usr/bin/env python
format = {'fmt':'mpeg','ext':'.mpeg'}
import os
import re
import sys
from optparse import OptionParser
from subprocess import call,Popen,STDOUT,PIPE
from time import sleep,time

class ripper():
    def __init__(self,options = None):
        """ Options is the (options,args) tuple optparse.
        if not provided will be aquired automaticly"""
        if options == None:
            (self.options,self.args) = self.get_args()
        else:
            (self.options,self.args) = options
        print format
    def run(self,):
        while True:
            self.drvclose()
            sleep(12)
            self.lsdvd = self.get_lsdvd_output()
            if self.lsdvd != None:
                self.title = self.get_title(self.lsdvd)
                #print self.title
                self.track = self.get_longest_track(self.lsdvd)
                #print self.track
                self.fn = self.gen_file_name()
                #print self.fn
                me_cmd = []
                me_cmd.extend(['mencoder', 'dvdnav://' + str(self.track), '-oac'])
                me_cmd.extend(['copy', '-msglevel', 'all=-1'])
                me_cmd.extend(['-ovc', 'copy', '-alang', 'en', '-channels', ])
                me_cmd.extend(['6', '-of', format["fmt"], '-o', self.fn])
                print " ".join(me_cmd)
    
                p = Popen(me_cmd, stdout=PIPE, stderr=STDOUT, shell=False)
                p.wait()
            else:
                print "failed to read disk, try again or insert a new one"
                
            self.drvopen()
            raw_input("Press enter to start next disk")

    def gen_file_name(self,):
        nfn = self.title + format["ext"]
        if not os.access("./" + nfn, os.F_OK):
            return nfn
        else:
            return nfn.split(".")[0] + "".join(str(time()).split(".")) + ".mpeg"

    def drvclose(self):
        call(["eject", "-t", self.options.dev])
    def drvopen(self):
        call(["eject", self.options.dev])
        
    def get_args(self,):
        p = OptionParser()
        p.add_option("--D", "--device", dest="dev", default="/dev/dvd",
                    help="which device to rip from.\n\tDefault: /dev/dvd")
        return p.parse_args()

    def get_lsdvd_output(self,):
        cmd=[]
        cmd.extend(["lsdvd",self.options.dev])
        p = Popen(cmd, stdout=PIPE, stderr=STDOUT,shell=False)
        return p.communicate()[0]

    def get_longest_track(self,s):
        track = re.search('(?<=^Longest track: )[0-9]{2}',s, re.MULTILINE)
        if track != None:
            track = int(track.group(0))
        return track

    def get_title(self,s):
        regex = '(?<=^Disc Title: ).*$'
        ptr = re.compile(regex, re.MULTILINE)
        title = ptr.search(s)
        if title != None:
            title = title.group(0).title().replace("_", " ")
        return title

if __name__ == "__main__": 
    r = ripper()
    r.run()

