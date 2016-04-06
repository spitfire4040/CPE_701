#!/usr/bin/python

# header files
import socket
import sys
import thread
import SocketServer
import os
import time
import random
import binascii
import pickle
import json

# create path to included files
sys.path.append('../PhysicalLayer')
sys.path.append('../NetworkLayer')
sys.path.append('../RoutingProtocol')

# import files
import Physical
import Network
import Routing

# set global variables
hostname = ' '
port = 0
link1_hostname = ' '
link1_port = ' '
link2_hostname = ' '
link2_port = ' '
LOSS_FLAG = False
CORRUPT_FLAG = False
link1_flag = False
link2_flag = False
timer1_flag = False
timer2_flag = False
inhibit1 = False
inhibit2 = False
mynode = None
L = 0
C = 0


# Class: MyUDPHandler
class MyUDPHandler(SocketServer.BaseRequestHandler):

  # interrupt handler for incoming messages
    def handle(self):
      global mynode, link1_port, link2_port, link1_flag, link2_flag

      data = self.request[0].strip()
      #socket = self.request[1]

      # set message and split
      message = data
      message = message.split()

      # look for 'hello' message
      if message[0] == "hhhhh":

        # set link flags
        if message[1] == link1_port:
          link1_flag = True
        if message[1] == link2_port:
          link2_flag = True

      # not hello, forward to network layer
      else:
        Network.l3_recvfrom(mynode, data)


# Function: l2_sendto()
def l2_sendto(node, last_nid, dest_nid, payload):
  global mynode, nid, LOSS_FLAG, CORRUPT_FLAG, L, C

  # call garbler function each time...
  garbler()

  # check garbler flags to see if packet lost
  if (LOSS_FLAG == False):    
    try:
      if (CORRUPT_FLAG == True):

        # unpack payload from layer 3
        datagram = json.loads(payload)

        # get segment from datagram (l3)
        frame = datagram['payload']

        # unpack segment (packed at l4)
        segment = json.loads(frame)

        # get data from frame (l4)
        message = segment['data']

        # append message
        message = (message + 'abcde')

        # put message back in segment
        segment['data'] = message

        # repack segment (frame)
        frame = json.dumps(segment)

        # put frame back in datagram
        datagram['payload'] = frame

        # repack datagram (payload)
        payload = json.dumps(datagram)

      # get link table and find links for this node
      links = node.GetLinkTable()
      for link in links:
        if int(link) == int(node.GetNID()):
          this_node = links[link]
          n1 = this_node[0]
          n2 = this_node[1]

      # find the link that was not the last link (no loops), set as target
      if int(n1) == int(last_nid):
        target = n2

      elif int(n2) == int(last_nid):
        target = n1

      else:
        #target = n1
        target = Routing.next_hop(node, dest_nid)

      # get links for this node
      links = node.GetLinks()
      link1 = links[0]
      link2 = links[1]

      # find the right link and set address, port
      if str(link1[0]) == str(target):
        dest_hostname = link1[1]
        dest_port = link1[2]

      if str(link2[0]) == str(target):
        dest_hostname = link2[1]
        dest_port = link2[2]

      # create udp socket and send
      sock = socket.socket(socket.AF_INET, # Internet
                   socket.SOCK_DGRAM) # UDP
      sock.sendto(payload, (dest_hostname, int(dest_port)))
    except:
      print "couldn't send message"
  else:
    pass

  # reset garbler
  LOSS_FLAG = False
  CORRUPT_FLAG = False
  L = 0
  C = 0


# function: start listener
def start_listener(node):
  # global variables
  global mynode, hostname, port, nid, link1_hostname, link1_port, link2_hostname, link2_port

  mynode = node

  # check links for node attributes
  links = node.GetLinks()
  link1 = links[0]
  link2 = links[1]

  link1_hostname = link1[1]
  link1_port = link1[2]

  link2_hostname = link2[1]
  link2_port = link2[2]

  hostname = node.GetHostName()
  nid = node.GetNID()
  port = node.GetPort()

  # slight pause to let things catch up
  time.sleep(2)

  # start threads for listener, hello, and timer
  thread.start_new_thread(receiver, ())
  thread.start_new_thread(hello, ())
  thread.start_new_thread(timer, (node,))


# function: receiver (listener)
def receiver():
  global hostname, port

  # set socket for listener
  try:
    server = SocketServer.UDPServer((hostname, int(port)), MyUDPHandler)
    server.serve_forever()

  # report error if fail
  except:
    print "failed to start listener"


# function: hello (alive)
def hello():
  # global variables
  global hostname, port, link1_hostname, link1_port, link2_hostname, link2_port

  # eternal loop
  while (1):

    # open socket and send to neighbor 1
    sock = socket.socket(socket.AF_INET, # Internet
                   socket.SOCK_DGRAM) # UDP
    sock.sendto("hhhhh" + ' ' + port, (link1_hostname, int(link1_port)))
    time.sleep(1)

    # open socket and send to neighbor 2
    sock = socket.socket(socket.AF_INET, # Internet
                   socket.SOCK_DGRAM) # UDP
    sock.sendto("hhhhh" + ' ' + port, (link2_hostname, int(link2_port)))
    time.sleep(1)


# function: timer (for hello)
def timer(node):
  global link1_flag, link2_flag, inhibit1, inhibit2

  # eternal loop
  while (1):

    # first wait 10 seconds, then set flags to false
    for x in range(10):
      time.sleep(1)
    link1_flag = False
    link2_flag = False

    # now check for true for 5 second period
    for x in range(5):
      time.sleep(1)

    # if true flag found, set neighbor 1 up flag
    if link1_flag == False:
      node.SetUpFlagL1(False)
    if link1_flag == True and inhibit1 == False:
      node.SetUpFlagL1(True)

    # check for inhibit
    if inhibit1 == True:
      node.SetUpFlagL1(False)

    # if true flag found, set neighbor 2 flag
    if link2_flag == False:
      node.SetUpFlagL2(False)
    if link2_flag == True and inhibit2 == False:
      node.SetUpFlagL2(True)

    # check for inhibit
    if inhibit2 == True:
      link2.SetUpFlagL2(False)

    #print "up flag 1: ", node.GetUpFlagL1()
    #print "up flag 2: ", node.GetUpFlagL2()


# function: inhibit
def inhibit(N):
  global inhibit1, inhibit2
  if N == 'i1':
    inhibit1 = True

  if N == 'u1':
    inhibit1 = False

  if N == 'i2':
    inhibit2 = True

  if N == 'u2':
    inhibit2 = False


# function: set_garbler
def set_garbler(l, c):
  # initialize global variables
  global L, C

  # set global values
  L = l
  C = c

# function: garbler
def garbler():
  # Packet Loss Flags, probablility variable
  global LOSS_FLAG, CORRUPT_FLAG, L, C

  # generate random number and set flag
  lossList = []

  # generate random number and set flag
  lossList = random.sample(range(1, 101), int(L))
  if (50 in lossList):
    LOSS_FLAG = True

  # Corruption Flags, probablility variable
  corruptList = []

  # generate random number and set flag
  corruptList = random.sample(range(1, 101), int(C))
  if (50 in corruptList):
    CORRUPT_FLAG = True
