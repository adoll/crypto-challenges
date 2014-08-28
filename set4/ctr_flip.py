from Crypto import Random
from set3 import ctrmode
import string
import urllib

prepend_string = 'comment1=cooking%20MCs;userdata='
append_string = ';comment2=%20like%20a%20pound%20of%20bacon'

key = Random.new().read(16)

def encrypt(userdata):
    userdata = urllib.quote(userdata)
    plaintext = prepend_string + userdata + append_string
    # just use 0 as the nonce
    ciphertext = ctrmode.encrypt(plaintext, key, 0)
    return ciphertext

def is_admin(ciphertext):
    plaintext = ctrmode.decrypt(ciphertext, key, 0)
    print plaintext
    return ';admin=true' in plaintext

ciphertext = encrypt('9admin9true')
s = list(ciphertext)
# in ctr just flip desired bits directly (don't have to flip bits in prev blocks)
s[32] = chr(ord(ciphertext[32])^2)
s[32 + 6] = chr(ord(ciphertext[32+6])^4)
ciphertext = ''.join(s)

if is_admin(ciphertext):
    print 'success'
else:
    print 'failure'

