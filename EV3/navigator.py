#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from driver import Direction

class Navigator:

    def __init__(self):
        pass
    
    
    def find_commands(self):
        return 0, Direction.STRAIGHT
    
    def get_bt(self, data):
        return True