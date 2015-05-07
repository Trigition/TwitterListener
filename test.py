#!/usr/bin/env python
__author__ = 'William'

import pyttsx

engine = pyttsx.init()
engine.setProperty('rate', 70)

voices = engine.getProperty('voices')
for voice in voices:
    print "Using voice:", voice.id
    engine.setProperty('voice', voice.id)
    print "Saying: \"Hi there, how are you?\""
    engine.say("Hi there, how are you ?")
engine.runAndWait()