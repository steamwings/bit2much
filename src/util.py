import sys
import binascii

verbose = False
little_endian = (sys.byteorder == 'little')

# bytearray (to hex string then) to integer
# Switches byte order for Little Endian systems unless ntoh=False
def ba2int(bytearr, ntoh=True):
    if str(bytearr) == '': return 0;
    if ntoh and little_endian: 
        bytearr.reverse()
    return int(binascii.hexlify(bytearr), 16)

# octet hex representation of int
def octets(n):
    f = format(n,'x')
    if len(f) % 2 == 1: # Need even number of digits for octets
        f = '0'+f
    return f

# integer (to hex string then) to bytearray
def int2ba(n, numbytes=None, hton=True):
    f = octets(n) 
    ba = bytearray(binascii.unhexlify(f))

    if numbytes is None:
        pass # ignore padding
    elif len(ba) < numbytes: # pad zeros if needed
        ba = bytearray(numbytes-len(ba)) + ba
    elif len(ba) > numbytes: # overflow!
        ba = ba[0:4]
        print(verbose)
        if verbose: print("Overflow warning: int2ba")

    if hton and little_endian:
        ba.reverse()
    return ba

