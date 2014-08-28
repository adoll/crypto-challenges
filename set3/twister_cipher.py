from set1 import xor
import sys
import string
import struct
import rng
import random
import time
from set2 import oracle

def encrypt(plaintext, key):
    cipher = rng.Rand(key)
    ciphertext = ''
    for i in xrange(0, len(plaintext), 4):
        stream_key = cipher.number()
        stream = struct.pack('>I', stream_key)
        ciphertext += xor.charXor(plaintext[i:i+4], stream).decode('hex')
    return ciphertext
# these are identical, but might as well use separate methods for clarity
# when calling
def decrypt(ciphertext, key):
    cipher = rng.Rand(key)
    plaintext = ''
    for i in xrange(0, len(ciphertext), 4):
        stream_key = cipher.number()
        stream = struct.pack('>I', stream_key)
        plaintext += xor.charXor(ciphertext[i:i+4], stream).decode('hex')
    return plaintext

def crack_key():
    plaintext = 'A'*14
    plaintext = oracle.append_begin(plaintext, random.randint(0, (2**8)-1))
    the_key = random.randint(0, (2**16) - 1)
    ciphertext = encrypt(plaintext, the_key)
    # 2**16 -1 is small, so just bruteforce the key
    for i in xrange(0, (2**16) -1):
        plaintext = decrypt(ciphertext, i)
        if ('A'*14) in plaintext:
            print 'Success! We found the key and it\'s ' + str(i)
            print 'The correct key is ' + str(the_key)
            break
def generate_token(length):
    cipher = rng.Rand(int(time.mktime(time.gmtime())))
    token = ''
    for i in xrange(0, length, 4):
        token += struct.pack('>I', cipher.number())
    return token

def validate_token(token, length):
    if generate_token(length) == token:
        return True
    else:
        return False
