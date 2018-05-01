#! /usr/bin/env python
#src code taken from https://github.com/utdemir/bencoder/blob/master/bencoder.py

"""
A simple bencoding implementation in pure Python.
Consult help(encode) and help(decode) for more info.
>>> encode(42) == b'i42e'
True
>>> decode(b'i42e')
42
"""

import re
import string
import itertools as it
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

def encode(obj):
    """
    bencodes given object. Given object should be a int,
    bytes, list or dict. If a str is given, it'll be
    encoded as ASCII.
    >>> [encode(i) for i in (-2, 42, b"answer", b"")] \
            == [b'i-2e', b'i42e', b'6:answer', b'0:']
    True
    >>> encode([b'a', 42, [13, 14]]) == b'l1:ai42eli13ei14eee'
    True
    >>> encode({b'bar': b'spam', b'foo': 42, b'mess': [1, b'c']}) \
            == b'd3:bar4:spam3:fooi42e4:messli1e1:cee'
    True
    """

    if isinstance(obj, int):
        return b"i" + str(obj).encode() + b"e"
    elif isinstance(obj, bytes):
        return str(len(obj)).encode() + b":" + obj
    elif isinstance(obj, str):
        return encode(obj.encode("ascii"))
    elif isinstance(obj, list):
        return b"l" + b"".join(map(encode, obj)) + b"e"
    elif isinstance(obj, dict):
        if all(isinstance(i, bytes) for i in obj.keys()):
            items = list(obj.items())
            items.sort()
            return b"d" + b"".join(map(encode, it.chain(*items))) + b"e"
        else:
            raise ValueError("dict keys should be bytes")
    raise ValueError("Allowed types: int, bytes, list, dict; not %s", type(obj))

if __name__ == "__main__":
   import doctest
   doctest.testmod()
