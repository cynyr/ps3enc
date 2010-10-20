#!/usr/bin/env python
from __future__ import print_function
from subprocess import Popen,PIPE,STDOUT
import re,sys

class Mediainfo():
    pass

def get_source_interlace(source):
    p = Popen(["mediainfo", source], stdout=PIPE, stderr=STDOUT,shell=False,
              universal_newlines=True)
    out = p.communicate()[0]
    #print(out)
    re_scantype=r"(?<=Scan type                        : ).*?$"
    p = re.compile(re_scantype, re.MULTILINE)
    s = p.search("".join(out))
    print(s)
    if s:
        scantype = s.group(0))
    



if __name__ == "__main__":
    get_source_interlace(sys.argv[1])
