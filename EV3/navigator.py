#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from ev3_statemachine import EV3StateMachine
from ev3_statemachine import State
from ev3_statemachine import Transition
from driver import Direction

class order:
    @staticmethod
    def stop(duration=0):
        return (Direction.STOP, duration)
    
    @staticmethod
    def straight(duration=0):
        return (Direction.STRAIGHT, duration)
    
    @staticmethod
    def reverse(duration=0):
        return (Direction.REVERSE, duration)

    @staticmethod
    def left(duration=0):
        return (Direction.LEFT, duration)
    
    @staticmethod
    def right(duration=0):
        return (Direction.RIGHT, duration)
    
    @staticmethod
    def open():
        return (Direction.OPEN, 500)
    
    @staticmethod
    def close():
        return (Direction.CLOSE, 500)
    
    @staticmethod
    def keep_going():
        return (Direction.STRAIGHT, -1)
    
class Navigator:

    def __init__(self):
        self.__bt_data = 0
        self.__line_data = 0
        
        self.__mach = EV3StateMachine()
        
        self.__mach.assign_function (State.SEARCH,      self.__search)
        self.__mach.assign_function (State.APPROACH,    self.__approach)
        self.__mach.assign_function (State.GRAB,        self.__grab)
        self.__mach.assign_function (State.RETRIEVE,    self.__find_site)
        self.__mach.assign_function (State.LINE,        self.__follow_line)
        self.__mach.assign_function (State.RELEASE,     self.__release)
        self.__mach.assign_function (State.EVASION,       self.__evasion)
        self.__mach.assign_function (State.REGAIN,      self.__regain)
            
    def find_commands(self, queue_size):
        orders, transition = self.__mach.execute_functions(self.__line_data, self.__bt_data)
        
        if transition != 0:
            if not self.__mach.transition(transition):
                return False, 0
        
        return orders
    
    def get_bt(self, data):
        #TODO interpret data
        self.__bt_data = data
        return True
    
    def get_line(self, data):
        self.__line_data = data # assumption: bool. TODO: handle differently; to allow distinction between sites and lines.
        #TODO get directly from sensor
    
    def __nearest_obstacle(self, line_data, bt_data):
        return 0
    
    
    def __search(self, line_data, bt_data):
        # 1.) hit line --> turn
        if self.__line_data:
            return order.stop(), Transition.LINE
        
        # 2.) found obstacle
        if self.__nearest_obstacle(bt_data) != 0:
            return order.stop(), Transition.SUCCESS
        
        # 3.) drive straight
        return order.drive()

    def __approach(self, line_data, bt_data):
        # 1.) hit line --> turn. Should not happen in convex field
        if self.__line_data:
            return order.stop(), Transition.LINE
        
        # if found --> success
        # if seen --> approach further
        # if lost --> fail
        
        return order.stop(), 0
    
    def __grab(self, line_data, bt_data):
        """close gripper, check for success and color"""
        
        # close gripper
        # if closed and ball in front of sensor --> success
        # if closed and nothing in front of sensor --> fail
        
        return order.stop(), 0
    
    def __find_site(self, line_data, bt_data):
        """move randomly until line or site is found"""
        
        # move rand
        # if line or wrong site --> line
        # if correct site --> success
        
        return order.stop(), 0
    
    def __follow_line(self, line_data, bt_data):
        """follow line"""
        
        # stay on line
        # if correct site --> success
        
        return order.stop(), 0
    
    def __release(self, line_data, bt_data):
        """open gripper"""
        
        # open gripper
        # if open --> success (what about turning and facing the field again? Done in "Search", because site is seen as line?)
        
        return order.stop(), 0
            
    def __evasion(self, line_data, bt_data):
        """ return the way you came and turn. when finished, Transition.FAIL"""
        
        # drive backwards and turn
        # if finished --> success
        
        return order.stop(), 0
    
    def __regain(self, line_data, bt_data):
        """ wiggle around on position to find a lost object."""
        
        # stand still for short time. wiggle around.
        # if after this nothing found --> fail
        # if sometimes in between object seen --> success
        
        return order.stop(), 0
