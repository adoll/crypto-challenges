from Crypto import Random
import sys
import string
import aes
import pkcs
import urllib
#                 01234567891234560123456789123456
prepend_string = 'comment1=cooking%20MCs;userdata='
#01234567891
#9admin9true;
append_string = ';comment2=%20like%20a%20pound%20of%20bacon'
key = Random.new().read(16)
iv = Random.new().read(16)
blocksize = 16
def encrypt(userdata):
    userdata = urllib.quote(userdata)
    plaintext = prepend_string + userdata + append_string
    ciphertext = aes.cbcEncrypt(plaintext, key, iv)
    return ciphertext

def is_admin(ciphertext):
    plaintext = aes.cbcDecrypt(ciphertext, key, iv)
    print plaintext
    return ';admin=true' in plaintext

#while(True):
    #input = sys.stdin.readline()
ciphertext = encrypt('9admin9true')
s = list(ciphertext)
# flipping the 1st and 6th bit of the ciphertext
s[blocksize] = chr(ord(ciphertext[blocksize])^2)
s[blocksize+6] = chr(ord(ciphertext[blocksize+6])^4)
ciphertext = "".join(s)
if is_admin(ciphertext):
    print 'success'
else:
    print 'failure'
        
