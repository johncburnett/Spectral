__author__ = 'John Burnett'

import math

#-------------------------------------------------------------------------------
#_Conversions

def MtoF(m):
    frequency = 440 * 2**((m-9)/12)
    return frequency

def MtoF_l(m):
    f = []
    for i in range(len(m)):
        f.append( 440 * 2**( (m[i]-9) / 12 ) )
    return f

def FtoM(f):
    midi = 9 + 12 * math.log(f/440,2)
    return midi

def FtoM_l(f):
    m = []
    for i in range(len(f)):
        m.append( 9 + 12 * math.log(f[i]/440,2) )
    return m

def roundMicro(x,semitones):
    if (semitones == 2):
        return int(x)
    elif (semitones == 4):
        return round(x * 2) / 2

#-------------------------------------------------------------------------------
#_List Processing

def scale(c,l):
    m = []
    for e in l:
        m.append(e*c)
    return m

def vAdd(c,l):
    m = []
    for e in l:
        m.append(e+c)
    return m