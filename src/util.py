import sys
import binascii

verbose = False
little_endian = (sys.byteorder == 'little')

# bytearray OR string (to hex string then) to integer
# Switches byte order for Little Endian systems unless ntoh=False
def ba2int(bytearr, ntoh=True):
    if str(bytearr) == '': return 0;
    if ntoh and little_endian: 
        bytearr.reverse()
    return int(binascii.hexlify(bytearr), 16)

# integer (to hex string then) to byte array
def int2ba(n, hton=True):
    f = format(n,'x')
    if len(f) % 2 == 1: # Need even number of digits for octets
        f = '0' + f
    ba = bytearray(binascii.unhexlify(f))
    if hton and little_endian:
        ba.reverse()
    return ba

