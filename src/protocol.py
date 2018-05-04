#! /usr/bin/env python
from scapy.all import *
from util import *

incomplete = True
threads = []
handshake = None # This will be set in main
types = {0:"choke",1:"unchoke",2:"interested",3:"not_interested",\
        4:"have",5:"bitfield",6:"request",7:"request",8:"piece",\
        9:"cancel",10:"port",20:"extended"}
types_by_name = {v: k for k,v in types.iteritems()}

# This will run in a thread for each peer
def peer_handler(socket, addr, peer_id=None):
    # request random pieces from rarest
    # download and upload
    if peer_id != None: # initiate handshake
        socket.send(handshake)
        socket.recv(62) # length of handshake 

    buf_sz = 1024
    while(incomplete):
        data = socket.recv(buf_sz)
        msg = bt_parse(data) 

    threads.remove(thread.get_ident()) # remove tid from threads
    thread.exit()

# This will run in only one thread
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
def get_handshake(info_hash, peer_id):
    return bytearray.fromhex('13') \
            + bytearray('BitTorrent protocol') \
            + bytearray(8) \
            + bytearray(info_hash) + bytearray(peer_id)

class BT:
    __init__(self, data='0'):
        data = bytearray(data)
        self.payload = None
        if data == "0": 
            self.len = 0
            self.type = types_by_name["keep_alive"] 
        else:
            self.len = int(data[0:4]) # len is 4 bytes?
            self.type = int(data[4])
            if self.len > 5:
                self.payload = data[5:]
    
