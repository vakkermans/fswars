from freesound_python import *
import sys
import os
from algorithms_settings import key


# UTILS
def level_filter(d, fields, sep='.'):
    new_d = {}
    for f in fields:
        fs = f.split(sep)
        level_filter_set(new_d, fs, level_filter_get(d, fs))
    return new_d

def level_filter_set(d, levels, value):
    if len(levels) <= 0:
        return d
    if len(levels) == 1:
        d[levels[0]] = value
    else:
        if not d.has_key(levels[0]):
            d[levels[0]] = {}
        level_filter_set(d[levels[0]], levels[1:], value)
    return d

def level_filter_get(d, levels):
    if len(levels) <= 0:
        return d
    if len(levels) == 1:
        return d.get(levels[0], '')
    else:
        return level_filter_get(d[levels[0]], levels[1:])


def init():
    print "init()\n------"
    
    # Set API key
    Freesound.set_api_key(key)
    
    # Retrieve API key
    print "Freesound API key is: " + Freesound.get_api_key()    
    print "\n"


def getSoundAnalysisData(id, filter):
    s = Sound.get_sound(6)
    analysis = s.get_analysis(showall = True)
    
    analysis = level_filter(analysis, filter)
    
    return analysis


LOUDNESS_DESCRIPTORS = [ 'lowlevel.average_loudness']
RHYTHM_DESCRIPTORS = [ 'rhythm.beats_loudness.mean']
TONALITY_DESCRIPTORS = [ 'tonal.key_strength']



if __name__ == '__main__':
    print "Algortithms for fsWars\n---------------------\n"
    init()
    print getSoundAnalysisData(6,LOUDNESS_DESCRIPTORS)