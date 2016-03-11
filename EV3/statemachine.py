#!/usr/bin/env python2
# -*- coding: utf-8 -*-

class State:

    def __init__(self, name):
        self.__next = {}
        self.__generic_functions = {}
        self.__name = name #only for error handling
    
    def add_transition(self, successor, identifier):
        self.__next[identifier] = successor

    def transition(self, identifier):
        if identifier not in self.__next:
            print "ERROR! This transition was not defined! (State: ", self.__name, ", transition: ", identifier, ")"
            return 0
        
        return self.__next[identifier]

    def get_possible_transitions(self):
        return self.__next.keys()

    def name(self):
        """only for debugging"""
        return self.__name

    def assign_generic_function(self, identifier, function_name):
        self.__generic_functions[identifier] = function_name

    def execute_function(self, identifier, *params):
        return self.__generic_functions[identifier](*params)

class StateMachine:
    
    def __init__(self):
        self.__states = {}
        self.__current = 0
    
    def _add_state(self, identifier):
        """First State is always start state!"""
        
        self.__states[identifier] = State(identifier)
        if self.__current == 0:
            self.__current = self.__states[identifier]
    
    def _add_transition(self, pred, suc, identifier):
        # TODO: currently no error handling, assume correct usage
        self.__states[pred].add_transition(self.__states[suc], identifier)
    
    def assign_generic_function(self, state_identifier, function_identifier, function):
        self.__states[state_identifier].assign_generic_function(function_identifier, function)
        
    def current(self):
        return self.__current
    
    def transition(self, transition):
        new_state = self.__current.transition(transition)
        
        if new_state != 0:
            self.__current = new_state
            return True
        else:
            return False
        