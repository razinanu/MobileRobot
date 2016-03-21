#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from statemachine import StateMachine

class State:
    SEARCH = 'search'
    APPROACH = 'approach'
    GRAB = 'grab'
    RETRIEVE = 'retrieve'
    LINE = 'on line'
    RELEASE = 'release'
    EVASION = 'avoid line'
    REGAIN = 'regain object'

class Transition:
    SUCCESS = 'state successful'
    FAIL = 'failed'
    LINE = 'found line'
    
#     FOUND_OBJECT = 'found object'
#     REACHABLE = 'reachable'  
#     FOUND_DEPOSIT = 'found deposit'
#     RESTART = 'restart'
#     LOST = 'lost current object'
#     REGAINED = 'regained lost object'

class EV3StateMachine(StateMachine):
    
    def __init__(self):
        StateMachine.__init__(self)
        
        self._add_state(State.SEARCH)
        self._add_state(State.APPROACH)
        self._add_state(State.GRAB)
        self._add_state(State.RETRIEVE)
        self._add_state(State.LINE)
        self._add_state(State.RELEASE)
        self._add_state(State.EVASION)
        self._add_state(State.REGAIN)
        
        self._add_transition(State.SEARCH, State.APPROACH, Transition.SUCCESS)
        self._add_transition(State.SEARCH, State.EVASION, Transition.LINE)
        
        self._add_transition(State.APPROACH, State.GRAB, Transition.SUCCESS)
        self._add_transition(State.APPROACH, State.EVASION, Transition.LINE)
        self._add_transition(State.APPROACH, State.REGAIN, Transition.FAIL)
        
        self._add_transition(State.EVASION, State.SEARCH, Transition.SUCCESS)
        
        self._add_transition(State.REGAIN, State.SEARCH, Transition.FAIL)
        self._add_transition(State.REGAIN, State.APPROACH, Transition.SUCCESS)
        
        self._add_transition(State.GRAB, State.RELEASE, Transition.FAIL)    # maybe different state?
        self._add_transition(State.GRAB, State.RETRIEVE, Transition.SUCCESS)
        
        self._add_transition(State.RETRIEVE, State.LINE, Transition.LINE)
        self._add_transition(State.RETRIEVE, State.RELEASE, Transition.SUCCESS)
        
        self._add_transition(State.LINE, State.RELEASE, Transition.SUCCESS) #TODO: could move away from line, should include fail and return to "retrieve"
        
        self._add_transition(State.RELEASE, State.SEARCH, Transition.SUCCESS)

    def assign_function(self, state_identifier, function_identifier):
        self.assign_generic_function(state_identifier, "command", function_identifier)
    
    def execute_functions(self, line_data, bt_data, queue_size):
        return self.current().execute_function("command", line_data, bt_data, queue_size)
        