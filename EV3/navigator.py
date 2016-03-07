#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ev3dev.ev3 as ev3


class Navigator:
    
    def __init__(self):
        self.__left = ev3.Motor('outA')
        self.__right = ev3.Motor('outB')
        
    def drive_straight(self, duration):
        """
        duration in ms
        """
        
        self.__left.run_timed(time_sp=duration, duty_cycle_sp=75)
        self.__right.run_timed(time_sp=duration, duty_cycle_sp=75)
        
    def turn(self, duration, turn_left):
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
        