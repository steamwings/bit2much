#! /usr/bin/env python
import sys
import urllib2
import argparse
sys.path.insert(0, '/home/vmuser/Desktop/Bit2Much/src')
from parse_torrent import *
from req_resp import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Bit2Much.py')
    parser.add_argument('--verbose', '-v', action='store_true', help='-v for more information')
    parser.add_argument('--file', '-f', required=False, help='Path to .torrent file')
    
    args = parser.parse_args()
    verbose = args.verbose
    file_path = args.file if args.file is not None \
        else '/home/vmuser/Desktop/Bit2Much/files/ubuntu.torrent'

    if verbose: # Not sure this works. We may have to getLogger before importing scapy
        import logging
        logging.getLogger("scapy").setLevel(1)

###############################PARSING###############################

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
    left = str(metainfo.calc_total())
    
    #port that client is listening on
    port = str(6886)
    
    #total amount uploaded
    uploaded = str(0)
    
    #total amount downloaded
    downloaded = str(0)
    
    #indicates that the client accepts a compact response
    compact = str(1)
     
    #assemble a tracker url
    tracker_url = metainfo.URL + "?info_hash=" + info_hash + "&peer_id=" + peer_id + "&port=" + port + "&uploaded=" + uploaded + "&downloaded=" + downloaded + "&left=" + left + "&compact=" + compact
    
    if verbose:
        print tracker_url
    
    #send HTTP request to the tracker
    url_request = urllib2.Request(tracker_url)
    url_response = urllib2.urlopen(url_request)
    url_resp = url_response.read()
    
   
##########################TRACKER RESPONSE########################### 
    
    decoded_resp = decode_data(url_resp)
    if verbose:
        print decoded_resp
    parsed_resp = parse_resp(decoded_resp)
    
    #indicates a failure reason
    if parsed_resp is None:
        sys.exit()
    
    #a tuple of information from Tracker's Response
    (interval, tracker_id, complete, incomplete, peers) = parsed_resp
    for k in sorted(peers.iterkeys()):
        print k + ": " + str(peers[k])
    
    
    
    
    
    
    
    
    
    
    
    
    
        
