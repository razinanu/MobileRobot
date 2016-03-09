#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from rfcomm_server import RFCOMMServer
from navigator import Navigator
import time


LOOP_DURATION = 0.01  # in s
ok = True

print "Welcome!"

print "Waiting for bluetooth connection..."
btserver = RFCOMMServer()
btserver.wait_for_connection()
print "Connected!"


nav = Navigator(LOOP_DURATION)

while ok:
    start = time.time()
    nav.move()  #no code before this point!
    
    # TODO: here comes the other code
    
    
    data = btserver.wait_for_data() # no code after this point!
    
    end = time.time()
    remain = start + LOOP_DURATION - end
    if remain > 0:
        time.sleep(remain)


print "Close bluetooth connection..."
btserver.close()
print "Closed!"

print "Program finished."