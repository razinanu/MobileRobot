#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from rfcomm_server import RFCOMMServer
from driver import Driver
from navigator import Navigator
import time
from driver import Direction

LOOP_DURATION = 0.01  # in s
ok = True
bt_data = 0

print "Welcome!"

print "Waiting for bluetooth connection..."
#btserver = RFCOMMServer()
#btserver.wait_for_connection()
print "Connected!"

driver = Driver(LOOP_DURATION)
nav = Navigator()

driver.give_commands((Direction.STRAIGHT, 0))
a = 300
while ok:
    try:
        start = time.time()
        ok = ok and driver.move()  #no code before this point!
        
        # TODO: here comes the other code
        ok = ok and nav.get_bt(bt_data)
    #    ok = ok and driver.give_commands(nav.find_commands(driver.get_command_count()))
        a -= 1
        if a == 0:
            driver.give_commands((Direction.REVERSE,2000, 30,60))
        
    #    bt_data = btserver.wait_for_data() # no code after this point!
        
        end = time.time()
        remain = start + LOOP_DURATION - end
        if remain > 0:
            time.sleep(remain)
    except KeyboardInterrupt:
        break


print "Close bluetooth connection..."
#btserver.close()
print "Closed!"

print "Program finished."