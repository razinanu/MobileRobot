#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from rfcomm_server import RFCOMMServer
from driver import Driver
from navigator import Navigator
import time

LOOP_DURATION = 0.01  # in s
ok = True
bt_data = 0

print "Welcome!"

print "Waiting for bluetooth connection..."
btserver = RFCOMMServer()
btserver.wait_for_connection()
print "Connected!"

driver = Driver(LOOP_DURATION)
nav = Navigator()

while ok:
    start = time.time()
    ok = ok and driver.move()  #no code before this point!
    
    # TODO: here comes the other code
    ok = ok and nav.get_bt(bt_data)
    ok = ok and driver.give_command(nav.find_commands(), LOOP_DURATION)
    
    
    bt_data = btserver.wait_for_data() # no code after this point!
    
    end = time.time()
    remain = start + LOOP_DURATION - end
    if remain > 0:
        time.sleep(remain)


print "Close bluetooth connection..."
btserver.close()
print "Closed!"

print "Program finished."