#!/usr/bin/python

import socket
import sys
import threading
import json
import re

sys.path.append('../PhysicalLayer')
sys.path.append('../LinkLayer')
sys.path.append('../RoutingProtocol')
sys.path.append('../TransportLayer')

import Physical
import Link
import Routing
import Transport
      

def l3_sendto(node, dest_nid, segment):

  # get list of all links from link table and find link for this node
  links = node.GetLinks()
  link1 = links[0]

  # set hostname, port this node
  hostname = link1[1]
  port = link1[2]

  # set sequence number (fix later)
  sequence_number = 1

  # set sequence total (fix later)
  sequence_total = 1

  # set ttl
  ttl = 20

  # set mtu
  mtu = 1000

  # get port table for this node and set values for destination target
  PortTable = node.GetPortTable()
  for link in PortTable:
    info = PortTable[link]
    if info[0] == dest_nid:
      dest_hostname = info[1]
      dest_port = info[2]

  # set last nid value (for routing)
  last_nid = node.GetNID()

  # build datagram
  datagram = {}
  datagram['source_hostname'] = node.GetHostName()
  datagram['source_nid'] = node.GetNID()
  datagram['source_port'] = node.GetPort()
  datagram['destination_hostname'] = dest_hostname
  datagram['destination_nid'] = dest_nid
  datagram['destination_port'] = dest_port
  datagram['ttl'] = ttl
  datagram['mtu'] = mtu
  datagram['payload'] = segment
  datagram['last_nid'] = node.GetNID()

  # encode payload
  payload = json.dumps(datagram)

  # pass to link layer for sending
  Link.l2_sendto(node, last_nid, dest_nid, payload)


# function: l3_recvfrom
def l3_recvfrom(node, message):
  
  # decode payload
  data = json.loads(message)

  # get destination nid from payload
  dest_nid = data['destination_nid']

  # get last nid from payload
  last_nid = data['last_nid']

  # reset last nid
  data['last_nid'] = node.GetNID()

  # set variable for segment
  segment = data['payload']

  # if it is for this node, pass it up to layer 4
  if str(dest_nid) == str(node.GetNID()):
    Transport.l4_recvfrom(segment)

  # if its not for this node, send it back down to layer 2
  else:
    ttl = data['ttl']
    new_ttl = (ttl - 1)
    data['ttl'] = new_ttl
    if (data['ttl'] > 0):
      datagram = json.dumps(data)
      Link.l2_sendto(node, last_nid, dest_nid, datagram)
    else:
      pass

 # April 28, 2016