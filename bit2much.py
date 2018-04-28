#!/bin/bash/env python
import sys
import urllib2
sys.path.insert(0, '/home/vmuser/Desktop/Bit2Much/src')
from parse_torrent import *
from req_resp import *

if __name__ == '__main__':
    
###############################PARSING###############################

    #filepath to the .torrent file
    file_path = '/home/vmuser/Desktop/Bit2Much/files/multifile.torrent' 
    
    #reads bencoded data from file
    file_data = read_file(file_path)
    
    #decodes bencoded data from file
    decoded_data = decode_data(file_data)
           
    #parses decoded data from .torrent into a MetaInfo object
    metainfo = parse_data(decoded_data)     

###########################TRACKER REQUEST###########################   
    
    #info_hash->urlencoded 20-byte SHA1 hash of the value of the info key from the MetaInfo file
    info_hash = get_info_hash(decoded_data)
    
    #peer_id->urlencoded 20-byte string used as a unique ID for the client
    peer_id = create_id()
    
    #left->number of bytes this client still has to download in base 10 ASCII
    left = str(calc_total(metainfo))
    
    #assemble a tracker url
    tracker_url = metainfo.URL + "?info_hash=" + info_hash + "&peer_id=" + peer_id + "&left=" + left
    
    print tracker_url
    
    #send HTTP request to the tracker
    url_request = urllib2.Request(tracker_url)
    url_response = urllib2.urlopen(url_request)
    print url_response.read()
   
##########################TRACKER RESPONSE########################### 
    
    #decoded_resp = decode_data(url_response)
    #(interval, tracker_id, complete, incomplete, peers) = parse_resp(decoded_resp)
    #if len(tracker_id) == 0:
        #sys.exit()
    #peers is a list of dicts with keys: peer id, ip, port
        
