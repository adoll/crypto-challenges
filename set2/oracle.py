from Crypto import Random
import random
import aes
import sys
from set1 import findecb
random.seed()


def append_begin(plaintext, numBytes):
    appendString = ''
    for i in range(0, numBytes):
        appendString += chr(random.randint(0, 255))
    return (appendString + plaintext)

def append_end(plaintext, numBytes):
    appendString = ''
    for i in range(0, numBytes):
        appendString += chr(random.randint(0,255))
    return (plaintext + appendString)

def append_bytes(plaintext):
    r = random.randint(5, 10)
    plaintext = append_begin(plaintext, r)
    r = random.randint(5,10)
    plaintext = append_end(plaintext, r)
    return plaintext

def encryption_oracle(plaintext):
    key = Random.new().read(16)
    iv = Random.new().read(16)
    r = random.randint(0,1)
    plaintext = append_bytes(plaintext)
    if r == 0:
        ciphertext = aes.ecbEncrypt(plaintext, key)
        return ciphertext
    else:
        ciphertext = aes.cbcEncrypt(plaintext, key, iv)
        return ciphertext

#plaintext = sys.stdin.read()
#ciphertext = encryption_oracle(plaintext)
#print ciphertext
#if findecb.isEcb(ciphertext):
#    print 'ECB'
#else:
#    print 'CBC'
