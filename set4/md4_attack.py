import md4
import struct
import random
import heapq


def pad(message):
    n = len(message)
    bit_len = n * 8
    index = (bit_len >> 3) & 0x3fL
    pad_len = 120 - index
    if index < 56:
        pad_len = 56 - index
    padding = '\x80' + '\x00'*63
    return padding[:pad_len] + struct.pack('<Q', bit_len)

# get random key
lines = (line for line in open("/usr/share/dict/words"))
word_pairs = ((random.random(), word) for word in lines)
key = heapq.nlargest(1, word_pairs)[0][1]

msg = "comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
# create target message and mac to compare with ours
comp_msg = key + msg + pad(key+msg) + ';admin=true'
padding = pad(comp_msg)
comp_msg += padding
m = md4.MD4()
m.update(comp_msg)
comp_mac = m.digest()
print comp_mac

#this is the mac we are given
m1 = md4.MD4()
m1.update(key+msg + pad(key+msg))
mac = m1.digest()

a = struct.unpack('<I', mac[0:8].decode('hex'))[0]
b = struct.unpack('<I', mac[8:16].decode('hex'))[0]
c = struct.unpack('<I', mac[16:24].decode('hex'))[0]
d = struct.unpack('<I', mac[24:32].decode('hex'))[0]
for i in xrange(0, 512):
    our_msg = ';admin=true' + pad(i*'A')
    try:
        m2 = md4.MD4(a, b, c, d)
        m2.update(our_msg)
        our_mac = m2.digest()
        if our_mac == comp_mac:
            print 'success'
            print our_mac
    except:
        continue
