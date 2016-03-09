#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ev3dev.ev3 as ev3

class Direction:
    STRAIGHT = 'straight'
    REVERSE = 'reverse'
    LEFT = 'left'
    RIGHT = 'right'

class Driver:
    
    def __init__(self, loop_duration):
        self.__left = ev3.Motor('outA')
        self.__right = ev3.Motor('outB')
        self.__loop_duration = loop_duration / 1000.0
        
        self.__move_duration = 0
        self.__direction =  Direction.STRAIGHT
    
    def move(self):
        if self.__move_duration <= 0:
            return
        
        if self.__move_duration > self.__loop_duration:
            dur = self.__loop_duration
        else:
            dur = self.__move_duration
        
        self.__move_duration -= dur
        
        if self.__direction == Direction.STRAIGHT:
            self.__drive_straight(dur, 'normal')
        elif self.__direction == Direction.REVERSE:
            self.__drive_straight(dur, 'inversed')
        elif self.__direction == Direction.LEFT:
            self.__turn(dur, True)
        elif self.__direction == Direction.RIGHT:
            self.__turn(dur, False)
        else:
            print "ERROR! Navigation direction not understood. Given command was: ", self.__direction
            return False
        
        return True
            
    def give_command(self, duration, direction):
        """ Use this command to control the robot.
        
        possible directions: 'straight', 'reverse', 'left', 'right'
        duration in ms. If duration < 0, keep old orders.
        """
        if duration < 0:
            return True
        
        if direction not in [Direction.STRAIGHT, Direction.REVERSE, Direction.LEFT, Direction.RIGHT]:
            print "ERROR! Given direction was not understood. (", direction, ")"
            return False
        
        self.__move_duration = duration
        self.__direction = direction
        
        return True
    
        
    def __drive_straight(self, duration, direction):
        """
        duration in ms
        """
        
        self.__left.run_timed(time_sp=duration, polarity=direction, duty_cycle_sp=75)
        self.__right.run_timed(time_sp=duration, polarity=direction, duty_cycle_sp=75)
        
    def __turn(self, duration, turn_left):
        """
        duration in ms
        turn_left = true --> left, else right
        """
        
        if turn_left:
            self.__left.run_timed(time_sp=duration, duty_cycle_sp=75, polarity='inversed')
            self.__right.run_timed(time_sp=duration, duty_cycle_sp=75, polarity='normal')
        else:
            self.__left.run_timed(time_sp=duration, duty_cycle_sp=75, polarity='normal')
            self.__right.run_timed(time_sp=duration, duty_cycle_sp=75, polarity='inversed')
     
    def stop_movement(self):
        """ stop all movement """
        self.__left.stop()
        self.__right.stop()       
        