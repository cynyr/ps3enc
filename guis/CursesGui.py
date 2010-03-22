from __future__ import print_function
from socket import socket,AF_INET,SOCK_DGRAM,timeout
import threading
import sys
from os.path import basename
import curses

def _fit_string(string,width):
    return string[:((width/2)-2)] + "..." + string[-((width/2)-2):]

def do_curses_gui(sock=None,hostname="localhost",port=36134)
    curses.wrapper(_do_curses_gui,sock=sock,hostname=hostname,port=port)

def _do_curses_gui(sock=None,hostname="localhost",port=36134):
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
