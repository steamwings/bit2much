#! /usr/bin/env python
from scapy.all import *
from util import *

threads = []
handshake = None # This will be set in main
bt_types = {0:"choke",1:"unchoke",2:"interested",3:"not_interested",\
            4:"have",5:"bitfield",6:"request",7:"request",8:"piece",\
            9:"cancel",10:"port",20:"extended"}
 
# This will run in a thread for each peer
def peer_handler(socket, addr, peer_id=None):
    # request random pieces from rarest
    # download and upload
    if peer_id != None: # initiate handshake
        socket.send(handshake)
        socket.recv(62)

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

def parse_bt(data):
    
class BT:
    __init__(self, data):
        if data == "0" 

'''
if __name__ == "__main__":
    #interact(mydict=globals(), mybanner="Test scapy BT")
class BT(Packet):
    name = "BT"
    bt_types = {0:"choke",1:"unchoke",2:"interested",3:"not_interested",\
            4:"have",5:"bitfield",6:"request",7:"request",8:"piece",\
            9:"cancel",10:"port",20:"extended"}
    field_desc = [
        IntField("len",0),
        ConditionalField(ByteEnumField("type",0,bt_types),lambda pkt:pkt.len > 0)
        ]
'''


'''
class BTSTAT(Packet):
    name = "BT_STATUS"
    field_desc = [
        
    ]
'''

'''
class BT(Packet):
    name = "BTLEN"
    field_desc = [
        IntField("len",0,
    ]

# Standard BitTorrent post-handshake message
class BTTYPE(Packet):
    name = "BT"
    bt_types = {0:"choke",1:"unchoke",2:"interested",3:"not_interested",4:"have",5:"bitfield",6:"request",7:"piece",8:"cancel",10:"port",20:"extended"}
    field_desc = [
        ByteEnumField("type",None,bt_types),
    ]

'''
''' 
# BitTorrent handshake
class BTHS(Packet):
    name = "BTHS"
    fields_desc = [ 
        ByteField("bt_name_sz",None,"name"),
        StrFixedLenField("bt_name","BitTorrent protocol",0x13),
'''

