#!/usr/bin/python

# import header files
import sys
import os

node = None


# function: InitializeTopology
def InitializeTopology (nid, itc):

  # initialize node object
  node = Node(nid)

  # open itc.txt file and read to list
  infile = open(itc)
  list = infile.readlines()

  # initialize lists for hostnames and port numbers
  hostnames = []
  ports = []

  # populate lists
  for entry in list:
    temp = entry.split(' ')
    hostnames.append(temp[1])
    ports.append(temp[2])

  # use list to populate LinkTable and PortTable
  for entry in list:
    temp = entry.split(' ')
    node.SetLinkTable(int(temp[0]), (int(temp[3]), int(temp[4])))
    node.SetPortTable(temp[0], temp[1], temp[2])

    if node.GetNID() == temp[0]:
      node.SetHostName(temp[1])
      node.SetPort(temp[2])

      # Add links 
      number_of_nodes = len(temp) - 4
      index = 3
      
      for i in range(number_of_nodes):
        corresponding_hostname = hostnames[int(temp[index+i])-1]
        corresponding_port = ports[int(temp[index+i])-1]
        node.AddLink((int(temp[index+i]), corresponding_hostname, corresponding_port))
    
      # set mtu for local node
      node.SetMTU(int(temp[-1].strip()))

  # close itc.txt file
  infile.close()
  
  # return object
  return node


# class: Node
class Node(object):

  # initialize node
  def __init__ (self, nid=0, host_name=None, udp_port=0, links=[], portTable = [], mtu=0, linkTable={}):
    self.nid = nid
    self.host_name = host_name
    self.udp_port = udp_port

    if links is not None:
      self.links = list(links)

    self.mtu = mtu
    self.upL1 = False
    self.upL2 = False
    self.linkTable = {}
    self.portTable = {}
    

  # get nid
  def GetNID (self):
    return self.nid
    

  # get hostname
  def GetHostName (self):
    return self.host_name
  

  # get port number
  def GetPort (self):
    return self.udp_port

  
  # get list of links
  def GetLinks (self):
    return self.links
  
  
  # get mtu
  def GetMTU (self):
    return self.mtu
  
  
  # get shutdown status
  def GetShutdownStatus (self):
    return self.shutdown
    
  
  # get link table (all links)
  def GetLinkTable (self):
    return self.linkTable


  # get port table (all ports)
  def GetPortTable (self):
    return self.portTable

  # get up flag for neighbor 1
  def GetUpFlagL1 (self):
    return self.upL1


  # get up flag for neighbor 2
  def GetUpFlagL2 (self):
    return self.upL2


  # set up flag for neighbor 1
  def SetUpFlagL1 (self, flag):
    self.upL1 = flag


  # set up flag for neighbor 2
  def SetUpFlagL2 (self, flag):
    self.upL2 = flag
    
  
  # set nid
  def SetNID (self, nid):
    self.nid = nid
    
  
  # set hostname
  def SetHostName (self, host_name):
    self.host_name = host_name
    
    
  # set port number
  def SetPort (self, udp_port):
    self.udp_port = udp_port
    
  
  # updata all links
  def UpdateAllLinks (self, links):
    self.links = list(links)
    
  
  # update link status
  def UpdateLinkStatus (self, individual_link):
    self.links.remove(individual_link)
    self.links.append((individual_link[0], individual_link[1], abs(individual_link[2]-1)))
  
  
  # add link to links list
  def AddLink (self, individual_link):
    self.links.append(individual_link)
    
  
  # remove a link
  def RemoveLink (self, individual_link):
    self.links.remove(individual_link)
    
  
  # set mtu local node
  def SetMTU (self, mtu):
    self.mtu = mtu
  
  
  # set shutdown status
  def SetShutdownStatus (self, shutdown_status):
    self._shutdown = shutdown_status
    
  
  # set link table
  def SetLinkTable (self, source_nid, neighbor_nid):
    self.linkTable[source_nid] = neighbor_nid
    pass


  # set port table
  def SetPortTable (self, nid, hostname, port):
    self.portTable[nid] = nid, hostname, port
    pass
    
  
  # print status
  def PrintStatus(self):

    os.system('clear')
    print "Status of this node"
    print "-------------------"
    print "NID: ", (self.nid)
    print "HostName: ", (self.host_name)
    print "UDP Port: ", (self.udp_port)
    print "Links: ", self.links
    print "MTU: ", (self.mtu)
    print "Link Table: ", (self.linkTable)
    print "Node 1 up: ", (self.upL1)
    print "Node 2 up: ", (self.upL2)
    print "Port Table: ", (self.portTable)
    print "-------------------"
    raw_input("press enter to continue...")



# for testing.....
def main(argv):

  if len(sys.argv) != 3:
    print "Usage: <program_file><nid><itc.txt>"
    exit(1)

  node = InitializeTopology(sys.argv[1], sys.argv[2])
  node.PrintStatus()
  links = node.GetLinks()



if __name__ == "__main__":
  main(sys.argv)

 # April 28, 2016