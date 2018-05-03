from scapy.packet import *
from util import *

threads = []

# This will run in a thread for each peer
def peer_handler(socket, addr, peer_id=None):
    # download and upload
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



'''
class BT(Packet):
    name = "BTLEN"
    field_desc = [
        IntField("len",0,
    ]

# Standard BitTorrent post-handshake message
class BTTYPE(Packet):
    name = "BT"
    bt_types = {0:"choke",1:"unchoke",2:"interested",3:"not_interested",4:"have",5:"bitfield",6:"request",7:"request",8:"piece",9:"cancel",10:"port",20:"extended"}
    field_desc = [
        ByteEnumField("type",None,bt_types),
    ]

class BTSTAT(Packet):
    name = "BT_STATUS"
    field_desc = [
        
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

