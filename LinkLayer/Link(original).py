#!/usr/bin/python

import socket
import sys
import thread
import threading
import select
import time
import SocketServer

sys.path.append('../PhysicalLayer')
sys.path.append('../NetworkLayer')

import Physical
import Network


def InitializeSocket (node=None):

  hostname = node.GetHostName()

  # Resolve the IP address.
  ip = socket.gethostbyname(hostname)
  port = node.GetPort()
  
  client_address = (ip, port)

  # Create client's socket. We are using UDP.
  client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

  # Set any socket options pertaining to multicast.
  client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  client_socket.setblocking(0)
  client_socket.bind(client_address)
  
  return client_address, client_socket
  
  
def l2_sendto (client_socket=None, hostname=None, datagram=None, node=None):
  """
  This function expects a Datagram passed from Layer 3. It will pack Frame-related 
  stuff onto this, thus making all the Datagram stuff our Frame's payload.
  
  There are several states within this function.
  
  State (1). Is host name blank?
    Yes: Print error
    No: Move to State (2).
  
  State (2). Is hostname "physically" connect to us?
    Yes: Move to State (3).
    No: Print error
  
  State (3). Is payload larger than MTU - 2?
    Yes: Print error
    No: Send via UDP.
  """
  if hostname is not None:

    # 'entry' in this case is a tuple. ie., (NID, hostname, flag).
    for entry in node.GetLinks():

      if hostname in entry:

        # -2 for \r\n, which is appended in send() and recv() functions.
        if datagram.GetLength() >= datagram.GetMTU() - 2:
          print('Cannot send over wire. Payload > MTU of the link.')

        elif datagram.GetLength() <= node.GetMTU() - 2:

          # Resolve host name by doing host name -> ip address. Then include the port.
          # Unless the destination port was previous explicitly changed, it will use the 
          # default of port # 5555.
          dest_address = (socket.gethostbyname(hostname), datagram.GetDestPort())
          source_address = (socket.gethostbyname(node.GetHostName()), node.GetPort())
          
          # Set Frame headers
          frame = Frame(source_address[0], source_address[1], dest_address[0], dest_address[1])

          # Take the Datagram, make it the payload of the Frame.
          # Create the Frame and set its headers then send it over UDP.
          d_sequence_number = str(datagram.GetSequenceNumber())
          d_total_sequence_numbers = str(datagram.GetTotalSequenceNumbers())
          d_mtu = str(datagram.GetMTU())
          d_ttl = str(datagram.GetTTL())
          d_source_nid = str(datagram.GetSourceNID())
          d_source_port = str(datagram.GetSourcePort())
          d_dest_nid = str(datagram.GetDestNID())
          d_dest_port = str(datagram.GetDestPort())
          d_length = str(datagram.GetLength())
          datagram_payload = datagram.GetPayload()    # This will be Segment headers and stuff. But for now, it is a string.
          
          # The '@@' symbols are delimeters to distinguish between different packet payloads.
          # Each @@ will separate the Segment, Datagram, and Frame headers and payload stuff.
          # We will use string.split('@@') to determine which portion of the payload we 
          # will work with.
          #
          # We need to add a '\r\n' at the end so we can know when to stop reading.
          
          f_source_ip = str(frame.GetSourceIP())
          f_source_port = str(frame.GetSourcePort())
          f_dest_ip = str(frame.GetDestIP())
          f_dest_port = str(frame.GetDestPort())
          
          # We will have to do Segment_payload stuff here as well when the time comes.
          frame_payload = d_sequence_number + '@' + d_total_sequence_numbers + '@' + \
                          d_mtu + '@' + d_ttl + '@' + d_source_nid + '@' + d_source_port + '@' + \
                          d_dest_nid + '@' + d_dest_port + '@' + d_length + '@@' + datagram_payload
          
          to_wire = f_source_ip + '@' + f_source_port + '@' + f_dest_ip + '@' + \
                    f_dest_port + '@' + str(len(frame_payload)) + '@@' + frame_payload
                          
          
          
          # Now that we have created the frame payload, we call SetPayload to finish creating 
          # our Frame so we can prepare to send it over the wire.
          frame.SetPayload(frame_payload)

          # Now send it over the wire. Don't forget to encode to a byte string.
          client_socket.sendto(to_wire.encode(), dest_address)

        # Break out of the 'for' loop.
        return frame
      #else:
        #print('You are not "physically" connected to that node.')
        # Break out of the 'for' loop.
        #break
  else:
    print('No host name specified for l2_sendto.')
  

def l2_recvfrom (client_socket=None, node=None):
  """
  This function will be used in Layer 3, the Network layer. Nowhere in this Layer 2
  is this function used--rather, this layer purely uses good ol' UDP recvfrom.
  """
  while 1:
    data = ''.encode()
    buffer = ''.encode()
    
    # Read a bunch of bytes up to the MTU or length of data.
    while len(data) <= 4096:
      buffer, external_address = client_socket.recvfrom(4096-len(data))

      if buffer:
        data += buffer

      else:
        #thread.interrupt_main()
        break
        
      # This is our protocol. Stop reading when we see \r\n.
      if '\r\n'.encode() in buffer:
        #thread.interrupt_main()
        break
    
    # Split the headers.
    packet = data.decode().split('@@')
    frame_header = packet[0].split('@')
    datagram_header = packet[1].split('@')    
    
    # Now we should have something like [Frame, Datagram, Segment].
    # Step 1. Build a new Frame.
    frame = Frame(frame_header[2], int(frame_header[3]), frame_header[0], int(frame_header[1]), 
                            int(frame_header[4]), packet[1])
                            
    # Step 2. Build a new Datagram so we can pass it to l3_recvfrom().
    # The order goes 6, 7, then 4, 5 because 6/7 is the destination of this packet, which is 
    # destined for where the source is. It's backwards since we are receiving, not sending.
    datagram = Network.Datagram(int(datagram_header[0]), int(datagram_header[1]), int(datagram_header[2]), 
                            int(datagram_header[3]), int(datagram_header[6]), int(datagram_header[7]), 
                            int(datagram_header[4]), int(datagram_header[5]), int(datagram_header[8]), 
                            packet[2])
    
    # l3_recvfrom will return something, but right now, we are not storing that value yet.
    #NetworkLayer.l3_recvfrom(datagram)
    
    return len(buffer), frame, datagram, external_address, \
           Network.l3_recvfrom(client_socket, str(packet[1]+'@@'+packet[2]), node)


class Frame (object):
  """
  This class defines our layer 2 unit, the frame. In this class, we include the 
  header and the payload of our frame. The header consists of the following:
  
    [1] _source_ip = string
      This is the 32-bit IP address of the host.
      
    [2] _source_port = integer
    
    [3] _dest_ip = string
      This is the 32-bit IP address of where we are sending our information.
    
    [4] _dest_port = integer
      
    [5] _length = integer
      This is the length of the payload.
      
    [6] _payload = string
      This is the message we are sending.
      
  NOTE: Layer 3 will reference NIDs instead of IPs.
  """
  def __init__ (self, source_ip='localhost', source_port=5555, 
                dest_ip='localhost', dest_port=9001, length=0, payload=None):
    self._source_ip = source_ip
    self._source_port = source_port
    self._dest_ip = dest_ip
    self._dest_port = dest_port
    if payload is not None:
      self._length = len(payload)
    self._payload = payload
    
  
  def GetSourceIP (self):
    return self._source_ip
    
    
  def GetSourcePort (self):
    return self._source_port
    
    
  def GetDestIP (self):
    return self._dest_ip
    
    
  def GetDestPort (self):
    return self._dest_port
    
    
  def GetLength (self):
    return self._length
    
  
  def GetPayload (self):
    return self._payload
    
    
  def SetSourceIP (self, source_ip):
    self._source_ip = source_ip
    
    
  def SetSourcePort (self, source_port):
    self._source_port = source_port
    
    
  def SetDestIP (self, dest_ip):
    self._dest_ip = dest_ip
    
    
  def SetDestPort (self, dest_port):
    self._dest_port = dest_port
    
  
  def SetPayload (self, payload):
    self._payload = payload
    self._length = len(payload)


  def PrintContents (self):
    print(self._source_ip)
    print(self._source_port)
    print(self._dest_ip)
    print(self._dest_port)
    print(self._length)
    print(self._payload)

 
# for testing.....

def main(argv):

  # check for proper number of arguments
  if len(sys.argv) != 4:
    print "Usage: <program_file> <my_nid> <receiver_nid> <itc.txt>"
    exit(1)

  # initialize node object in physical layer
  node = Physical.InitializeTopology(sys.argv[1], sys.argv[3])

  # initialize socket with node, get client address and socket in this layer
  client_address, client_socket = InitializeSocket(node)

  # initialize datagram object in network layer
  datagram = Network.Datagram()
  datagram.SetMTU(node.GetMTU())

  # read all of itc.txt into a_list
  itc_script = open(sys.argv[3])
  a_list = itc_script.readlines()
  itc_script.close()

  # iterate through a_list by line
  for entry in a_list:

    # separate into individual words
    temp = entry.split(' ')

    # if the first word is what I chose for my NID
    if sys.argv[1] == temp[0]:

      # set my source port
      datagram.SetSourcePort(int(temp[2]))

    # find the line with my dest. node id and set the dest port from that
    if sys.argv[2] in temp[0]:
      datagram.SetDestPort(int(temp[2]))

  
  inputs = [client_socket, sys.stdin]

  go=1
  while(go is 1):
    inputready,outputready,exceptready = select.select(inputs,[],[])

    for s in inputready:

      if s == client_socket:
        length_of_buffer, received_frame, datagram_to_pass, external_address, received_segment = l2_recvfrom(client_socket, node) # added node as a parameter 04-06-2010.
        print(datagram_to_pass.GetPayload())

      #  received_segment.PrintContents()
      elif s == sys.stdin:
        payload = list(sys.stdin.readline())
        payload.remove('\n')
        payload.append('\r')
        payload.append('\n')
        payload = ''.join(payload)

        if 'exit' in payload:
          print('exiting...')
          go=0

        datagram.SetPayload(payload)
        hn = Network.ResolveNID(int(sys.argv[2]), node)
        what_was_sent = l2_sendto(client_socket, hn, datagram, node)

  client_socket.close()



if __name__ == "__main__":
  main(sys.argv)
