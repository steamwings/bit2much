import sys
import binascii
verbose = False

# bytearray (to hex string then) to integer
# Switches byte order for Little Endian systems unless ntoh=False
def ba_to_int(bytearr, ntoh=True):
    if str(bytearr) == '': return 0;
    if ntoh and (sys.byteorder == 'little'): bytearr.reverse()
    return int(binascii.hexlify(bytearr), 16)

def int_to_ba(n, hton=True):
    ba = bytearray(binascii.unhexlify(str(n)))
    if hton and (sys.byteorder == 'little'):
        ba.reverse()
    return ba

