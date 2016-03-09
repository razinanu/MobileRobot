#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from ev3_statemachine import EV3StateMachine
from ev3_statemachine import State
from ev3_statemachine import Transition
from driver import Direction

class Navigator:

    def __init__(self):
        self.__bt_data = 0
        
        self.__mach = EV3StateMachine()
        
        self.__mach.assign_line_function(State.SEARCH, self.__avoid_line)
        self.__mach.assign_line_function(State.APPROACH, self.__avoid_line)
        self.__mach.assign_line_function(State.GRAB, self.__avoid_line)  #should not be used
        self.__mach.assign_line_function(State.RETRIEVE, self.__lock_line)    # TODO: something different
        self.__mach.assign_line_function(State.LINE, self.__lock_line)
        self.__mach.assign_line_function(State.RELEASE, self.__avoid_line)   #should not be used
        
        self.__mach.assign_command_function(State.SEARCH, self.__search)
        self.__mach.assign_command_function(State.APPROACH, self.__approach)
        self.__mach.assign_command_function(State.GRAB, self.__grab)
        self.__mach.assign_command_function(State.RETRIEVE, self.__find_site)
        self.__mach.assign_command_function(State.LINE, self.__follow_line)
        self.__mach.assign_command_function(State.RELEASE, self.__release)
            
    def find_commands(self):
        self.__mach.execute_line_function(self.__line_data)
        direction, transition = self.__mach.execute_command_function(self.__bt_data)
        
        if transition != 0:
            if not self.__mach.transition(transition):
                return 0
        
        return direction
    
    def get_bt(self, data):
        #TODO interpret data
        self.__bt_data = data
        return True
    
    def get_line(self, data):
        self.__line_data = data
        #TODO get directly from sensor
    
    
    
    def __search(self, bt_data):
        # 1.) hit line --> turn
        if self.__avoid_line:
            return self.__evasion()
        
        # 2.) found obstacle
        if self.__nearest_obstacle(bt_data) != 0:
            return Direction.STOP, Transition.FOUND_OBJECT
        
        # 3.) drive straight
        return Direction.STRAIGHT, 0

    def __approach(self, bt_data):
        # 1.) hit line --> turn. Should not happen in convex field
        if self.__avoid_line:
            return self.__evasion()
        
        if self.__nearest_obstacle(bt_data) != 0:
            #TODO: approach without hitting other objects.
            return Direction.STRAIGHT, 0
        else:
            #TODO: wait a short time, then return to search
            return Direction.STOP, Transition.FAIL
    
    def __grab(self, bt_data):
        """close gripper, check for success and color"""
        pass
    
    def __find_site(self, bt_data):
        """move randomly until line or site is found"""
        pass
    
    def __follow_line(self, bt_data):
        """follow line"""
        pass
    
    def __release(self, bt_data):
        """open gripper"""
        pass
            
    def __evasion(self):
        """ return the way you came and turn. when finished, Transition.FAIL"""
        pass 
     
    def __nearest_obstacle(self, bt_data):
        return 0
        
    def __avoid_line(self, line_seen):
        """Resets to False as soon as avoidance is finished (in different function)"""
        #TODO: assumption: line_data is bool. Else convert to bool
        self.__avoid_line = self.__avoid_line or line_seen
          
    def __lock_line(self, line_seen):
        self.__line_following = line_seen
            