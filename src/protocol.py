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

def next_message(sock):
    try:
        mlen = sock.recv(4) # length prefix
        msg = BT(sock.recv(mlen))
    except:
        msg = None
    return msg

class BT:
    def __init__(self, data=''):
        data = bytearray(data)
        self.len = len(data)
        self.payload = None
        if data == '': 
            self.type = types_by_name["keep_alive"] 
        else:
            self.type = int(data[0])
            if self.len > 1:
                self.payload = data[1:]
        
        if self.type == types_by_name["request"] \
            or self.type == types_by_name["cancel"]:
            self.index = data[1:5]
            self.begin = data[5:9]
            self.piece = data[9:13]
        elif self.type == types_by_name["have"]:
            self.index = data[1:5]
            self.begin = data[5:9]
            self.length = data[9:13]

