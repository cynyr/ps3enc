#!/usr/bin/python

import sys
import re
from subprocess import Popen,PIPE,STDOUT

def get_output_line(p):
    output_line=[]
    while True:
        o=p.stdout.read(1)
        if o == "\r" or o == "\n":
            break
        else:
            output_line.append(o)
    return "".join(output_line)

command="ffmpeg -i %s -an -pass 1 -vcodec libx264 -vpre fastfirstpass -b 2000kb -bt 200kb -threads 0 -level 41 -vframes 1000 -f rawvideo -y /dev/null" % sys.argv[1]
#command = "ffmpeg -i %s -vcodec copy -acodec copy /dev/null" % (sys.argv[1])
p = Popen(command.split(),stdout=PIPE,stderr=STDOUT,shell=False,universal_newlines=True)
_NON_ASCII = re.compile('[^ -~]')

re_framenum=re.compile(r"(?<=frame=)\s+[0-9]+")

while p.poll() == None:
    linem = p.communicate()[0][-1]
    print linem
    #line = get_output_line(p)
    if linem.count(' ') > 0:
        line = linem.split()
        #if line[0] == 'frame=':
        framenum = re_framenum.search(linem)
        if framenum != None:
            #print line
            time = int(line[7].split('=')[1].split('.')[0])
            #if time >= 15:
                #break
            #print time
            if total_seconds != None:
                percent = float(time)/float(total_seconds) * 100.0
                print "%3.2f %%" % (percent,)
                frame = int(framenum.group(0)) #int(line[1])
                print "Frame: %i" %(frame)
                fps= int(line[3])
                if fps == 0:
                    fps = 1
                remaining_frames = total_frames - frame
                eta = remaining_frames/fps
                print repr(eta) + " seconds remaining"
    
    
        if line[0] == 'Duration:':
            duration_string = line[1].rstrip(',')
            d = duration_string.split(':')
            s = int(d[2].split('.')[0])
            total_seconds = int((int(d[0])  *60 + int(d[1])) * 60 + s)
            print total_seconds
            total_frames = int(total_seconds * 29.97)
            print total_frames
#p.communicate("q")    
sys.exit()
