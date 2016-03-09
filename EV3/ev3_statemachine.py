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

class Transition:
    FOUND_OBJECT = 'found object'
    REACHABLE = 'reachable'
    GRABBING_SUCCESS = 'grabbed'
    FAIL = 'failed'
    LINE = 'found line'
    FOUND_DEPOSIT = 'found deposit'
    RESTART = 'restart'

class EV3StateMachine(StateMachine):
    
    def __init__(self):
        StateMachine.__init__(self)
        
        self._add_state(State.SEARCH)
        self._add_state(State.APPROACH)
        self._add_state(State.GRAB)
        self._add_state(State.RETRIEVE)
        self._add_state(State.LINE)
        self._add_state(State.RELEASE)
        
        self._add_transition(State.SEARCH, State.RELEASE, Transition.FOUND_OBJECT)
        self._add_transition(State.SEARCH, State.SEARCH, Transition.FAIL)
        self._add_transition(State.APPROACH, State.GRAB, Transition.REACHABLE)
        self._add_transition(State.APPROACH, State.RELEASE, Transition.FAIL)
        self._add_transition(State.GRAB, State.RELEASE, Transition.FAIL)
        self._add_transition(State.GRAB, State.RETRIEVE, Transition.GRABBING_SUCCESS)
        self._add_transition(State.RETRIEVE, State.LINE, Transition.LINE)
        self._add_transition(State.RETRIEVE, State.RELEASE, Transition.FOUND_DEPOSIT)
        self._add_transition(State.LINE, State.RELEASE, Transition.FOUND_DEPOSIT) #TODO: could move away from line, should include fail and return to "retrieve"
        self._add_transition(State.RELEASE, State.SEARCH, Transition.RESTART)

    def assign_line_function(self, state_identifier, function):
        self.assign_function(state_identifier, "line", function)
        
    def assign_command_function(self, state_identifier, function):
        self.assign_function(state_identifier, "command", function)
    
    def execute_line_function(self, data):
        return self.current().execute_function("line", data)
    
    def execute_command_function(self, data):
        return self.current().execute_function("commands", data)
        