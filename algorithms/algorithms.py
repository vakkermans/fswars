try:
    from freesound_python import *
except ImportError:
    from freesound import *
    
from api_key import key
import random
import webbrowser
import math
import numpy
import sys
import os


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

def getSoundAnalysisData(id):
    
    s = Sound.get_sound(id)
    #webbrowser.open(s['url']);
    analysis = s.get_analysis(showall = True)

    return analysis, s['id']

# INIT

def init():
    print "init()\n------"
    
    # Set API key
    Freesound.set_api_key(key)
    
    # Retrieve API key
    print "Freesound API key is: " + Freesound.get_api_key()    
    print "\n"


# ALGORITHMS

def templateAlgorithm(analysis1, analysis2):
    b1 = analysis1['lowlevel']['spectral_centroid']['mean']
    b2 = analysis2['lowlevel']['spectral_centroid']['mean']
    
    value1 = b1
    value2 = b2
    
    if math.fabs(value1-value2) < TIE_THRESHOLD :
        value2 = value1 # Make them tie
        
    if value1 > value2:
        return 1, value1, value2 # sound 1 wins
    elif value1 < value2:
        return 2, value1, value2 # Sound 2 wins
    else:
        return False, value1, value2 # Tie


def brightnessAlgorithm(analysis1, analysis2):
    b1 = analysis1['lowlevel']['spectral_centroid']['mean']
    b2 = analysis2['lowlevel']['spectral_centroid']['mean']
    
    value1 = b1
    value2 = b2
    
    if math.fabs(value1-value2) < TIE_THRESHOLD :
        value2 = value1 # Make them tie
    
    if value1 > value2:
        return 1, value1, value2 # sound 1 wins
    elif value1 < value2:
        return 2, value1, value2 # Sound 2 wins
    else:
        return False, value1, value2 # Tie


def brightness2Algorithm(analysis1, analysis2):
    b1 = analysis1['highlevel']['timbre']['all']['bright']
    b2 = analysis2['highlevel']['timbre']['all']['bright']
    
    value1 = b1
    value2 = b2
    
    if math.fabs(value1-value2) < TIE_THRESHOLD :
        value2 = value1 # Make them tie
    
    if value1 > value2:
        return 1, value1, value2 # sound 1 wins
    elif value1 < value2:
        return 2, value1, value2 # Sound 2 wins
    else:
        return False, value1, value2 # Tie


def noisinessAlgorithm(analysis1, analysis2):

    flatness1 = analysis1['lowlevel']['spectral_flatness_db']['mean']
    flatness2 = analysis2['lowlevel']['spectral_flatness_db']['mean']
   
    kurtosis1 = analysis1['lowlevel']['spectral_kurtosis']['mean']
    kurtosis2 = analysis2['lowlevel']['spectral_kurtosis']['mean']
   
    inharmonicity1 = analysis1['sfx']['inharmonicity']['mean']
    inharmonicity2 = analysis2['sfx']['inharmonicity']['mean']

    dissonance1 = analysis1['lowlevel']['dissonance']['mean']
    dissonance2 = analysis2['lowlevel']['dissonance']['mean']    

    value1 = ((1-flatness1)+dissonance1)/2
    value2 = ((1-flatness2)+dissonance2)/2
   
    if math.fabs(value1-value2) < TIE_THRESHOLD :
        value2 = value1 # Make them tie
    
    if value1 > value2:
        return 1, value1, value2 # sound 1 wins
    elif value1 < value2:
        return 2, value1, value2 # Sound 2 wins
    else:
        return False, value1, value2 # Tie




def tonalAlgorithm(analysis1, analysis2):
    n1 = analysis1['tonal']['key_strength']
    n2 = analysis2['tonal']['key_strength']
    
    value1 = n1
    value2 = n2
    
    if math.fabs(value1-value2) < TIE_THRESHOLD :
        value2 = value1 # Make them tie
    
    if value1 > value2:
        return 1, value1, value2 # sound 1 wins
    elif value1 < value2:
        return 2, value1, value2 # Sound 2 wins
    else:
        return False, value1, value2 # Tie


def loudnessAlgorithm(analysis1, analysis2):

    loudness1 = analysis1['lowlevel']['average_loudness']
    loudness2 = analysis2['lowlevel']['average_loudness']
    midhigh1 = analysis1['lowlevel']['spectral_energyband_middle_high']['mean']
    midhigh2 = analysis2['lowlevel']['spectral_energyband_middle_high']['mean']
   
    value1 = loudness1*midhigh1
    value2 = loudness2*midhigh2

    if math.fabs(value1-value2) < TIE_THRESHOLD :
        value2 = value1 # Make them tie
   
    if value1 > value2:
        return 1, value1, value2 # sound 1 wins
    elif value1 < value2:
        return 2, value1, value2 # Sound 2 wins
    else:
        return False, value1, value2 # Tie
   

def rhythmRegularityAlgorithm(analysis1, analysis2):
    b1 = analysis1['rhythm']['bpm_estimates']
    b2 = analysis2['rhythm']['bpm_estimates']
   
    value1 = numpy.std(b1)
    value2 = numpy.std(b2)

    if abs(value1-value2) < 0.05:
        value1 = -analysis1['rhythm']['beats_loudness']['mean']
        value2 = -analysis2['rhythm']['beats_loudness']['mean']
    
    if (value1==0 or value2==0) and (value1<>value2):
        if value1==0:
            return 2, value1,value2
        else:
            return 1, value1,value2
    
    if math.fabs(value1-value2) < TIE_THRESHOLD :
        value2 = value1 # Make them tie
        
    if value1 < value2:
        return 1, value1, value2 # sound 1 wins
    elif value1 > value2:
        return 2, value1, value2 # Sound 2 wins
    else:
        return False, value1, value2 # Tie


# BATTLES

TIE_THRESHOLD = 0.0
ALGORITHM_CLASSES = { 'LOUDNESS': loudnessAlgorithm,
                      'BRIGHTNESS': brightness2Algorithm,
                      'TONAL': tonalAlgorithm,
                      'NOISINESS': noisinessAlgorithm,
                      'RHYTHM': rhythmRegularityAlgorithm
                    }

def computeBattle(id1, id2, algorithm):
     
    as1, id1 = getSoundAnalysisData(id1)
    as2, id2 = getSoundAnalysisData(id2)
    
    winner, v1, v2 = algorithm(as1, as2)
    points = 10 + int(abs(v1 - v2) * 100)
    
    result = {'winner': winner,
              'points': points
              }
    
    print "\n\nBattle: " + str(algorithm)
    #displayWinner(id1,id2,v1,v2,winner)
    print result
    
    return result
    

if __name__ == '__main__':
    print "Algorithms for fsWars\n---------------------\n"
    init()
    id1 = random_id()
    id2 = random_id()
    
    computeBattle(id1,id2, ALGORITHM_CLASSES['RHYTHM'] )
    computeBattle(id1,id2, ALGORITHM_CLASSES['BRIGHTNESS'] )
    computeBattle(id1,id2, ALGORITHM_CLASSES['TONAL'] )
    computeBattle(id1,id2, ALGORITHM_CLASSES['NOISINESS'] )
    computeBattle(id1,id2, ALGORITHM_CLASSES['LOUDNESS'] )
    
