#!/usr/bin/env python

def test_unpack(*args, **keywords):
    print args,keywords
    for key in keywords.keys():
        print keywords[key]

l=range(10)
d=dict(a="hello",b="World!")
#the following shows the unpacking of a list and a dict into args and keywords 
test_unpack(*l,**d)
