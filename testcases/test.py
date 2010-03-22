#!/usr/bin/env python
from __future__ import print_function
import ConfigParser
import re
from optparse import OptionParser

class Configcls():
    pass

def add_option(option, opt_str, value, parser, configcls):
    print(option.dest,value)
    setattr(configcls,option.dest,value)

cfgcls = Configcls()
p = OptionParser()
p.add_option("-g", "--gui", dest="gui", help="Which gui to use, Term or QT",
             action="callback", callback=add_option, callback_args=(cfgcls,),
             nargs=1, type="string")
p.add_option("-c", "--config", dest="configfile",
             help="Use this config file instead of the system ones.")

config = ConfigParser.ConfigParser()
config.read(["testconfig.txt"])
options = config.items("config")
for name,val in options:
    s = re.search(r"^[\w\s]+[^\w\#]?",val)
    if s:
        s = s.group(0).strip()
        setattr(cfgcls, name, s)
        print(name,s)
(options, args) = p.parse_args()
print(options.configfile)
print(dir(cfgcls))
print(cfgcls.gui)

