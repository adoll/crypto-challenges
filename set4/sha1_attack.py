import sha1
import struct
import random
import heapq


def pad(message):
    # Pre-processing:
    original_byte_len = len(message)
    original_bit_len = original_byte_len * 8
    
    # append the bit '1' to the message
    padding = b'\x80'
    
    # append 0 <= k < 512 bits '0', so that the resulting message length (in bits)
    #    is congruent to 448 (mod 512)
    padding += b'\x00' * ((56 - (original_byte_len + 1) % 64) % 64)
    # append length of message (before pre-processing), in bits, as 64-bit big-endian integer
    padding += struct.pack(b'>Q', original_bit_len)
    return padding

# get random key
lines = (line for line in open("/usr/share/dict/words"))
word_pairs = ((random.random(), word) for word in lines)
key = heapq.nlargest(1, word_pairs)[0][1]

msg = "comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
# create target message and mac to compare with ours
comp_msg = key + msg + pad(key+msg) + ';admin=true'
padding = pad(comp_msg)
comp_msg += padding
comp_mac = sha1.sha1(comp_msg)

#this is the mac we are given
mac = sha1.sha1((key + msg) + pad(key+msg))
h0 = int(mac[0:8], 16)
h1 = int(mac[8:16], 16)
h2 = int(mac[16:24], 16)
h3 = int(mac[24:32], 16)
h4 = int(mac[32:40], 16)
for i in xrange(0, 512):
    our_msg = ';admin=true' + pad(i*'A')
    try:
        our_mac = sha1.sha1(our_msg, h0, h1, h2, h3, h4)
        if our_mac == comp_mac:
            print 'success'
            print our_mac
    except:
        continue

