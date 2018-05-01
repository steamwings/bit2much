#! /usr/bin/env python
import urllib
import hashlib
import random
from parse_torrent import *
from encode_src import *

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
            peers = v     
    return (interval, tracker_id, complete, incomplete, peers)          

def create_id():
    peer_id = "-IFZW417-"
    for i in range(11):
        peer_id = peer_id + str(random.randint(0,9))
    return url_encode(peer_id)    
    
def calc_total(metainfo):
    left = 0
    if metainfo.type == "single":
        left = metainfo.file_len
    elif metainfo.type == "mult":
        for entry in metainfo.file_dict:
            for k, v in entry.items():
                if k == "length":
                    left = left + v
    return left

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
