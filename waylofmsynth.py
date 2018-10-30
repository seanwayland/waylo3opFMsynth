#!/usr/bin/env python
# encoding: utf-8
"""
3 oscillators FM synthesis class.

"""
from pyo import *
import math
import sys

attacksetting = 0.001

decaysetting= 0.3

sustainsetting= 0.9

releasesetting= 0.07

polyphony= 8

bendrange= 2

samplerate = 44100

buffsize = 512
s = Server(sr=samplerate, buffersize=buffsize).boot()

n = Notein(poly=polyphony,scale=1) # transpo
bend = Bendin(brange=bendrange, scale=1)
env = MidiAdsr(n['velocity'], attack=attacksetting, decay=decaysetting, sustain=sustainsetting, release=releasesetting)
t = HarmTable([1,0.1])
pit = n["pitch"]
vel = n["velocity"]


class FM3:

    def __init__(self, fcar, ratio1, ratio2, index1, index2, out=0):
        self.fmod = fcar * ratio1
        self.fmodmod = self.fmod * ratio2
        self.amod = self.fmod*index1
        self.amodmod = self.fmodmod * index2
        self.modmod = Sine(self.fmodmod, mul=self.amodmod)
        self.mod = Sine(self.fmod+self.modmod, mul=self.amod)
        self.car = Osc(t, fcar+self.mod, mul=env)
        self.eq = EQ(self.car, freq=fcar, q=0.707, boost=-12)
        self.filt = ButLP(self.eq, freq = 700+vel*3)
        #self.fx2 = STRev(self.eq, inpos=0.25, revtime=2, cutoff=5000, mul=env, bal=0.01, roomSize=1)
        #self.out = DCBlock(self.out).out(out)
        #self.eq = EQ(self.car, freq=fcar, q=0.707, boost=-12)
        
        self.out = DCBlock(self.filt).out(out)

a = FM3(pit*bend, 0.33001, 2.9993, 8, 4, 0)
b = FM3(pit*bend +0.12, 0.33003, 2.9992, 8, 4, 1)
c = FM3(pit*2*bend - 0.1 , 0.33004, 2.9995, 8, 4, 0)
d = FM3(pit*2*bend - 0.11, 0.33006, 2.9991, 8, 4, 1)


s.gui(locals())
