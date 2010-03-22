#!/usr/bin/env python
import sys
from optparse import OptionParser

parser = OptionParser()

parser.add_option("-g", "--gui",
                  action="store", dest="gui", default="qt",
                  help="enable the gui")
parser.add_option("-n", action="store", dest="num", help="the number of")

(options, args) = parser.parse_args()

print options
print args
