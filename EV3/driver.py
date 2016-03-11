#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ev3dev.ev3 as ev3

class Direction:
    STRAIGHT = 'straight'
    REVERSE = 'reverse'
    LEFT = 'left'
    RIGHT = 'right'
    STOP = 'stop'

class Driver:
    
    def __init__(self, loop_duration):
        self.__left = ev3.Motor('outA')
        self.__right = ev3.Motor('outB')
        self.__loop_duration = loop_duration / 1000.0
        
        self.__orders = [(Direction.STRAIGHT, 0),]
    
    def move(self):
        if len(self.__orders) == 0:
            return
        
        move_direction, move_duration = self.__current_order()
        
        if move_direction == Direction.STRAIGHT:
            self.__drive_straight(move_duration, 'normal')
        elif move_direction == Direction.REVERSE:
            self.__drive_straight(move_duration, 'inversed')
        elif move_direction == Direction.LEFT:
            self.__turn(move_duration, True)
        elif move_direction == Direction.RIGHT:
            self.__turn(move_duration, False)
        elif move_direction == Direction.STOP:
            self.__stop_movement()
        else:
            print "ERROR! Navigation direction not understood. Given command was: ", move_direction
            return False
        
        return True
    
    def __current_order(self):
        move_direction = self.__orders[0][0]
        move_duration = self.__orders[0][1]
        
        if move_duration > self.__loop_duration:
            dur = self.__loop_duration
        else:
            dur = move_duration
        
        move_duration -= dur
        
        if move_duration > 0:
            self.__orders[0] = (move_direction, move_duration)
        else:
            self.__orders.pop(0)
        
        return move_direction, dur
            
    def give_commands(self, orders):
        """ Use this command to control the robot.
        
        possible directions: 'straight', 'reverse', 'left', 'right'
        duration in ms. If duration < 0, keep old orders.
        
        TODO: queue of timed actions. or endless action.
        """
        if isinstance(orders, list):
            r = True
            for order in orders:
                r = r and self.__give_command(order[0], order[1])
            return r
        else:
            return self.__give_command(orders[0], orders[1])
            
    def __give_command(self, direction, duration):
        
        if duration < 0:
            return True
        
        if direction not in [Direction.STRAIGHT, Direction.REVERSE, Direction.LEFT, Direction.RIGHT, Direction.STOP]:
            print "ERROR! Given direction was not understood. (", direction, ")"
            return False
        
        if duration == 0:
            del self.__orders[:]
            self.__orders.append((direction, duration))
        
        return True
    
    def get_command_count(self):
        #TODO: queue of orders
        return 0
    
        
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
     
    def __stop_movement(self):
        """ stop all movement """
        self.__left.stop()
        self.__right.stop()       
        