#! /usr/bin/env python
import urllib
import hashlib
import random
import binascii
import socket
import sys
from parse_torrent import *
from encode_src import *

# bytearray (to hex string then) to integer
# Switches byte order for Little Endian systems unless ntoh=False
def ba_to_int(bytearr, ntoh=True):
    if ntoh and (sys.byteorder == 'little'): bytearr.reverse()
    return int(binascii.hexlify(bytearr), 16)

def int_to_ba(n, hton=True):
    ba = bytearray(binascii.unhexlify(str(n)))
    if hton and (sys.byteorder == 'little'):
        ba.reverse()
    return ba

def parse_peers(peer_string, compact=1):
    peers = [] 
    peer_list = list(peer_string)      
    peer_bytes = bytearray(peer_list)
      
    if compact==0: # support for peer_id
        ip_st = 20
        port_st = 24
    else:
        ip_st = 0
        port_st = 4
    peer_st = 0 
    end = port_st + 2
    inc = end

    peers_count = len(peer_bytes)/6
   
    for i in range(0, peers_count):
        peer_net = peer_bytes[peer_st:ip_st]
        ip_net = peer_bytes[ip_st:port_st]
        port_net = peer_bytes[port_st:end]
       
        peer_id = ba_to_int(peer_net)

        ip_host = ba_to_int(ip_net) # instead of ip_net.reverse()
        bytes_str = str(ip_host) #instead of "".join(map(chr, ip_host))
        ip_str = socket.inet_ntoa(bytes_str)
        
        port_int = ba_to_int(port_net)  
        peers.append((ip_str, port_int, peer_id))
         
        peer_st += inc
        ip_st += inc
        port_st += inc
        end += inc
       
    return peers
    
def parse_resp(response):
    interval = 0
    tracker_id = ""
    complete = 0
    incomplete = 0
    peers = list()
    for k,v in response.items():
        if k == "failure reason":
            print v
            return None
        elif k == "interval":
            interval = v
        elif k == "tracker_id":
            tracker_id = v
        elif k == "complete":
            complete = v
        elif k == "incomplete":
            incomplete = v
        elif k == "peers":
            peers = parse_peers(v)   
    return (interval, tracker_id, complete, incomplete, peers)          

def create_id():
    peer_id = "-IFZW417-"
    for i in range(11):
        peer_id += str(random.randint(0,9))
    return url_encode(peer_id)    

def url_encode(to_encode):
    encoded = urllib.quote(to_encode, '/~')
    return encoded

def get_info_hash(decoded_data):
    for key, value in decoded_data.items():
        if key == "info":                  
            encoded_info = encode(value)
            sha = hashlib.sha1()
            sha.update(encoded_info)
            info_hash = sha.digest()
            return url_encode(info_hash)
