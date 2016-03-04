#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import bluetooth
import time

class RFCOMMServer:

    def __init__(self):
        self.__server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
    
        port = 1
        self.__server_sock.bind(("",port))
        self.__server_sock.listen(1)
    
    def wait_for_connection(self):
        self.__client_sock,address = self.__server_sock.accept()
        print "Accepted connection from ",address
    
    def wait_for_data(self):
        """ IMPORTANT: blocks other processes. Stop movement before calling this method!
        """
        
        data = self.__client_sock.recv(1024)
        print "received [%s]" % data
        return data
    
    def close(self):
        self.__client_sock.close()
        self.__server_sock.close()
