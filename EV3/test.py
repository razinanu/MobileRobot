#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from ev3_statemachine import EV3StateMachine
from ev3_statemachine import Transition

print "start"

mac = EV3StateMachine()

print mac.current().name()
mac.transition(Transition.FAIL)
print mac.current().name()
mac.transition(Transition.FOUND_OBJECT)
print mac.current().name()

print mac.current().get_possible_transitions()


print "end"