#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ev3dev.ev3 as ev3

class SensorInterface:
    
    def __init__(self):
        self.__ground = ev3.Sensor('in1')
        self.__gripper = ev3.ColorSensor('in2')
        
        self.__ground.mode = 'COL-COLOR'
        self.__gripper.mode = 'COL-COLOR'
        
    def getGroundValue(self):
        return self.__ground.value
        
    def getFrontValue(self):
        return self.__gripper.value