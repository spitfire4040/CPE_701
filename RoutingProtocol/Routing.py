#!/usr/bin/python

import sys

sys.path.append('../PhysicalLayer')
sys.path.append('../LinkLayer')

import Physical
import Link

# function: route table

"""
This command prints the local routing table at the node. It must show the
corresponding next-hop and the cost of the route in terms of number of hops.
"""

# Hello Sifat! The flags are now working, can they be used to dynamically determine the next hop?
# I set them as global, and they are called when the function is called (link1_flag, link2_flag)

# initialize global variables
link1_flag = ''
link2_flag = ''

def route_table(node):
	# include global variables
	global link1_flag, link2_flag

	# set state of link flags
	link1_flag = node.GetUpFlagL1()
	link2_flag = node.GetUpFlagL2()

	links = node.GetLinks()
	tabl = node.linkTable
	print tabl
	print "Destination NID   Cost/Metrix   Next Hop\n"
	for k in tabl.keys():
		if (k!=int(node.nid)):
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
							#print tn2
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
							#print tn2
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

	#print link2[0]
	# print state of flags (for testing)
	print "Link 1 flag is ", link1_flag
	print "Link 2 flag is ", link2_flag


	raw_input("press enter to continue...")

	#pass

def next_hop(node, last_nid):
	# include global variables
	global link1_flag, link2_flag

	# set state of link flags
	link1_flag = node.GetUpFlagL1()
	link2_flag = node.GetUpFlagL2()

	links = node.GetLinks()
	tabl = node.linkTable
	print "in routing", last_nid;
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
							#print tn2
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
							#print tn2
						break
				if metrix2>10:
					break
			if metrix2>metrix1: 
				metrix = metrix1
				nh = links[0][0]
				print nh
			else: 
				metrix = metrix2
				nh = links[1][0]
				print nh
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