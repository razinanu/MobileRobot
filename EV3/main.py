#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from rfcomm_server import RFCOMMServer


btserver = RFCOMMServer()

btserver.wait_for_connection()


while True:
    data = btserver.wait_for_data()

btserver.close()