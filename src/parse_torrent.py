#! /usr/bin/env python
from decoder import bdecode

class MetaInfo:
    def __init__(self, URL):
        self.URL = URL
        self.name = ""
        self.piece_len = 0
        self.pieces = ""
        self.type = ""
        self.file_dict = list()
        self.file_len = 0
    
    def set_mult(self, files):
        self.type = "mult"
        self.file_dict = files
        
    def set_single(self, length):
        self.type = "single"
        self.file_len = length
    
    def parse(self, info):        
        for key, value in info.items():            
            if key == "name":
                self.name = value
            elif key == "piece length":
                self.piece_len = value
            elif key == "pieces":
                self.pieces = value
            elif key == "files":
                self.set_mult(value)
            elif key == "length":
                self.set_single(value)
                
    def toStr(self):
        print "URL: " + self.URL
        print "Name: " + self.name
        print "Piece length: " + str(self.piece_len)
        print "Pieces: " + self.pieces
        print "Type: " + self.type
        if self.type == "single":
            print "File length: " + str(self.file_len)
        elif self.type == "mult":
            print "Files dictionary: ",
            print self.file_dict

def parse(file_path):
    data = ""
    file = open(file_path, "r") 
    for line in file: 
        data = data + line  
    decoded_data = bdecode(data) 
    
    for key, value in decoded_data.items():
        if key == "announce":
            metainfo = MetaInfo(value)
        elif key == "info":
            metainfo.parse(value)
            
    metainfo.toStr()
   # return metainfo
             
      
if __name__ == '__main__':
    file_path = '/home/vmuser/Desktop/Bit2Much/files/multifile.torrent'
    #return parse(file_path)
    parse(file_path)
