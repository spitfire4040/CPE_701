#!/usr/bin/python

import socket     # Low-level networking interface.
import sys        # Basic system functionality.
import threading  # Higher-level threading interface.
import json
import hashlib
import os
import time

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


def chunkstring(string, length):
	return (string[0+i:length+i] for i in range(0, len(string), length))


def l4_sendto(node, dest_nid, data):
	"""
	# if sending a file, check size
	if SID == 33:
		os.system('clear')
		size = sys.getsizeof(data)
		print "file size: ", size
		print data

		mylist = list(chunkstring(data, 20000))
		listlength = len(mylist)

		for x in range(0, listlength):
			print mylist[x]
			print ' '


		time.sleep(5)
	"""


	# get port table for this node and set values for destination target
	PortTable = node.GetPortTable()
	for link in PortTable:
		info = PortTable[link]

		if info[0] == dest_nid:
			dest_port = info[2]

	# get md5 hash of data for checksum
	m = hashlib.md5()
	m.update(data)
	checksum = m.hexdigest()


	# build datagram
	frame = {}
	frame['source_nid'] = node.GetNID()
	frame['source_port'] = node.GetPort()
	frame['destination_nid'] = dest_nid
	frame['destination_port'] = dest_port
	frame['sequence_number'] = 1
	frame['ack_number'] = 1
	frame['window_size'] = 15
	frame['checksum'] = checksum
	frame['data'] = data

	# encode payload
	payload = json.dumps(frame)

	Network.l3_sendto(node, dest_nid, payload)


def l4_recvfrom(segment):

	frame = json.loads(segment)

	source_nid = frame['source_nid']
	source_port = frame['source_port']
	dest_nid = frame['destination_nid']
	dest_port = frame['destination_port']
	sequence_number = frame['sequence_number']
	ack_number = frame['ack_number']
	window_size = frame['window_size']
	checksum = frame['checksum']
	data = frame['data']

	# get md5 hash of data for checksum
	m = hashlib.md5()
	m.update(data)
	test = m.hexdigest()

	# compare checksums
	if (checksum == test):
		Application.l5_recvfrom(source_nid, dest_nid, data)
	else:
		data = "message was corrupted"
		Application.l5_recvfrom(source_nid, dest_nid, data)