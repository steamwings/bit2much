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

    if verbose:
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
    left = str(calc_total(metainfo))
    
    port = str(6886)
    
    uploaded = str(0)
    
    downloaded = str(0)
    
    compact = str(1)
     
    #assemble a tracker url
    tracker_url = metainfo.URL + "?info_hash=" + info_hash + "&peer_id=" + peer_id + "&port=" + port + "&uploaded=" + uploaded + "&downloaded=" + downloaded + "&left=" + left + "&compact=" + compact
    #tracker_url = "http://bt1.archive.org:6969/announce?info_hash=U%15%b8%5eY%3ay%a1%06%10W%f5%88o%03%d1%09~%9c%f3&peer_id=-TR2840-ocsg19zy1vxs&port=51413&uploaded=0&downloaded=0&left=56037050&numwant=80&key=16a5b84c&compact=1&s"
    
    print tracker_url
    
    #send HTTP request to the tracker
    url_request = urllib2.Request(tracker_url)
    url_response = urllib2.urlopen(url_request)
    url_resp = url_response.read()
    
    #[Full request URI [truncated]: http://bt2.archive.org:6969/announce?info_hash=v%5bS%22%bc%db%bb%ab%2a%ca%ba%29%a1-%1d%60%e1J%968&peer_id=-TR2840-ple1svqkc36t&port=51413&uploaded=0&downloaded=0&left=21571428&numwant=80&key=103e6e0f&compact=1] for Duemma
    #[http://bt1.archive.org:6969/announce?info_hash=U%15%b8%5eY%3ay%a1%06%10W%f5%88o%03%d1%09~%9c%f3&peer_id=-TR2840-ocsg19zy1vxs&port=51413&uploaded=0&downloaded=0&left=56037050&numwant=80&key=16a5b84c&compact=1&s] for weight



    

   
##########################TRACKER RESPONSE########################### 
    
    decoded_resp = decode_data(url_resp)
    print decoded_resp
    #(interval, tracker_id, complete, incomplete, peers) = parse_resp(decoded_resp)
    #if len(tracker_id) == 0:
        #sys.exit()
    #peers is a list of dicts with keys: peer id, ip, port
        
