from __future__ import print_function
"""ffmpegbase2 - A Python library for spawning a very specific ffmpeg thread"""
#__name__ = "ffmpegbase2"
__version__ = (0, 0, 2)
__author__ = "Andrew Frink <andrew.frink@gmail.com>"

try:
    import os
    import sys
    import re
    import threading
    from time import time
    from subprocess import Popen,PIPE,STDOUT
    from socket import socket,AF_INET,SOCK_DGRAM,timeout
except ImportError as err:
    print(err.args)

class _Mapping():
    """Audio Maping Data

    Provides a storage method for the audio mapping data and an easy way to
    pass it around.
    
    """
    def __init__(self):
        self.map = None
        self.channels = None
        self.codec = None
        self.stream_id = None

class Ffmpeg(threading.Thread):
    """Specific ffmpeg thread

    This class provides a specific set of options to ffmpeg. It uses popen to
    start up ffmpeg. This then communicates on a UDP port.

    """
    def __init__(self,files,host="localhost", port=36134,
                 abr="256kb",crf="22", scaleto=None, socket_=None,
                 output_dir="./", printcmd=True):
        """Ffmpeg(files, host, port, abr, crf, scaleto, socket_, output_dir,

                  printcmd)
        files as a iterable,
        host as a string, default "localhost"
        port as an int, defalt 36134
        abr as a string, default "256kb"
        crf as a string, default "22"
        scaleto as a string for a size ffmpeg recognises
        socket_ as a socket, needs to be a UDP socket.
        output_dir as a string, default = "./"
        printcmd as a boolean, default = True (for now)

        """
        threading.Thread.__init__(self)

        if not output_dir.endswith("/"):
            self.output_dir = "".join(self.output_dir, "/")
            #I wonder why is didn't just dir + "/" here.
        else:
            self.output_dir = output_dir

        self.extension = ".mp4"
        self.files = list(files)
        self.scaleto = str(scaleto)
        self.track_id = "0x80"
        #self.fps = 59.94
        self.ffmpeg = ["ffmpeg", "-i"]
        self.crf = ["-crf", str(crf)]
        self.video_preset = ["-vpre","hq"]
        self.video_codec = ["-vcodec","libx264"]
        self.audio_codec = ["-acodec", "libfaac"]
        self.main_channels = ["-ac", "6"]
        self.second_channels = ["-ac", "2"]
        self.audio_bitrate = ["-ab", str(abr)]
        self.video_map = ["-map", ]
        self.level = ["-level", "41"]
        self.threads = ["-threads", "0"]
        self.deinterlace = ["-deinterlace"]
        self.newaudio = ["-newaudio"]
        #used to test that the encoder, limits the length of the encode.
        self.test_settings = ["-vframes", "500", "-f", "rawvideo", "-y"]
        self.outputframerate = ["-r", "24000/1001"]
        self.printcmd = printcmd
        #setup the socket.
        if socket_:
            self._socket = socket_
        else:
            self._address = (str(host),int(port))
            self._socket = socket(AF_INET, SOCK_DGRAM)
            self._socket.connect(self._address)
    
    def add_file(self,file):
        """Appends a file to the list of files"""
        #this hasn't been tested yet.
        self.files.append(file)
    
    def output(self,eta,percent,file,currentfilenumber,totalfiles):
        """output(eta,percent,file,currentfilenumber,totalfiles)

        This sends the data down the socket, the format of the message is
        elements are seperated by "||".

        """
        data = "||".join((eta,percent,file,currentfilenumber,totalfiles))
        self._socket.send(data.encode())

    def get_video_map(self,source_info):
        """get_video_map(source_info)

        Parses the source file info and returns which stream the video is.
        source_info as returned by self.get_source_info()

        """
        m = re.search(r"(?<=\#)[0-9]\.[0-9](?=.*Video\:)", source_info)
        if m:
            return m.group(0)
        else:
            return "0:0"

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
        mapping_ = _Mapping()

        pattern = re.compile(re_track, re.MULTILINE)
        s = pattern.search(source_info)
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
                mapping_.map = ["-map", map.group(0)]
                mapping_.stream_id = map.group(0)
            if channels:
                mapping_.channels = channels.group(0)
            if codec:
                mapping_.codec = codec.group(0)
        return mapping_

    def get_command(self, source_info, source, destination, test=False):
        """get_command(sources_info,source,destination)

        builds the command to pass to popen.
        source_info as str returned by get_source_info()
        source as str - filename of the source
        destination as str - filename of the destination

        """
        self.video_map.append(self.get_video_map(source_info))
        cmd = []
        cmd.extend(self.ffmpeg + [source] + self.video_map)
        audio_map = self.get_audio_map(source_info)
        cmd.extend(audio_map.map)
        cmd.extend(self.deinterlace + self.video_codec + self.video_preset)
        cmd.extend(self.crf + self.threads + self.level + self.audio_codec)
        cmd.extend(self.main_channels + self.audio_bitrate)
        cmd.extend(self.outputframerate)
        if test:
            cmd.extend(self.test_settings)
        cmd.append(destination)
        if audio_map.channels != "stereo" and audio_map.codec != "aac":
            cmd.extend(audio_map.map + self.audio_codec)
            cmd.extend(self.second_channels + self.audio_bitrate)
            cmd.extend(self.newaudio)
        return cmd
    
    def get_source_info(self, source):
        """Returns ffmpeg info about source"""
        cmd = []
        cmd.extend(self.ffmpeg)
        cmd.append(source)

        p = Popen(cmd,stdout=PIPE,stderr=STDOUT,shell=False,
                  universal_newlines=True)
        return p.communicate()[0]
    
    def get_output_name(self, filename, test=False):
        """get_output_name(filename)

        Generates a unique file name for the output. This is done by appending
        current time from Epoch to the end of the name. 

        """
        #if we are in test mode, send null back.
        if test:
            return os.devnull
        basename = os.path.basename(filename)
        new_name = basename.split(".")[0] + self.extension
        if os.access(new_name, os.F_OK):
            key = "-" + str(time()).replace(".","")
            new_name = new_name.split(".")[0] + key + self.extension
        new_name = "".join([self.output_dir, new_name])
        return new_name

    def get_duration(self, source_info):
        """get_duration(source_info)

        finds the total duration and returns it as "hh:mm:ss.ss"
        source_info as returned by self.get_source_info()

        """
        #this is outputing the raw string from ffmpeg, if they change the 
        #output it will break
        pattern = re.compile(r"(?<=Duration:\s)([0-9]+:)+[0-9]+\.[0-9]+",
                             re.MULTILINE)
        s = pattern.search(source_info)
        duration = None
        if s:
            duration = s.group(0)
        else:
            #add using mplayer to get the duration here later
            pass
        return duration
                
    def get_source_fps(self,source_info):
        """get_source_fps(source_info)

        Returns 24000/1001. This is because the output framerate is now 
        specified as 24000/1001.

        """
        #fps = None
        #pattern = re.compile(r"[0-9]+\.[0-9]+(?=\stbr)", re.MULTILINE)
        #s = pattern.search(source_info)
        #if s:
            #fps = s.group(0)
        #--------------
        #Most Dvds seem to report the wrong framerate, and mpeg has no real 
        #framerate.
        #This just forces 24000/1001. This is only used for guessing at the
        #time left.
        #--------------
        fps = 23.97
        return fps

    def parse_ffmpeg_output(self,output_line,total_frames,duration):
        """parse_ffmpeg_output(output_line,total_frames):

        Returns (eta,percent) ETA based on total_frames/fps.
        percent based on total duration and curent position."""
        eta=0
        percent=0
        frame_number = re.search(r"(?<=frame=)\s*[0-9]+", output_line)
        fps = re.search(r"(?<=fps=)\s*[0-9]+", output_line)
        time = re.search(r"(?<=time=)\s*[0-9]+\.[0-9]+", output_line)
        if frame_number and fps and time:
            frame_number = int(frame_number.group(0).strip())
            fps = int(fps.group(0).strip())
            time = float(time.group(0).strip())
            #print([frame_number, fps, time, duration])
            if fps == 0:
                fps = 1
            frames_remaining = total_frames-frame_number
            eta = int(frames_remaining/fps)
            percent = (time/duration)*100

        return (eta,percent)
        
    def isotime_to_seconds(self,isotime):
        """isotime_to_seconds(isotime)

        makes "hh:mm:ss.ss" into seconds
        returns a float of the seconds. 

        """
        hours,minutes,seconds = isotime.split(":")
        seconds = float(seconds)
        seconds += float(hours) * 3600.0
        seconds += float(minutes) * 60.0
        return seconds

    def run(self):
        """run() called when self.start() is called. does the lifting"""

        for file in self.files:
            print("starting file: " + file)
            if not os.access(file, os.F_OK):
                break
            #self.output("1","2",file,str(self.files.index(file)+1),
            #            str(len(self.files)))
            source_info = self.get_source_info(file)
            dest_file_name = self.get_output_name(file)
            duration = self.get_duration(source_info)
            if not duration:
                break
            duration = self.isotime_to_seconds(duration)
            framerate = self.get_source_fps(source_info)
            #print("framerate: " + str(framerate))
            total_frames = duration * float(framerate)
            ffmpeg_command = self.get_command(source_info, file,
                                              dest_file_name)
            if self.printcmd:
                print(" ".join(ffmpeg_command))
            #time1 = time()
            ffmpeg_p = Popen(ffmpeg_command, stdout=PIPE,stderr=STDOUT,
                             shell=False,universal_newlines=True)
            while ffmpeg_p.poll() == None:
                output_line = ffmpeg_p.stdout.readline()
                #print(output_line)
                (eta,percent)=self.parse_ffmpeg_output(output_line,total_frames,duration)
                #self.output(eta,percent,file,currentfilenumber,totalfiles):
                self.output(str(eta),str(percent),file,
                            str(self.files.index(file)+1), 
                            str(len(self.files)))

            

if __name__ == "__main__":
    import sys
    from optparse import OptionParser
    p = OptionParser()
    p.add_option("-d", dest="dir", default="./",
                 help="Where to save the output files")
    (options, args) = p.parse_args()
    ff=Ffmpeg(args, output_dir=options.dir, printcmd=True)
    ff.start()
    sock = socket(AF_INET,SOCK_DGRAM)
    sock.bind(("localhost",36134))
    sock.settimeout(15)
    old_len = 0
    old_filenum = 1
    while threading.activeCount() > 1:
        try:
            data,addr = sock.recvfrom(1024)
        except timeout:
            print()
            sys.exit(3)
        if data:
            sys.stdout.write("\r" + " "*old_len)
            eta,percent,file,filenumber,totalfiles = data.decode().split("||")
            if int(filenumber) != old_filenum:
                print()
                old_filenum = int(filenumber)
            s = "\r%d/%d %03.02f%% %i left on %s" % (int(filenumber),
                                                  int(totalfiles),
                                                  float(percent),int(eta),
                                                  os.path.basename(file))
            old_len = len(s)
            sys.stdout.write(s)
    print()
        
