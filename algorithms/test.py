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
    s = Sound.get_sound(id)
    
    print "Sound " + str(id) + " " + s['preview-hq-mp3']
    
    analysis = s.get_analysis(showall = True)
    analysis = level_filter(analysis, filter)

    return analysis


def computeBattle(id1, id2, descriptors):
    
    
    print "Battle: " + str(descriptors)
    
    as1 = getSoundAnalysisData(id1, descriptors)
    as2 = getSoundAnalysisData(id2, descriptors)
    
    filters = descriptors[0].split('.')
    
    if len(filters) == 1:
        v1 = as1[filters[0]]
        v2 = as2[filters[0]]
    elif len(filters) == 2:
        v1 = as1[filters[0]][filters[1]]
        v2 = as2[filters[0]][filters[1]]
    elif len(filters) == 3:
        v1 = as1[filters[0]][filters[1]][filters[2]]
        v2 = as2[filters[0]][filters[1]][filters[2]]
    elif len(filters) == 4:
        v1 = as1[filters[0]][filters[1]][filters[2]][filters[3]]
        v2 = as2[filters[0]][filters[1]][filters[2]][filters[3]]


    if v1 > v2:
        print "Sound " + str(id1) + " wins (" + str(v1) + " > " + str(v2) + ")" 
    elif v1 == v2:
        print "Tie (" + str(v1) + " = " + str(v2) + ")"
    else:
        print "Sound " + str(id2) + " wins (" + str(v2) + " > " + str(v1) + ")"

    print ""



LOUDNESS = [ 'lowlevel.average_loudness']
RHYTHM = [ 'rhythm.beats_loudness.mean']
TONALITY = [ 'tonal.key_strength']
#NOISINESS = 
#BRIGHTNESS = 


if __name__ == '__main__':
    print "Algortithms for fsWars\n---------------------\n"
    init()
    
    
    computeBattle(6,7,LOUDNESS)
    computeBattle(6,7,RHYTHM)
    computeBattle(6,7,TONALITY)