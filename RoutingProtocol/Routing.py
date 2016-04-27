#!/usr/bin/python

import sys

sys.path.append('../PhysicalLayer')
sys.path.append('../LinkLayer')

import Physical
import Link

# initialize global variables
link1_flag = ''
link2_flag = ''

# function: route table printing
def route_table(node):
	# include global variables
	global link1_flag, link2_flag	# Flags to check link status of the current node

	link1_flag = Link.routing_flag1()
	link2_flag = Link.routing_flag2()

	links = node.GetLinks()	  	# Links of the current node
	tabl = node.linkTable		# Link table of the topology
	print "Destination NID   Cost/Metrix   Next Hop\n"
	for k in tabl.keys():		# Traverse through the Link Table
		# If the node is not the current node
		if (k!=int(node.nid)):	
			# Since there are maximum two links per node, only two possible routes to the destination
			# exists. This portion of the code calculates the costs and next hop values for both of these
			# routes, one by one
			metrix1 = 1
			tn1 = int(node.nid)	# Source (current) NID	
			tn2 = links[0][0]	# One of the connected nodes' NID
			while tn2!=k:				
				for key, value in tabl.items():
					if key==tn2:
						# If end of path occurs
						if len(filter(bool, value))==1:
							metrix1 = 100
							break
						# Else, continue traversing, by updating values of tn1 and tn2
						else:
							if value[0]==tn1:
								tn1 = tn2
								tn2 = value[1]
								metrix1 += 1
							else:
								tn1 = tn2
								tn2 = value[0]
								metrix1 += 1
						break
				if metrix1>10:
					break
			metrix2 = 1
			tn1 = int(node.nid)	# Source (current) NID
			tn2 = links[1][0]	# Other connected nodes' NID
			while tn2!=k:				
				for key, value in tabl.items():
					if key==tn2:
						# If end of path occurs
						if len(filter(bool, value))==1:
							metrix2 = 100
							break
						# Else, continue traversing, by updating values of tn1 and tn2
						else:
							if value[0]==tn1:
								tn1 = tn2
								tn2 = value[1]
								metrix2 += 1
							else:
								tn1 = tn2
								tn2 = value[0]
								metrix2 += 1
						break
				if metrix2>10:
					break
			if metrix2>metrix1: 
				metrix = metrix1
				nhop = links[0][0]
			else: 
				metrix = metrix2
				nhop = links[1][0]
			if link1_flag==False and link2_flag==False:
				metrix = "inf"
				nhop = "not reachable"
			if link1_flag==False and link2_flag==True:
				metrix = metrix2
				nhop = links[1][0]
			if link1_flag==True and link2_flag==False:
				metrix = metrix1
				nhop = links[0][0]
			print '{0:^14}{1:^21}{2:^3}\n'.format(k, metrix, nhop)
	# print state of flags (for testing)
	print "Link 1 flag is ", link1_flag
	print "Link 2 flag is ", link2_flag

	raw_input("press enter to continue...")

# Function to find the next hop for a particular destination. It is same as the route table function, except it
# only calculates the next hop for the shortest path to reach to that particular destination (not all the other nodes.)

def next_hop(node, last_nid):
	# include global variables
	global link1_flag, link2_flag

	link1_flag = Link.routing_flag1()
	link2_flag = Link.routing_flag2()

	links = node.GetLinks()
	tabl = node.linkTable
	#print "in routing", last_nid;
	for k in tabl.keys():
		if (k==int(last_nid)):
			metrix1 = 1
			tn1 = int(node.nid)
			tn2 = links[0][0]
			while tn2!=k:				
				for key, value in tabl.items():
					if key==tn2:
						if len(filter(bool, value))==1:
							metrix1 = 100
							break
						else:
							if value[0]==tn1:
								tn1 = tn2
								tn2 = value[1]
								metrix1 += 1
							else:
								tn1 = tn2
								tn2 = value[0]
								metrix1 += 1
						break
				if metrix1>10:
					break
			metrix2 = 1
			tn1 = int(node.nid)
			tn2 = links[1][0]
			while tn2!=k:				
				for key, value in tabl.items():
					if key==tn2:
						if len(filter(bool, value))==1:
							metrix2 = 100
							break
						else:
							if value[0]==tn1:
								tn1 = tn2
								tn2 = value[1]
								metrix2 += 1
							else:
								tn1 = tn2
								tn2 = value[0]
								metrix2 += 1
						break
				if metrix2>10:
					break
			if metrix2>metrix1: 
				metrix = metrix1
				nh = links[0][0]
				#print nh
			else: 
				metrix = metrix2
				nh = links[1][0]
				#print nh
			if link1_flag==False and link2_flag==False:
				metrix = "inf"
				nh = "not reachable"
			if link1_flag==False and link2_flag==True:
				metrix = metrix2
				nh = links[1][0]
			if link1_flag==True and link2_flag==False:
				metrix = metrix1
				nh = links[0][0]
	return nh
