from __future__ import print_function
from socket import socket,AF_INET,SOCK_DGRAM,timeout
import threading
import sys
from os.path import basename

def hello_world():
    print("Hello World")

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
            print()
            sys.exit(3)
        if data:
            sys.stdout.write("\r" + " "*old_len)
            eta,percent,file,filenumber,totalfiles = data.decode().split("||")
            if int(filenumber) != old_file_number:
                print()
                old_file_number = int(filenumber)
            s = "\r%d/%d %03.02f%% %i left on %s" % (int(filenumber),
                                                  int(totalfiles),
                                                  float(percent),int(eta),
                                                  basename(file))
            old_len = len(s)
            sys.stdout.write(s)
    print()

