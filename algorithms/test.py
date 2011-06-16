from freesound_python import *
import sys
import os

key = "fcbbed20c2114502b72bd6d9546f94da"

def init():
    print "init()\n------"
    
    # Set API key
    Freesound.set_api_key(key)
    
    # Retrieve API key
    print "Freesound API key is: " + Freesound.get_api_key()    
    print "\n"

    s = Sound.get_sound(6)
    s.get_analysis()
    print s

#s.retrieve_analysis_frames(".")
#s.retrieve_analysis_frames(^_^)
#sounds=Sound.search(q="cat")



if __name__ == '__main__':
    print "Algortithms for fsWars\n---------------------\n"
    init()