from Crypto.Cipher import AES
from set1 import xor
import sys
import string
import base64
import struct

def encrypt(plaintext, key, nonce):
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = ''
    for i in xrange(0, len(plaintext), 16):
        stream_key = struct.pack('<QQ', nonce, i/16)
        stream = cipher.encrypt(stream_key)
        cur_text = plaintext[i:i+16]
        ciphertext += xor.charXor(cur_text, stream).decode('hex')
    return ciphertext
# these are identical, but might as well use separate methods for clarity
# when calling
def decrypt(ciphertext, key, nonce):
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = ''
    for i in xrange(0, len(ciphertext), 16):
        stream_key = struct.pack('<QQ', nonce, i/16)
        stream = cipher.encrypt(stream_key)
        plaintext += xor.charXor(ciphertext[i:i+16], stream).decode('hex')
    return plaintext


#encryption = base64.b64decode('L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==')
#ptext = 'Yo, VIP Let\'s kick it Ice, Ice, baby Ice, Ice, baby '
#ctext = base64.b64encode(encrypt(ptext, 'YELLOW SUBMARINE', 0))
#print ctext
#print 'L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=='
#print decrypt(encryption, 'YELLOW SUBMARINE', 0)
#print decrypt(base64.b64decode(ctext), 'YELLOW SUBMARINE', 0)
