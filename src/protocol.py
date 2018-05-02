from scapy.packet import *
from util import *

# return handshake bytes
def get_handshake(info_hash, peer_id):
    return bytearray.fromhex('13') \ # length of protocol name
            + bytearray('BitTorrent protocol') \ # protocol name
            + bytearray(8) \ # padding
            + info_hash + int_to_ba(peer_id)

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
# BitTorrent handshake
class BTHS(Packet):
    name = "BTHS"
    fields_desc = [ 
        ByteField("bt_name_sz",None,"name"),
        StrFixedLenField("bt_name","BitTorrent protocol",0x13),
'''

