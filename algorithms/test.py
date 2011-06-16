from freesound_python import *
import sys
import os
from algorithms_settings import key
import random
import webbrowser



# UTILS

def random_id():
    maxID = 100000
    r = int(random.random()*maxID)
    if r == 0:
        r = 1 
    return r
        
def displayWinner(id1,id2,v1,v2,winner):
    print "Sound 1: " + str(id1) + " (" + str(v1) + ")"
    print "Sound 2: " + str(id2) + " (" + str(v2) + ")"
    if winner == 1:
        print "Winner: " + str(id1)
    elif winner == 2:
        print "Winner: " + str(id2)
    else :
        print "Tie"

# INIT

def init():
    print "init()\n------"
    
    # Set API key
    Freesound.set_api_key(key)
    
    # Retrieve API key
    print "Freesound API key is: " + Freesound.get_api_key()    
    print "\n"


def getSoundAnalysisData(id):#, filter):
    s = Sound.get_sound(id)
    webbrowser.open(s['url']);
    analysis = s.get_analysis(showall = True)
    #analysis = level_filter(analysis, filter)

    return analysis, s['id']


def computeBattle(id1, id2, algorithm):
     
    as1, id1 = getSoundAnalysisData(id1)
    as2, id2 = getSoundAnalysisData(id2)
    
    winner, v1, v2 = algorithm(as1, as2)
    
    print "\n\nBattle: " + str(algorithm)
    displayWinner(id1,id2,v1,v2,winner)


def templateAlgorithm(analysis1, analysis2):
    b1 = analysis1['lowlevel']['spectral_centroid']['mean']
    b2 = analysis2['lowlevel']['spectral_centroid']['mean']
    
    value1 = b1
    value2 = b2
    
    if value1 > value2:
        return 1, value1, value2 # sound 1 wins
    elif value1 < value2:
        return 2, value1, value2 # Sound 2 wins
    else:
        return 0, value1, value2 # Tie


def brightness1Algorithm(analysis1, analysis2):
    b1 = analysis1['lowlevel']['spectral_centroid']['mean']
    b2 = analysis2['lowlevel']['spectral_centroid']['mean']
    
    value1 = b1
    value2 = b2
    
    if value1 > value2:
        return 1, value1, value2 # sound 1 wins
    elif value1 < value2:
        return 2, value1, value2 # Sound 2 wins
    else:
        return 0, value1, value2 # Tie


def brightness2Algorithm(analysis1, analysis2):
    b1 = analysis1['highlevel']['timbre']['all']['bright']
    b2 = analysis2['highlevel']['timbre']['all']['bright']
    
    value1 = b1
    value2 = b2
    
    if value1 > value2:
        return 1, value1, value2 # sound 1 wins
    elif value1 < value2:
        return 2, value1, value2 # Sound 2 wins
    else:
        return 0, value1, value2 # Tie


def darkness1Algorithm(analysis1, analysis2):
    d1 = analysis1['highlevel']['timbre']['all']['dark']
    d2 = analysis2['highlevel']['timbre']['all']['dark']
    
    value1 = d1
    value2 = d2
    
    if value1 > value2:
        return 1, value1, value2 # sound 1 wins
    elif value1 < value2:
        return 2, value1, value2 # Sound 2 wins
    else:
        return 0, value1, value2 # Tie

def noisiness1Algorithm(analysis1, analysis2):
    n1 = analysis1['lowlevel']['spectral_flatness_db']['mean']
    n2 = analysis2['lowlevel']['spectral_flatness_db']['mean']
    
    value1 = n1
    value2 = n2
    
    if value1 > value2:
        return 1, value1, value2 # sound 1 wins
    elif value1 < value2:
        return 2, value1, value2 # Sound 2 wins
    else:
        return 0, value1, value2 # Tie



if __name__ == '__main__':
    print "Algortithms for fsWars\n---------------------\n"
    init()
    
    id1 = random_id()
    id2 = random_id()
    
    computeBattle(id1,id2,noisiness1Algorithm)
