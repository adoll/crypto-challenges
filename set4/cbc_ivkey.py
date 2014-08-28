from Crypto import Random
import sys
import string
from set2 import aes
from set1 import xor
import urllib

prepend_string = 'comment1=cooking%20MCs;userdata='
append_string = ';comment2=%20like%20a%20pound%20of%20bacon'
key = Random.new().read(16)

def encrypt(userdata):
    userdata = urllib.quote(userdata)
    plaintext = prepend_string + userdata + append_string
    ciphertext = aes.cbcEncrypt(plaintext, key, key)
    return ciphertext

def verify(ciphertext):
    plaintext = aes.cbcDecrypt(ciphertext, key, key)
    try:
        plaintext.decode('ascii')
    except UnicodeDecodeError:
        print "Not Ascii"
        return plaintext
    return None
blocksize = 16
ciphertext = encrypt('hey! my name is aaron')
plaintext = verify(ciphertext[0:blocksize] + '\x00'*blocksize 
                   + ciphertext[0:blocksize] + ciphertext)
if verify != None:
    key_guess = xor.charXor(plaintext[0:blocksize], plaintext[2*blocksize:3*blocksize])
    print key.encode('hex')
    print key_guess
    print key == key_guess.decode('hex')
    
