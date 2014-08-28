import string
import sys
import aes
import random
import pkcs
from Crypto import Random

key = Random.new().read(16)

def parseString(buf):
    cookie = {}
    tokens = buf.split('&')
    for token in tokens:
        key_pair = token.split('=')
        cookie[key_pair[0]] = key_pair[1]
    return cookie

def profile_for(email):
    email = email.replace('=', '')
    email = email.replace('&', '')
    # len is 19 up to the role, using randomly generated uid would
    # make it slightly more difficult, but for every digit increase
    # we could just decrease the email length
    cookieString = 'email=' + email + '&uid=10' + '&role=user'
    return cookieString, parseString(cookieString)

def encrypt_profile(encoding):
    return aes.ecbEncrypt(encoding, key)

def decrypt_profile(ciphertext):
    plaintext = aes.ecbDecrypt(ciphertext, key)
    return parseString(plaintext)
#any 13 (mod 16) char email will work for 2 digit uid, 12 for 3, etc 
profile = profile_for('ajd@gmail.com')
admin_string = pkcs.pad('admin', 16)
#offset by 10 so admin_string starts a block
target = profile_for('0123456789'+admin_string)
encrypted = encrypt_profile(profile[0])
targetencrypted = encrypt_profile(target[0])
encrypted = encrypted[:-16] + targetencrypted[16:32]
print decrypt_profile(encrypted)
