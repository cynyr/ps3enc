from __future__ import print_function
from socket import socket,AF_INET,SOCK_DGRAM,timeout
import threading
import sys
from os.path import basename
import curses

def _fit_string(string,width):
    return string[:((width/2)-2)] + "..." + string[-((width/2)-2):]

def do_curses_gui(sock=None,hostname="localhost",port=36134,callable=_do_curses_gui)
    curses.wrapper(callable,sock=sock,hostname=hostname,port=port)

def _do_curses_gui(stdscr,sock=None,hostname="localhost",port=36134):
     if not sock:
        sock=socket(AF_INET,SOCK_DGRAM)
        sock.bind((hostname,port))
        sock.settimeout(15)
    old_len = 0
    old_file_number = 1

    (y,x) = stdscr.getmaxyx()
    stdscr.addstr(y-2, 0, "Keybindings"+ " "*(x-10), curses.A_REVERSE)
    stdscr.addstr(y-1, 0, "q: Quit, p: Pause, s: restart" )
    stdscr.refresh()

    while threading.activeCount() > 1:
        try:
            data,addr = sock.recvfrom(1024)
        except timeout:
            print()
            sys.exit(3)
        if data:
            
