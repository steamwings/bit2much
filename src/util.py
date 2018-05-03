import sys
import binascii

verbose = False
little_endian = (sys.byteorder == 'little')


# bytearray OR string (to hex string then) to integer
# Switches byte order for Little Endian systems unless ntoh=False
def ba_to_int(bytearr, ntoh=True):
    if str(bytearr) == '': return 0;
    if ntoh and little_endian: 
        bytearr.reverse()
    return int(binascii.hexlify(bytearr), 16)

# integer (to hex string then) to byte array
def int_to_ba(n, hton=True):
    ba = bytearray(binascii.unhexlify(format(n,'x')))
    if hton and little_endian:
        ba.reverse()
    return ba

