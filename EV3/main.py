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
    
    objects = btstring.split(" ")
    if objects[0] == '':
        return []
    
    object_list = []
    
    for o in objects:
        try:
            one = parseOne(o)
        except ValueError as er:
            print "###########################################"
            print "###########################################"
            print "ERROR! ", er, "(Message: ", o, ")"
            print "###########################################"
            print "###########################################"
            object_list = []
            one = parseOneFaultyElement(o)
        
        object_list.append(one)
        
    
    return object_list

def parseRazi(btstring):
    if btstring == "0":
        return 0,0,0
    else:
        xs = btstring[0:3]
        ys = btstring[3:7]
        zs = btstring[7:8]
        
        x = int(xs)
        y = int(ys)
        z = int(zs)
        return x,y,z
        

def parseOne(o):
    elements = o.split("#")
    
    return (elements[0], int(elements[1]), int(elements[2]), int(elements[3]))

def parseOneFaultyElement(o):
    elements = o.split("#")
    
    color = ""
    if "X" in elements[3]:
        color = "X"
    elif "B" in elements[3]:
        color = "B"
    elif "R" in elements[3]:
        color = "R"
        
    return (color, int(elements[4]), int(elements[5]), int(elements[6]))
    

LOOP_DURATION = 0.1  # in s
ok = True
bt_data = 0

print "Welcome!"

# print "Waiting for bluetooth connection..."
# btserver = RFCOMMServer()
# btserver.wait_for_connection()
# print "Connected!"

driver = Driver(LOOP_DURATION)
nav = Navigator()

driver.give_commands((Direction.STRAIGHT, 0))

while ok:
    try:
        start = time.time()
        ok = ok and driver.move()  #no code before this point!
        
        # TODO: here comes the other code
        #ok = ok and nav.get_bt(parseRazi(bt_data))
        ok = ok and nav.get_bt(parseRazi("12312342"))
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