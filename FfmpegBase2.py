#!/usr/bin/env python

try:
    import os
    import sys
    import re
    import threading
    from time import time
    from subprocess import Popen,PIPE,STDOUT
    from socket import socket,AF_INET,SOCK_DGRAM
except ImportError,why:
    print why

class mapping():
    def __init__(self):
        self.map = None
        self.channels = None
        self.codec = None
        self.stream_id = None

class Ffmpeg(threading.Thread):
    def __init__(self,files,host="localhost", port=36134,
                 abr="256kb",crf="22", scaleto=None, socket_=None):
        threading.Thread.__init__(self)
        self.files = list(files)
        self.scaleto = str(scaleto)
        self.track_id = "0x80"
        self.fps = 59.94
        self.ffmpeg = ["ffmpeg", "-i"]
        self.crf = ["-crf", str(crf)]
        self.video_preset = ["-vpre","normal"]
        self.video_codec = ["-vcodec","libx264"]
        self.audio_codec = ["-acodec", "libfaac"]
        self.main_channels = ["-ac", "6"]
        self.second_channels = ["ac", "2"]
        self.audio_bitrate = ["-ab", str(abr)]
        self.video_map = ["-map", "0:0"]
        self.level = ["-level", "41"]
        self.theads = ["-threads", "0"]
        self.deinterlace = ["-deinterlace"]
        self.newaudio = ["-newaudio"]
        self.test_settings = ["-vframes", "3000", "-f", "rawvideo", "-y"]
        
        self._address = (str(host),int(port))
        if socket_:
            self._socket = socket_
        else:
            self._socket = socket(AF_INET, SOCK_DGRAM)
    
    def add_file(self,file):
        self.files.append(file)
    
    def output(self,eta,percent,file,currentfilenumber,totalfiles):
        data = "||".join((eta,percent,file,currentfilenumber,totalfiles))
        print data
        print self._address
        self._socket.sendto(data,self._address)

    def get_audio_map(self,source_info,):
        """get_audio_map(source_info,track="0x80")

        Returns a mapping object using info.
        trys to find the track specified, defaults to the first audio
        track otherwise.
        
        """
        re_codec = r"(?<=Audio: ).*?(?=,)"
        re_map = r"(?<=#)([0-9]\.[0-9])"
        re_channels = r"(?<!#)([0-9]\.[0-9])|(stereo)"
        re_track = "^\s*Stream.*\[" + self.track_id + r"\].*$"
        re_audio1 = r"^\s*Stream.*Audio.*$"
        mapping_ = mapping()

        pattern = re.compile(re_track, re.MULTILINE)
        s = pattern.search(source_info)
        print s

        if s:
            s = s.group(0)
        else:
            pattern = re.compile(re_audio1, re.MULTILINE)
            s = pattern.search(source_info)
            if s:
                s = s.group(0)
        
        if s:
            map = re.search(re_map, s)
            channels = re.search(re_channels, s)
            codec = re.search(re_codec, s)
            if map:
                mapping_.map = ["-map", map.group(0).replace(".",":")]
                mapping_.stream_id = map.group(0).replace(".",":")
            if channels:
                mapping_.channels = channels.group(0)
            if codec:
                mapping_.codec = codec.group(0)
        return mapping_


    def get_command(self, source_info, source, destination):
        """get_command(sources_info,source,destination)

        builds the command to pass to popen.
        source_info as str returned by get_source_info()
        source as str - filename of the source
        destination as str - filename of the destination

        """
        cmd = []
        cmd.extend(self.ffmpeg + [source] + self.video_map)
        audio_map = self.get_audio_map(source_info)
        print audio_map.map
        cmd.extend(audio_map.map)

        return cmd
    
    def get_source_info(self, source):
        """Returns ffmpeg info about source"""
        cmd = []
        cmd.extend(self.ffmpeg)
        cmd.append(source)

        p = Popen(cmd,stdout=PIPE,stderr=STDOUT,shell=False,
                  universal_newlines=True)
        return p.communicate()[0]

    def run(self):
        for file in self.files:
            #self.output("1","2",file,str(self.files.index(file)+1),
            #            str(len(self.files)))
            source_info = self.get_source_info(file)
            print self.get_command(source_info, file, "./foo")
            pass

if __name__ == "__main__":
    import sys
    ff=Ffmpeg(sys.argv[1:])
    ff.start()
