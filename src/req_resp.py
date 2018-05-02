#! /usr/bin/env python
import urllib
import hashlib
import random
import binascii
import socket
import struct
from parse_torrent import *
from encode_src import *

def parse_peers(peer_string):
    peers = dict()
    peer_list = list(peer_string)
    peer_bytes = bytearray(peer_list)
    
    start = 0
    mid = 4
    end = 6   
    for i in xrange(0, len(peer_bytes), 6):
        ip_net = peer_bytes[start:mid]
        peer_net = peer_bytes[mid:end]
        ip_int = 0
        for b in ip_net:
            ip_int = ip_int * 256 + int(b)    
        ip = socket.ntohl(ip_int)
        ip_str = socket.inet_ntoa(struct.pack(">I",ip))
        port_int = peer_net[0] * 256 + peer_net[1]
        peers[ip_str] = port_int
        start = start + 6
        mid = mid + 6
        end = end + 6
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
        peer_id = peer_id + str(random.randint(0,9))
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
