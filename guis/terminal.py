from __future__ import print_function
from socket import socket,AF_INET,SOCK_DGRAM,timeout
import threading
import sys
from os.path import basename

def hello_world():
    print("Hello World")

def humanize(seconds):
    if not isinstance(seconds,(int,float)):
        seconds = float(seconds)
    (minutes, seconds) = divmod(seconds, 60)
    (hours, minutes) = divmod(minutes, 60)
    return "%02d:%02d:%02d" % (hours,minutes,seconds)

def do_terminal_gui(sock=None,hostname="localhost",port=36134):
    if not sock:
        sock=socket(AF_INET,SOCK_DGRAM)
        sock.bind((hostname,port))
        sock.settimeout(15)
    old_len = 0
    old_file_number = 1

    while threading.activeCount() > 1:
        try:
            data,addr = sock.recvfrom(1024)
        except timeout:
            print("\nSocket read timed out, exiting . . .")
            sys.exit(3)
        if data:
            sys.stdout.write("\r" + " "*old_len)
            eta,percent,file,filenumber,totalfiles = data.decode().split("||")
            if int(filenumber) != old_file_number:
                print()
                old_file_number = int(filenumber)
            #s = "\r%d/%d %03.02f%% %i left on %s" % (int(filenumber),
            #                                      int(totalfiles),
            #                                      float(percent),int(eta),
            #                                      basename(file))
            s="\r%02.00f/%02.00f %03.02f%% %s left on %s"
            t=[float(x) for x in [filenumber, totalfiles, percent]]
            t.append(humanize(eta))
            t.append(basename(file))
            s=s % tuple(t)
            old_len = len(s)
            sys.stdout.write(s)
    print()

