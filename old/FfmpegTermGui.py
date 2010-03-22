#!/usr/bin/env python

import sys
from Ffmpeg_Base import Ffmpeg

class FfmpegTermGui(Ffmpeg):
    def __init__(self,abr="256kb",crf="20"):
        Ffmpeg.__init__(self,abr,crf)

    def output_total(self,file, total_time):
        """output_totals(file,seconds)
    
        prints the file name and total time taken to stdout"""
        print
        print file + " compleated in: " + self.sec_to_hms(str(total_time))
    
    def output(self, eta, percent, file, filenum=1, total_files=1):
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
        sys.stdout.write(" " + self.sec_to_hms(eta) + ", %3.2f%%" % (percent))
