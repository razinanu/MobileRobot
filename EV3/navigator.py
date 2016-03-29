#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from ev3_statemachine import EV3StateMachine
from ev3_statemachine import State
from ev3_statemachine import Transition
from driver import Direction
import time
import ev3dev.ev3 as ev3

class order:
    @staticmethod
    def stop(duration=0):
        return (Direction.STOP, duration)
    
    @staticmethod
    def straight(duration=0, speed_left=Direction.standard_speed, speed_right=Direction.standard_speed):
        return (Direction.STRAIGHT, duration, speed_left, speed_right)
    
    @staticmethod
    def reverse(duration=0, speed_left=Direction.standard_speed, speed_right=Direction.standard_speed):
        return (Direction.REVERSE, duration, speed_left, speed_right)

    @staticmethod
    def left(duration=0, speed_left=Direction.standard_speed, speed_right=Direction.standard_speed):
        return (Direction.LEFT, duration, speed_left, speed_right)
    
    @staticmethod
    def right(duration=0, speed_left=Direction.standard_speed, speed_right=Direction.standard_speed):
        return (Direction.RIGHT, duration, speed_left, speed_right)
    
    @staticmethod
    def move(duration=0, speed_left=Direction.standard_speed, speed_right=Direction.standard_speed):
        if speed_left >= 0 and speed_right >= 0:
            return order.straight(duration, speed_left, speed_right)
        
        if speed_left < 0 and speed_right >= 0:
            return order.left(duration, -speed_left, speed_right)
        
        if speed_left >= 0 and speed_right < 0:
            return order.right(duration, speed_left, -speed_right)
        
        if speed_left < 0 and speed_right < 0:
            return order.reverse(duration, -speed_left, -speed_right)
    
    @staticmethod
    def open():
        return (Direction.OPEN, 900)
    
    @staticmethod
    def close():
        return (Direction.CLOSE, 900)
    
    @staticmethod
    def keep_going():
        return (Direction.STRAIGHT, -1)
    
class Navigator:

    def __init__(self):
        self.__bt_data = 0
        self.__line_data = 0
        self.__is_near = False
        
        self.__mach = EV3StateMachine()
        self.__lastChange = time.time()
        
        self.__ground = ev3.Sensor('in2')
        self.__gripper = ev3.ColorSensor('in1')
        
        self.__ground.mode = 'COL-COLOR'
        self.__gripper.mode = 'COL-COLOR'
        
        self.__mach.assign_function (State.SEARCH,      self.__search)
        self.__mach.assign_function (State.APPROACH,    self.__approach)
        self.__mach.assign_function (State.GRAB,        self.__grab)
        self.__mach.assign_function (State.RETRIEVE,    self.__find_site)
        self.__mach.assign_function (State.LINE,        self.__follow_line)
        self.__mach.assign_function (State.RELEASE,     self.__release)
        self.__mach.assign_function (State.EVASION,     self.__evasion)
        self.__mach.assign_function (State.REGAIN,      self.__regain)
        
        self.__mach.assign_transition_function (State.SEARCH,      self.__start_search)
        self.__mach.assign_transition_function (State.APPROACH,    self.__start_approach)
        self.__mach.assign_transition_function (State.GRAB,        self.__start_grab)
        self.__mach.assign_transition_function (State.RETRIEVE,    self.__start_retrieve)
        self.__mach.assign_transition_function (State.LINE,        self.__start_line)
        self.__mach.assign_transition_function (State.RELEASE,     self.__start_release)
        self.__mach.assign_transition_function (State.EVASION,     self.__start_evasion)
        self.__mach.assign_transition_function (State.REGAIN,      self.__start_regain) 
               
    def find_commands(self, queue_size):
        print self.__mach.current().name()
        orders, transition = self.__mach.execute_functions(self.__line_data, self.__bt_data, queue_size)

        if transition != 0:
            trans_result = self.__mach.transition(transition)
            if not trans_result:
                return False, 0
            else:
                return trans_result
        
        return orders
    
    def get_bt(self, data):
        #TODO interpret data
        self.__bt_data = data
        return True
    
    def get_line(self, data):
        self.__line_data = data # assumption: bool. TODO: handle differently; to allow distinction between sites and lines.
        #TODO get directly from sensor
    
    def __nearest_obstacle(self, bt_data):
        if len(bt_data) == 0:
            return 0,0
        else:
            return bt_data[0]
    
    
    def __search(self, line_data, bt_data, queue_size):
        # 1.) hit line --> turn
        if (self.__ground.value() == 1) and (self.__lastChange + 2 < time.time()):
            self.__lastChange = time.time() #Drehen in Auftrag geben
            return order.left(), 0
        
        elif (self.__lastChange + 1 > time.time()):
            return order.left(), 0    #Drehung ausführen
        
        elif (self.__lastChange + 2 > time.time()):
            return order.move(), 0    #ohne Sensor vorwärts fahren
                
        # 2.) found obstacle
        if self.__nearest_obstacle(bt_data) != 0:
            return order.stop(), Transition.SUCCESS
        
        # 3.) drive straight
        return order.move(), 0

    def __approach(self, line_data, bt_data, queue_size):
        """ approach an object.
        
        If found --> success.
        If lost --> fail.
        If seen --> approach further, using a p-controller.
        """
        
        # 1.) hit line --> turn. Should not happen in convex field
        if self.__line_data:
            return order.stop(), Transition.LINE
        
        obstacle = self.__nearest_obstacle(bt_data)
        
        seen = obstacle != 0
        
        if not seen:
            if self.__is_near:
                return order.stop(), Transition.SUCCESS
            else:
                return order.stop(), Transition.FAIL

        x = obstacle[1]
        y = obstacle[2]

        if x < 0.5:
            self.__is_near = True
        
        # p controller
        P = 1   # some proportional factor
        left = Direction.standard_speed - y*P
        right = Direction.standard_speed + y*P
         
        #assumption: left, right > 0. Else
        return order.move(speed_left = left, speed_right = right), 0
    
    def __find_site(self, line_data, bt_data, queue_size):
        """move randomly until line or site is found"""
        
        # move rand
        # if line or wrong site --> line
        # if correct site --> success
        
        return order.stop(), 0
    
    def __follow_line(self, line_data, bt_data, queue_size):
        """follow line"""
        
        # stay on line
        # if correct site --> success
        
        return order.stop(), 0
    
    def __evasion(self, line_data, bt_data, queue_size):
        """ return the way you came and turn. when finished, Transition.SUCCESS"""
        
        return [order.reverse(500), order.reverse(500, 0, 50), order.stop()], Transition.SUCCESS
        
    def __grab(self, line_data, bt_data, queue_size):
        """close gripper, check for success and color"""
        
        # close gripper
        # if closed and ball in front of sensor --> success
        # if closed and nothing in front of sensor --> fail
        
        return order.stop(), 0
    
    def __release(self, line_data, bt_data, queue_size):
        """ open gripper, drive a little backwards, transition to next state.
        
        Transition will be done immediately. But since timed orders cannot be overwritten, they are going to be 
        followed even in the next state.
        
        TODO: What about turning and facing the field again? Should be done in "Search", because the line sensor alarms.
        """
        
        # gives orders and goes directly to next state --> orders will be obeyed in other state too, next orders cannot overwrite them
        return [order.open(), order.reverse(500), order.stop()], Transition.SUCCESS 
            

    def __regain(self, line_data, bt_data, queue_size):
        """ wiggle around on position to find a lost object."""
        
        # stand still for short time. wiggle around.
        # if after this nothing found --> fail
        # if sometimes in between object seen --> success
        
        return order.stop(), 0

    
    def __start_search(self):
        return 0

    def __start_approach(self):
        return 0
    
    def __start_grab(self):
        return 0
    
    def __start_retrieve(self):
        return 0
    
    def __start_line(self):
        return 0
    
    def __start_release(self):
        return 0
    
    def __start_evasion(self):
        return 0
    
    def __start_regain(self):
        return 0