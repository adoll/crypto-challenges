from Crypto.Cipher import AES
from set1 import xor
import sys
import string
import base64
import pkcs

def my_range(start, end, step):
    while start <= end:
        yield start
        start += step

#doesn't remove padding at end of plaintext
def ecbDecryptSub(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext

def ecbDecrypt(ciphertext, key): 
    plaintext = ecbDecryptSub(ciphertext, key)
    plaintext = pcks.validate_padding(plaintext)
    return plaintext

def ecbEncryptSub(plaintext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(plaintext)
    return ciphertext

def ecbEncrypt(plaintext, key):
    plaintext = pkcs.pad(plaintext, 16)
    return ecbEncryptSub(plaintext, key)

def cbcEncrypt(plaintext, key, iv):
    plaintext = pkcs.pad(plaintext, 16)
    ciphertext = ''
    oldBlock = iv
    for i in my_range(0, len(plaintext), 16):
        newBlock = xor.charXor(oldBlock, plaintext[i:i+16])
        newBlock = ecbEncryptSub(newBlock.decode('hex'), key)
        ciphertext += newBlock
        oldBlock = newBlock
    return ciphertext

def cbcDecrypt(ciphertext, key, iv):
    oldBlock = iv
    plaintext = ''
    for i in my_range(0, len(ciphertext), 16):
        newBlock = ecbDecryptSub(ciphertext[i:i+16], key)
        newBlock = xor.charXor(oldBlock, newBlock)
        oldBlock = ciphertext[i:i+16]
        plaintext += newBlock.decode('hex')
    plaintext = pkcs.validate_padding(plaintext)
    return plaintext
        

#text = sys.stdin.read()
#key = "YELLOW SUBMARINE"
#iv = '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#ciphertext = cbcEncrypt(text, key, iv)
#print ciphertext
#plaintext = cbcDecrypt(ciphertext, key, iv)
#print plaintext
