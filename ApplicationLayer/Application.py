#!/usr/bin/python

# import header files
import os
import sys
import thread
import time
import base64
import binascii
import os.path
import json
from random import randint

# create paths to folders
sys.path.append('../PhysicalLayer')
sys.path.append('../LinkLayer')
sys.path.append('../NetworkLayer')
sys.path.append('../RoutingProtocol')
sys.path.append('../TransportLayer')

# include files
import Physical
import Link
import Network
import Routing
import Transport

# initialize node object in physical layer
node = Physical.InitializeTopology(sys.argv[1], sys.argv[2])

# initialize SID list
SID_LIST = {}
CONN_LIST = {}

		
# function: list_service_points
def list_service_points():
	global SID_LIST, CONN_LIST

	print "SID_LIST: ", SID_LIST
	print "CONN_LIST: ", CONN_LIST
	raw_input("Press enter to continue...")


# function: encode_file
def encode_file(myfile, SID):
	with open(myfile, "rb") as image_file:
		encoded_string = base64.b64encode(image_file.read())
	return encoded_string


# function: decode_file
def decode_file(myfile, SID):
	out = open(myfile, "wb")
	out.write(encoded_string.decode('base64'))
	out.close()


# function: print usage (bad input)
def PrintUsage ():
  print('\nUsage: python <filename> <nid> <itc script>')


# function menu
def menu():
	print "CHOOSE THE NUMBER OF YOUR SELECTION"
	print "-----------------------------------"
	print "1.   start service"
	print "2.   stop service:"
	print "3.   list service points"
	print "4.   connect"
	print "5.   close"
	print "6.   download"
	print "7.   set garbler"
	print "8.   route table"
	print "9.   link down"
	print "10.  link up"
	print "11.  send text message"
	print "12.  print status"
	print "13.  terminate program"
	print ' '


# function: start service
def start_service(P):
	global SID_LIST, CONN_LIST

	if (int(P) < 1):
		os.system('clear')
		print "start_service(0) - Failure: MaxCons=" + P + " bad argument"
	else:
		SID = randint(101, 999)
		SID_LIST[str(SID)] = (P,[])
		os.system('clear')
		print "start_service(" + str(P) + ") - Success: SID=" + str(SID) + ", MaxCons=" + str(P)
	raw_input("Press enter to continue...")


# function: stop service
def stop_service(S):
	global SID_LIST, CONN_LIST

	if (str(S)) in SID_LIST:
		del SID_LIST[str(S)]
		print "stop_service(" + str(S) + ") - Success: SID=" + str(S) + " is terminated"
	else:
		print "stop_service(" + str(S) + ") - Failure: SID=" + str(S) + " does not exist"
	raw_input("Press enter to continue...")


# function: connect
def connect(Y, S, W):
	global node, SID_LIST, CONN_LIST
	dest_nid = Y
	string = {}
	string['code'] = '20'
	string['source_nid'] = str(node.GetNID())
	string['SID'] = S
	string['window'] = W
	data = json.dumps(string)
	Transport.l4_sendto(node, dest_nid, data)


#function: close
def close(C):
	global SID_LIST, CONN_LIST
	pass

	"""
	This command closes the connection with CID C.
	Examples of resulting messages:
	"close(3) - Success: CID=3 is closed"
	"close(7) - Failure: CID=7 is not open"
	"close(8) - Failure: CID=8 cannot be closed"
	"""

# function: download
def download(N, F):
	global node, SID_LIST, CONN_LIST
	dest_nid = N
	filename = F
	SID = 32 #request file
	data = filename

	Transport.l4_sendto(node, dest_nid, SID, data)

	"""
	dest_nid = raw_input("Enter NID of target: ")
	data = raw_input("Enter Text Message: ")
	SID = 100
	Transport.l4_sendto(node, dest_nid, SID, data)
	"""




	"""
	This command downloads a file with name F through the connection with CID
	C. The transfer is possible only if that connection is not currently busy with another download
	operation. The file F should be present at the current working directory of the process running at 
	CPE 701 Internet Protocol Design CSE Department, UNR
	5
	the remote end of the connection. After the transfer is completed, a message should report the
	duration and average throughput of the transfer. Note that the same connection can be used for
	multiple download operations.
	Examples of resulting messages:
	"download(4, foo) - Success: File=foo has been downloaded (duration=3sec,throughput=160KBps)"
	"download(4, bar) - Failure: File=bar does not exist"
	"download(5, foo) - Failure: CID=5 does not exist"
	"download(6, bar) - Failure: CID=6 is busy with other transfer"
	"download(7, bar) - Failure: CID=7 is broken"
	"""

# function: set garbler
def set_garbler(L, C):
	print "L = ", L
	print "C = ", C
	if int(L) > 100:
		os.system('clear')
		print "Failure: Loss = " + str(L) + "% bad argument"
		raw_input("press enter to continue...")

	elif int(C) > 100:
		os.system('clear')
		print "Failure: Corruption = " + str(C) + "% bad argument"
		raw_input("press enter to continue...")

	else:
		Link.set_garbler(L, C)
		os.system('clear')


# function: route table
def route_table(node):
	os.system('clear')
	Routing.route_table(node)


# function: link down
def link_down(N):
	global Node

	# search links list for attributes
	links = node.GetLinks()
	link1 = links[0]
	link2 = links[1]

	status1 = node.GetUpFlagL1()
	status2 = node.GetUpFlagL2()

	# clear screen
	os.system('clear')

	# find the right link and set flag
	if int(N) == link1[0]:
		if status1 == False:
			print "Failure: link to node-" + N + " is already down"
			raw_input("press enter to continue...")
		else:
			Link.inhibit('i1')
			print "Success: link to node-" + N + " is down"
			raw_input("press enter to continue...")

	# find the right link and set flag
	elif int(N) == link2[0]:
		if status2 == False:
			print "Failure: link to node-" + N + " is already down"
			raw_input("press enter to continue...")
		else:
			Link.inhibit('i2')
			print "Success: link to node-" + N + " is down"
			raw_input("press enter to continue...")
	
	# if no link, print error message
	else:
		print "Failure: link to node-" + N + " does not exist"
		raw_input("press enter to continue...")


# function: link up
def link_up(N):
	global node

	# search links list for attributes
	links = node.GetLinks()
	link1 = links[0]
	link2 = links[1]

	status1 = node.GetUpFlagL1()
	status2 = node.GetUpFlagL2()

	# clear screen
	os.system('clear')

	# find the right link and set flag
	if int(N) == link1[0]:
		if status1 == True:
			print "Failure: link to node-" + N + " is already up"
			raw_input("press enter to continue...")
		else:
			Link.inhibit('u1')
			print "Success: link to node-" + N + " is up"
			raw_input("press enter to continue...")

	# find the right link and set flag
	elif int(N) == link2[0]:
		if status2 == True:
			print "Failure: link to node-" + N + " is already up"
			raw_input("press enter to continue...")
		else:
			Link.inhibit('u2')
			print "Success: link to node-" + N + " is up"
			raw_input("press enter to continue...")
	
	# if no link, print error message
	else:
		print "Failure: link to node-" + N + " does not exist"
		raw_input("press enter to continue...")

# function: l5_recvfrom (incoming message from layer 4)
def l5_recvfrom(source_nid, dest_nid, data):
	global node, SID_LIST, CONN_LIST

	data = json.loads(data)
	code = data['code']


	# if incoming message is a text message
	if (code == '10'):
		text = data['message']
		print '\n'
		os.system('clear')
		print "text: ", text
		raw_input("Press enter to continue... ")

	# if incoming message is a connection request
	elif (code == '20'):
		dest_nid = data['source_nid']
		SID = data['SID']
		window = data['window']
		CID = randint(1000, 9999)
		print "SID_LIST", SID_LIST
		print 'list_service_points', (list_service_points())
		if (SID in SID_LIST):
			if (len(SID_LIST['SID'][1]) < int(SID_LIST['SID'][0])):
				SID_LIST['SID'].append(str(CID))
				CONN_LIST['CID'] = dest_nid
				string = {}
				string['code'] = '30'
				string['CID'] = str(CID)
				data = json.dumps(string)
			else:
				string = {}
				string['code'] = '40'
				data = json.dumps(string)
		else:
			string = {}
			string['code'] = '50'
			data = json.dumps(string)

		Transport.l4_sendto(node, dest_nid, data)
		#print ("Press enter to continue... ")

	# if incoming message is a connection response
	if (code == '30'):
		print '\n'
		CID = data['CID']
		os.system('clear')
		print ("CID: " + CID)

	# if incoming message is a connection response
	if (code == '40'):
		print '\n'
		os.system('clear')
		print 'No connections for that SID available'

	# if incoming message is a connection response
	if (code == '50'):
		print '\n'
		os.system('clear')
		print 'SID does not exist'

	# if incoming message is a connection response
	if (code == 32):
		print '\n'
		filename = data
		os.system('clear')
		exists = os.path.isfile(filename)
		if (exists == True):
			print ("yup, it's here. I'll send it!")

			temp = []
			f = open(filename)
			cf = f.read()
			f.close()
			string = base64.b64encode(str(cf))
			newstring = bin(int(binascii.hexlify(string), 16))
			dest_nid = source_nid
			source_nid = node.GetNID()
			SID = 33
			data = newstring
			Transport.l4_sendto(node, dest_nid, SID, data)

		else:
			print ("nope, it's not here")
			dest_nid = source_nid
			source_nid = node.GetNID()
			SID = 100
			data = "file " + filename + " does not exist, sorry!"
			Transport.l4_sendto(node, dest_nid, SID, data)

		print ("Press enter to continue... ")

		if (code == 33):
			print "data: ", data

	else:
		pass


# main function
def main (argv):
	global node, SID_LIST, CONN_LIST

	#check for proper input
 	if len(sys.argv) != 3:
		PrintUsage()

    # good input, start program
	else:
		run = 1

  	# initialize node object in physical layer
  	node = Physical.InitializeTopology(sys.argv[1], sys.argv[2])

  	# wait for node to propagate
  	time.sleep(2)

	#start listen threads
	Link.start_listener(node)

	# begin loop
	while(run == 1):

		# clear screen
		os.system('clear')

		# print menu
		menu()

		# prompt for input
		message = raw_input("Enter your selection: ")

		# print menu to screen
		#if (message == "MENU") or (message == "Menu") or (message == "menu"):

		# start new service
		if (message == '1'):
			P = raw_input("Enter the maximum number of connections this service point will accept: ")
			start_service(P)

		# stop service
		if (message == '2'):
			S = raw_input("Enter the Service ID of the node you wish to stop service with: ")
			stop_service(S)

		# list service points
		if (message == '3'):
			list_service_points()

		# connect to node x
		if (message == '4'):
			Y = raw_input("Enter the node you would like to connect to: ")
			S = raw_input("Enter the SID of the node: ")
			W = raw_input("Enter a value between 1-5 to set the window for packets in flight: ")
			connect(Y, S, W)

		# close connection with node x
		if (message == '5'):
			C = raw_input("Enter the CID of the connection you would like to close: ")
			close(C)

		# download from node x
		if (message == '6'):
			N = raw_input("Enter the NID of the peer from whom you would like to download: ")
			F = raw_input("Enter the name of the file you would like to download: ")
			thread.start_new_thread(download, (N,F))

		# set garbler probability
		if (message == '7'):
			L = raw_input("Set the probability of packet loss (1-100): ")
			C = raw_input("Set the probability of packet corruption (1-100): ")
			set_garbler(L, C)

		# display next hop data
		if (message == '8'):
			route_table(node)

		# down link to node x
		if (message == '9'):
			N = raw_input("Enter the node with whom you would like to down a link: ")
			link_down(N)

		# up link to node x
		if (message == '10'):
			N = raw_input("Enter the node with whom you would like to up a link: ")
			link_up(N)

		# for testing, send simple text message
		if (message == "11"):
			dest_nid = raw_input("Enter NID of target: ")
			text = raw_input("Enter Text Message: ")
			string = {}
			string['code'] = '10'
			string['message'] = text
			data = json.dumps(string)
			Transport.l4_sendto(node, dest_nid, data)

		# for testing node at physical layer
		if (message == "12"):
			node.PrintStatus()

		# exit program
		if (message == '13') or (message == 'Exit') or (message == 'exit'):
			run = 0

  

if __name__ == '__main__':
  main(sys.argv)