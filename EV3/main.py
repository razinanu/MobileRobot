#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from rfcomm_server import RFCOMMServer
from navigator import Navigator
import time


#btserver = RFCOMMServer()
#btserver.wait_for_connection()

nav = Navigator()

print "drive 3s straight"

nav.drive_straight(3000)
time.sleep(4)

print "turn 2s left"

nav.turn(2000, True)
time.sleep(3)

print "turn 2s right"

nav.turn(2000, False)
time.sleep(3)

print "finished"

#while True:
    #data = btserver.wait_for_data() currently not used

#btserver.close()