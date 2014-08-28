import sys
import string

class BadPadding(Exception):
    pass

def pad(buf, blockLen):
    padding = blockLen - (len(buf) % blockLen)
    for i in range(0, padding):
        buf += chr(padding)
    return buf

def validate_padding(buf):
    padding = buf[-1]
    if padding == 0:
        raise BadPadding("Invalid Padding")
    if not all(ord(c) == ord(padding) for c in buf[-ord(padding):]):
        raise BadPadding("Invalid Padding")
    else:
        return buf[:-ord(padding)]
