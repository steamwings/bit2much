#! /usr/bin/env python
from util import *
import binascii

info_hash = None
my_peer_id = None
incomplete = True
threads = []
handshake = None # This must be set by set_handshake
types = {0:"choke",1:"unchoke",2:"interested",3:"not_interested",\
        4:"have",5:"bitfield",6:"request",7:"piece",\
        8:"cancel",9:"port",20:"extended",256:"keep_alive"}
types_by_name = {v: k for k,v in types.iteritems()}

# This will run in a thread for each TCP connection and peer
def peer_handler(socket, addr, peer_id=None):
    # request random pieces from rarest
    # download and upload
    if peer_id != None: # initiate handshake
        socket.send(handshake)
        recvd_handshake = socket.recv(68) # length of handshake 
        if not good_handshake(recvd_handshake, peer_id):
            end_from_thread(socket)

    #states
    am_choking = 1
    am_interested = 0
    peer_choking = 1
    peer_interested = 0
    
    # blocks are downloaded by a client when am_interested=1 and peer_choking=0
    # blocks are uploaded by a client when am_choking=0 and peer_interested=1    
    while(incomplete): # iterate on received messages
        msg = next_msg(socket)
        if msg is None: # Could not parse
            end_from_thread(socket)

        if verbose:
            print("Received %(t)s type" % types[msg.type])

        # default response
        bt = BT(bttype=types_by_name["keep_alive"]) # Observe that the 'bttype=' is not necessary since it's the second argument

        if msg.type == 0: #choke
            peer_choking = 1
        elif msg.type == 1: #unchoke
            peer_choking = 0
        elif msg.type == 2: #interested
            peer_interested = 1
        elif msg.type == 3: #not interested
            peer_interested = 0  
        elif msg.type == 4: #have
            have_msg(msg)  
        elif msg.type == 5: #bitfield
            bitfield_msg(msg)   
        elif msg.type == 6: #request
            request_msg(msg) 
        elif msg.type == 7: #piece
            piece_msg(msg) 
        elif msg.type == 8: #cancel
            cancel_msg(msg)   
        elif msg.type == 9: #port
            port_msg(msg)               
        # there are other message types

        send_msg(socket, bt) 


    end_from_thread(socket)

''' # EXAMPLE CODE
def example_bt(socket):
    b = BT(6) # Request type
    b.index = 55
    b.begin = 55
    b.piece = 55
    send_msg(socket,b) # send_msg calls b.get_data()
'''

# Not sure if it's worth it to have separate functions for each; we'll see how much logic is needed
def have_msg(msg):
    print "Received HAVE type"

def bitfield_msg(msg):
    print "Received BITFIELD type"
    
def request_msg(msg):
    print "Received REQUEST type"
    
def piece_msg(msg):
    print "Received PIECE type"

def cancel_msg(msg):
    print "Received CANCEL type"

def port_msg(msg):
    print "Received PORT type"

#exits the thread    
def end_from_thread(sock):
    sock.close()
    threads.remove(thread.get_ident())
    thread.exit()

# This will run in only one thread to accept incoming TCP connections
def accept_new_peers(port):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(('local_host',port))
    sock.listen(5)

    while True:
        newsock, addr = sock.accept()
        tid = thread.start_new_thread(peer_handler, (newsock,addr))
        threads.append(tid)


''' # I'd like to figure out what the issue was with the globals...    
    if info_hash is None:
        raise "info_hash is None"
    if my_peer_id is None:
        raise "my_peer_id is None"
'''
# return handshake bytearray
def set_handshake(hash_arg, id_arg):
    info_hash = hash_arg
    my_peer_id = id_arg
    handshake = bytearray.fromhex('13') \
            + bytearray('BitTorrent protocol') \
            + bytearray(8) \
            + bytearray(info_hash) + bytearray(my_peer_id)

#determine if the return handshake is valid
def good_handshake(h,peer_id):
    h = bytearray(h)
    if h[0] != 0x13:
        return False
    if h[1:20] != "BitTorrent protocol":
        return False
    if verbose and h[20:28] != bytearray(8): # If reserved bytes are not all zeros
        print("Warning: Reserved bytes (%s) contain non-zero values." % binascii.hexlify(h[15:24]))
    if h[28:48] != info_hash:
        return False
    if peer_id is not None:
        if h[48:68] != peer_id: return False

    return True


#creates a BT object based on the msg received
def next_msg(sock):
    try:
        mlen = sock.recv(4) # length prefix
        msg = BT(data=sock.recv(mlen))
    except:
        msg = None
    return msg

def send_msg(sock, bt):
    try:
        sock.send(bt.get_pkt())
        return True
    except:
        return False

class BT:
    def __init__(self, bttype=None, data=''):
        self.data = None
        if bttype == None: # Parse from data
            self.data = bytearray(data)
            self.len = len(data)
            self.payload = None
            if data == '': 
                self.type = types_by_name["keep_alive"] 
            else:
                self.type = ba2int(data[0], numbytes=1)
                if self.len > 1:
                    self.payload = data[1:]
        
            if self.type == types_by_name["request"] \
                or self.type == types_by_name["cancel"]:
                self.index = ba2int(data[1:5])
                self.begin = ba2int(data[5:9])
                self.piece = ba2int(data[9:13])
            elif self.type == types_by_name["have"]:
                self.index = ba2int(data[1:5])
                self.begin = ba2int(data[5:9])
                self.length = ba2int(data[9:13])
        else: # Create data from fields 
            self.type = bttype
            if self.type == types_by_name["request"] \
                or self.type == types_by_name["cancel"]\
                or self.type == types_by_name["piece"]:
                self.index = None
                self.begin = None
                self.piece = None
            elif self.type == types_by_name["have"]:
                self.index = None
                self.begin = None
                self.length = None
            elif self.type == types_by_name["bitfield"]:
                self.bitfield = None

    def get_pkt(self): # return packet data from fields (like i2m)
        self.data = int2ba(self.type, numbytes=4)

        if self.type == types_by_name["request"] \
            or self.type == types_by_name["cancel"]\
            or self.type == types_by_name["piece"]:
            if self.index is None or self.begin is None or self.piece is None:
                raise BTMemberNotSetException("You must set the index, begin, and piece members to create this type of packet!")
            else:
                self.data += int2ba(self.index,4)\
                    + int2ba(self.begin,4) \
                    + int2ba(self.piece,4)
        elif self.type == types_by_name["have"]:
            if self.index is None or self.begin is None or self.length is None:
                raise BTMemberNotSetException("You must set the index, begin, and length members to create this type of packet!")
            else:
                self.data += int2ba(self.index,4)\
                    + int2ba(self.begin,4)\
                    + int2ba(self.length,4)
        elif self.type == types_by_name["keep_alive"]:
            self.data = bytearray('')
        elif self.type == types_by_name["bitfield"]:
            if self.bitfield is None:
                raise BTMemberNotSetException("You must set the bitfield member to create this type of packet.")
            self.data += int2ba(self.bitfield)
        #else we're done because there's no payload    

        return str(int2ba(len(self.data),numbytes=4) + self.data)

    # It might be helpful to properly write this for debugging purposes
    def __str__(self):
        print("type: %(t)s..." % {'t':self.type})        

class BTMemberNotSetException(Exception):
    """Raise when a needed BT member was not set"""


        
