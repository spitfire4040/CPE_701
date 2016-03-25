#!/usr/bin/python

import errno      # For errors!
import socket     # Low-level networking interface.
import sys        # Basic system functionality.
import threading  # Higher-level threading interface.

sys.path.append('../PhysicalLayer')
sys.path.append('../LinkLayer')
sys.path.append('../NetworkLayer')
sys.path.append('../RoutingProtocol')
sys.path.append('../ApplicationLayer')

import Physical
import Link
import Network
import Routing
import Application

def l4_sendto(node, dest_nid, data):
  segment = data
  Network.l3_sendto(node, dest_nid, segment)

def l4_recvfrom(segment):
  data = segment
  Application.l5_recvfrom(data)
