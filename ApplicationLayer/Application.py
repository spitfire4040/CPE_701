#!/usr/bin/python

# import header files
import os
import sys

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


# function: print usage (bad input)
def PrintUsage ():
  print('\nUsage: python <filename> <nid> <itc script>')


# function menu
def menu():
	print "1.  start_service(P):"
	print "2.  stop_service(S):"
	print "3.  connect(Y, S, W):"
	print "4.  close(C):"
	print "5.  download(C, F):"
	print "6.  set_garbler(L, C):"
	print "7.  route_table():"
	print "8.  link_down(N):"
	print "9.  link_up(N):"
	print "Enter 'exit' to terminate program"
	raw_input("Press enter to continue...")


# function: start service
def start_service(P):
	pass

	"""
	This command establishes a service point at the local node, say X. The
	command returns a Service ID (SID) S, that is unique for each service point of node X. Other
	nodes can connect to S, and download files from that service point. The argument P is the
	maximum number of open connections that S can accept; requests for more than P connections
	are rejected.
	Examples of resulting messages:
	start_service(3) - Success: SID=123, MaxCons=3
	start_service(0) - Failure: MaxCons=0 bad argument 
	"""

# function: stop service
def stop_service(S):
	pass

	"""
	This command terminates the service point with SID S at the local node. Any
	open connections at that SID are aborted.
	Examples of resulting messages:
	"stop_service(123) - Success: SID=123 is terminated"
	print"stop_service(200) - Failure: SID=200 does not exist"
	"""

# function: connect
def connect(Y, S, W):
	pass

	"""
	This command establishes a connection from the local node, say X, to the
	service point with SID S of the remote node Y. The window for the connection should be W. The
	command returns a Connection ID (CID) C, that is unique for each open connection at the client.
	Examples of resulting messages:
	"connect(2, 123, 15000) - Success: DestNode=2, SID=123, CID=3, Win=15000B"
	"connect(3, 123, 15000) - Failure: DestNode=3 connection request timed out"
	"connect(3, 123, 15000) - Failure: DestNode=3 rejected connection request"
	"""

#function: close
def close(C):
	pass

	"""
	This command closes the connection with CID C.
	Examples of resulting messages:
	"close(3) - Success: CID=3 is closed"
	"close(7) - Failure: CID=7 is not open"
	"close(8) - Failure: CID=8 cannot be closed"
	"""

# function: download
def download(C, F):
	pass

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
		Link.garbler(L, C)
		os.system('clear')


# function: route table
def route_table():
	pass

	"""
	This command prints the local routing table at the node. It must show the
	corresponding next-hop and the cost of the route in terms of number of hops.
	"""


# function: link down
def link_down(node, N):

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
def link_up(node, N):

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
def l5_recvfrom(data):
	print '\n'
	os.system('clear')
	print data
	print "Enter A Command, or 'menu' to see all options: "


# main function
def main (argv):

	#check for proper input
 	if len(sys.argv) != 3:
		PrintUsage()

    # good input, start program
	else:
		run = 1

  	# initialize node object in physical layer
  	node = Physical.InitializeTopology(sys.argv[1], sys.argv[2])

	#start listen threads
	Link.start_listener(node)


	# begin loop
	while(run == 1):

		# clear screen
		os.system('clear')

		# prompt for input
		message = raw_input("Enter A Command, or 'menu' to see all options: ")

		# for testing node at physical layer
		if (message == "PrintStatus"):
			node.PrintStatus()

		# for testing, send simple text message
		if (message == "send message"):
			dest_nid = raw_input("Enter NID of target: ")
			data = raw_input("Enter Message: ")
			Transport.l4_sendto(node, dest_nid, data)

		# print menu to screen
		if (message == "MENU") or (message == "Menu") or (message == "menu"):
			menu()

		# start new service
		if (message == '1'):
			P = raw_input("Enter the maximum number of connections this service point will accept: ")
			start_service(P)

		# stop service
		if (message == '2'):
			S = raw_input("Enter the Service ID of the node you wish to stop service with: ")
			stop_service(S)

		# connect to node x
		if (message == '3'):
			Y = raw_input("Enter the node you would like to connect to: ")
			S = raw_input("Enter the SID of the node: ")
			W = raw_input("Enter a value between 1-5 to set the window for packets in flight")
			connect(Y, S, W)

		# close connection with node x
		if (message == '4'):
			C = raw_input("Enter the CID of the connection you would like to close: ")
			close(C)

		# download from node x
		if (message == '5'):
			C = raw_input("Enter the CID of the peer from whom you would like to download: ")
			F = raw_input("Enter the name of the file you would like to download")
			download(C, F)

		# set garbler probability
		if (message == '6'):
			L = raw_input("Set the probability of packet loss (1-100): ")
			C = raw_input("Set the probability of packet corruption (1-100): ")
			set_garbler(L, C)

		# display next hop data
		if (message == '7'):
			route_table(node)

		# down link to node x
		if (message == '8'):
			N = raw_input("Enter the node with whom you would like to down a link: ")
			link_down(node, N)

		# up link to node x
		if (message == '9'):
			N = raw_input("Enter the node with whom you would like to up a link: ")
			link_up(node, N)

		# exit program
		if (message == 'Exit') or (message == 'Exit') or (message == 'exit'):
			run = 0

  

if __name__ == '__main__':
  main(sys.argv)
