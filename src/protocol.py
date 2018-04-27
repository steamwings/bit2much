#! /usr/bin/env python
import sys
from parse_torrent import parse

if __name__ == '__main__':
    #this is the filepath to the torrent file
    file_path = '/home/vmuser/Desktop/Bit2Much/files/multifile.torrent'    
    #parse(file_path) moves the data from file_path into a MetaInfo object
    meta = parse(file_path);
    #prints out all the necessary keys
    #meta.toStr()
    print meta.URL
    sys.exit()
    

