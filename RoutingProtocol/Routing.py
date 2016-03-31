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

def route_table(node):
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
			print '{0:^14}{1:^21}{2:^3}\n'.format(k, metrix, nhop)

			#print link2[0]


	raw_input("press enter to continue...")

	#pass

def next_hop(node):
	links = node.GetLinks()
	tabl = node.linkTable
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
				nh = links[0][0]
			else: 
				metrix = metrix2
				nh = links[1][0]
	return nh
