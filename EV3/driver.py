#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import ev3dev.ev3 as ev3

class Direction:
    STRAIGHT = 'straight'
    REVERSE = 'reverse'
    LEFT = 'left'
    RIGHT = 'right'
    STOP = 'stop'
    
    OPEN = 'open'
    CLOSE = 'close'

class Driver:
    
    def __init__(self, loop_duration):
        self.__left = ev3.Motor('outA')
        self.__right = ev3.Motor('outB')
        self.__gripper = ev3.Motor('outC')
        self.__loop_duration = loop_duration * 1000.0
        self.__standard_speed = 0.75
        
        self.__orders = []
    
    def move(self):
        if len(self.__orders) == 0:
            return
        
        move_direction, move_duration, speed_l, speed_r = self.__current_order()
        
        if move_direction == Direction.STRAIGHT:
            self.__drive_straight(move_duration, 'normal', speed_l, speed_r)
        elif move_direction == Direction.REVERSE:
            self.__drive_straight(move_duration, 'inversed', speed_l, speed_r)
        elif move_direction == Direction.LEFT:
            self.__turn(move_duration, True, speed_l, speed_r)
        elif move_direction == Direction.RIGHT:
            self.__turn(move_duration, False, speed_l, speed_r)
        elif move_direction == Direction.STOP:
            self.__stop_movement()
        elif move_direction == Direction.OPEN:
            self.__move_gripper(move_duration, True)
        elif move_direction == Direction.CLOSE:
            self.__move_gripper(move_duration, False)
        else:
            print "ERROR! Navigation direction not understood. Given command was: ", move_direction
            return False
        
        return True
    
    def __current_order(self):
        if len(self.__orders) == 0:
            return Direction.STOP, self.__loop_duration, 0,0
        
        
        move_direction = self.__orders[0][0]
        move_duration = self.__orders[0][1]
        left = self.__orders[0][2]
        right = self.__orders[0][3]
        
        if move_duration == 0 and move_direction != Direction.STOP:
            return move_direction, self.__loop_duration, left, right
        
        if move_duration > self.__loop_duration:
            dur = self.__loop_duration
        else:
            dur = move_duration
            
        move_duration -= dur
        
        if move_duration > 0:
            self.__orders[0] = (move_direction, move_duration, left, right)
        else:
            self.__orders.pop(0)
        
        return move_direction, dur, left, right
            
    def give_commands(self, orders):
        """ Use this command to control the robot.
        
        possible directions: 'straight', 'reverse', 'left', 'right'
        duration in ms. If duration < 0, keep old orders.
        
        TODO: delete endless actions!
        """
        if isinstance(orders, list):
            r = True
            for order in orders:
                r = r and self.__give_command(order)
            return r
        else:
            return self.__give_command(orders)
            
    def __give_command(self, order):
        
        direction = order[0]
        duration = order[1]
        
        if duration < 0:
            return True
        
        if direction not in [Direction.STRAIGHT, Direction.REVERSE, \
                             Direction.LEFT, Direction.RIGHT, Direction.STOP, \
                             Direction.OPEN, Direction.CLOSE]:
            print "ERROR! Given direction was not understood. (", direction, ")"
            return False
        
        if len(order) == 4:     # Custom speed
            speed_l = order[2]
            speed_r = order[3]
        else:
            speed_l = self.__standard_speed
            speed_r = self.__standard_speed
            
        self.__orders.append((direction, duration, speed_l, speed_r))
        
        return True
    
    def get_command_count(self):
        return len(self.__orders)
        
    def __drive_straight(self, duration, direction, speed_l, speed_r):
        """
        duration in ms
        """
        
        self.__left.run_timed(time_sp=duration, polarity=direction, duty_cycle_sp=speed_l)
        self.__right.run_timed(time_sp=duration, polarity=direction, duty_cycle_sp=speed_r)
        
    def __turn(self, duration, turn_left, speed_l, speed_r):
        """
        duration in ms
        turn_left = true --> left, else right
        """
        
        if turn_left:
            self.__left.run_timed(time_sp=duration, duty_cycle_sp=speed_l, polarity='inversed')
            self.__right.run_timed(time_sp=duration, duty_cycle_sp=speed_r, polarity='normal')
        else:
            self.__left.run_timed(time_sp=duration, duty_cycle_sp=speed_l, polarity='normal')
            self.__right.run_timed(time_sp=duration, duty_cycle_sp=speed_r, polarity='inversed')
     
    def __stop_movement(self):
        """ stop all movement """
        self.__left.stop()
        self.__right.stop()       
    
    def __move_gripper(self, duration, should_open):
        if should_open:
            self.__gripper.run_timed(time_sp=duration, polarity='normal', duty_cycle_sp=50)
        else:
            self.__gripper.run_timed(time_sp=duration, polarity='inversed', duty_cycle_sp=50)