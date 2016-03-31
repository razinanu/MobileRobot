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
        return (Direction.OPEN, 400)
    
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
        self.__is_near = False
        
        self.YLL = 200
        self.YL = 450
        self.YR = 750
        self.YRR = 1080
        self.XU = 540
        self.THRESHHOLD = 440
        self.MITTE = 640
        
        self.__mach = EV3StateMachine()
        self.__lastChange = time.time() - 100
        
        self.__ground = ev3.Sensor('in2')
        self.__gripper = ev3.ColorSensor('in1')
        
        self.__ground.mode = 'COL-COLOR'
        self.__gripper.mode = 'COL-COLOR'
        self.__gripperOpen = True
        self.__redBallInGripper = False
        self.__blueBallInGripper = False
        
        self.__mach.assign_function (State.SEARCH,      self.__search)
        self.__mach.assign_function (State.APPROACH,    self.__approach)
        self.__mach.assign_function (State.GRAB,        self.__grab)
        self.__mach.assign_function (State.RETRIEVE,    self.__find_site)
        self.__mach.assign_function (State.LINE,        self.__follow_line)
        self.__mach.assign_function (State.RELEASE,     self.__release)
        self.__mach.assign_function (State.EVASION,     self.__evasion)
        self.__mach.assign_function (State.EVASION2,    self.__evasion2)
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
        orders, transition = self.__mach.execute_functions(self.__line_data, self.__bt_data, queue_size)

        if transition != 0:
            trans_result = self.__mach.transition(transition)
            if trans_result:
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
    
    # Suchen 
    def __search(self, line_data, bt_data, queue_size):
        # 1.) hit line --> turn
        
        print "Farbe Boden:", self.__ground.value()
        
        if self.__gripper.value() == 2 or self.__gripper.value() == 5:
            print "Ball beim Suchen gefunden"
            self.__lastChange = time.time() - 2
            return order.stop(), Transition.LINE
        
        if (self.__ground.value() == 1) and (self.__lastChange + 3.2 < time.time()):
            self.__lastChange = time.time() #Drehen in Auftrag geben
            return order.left(), 0
        
        elif (self.__lastChange + 1.2 > time.time()):
            print "drehen"
            return order.left(0,50,50), 0    #Drehung ausführen
        
        elif (self.__lastChange + 3.2 > time.time()):
            print "korrektur"
            return order.move(0,50,47), 0    #ohne Sensor vorwärts fahren
                
        # 2.) found obstacle       
        i = 0
        smallestX = 0, 0, "AZX"
        for i, val in enumerate(bt_data):
            if val[2] != "X":
                print "Ball gefunden, Zustand wechseln"
                return order.move(0,30,30), Transition.SUCCESS             
        
        # 3.) drive straight
        print "normal fahren"
        return order.move(), 0

    #Annähern
    def __approach(self, line_data, bt_data, queue_size):
        print "Ball annähern"
    
        if self.__gripper.value() == 2 or self.__gripper.value() == 5:
            print "Ball beim Annähern gefunden"
            self.__lastChange = time.time() - 2
            return order.stop(), Transition.SUCCESS
    
        # Linie behandeln
        if (self.__ground.value() == 1) and (self.__lastChange + 3.2 < time.time()):
            self.__lastChange = time.time() #Drehen in Auftrag geben
            return order.left(), 0
        
        elif (self.__lastChange + 1.2 > time.time()):
            print "drehen"
            return order.left(0,50,50), 0    #Drehung ausführen
        
        elif (self.__lastChange + 3.2 > time.time()):
            print "korrektur"
            return order.move(0,50,47), 0    #ohne Sensor vorwärts fahren
        
        # Objekte suchen
        if len(bt_data) == 0:
            print "Ball verloren, in Suchen zurueck"
            print bt_data
            return order.stop(), Transition.SUCCESS 
        
#         bt_data = [[9,2,3],[4,5,6],[7,8,9]]
        i = 0
        smallestX = 0, 0, "AZX"
        for i, val in enumerate(bt_data):
            if val[0] > smallestX[0]:                           # ist der Ball näher am Roboter?
                if val[2] != "X":                               # hat der Ball die richtige Farbe?                                             # ist der falsche Ball nah genug am Roboter?     
                    smallestX = val[0], val[1], val[2]
                elif smallestX[1] > self.YLL and smallestX[1] < self.YRR:   # liegt der andersfarbige Ball im Kollisionsbereich?
                    if val[0] > self.THRESHHOLD:
                        smallestX = val[0], val[1], val[2]
              
        print "annaehern", smallestX[0], smallestX[1]
        
        if smallestX[0] == 0:
            print "kein richtiger Ball, in Suchen zurueck"
            return order.stop(), Transition.SUCCESS 
        
        if smallestX[2] == "X":
            print "in Modus Ausweichen wechseln"
            return order.stop(), Transition.LINE                #in Ausweichen wechseln
        
        if smallestX[1] > self.YL and smallestX[1] < self.YR:           # liegt der Ball mittig?
            if smallestX[0] > self.XU:                              # liegt der mittige Ball im unteren Bildviertel?
                print "in Modus vorfahren und Greifen wechseln"    
                self.__lastChange = time.time()                        
                return order.stop(), Transition.SUCCESS         # Ball liegt richtig; in Vorfahren und Greifen wechseln
            else:
                print "nach vorne fahren"
                return order.move(0,30,29), 0                   # stück nach vorne fahren
            
        else:
            if smallestX[1] < self.MITTE:
                print "links drehen"
                return order.left(0,15,15), 0                   # links drehen
            else: 
                print "rechts drehen"
                return order.right(0,15,15), 0                  # rechts drehen
            
        
        
    
    # farbiges Feld finden
    def __find_site(self, line_data, bt_data, queue_size):
        """move randomly until line or site is found"""
        
        print "Farbe Boden:", self.__ground.value()
        
        if (self.__ground.value() == 1) and (self.__lastChange + 3.2 < time.time()):
            self.__lastChange = time.time() #Drehen in Auftrag geben
            return order.left(), 0
        
        elif (self.__lastChange + 1.2 > time.time()):
            print "drehen"
            return order.left(0,50,50), 0    #Drehung ausführen
        
        elif (self.__lastChange + 3.2 > time.time()):
            print "korrektur"
            return order.move(0,50,47), 0    #ohne Sensor vorwärts fahren
             
        # TODO Bällen ausweichen     
           
        # blaues Feld gefunden
        if self.__ground.value() == 2 and self.__blueBallInGripper:
            return order.stop(), Transition.SUCCESS
        
        # rotes Feld gefunden
        if self.__ground.value() == 5 and self.__redBallInGripper:
            return order.stop(), Transition.SUCCESS
        
        # 3.) drive straight
        print "normal fahren"
        return order.move(), 0
        
        # move rand
        # if line or wrong site --> line
        # if correct site --> success
        
        return order.stop(), 0
    
    def __follow_line(self, line_data, bt_data, queue_size):
        """follow line"""
        
        # stay on line
        # if correct site --> success
        
        return order.stop(), 0
    
    # Ausweichen
    def __evasion(self, line_data, bt_data, queue_size):
        """ return the way you came and turn. when finished, Transition.SUCCESS"""

        # Linie behandeln
        if (self.__ground.value() == 1) and (self.__lastChange + 3.2 < time.time()):
            self.__lastChange = time.time() #Drehen in Auftrag geben
            return order.left(), 0
        
        elif (self.__lastChange + 1.2 > time.time()):
            print "drehen"
            return order.left(0,50,50), 0    #Drehung ausführen
        
        elif (self.__lastChange + 3.2 > time.time()):
            print "korrektur"
            return order.move(0,50,47), 0    #ohne Sensor vorwärts fahren
        
        # wenn kein feindlicher Ball mehr gesehen wird, für 2 Sekunden geradeaus fahren
        if self.__lastChange + 2 > time.time():
            return order.move(0,50,47), 0
        
        # Objekte suchen
#         bt_data = [[9,2,3],[4,5,6],[7,8,9]]
        i = 0
        smallestX = 0, 0, "AZX"
        for i, val in enumerate(bt_data):
            if val[0] > smallestX[0]:                           # ist der Ball näher am Roboter?
                if val[2] != "X":                                 # hat der Ball die richtige Farbe?
                    smallestX = val[0], val[1], val[2]
#                 elif smallestX[1] > self.YLL and smallestX[1] < self.YRR:   # liegt der andersfarbige Ball im Kollisionsbereich?
#                     smallestX = val[0], val[1], val[2]
              
        print "ausweichen", smallestX[0], smallestX[1]
        
        if smallestX[2] != "X":
            print "in Modus Suchen wechseln"
            return order.stop(), Transition.SUCCESS             #in Suchen wechseln
        
        if not (smallestX[1] > self.YL and smallestX[1] < self.YR):       # der Ball liegt nicht mehr im Kollisionsbereich?
            self.__lastChange = time.time()
            return order.move(0,50,47), 0                       # Stück geradeaus fahren  
            
        else:
            if smallestX[1] > self.MITTE:
                return order.left(0,50,50), 0                   # links drehen
            else: 
                return order.right(0,50,50), 0                  # rechts drehen        
        
        
        #return [order.reverse(500), order.reverse(500, 0, 50), order.stop()], Transition.SUCCESS
    
    # Ausweichen mit Ball
    def __evasion2(self, line_data, bt_data, queue_size):
        # Linie behandeln
        if (self.__ground.value() == 1) and (self.__lastChange + 3.2 < time.time()):
            self.__lastChange = time.time() #Drehen in Auftrag geben
            return order.left(), 0
        
        elif (self.__lastChange + 1.2 > time.time()):
            print "drehen"
            return order.left(0,50,50), 0    #Drehung ausführen
        
        elif (self.__lastChange + 3 > time.time()):
            print "korrektur"
            return order.move(0,50,47), 0    #ohne Sensor vorwärts fahren
        
        if len(bt_data) == 0:
            print "kein Ball mehr gesehen"
            print bt_data
            return order.stop(), Transition.SUCCESS 
        
        # Objekte suchen
#         bt_data = [[9,2,3],[4,5,6],[7,8,9]]
        i = 0
        smallestX = 0, 0, "AZX"
        for i, val in enumerate(bt_data):
            if val[0] > smallestX[0]:                           # ist der Ball näher am Roboter?
                if smallestX[1] > self.YLL and smallestX[1] < self.YRR:   # liegt der andersfarbige Ball im Kollisionsbereich?
                    if val[0] > self.THRESHHOLD:     # nur vor dem Ball ausweichen, wenn dieser vor dem Roboter liegt
                        smallestX = val[0], val[1], val[2]
              
        print "ausweichen_2", smallestX[0], smallestX[1]
        
        if smallestX[2] == "AZX":
            print "kein Ball direkt vor dem Roboter"
            return order.stop(), Transition.SUCCESS 
        
        if smallestX[1] > self.MITTE:
            return order.left(0,50,50), 0                   # links drehen
        else: 
            return order.right(0,50,50), 0                  # rechts drehen        
        
        
        #return [order.reverse(500), order.reverse(500, 0, 50), order.stop()], Transition.SUCCESS
        
    def __grab(self, line_data, bt_data, queue_size):
        """close gripper, check for success and color"""
        
        # auf den Ball zu fahren; Zeit muss beim Moduswechsel auf aktuelle Zeit gesetzt werden!
        if (self.__lastChange + 1.5) > time.time():
            print "auf den ball zufahren"
            return order.move(0,30,27), 0
        
        if self.__gripperOpen:
            print "greifer schließen"
            self.__gripperOpen = False
            return order.close(), 0
        
        if not self.__gripperOpen and queue_size == 0:
            if self.__gripper.value() == 2: # blauer Ball
                self.__blueBallInGripper = True
                self.__redBallInGripper = False
                print "blauen Ball gegriffen"
                return order.stop(), Transition.SUCCESS
            elif self.__gripper.value() == 5:   # roter Ball
                self.__blueBallInGripper = False
                self.__redBallInGripper = True  
                print "roten Ball gegriffen"
                return order.stop(), Transition.SUCCESS
            else:
                self.__blueBallInGripper = False
                self.__redBallInGripper = False  
                print "leider kein richtiger Ball :("
                return order.stop(), Transition.FAIL            
            
        
        # close gripper
        # if closed and ball in front of sensor --> success
        # if closed and nothing in front of sensor --> fail
        print "close further"
        return order.keep_going(), 0
    
    # Ball freilassen
    def __release(self, line_data, bt_data, queue_size):
        
        if not self.__gripperOpen:
            self.__gripperOpen = True
            self.__lastChange = time.time()
            return order.open(), 0
        
        if (self.__lastChange + 1 > time.time()):
            print "zurueckfahren"
            return order.move(0,-50,-47), 0    # zurückfahren
        
        elif (self.__lastChange + 2 > time.time()):
            print "drehen"
            return order.left(0,70,70), 0    #ohne Sensor vorwärts fahren
        
        return order.stop(), Transition.SUCCESS 
        
        """ open gripper, drive a little backwards, transition to next state.
        
        Transition will be done immediately. But since timed orders cannot be overwritten, they are going to be 
        followed even in the next state.
        
        TODO: What about turning and facing the field again? Should be done in "Search", because the line sensor alarms.
        """
        
        # gives orders and goes directly to next state --> orders will be obeyed in other state too, next orders cannot overwrite them
        'return [order.open(), order.reverse(500), order.stop()], Transition.SUCCESS '
            

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