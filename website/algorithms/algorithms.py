try:
    from freesound_python import *
except ImportError:
    from freesound import *

from django.conf import settings
import random
import webbrowser
import math
import numpy
import sys
import os

TIE_THRESHOLD = 0.0


# generate random sound ID for testing
def random_id():
    maxID = 100000
    r = int(random.random()*maxID)
    if r == 0:
        r = 1
    return r

# print the result
def display_winner(id1,id2,v1,v2,winner):
    print "Sound 1: " + str(id1) + " (" + str(v1) + ")"
    print "Sound 2: " + str(id2) + " (" + str(v2) + ")"
    if winner == 1:
        print "Winner: " + str(id1)
    elif winner == 2:
        print "Winner: " + str(id2)
    else :
        print "Tie"


def get_sound_analysis_data(id):
    s = Sound.get_sound(id)
    return s.get_analysis(showall = True), s['id']


def init():
    Freesound.set_api_key(settings.API_KEY)


def __apply_threshold(value1, value2, use_threshold=True):
    if use_threshold:
        if math.fabs(value1-value2) < TIE_THRESHOLD :
            value2 = value1 # Make them tie

    if value1 > value2:
        return 1, value1, value2 # sound 1 wins
    elif value1 < value2:
        return 2, value1, value2 # Sound 2 wins
    else:
        return False, value1, value2 # Tie


def brightness_algorithm(analysis1, analysis2):
    value1 = float(analysis1['lowlevel']['spectral_centroid']['mean'])
    value2 = float(analysis2['lowlevel']['spectral_centroid']['mean'])
    return __apply_threshold(value1, value2)


def brightness_algorithm_2(analysis1, analysis2):
    value1 = float(analysis1['highlevel']['timbre']['all']['bright'])
    value2 = float(analysis2['highlevel']['timbre']['all']['bright'])
    return __apply_threshold(value1, value2)


def noisiness_algorithm(analysis1, analysis2):
    # spectral flatness
    flatness1 = float(analysis1['lowlevel']['spectral_flatness_db']['mean'])
    flatness2 = float(analysis2['lowlevel']['spectral_flatness_db']['mean'])
    # spectral kurtosis
    kurtosis1 = float(analysis1['lowlevel']['spectral_kurtosis']['mean'])
    kurtosis2 = float(analysis2['lowlevel']['spectral_kurtosis']['mean'])
    # key strength (to filter out tonal sounds)
    keystrength1 = float(analysis1['tonal']['key_strength'])
    keystrength2 = float(analysis2['tonal']['key_strength'])
    # amount of silent frames
    silencerate1 = float(analysis1['lowlevel']['silence_rate_60dB']['mean'])
    silencerate2 = float(analysis2['lowlevel']['silence_rate_60dB']['mean'])
    # dissonance measure
    dissonance1 = float(analysis1['lowlevel']['dissonance']['mean'])
    dissonance2 = float(analysis2['lowlevel']['dissonance']['mean'])

    # more weight is placed on flatness
    value1 = ((2.0*(1.0-flatness1))+dissonance1+(1.0-keystrength1)+(1.0-silencerate1))/5.0
    value2 = ((2.0*(1.0-flatness2))+dissonance2+(1.0-keystrength2)+(1.0-silencerate2))/5.0

    return __apply_threshold(value1, value2)


def tonal_algorithm(analysis1, analysis2):
    # simple, just the key strength
    value1 = float(analysis1['tonal']['key_strength'])
    value2 = float(analysis2['tonal']['key_strength'])
    return __apply_threshold(value1, value2)


def loudness_algorithm(analysis1, analysis2):
    #root mean square spectral energy instead of loudness
    loudness1 = float(analysis1['lowlevel']['spectral_rms']['mean'])
    loudness2 = float(analysis2['lowlevel']['spectral_rms']['mean'])
    # pseudonormalized based on the 'max' value
    loudness1 = loudness1/0.0025
    loudness2 = loudness2/0.0025

    midhigh1 = float(analysis1['lowlevel']['spectral_energyband_middle_high']['mean'])
    # ditto
    midhigh1 = midhigh1/0.004
    midhigh2 = float(analysis2['lowlevel']['spectral_energyband_middle_high']['mean'])
    # ditto
    midhigh2 = midhigh2/0.004
    silencerate1 = float(analysis1['lowlevel']['silence_rate_60dB']['mean'])
    silencerate2 = float(analysis2['lowlevel']['silence_rate_60dB']['mean'])

    # more weight on spectral rms
    value1 = (2.0*loudness1+midhigh1+(0.5*(1.0-silencerate1)))/3.5
    value2 = (2.0*loudness2+midhigh2+(0.5*(1.0-silencerate2)))/3.5

    return __apply_threshold(value1, value2)


def rhythm_regularity_algorithm(analysis1, analysis2):

    #get the standard deviation of all estimated BPMs (regularity of estimated BPMs)
    bpm1 = numpy.std(analysis1['rhythm']['bpm_estimates'])
    bpm2 = numpy.std(analysis2['rhythm']['bpm_estimates'])

    #get the weight of the first BPM peak (salience of rhythm)
    weight1 = float(analysis1['rhythm']['first_peak_weight'])
    weight2 = float(analysis2['rhythm']['first_peak_weight'])

    value1 = bpm1
    value2 = bpm2;

    # if estimated BPM is suspiciously low, check for the peak weight
    if bpm1<0.09 or bpm2<0.09:
        value1 = (1.0-weight1)*bpm1
        value2 = (1.0-weight2)*bpm2

    # if the difference is too small, rely on the loudness of the beats
    if abs(value1-value2)<0.05:
        value1 = -1.0 * float(analysis1['rhythm']['beats_loudness']['mean'])
        value2 = -1.0 * float(analysis2['rhythm']['beats_loudness']['mean'])

    # if one of the values is zero, just give the win to the other one
    if (value1==0.0 or value2==0.0) and (value1 != value2):
        if value1==0.0:
            return 2, value1, value2
        else:
            return 1, value1, value2

    return __apply_threshold(value1, value2, False)



ALGORITHM_CLASSES = { 'LOUDNESS': loudness_algorithm,
                      'BRIGHTNESS': brightness_algorithm_2,
                      'TONAL': tonal_algorithm,
                      'NOISINESS': noisiness_algorithm,
                      'RHYTHM': rhythm_regularity_algorithm
                    }



def computeBattle(id1, id2, algorithm):

    as1, id1 = get_sound_analysis_data(id1)
    as2, id2 = get_sound_analysis_data(id2)

    winner, v1, v2 = algorithm(as1, as2)

    # invert negative values
    v1 = abs(v1)
    v2 = abs(v2)

    # normalize values to calculate points
    v1 = v1/max(v1,v2)
    v2 = v2/max(v1,v2)

    points = 10.0 + int(min(abs(v1-v2),1.0)*20.0)
    #points = points + int(random.random()*5)
    result = {'winner': winner, 'points': points}

    return result


if __name__ == '__main__':
    print "Algorithms for fsWars\n---------------------\n"
    '''
    init()
    id1 = random_id()
    id2 = random_id()

    computeBattle(id1,id2, ALGORITHM_CLASSES['RHYTHM'] )
    computeBattle(id1,id2, ALGORITHM_CLASSES['BRIGHTNESS'] )
    computeBattle(id1,id2, ALGORITHM_CLASSES['TONAL'] )
    computeBattle(id1,id2, ALGORITHM_CLASSES['NOISINESS'] )
    computeBattle(id1,id2, ALGORITHM_CLASSES['LOUDNESS'] )
    '''
