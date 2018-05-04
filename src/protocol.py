#! /usr/bin/env python
from util import *
import binascii

info_hash = None
my_peer_id = None
incomplete = True
threads = []
handshake = None # This must be set by set_handshake
types = {0:"choke",1:"unchoke",2:"interested",3:"not_interested",\
        4:"have",5:"bitfield",6:"request",7:"request",8:"piece",\
        9:"cancel",10:"port",20:"extended"}
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

    while(incomplete):
        msg = next_msg(socket)
        if msg is None: # Could not parse
            end_from_thread(socket)
        # deal with msg

    end_from_thread(socket)

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


# return handshake bytearray
def set_handshake():
    if info_hash is None:
        raise "info_hash is None"
    if my_peer_id is None:
        raise "my_peer_id is None"
    handshake = bytearray.fromhex('13') \
            + bytearray('BitTorrent protocol') \
            + bytearray(8) \
            + bytearray(info_hash) + bytearray(my_peer_id)

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

def next_msg(sock):
    try:
        mlen = sock.recv(4) # length prefix
        msg = BT(sock.recv(mlen))
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
    def __init__(self, data='', bttype=None):
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


        
