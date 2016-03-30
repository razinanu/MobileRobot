#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from rfcomm_server import RFCOMMServer
from driver import Driver
from navigator import Navigator
import time
from driver import Direction

def parse(btstring):
    if btstring == 0:
        return []
    
    
    objects = btstring.split("#")
    if objects[0] == '':        #oder '0'
        return []
    
    object_list = []
    
    for o in objects:
        try:
            if(o != ''):
                one = parseOne(o)
        except ValueError as er:
            print("###########################################")
            print("###########################################")
            print("ERROR! ", er, "(Message: ", o, ")")
            print("###########################################")
            print("###########################################")
        object_list.append(one)
        
    return object_list

def parseOne(o):
    elements = o.split("$")
    return [int(elements[1]), int(elements[2]), elements[3]]
  

LOOP_DURATION = 0.1  # in s
ok = True
bt_data = 0

print "Welcome!"

print "Waiting for bluetooth connection..."
btserver = RFCOMMServer()
btserver.wait_for_connection()
print "Connected!"

driver = Driver(LOOP_DURATION)
nav = Navigator()

driver.give_commands((Direction.STRAIGHT, 0))

## TEST !!! ###
#btstring = "$450$550$B#$10$10$B#$100$100$X#$20$20$R#"

while ok:
    try:
        start = time.time()
        ok = ok and driver.move()  #no code before this point!
        
        # TODO: here comes the other code
        ok = ok and nav.get_bt(parse(bt_data))
#         ok = ok and nav.get_bt(parse(btstring))
        ok = ok and driver.give_commands(nav.find_commands(driver.get_command_count()))
    
        bt_data = btserver.wait_for_data() # no code after this point!
        
        end = time.time()
        remain = start + LOOP_DURATION - end
        
        if remain > 0:
            time.sleep(remain)
    except KeyboardInterrupt:
        break
    except AttributeError as er:
        print er.message()
        break


print "Close bluetooth connection..."
btserver.close()
print "Closed!"

print "Program finished."