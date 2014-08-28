from set2 import aes
from set2 import pkcs
from set1 import xor
from Crypto import Random
from Crypto.Cipher import AES
import base64
import random

key = Random.new().read(16)
iv = Random.new().read(16)
cipher = AES.new(key, AES.MODE_CBC, iv)
listStrings = ['MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=',
'MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=',
'MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==',
'MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==',
'MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl',
'MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==',
'MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==',
'MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=',
'MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=',
'MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93']

def encrypt(listStrings):
    index = random.randint(0, len(listStrings)-1)
    plaintext = base64.b64decode(listStrings[index])
    return aes.cbcEncrypt(plaintext, key, iv), iv

def padding_oracle(ciphertext, localIv):
    try:
        aes.cbcDecrypt(ciphertext, key, localIv)
        return True
    except Exception:
        return False

def solve_block(block, prev_block, block_size, known):
    if len(known) == block_size:
        return (xor.charXor(known, prev_block)).decode('hex')
    
    data = '\x00'*block_size
    attempt = list(data)
    
    #setting known bytes
    i = block_size - 1
    for c in reversed(list(known)):
        attempt[i] = chr(ord(c) ^ (len(known) + 1)) #^ ord(prev_block[i]))
        i -= 1
    
    target_byte = block_size - len(known) - 1
    i = 0
    while not padding_oracle(block, ''.join(attempt)):
        attempt[target_byte] = chr(ord(data[target_byte]) ^ i)
        i += 1
    #backtrack to check for cases where end byte is not 1
    index = 0
    while index < target_byte:
        attempt[index] = chr(ord(attempt[index]) ^ 1)
        if not padding_oracle(block, "".join(attempt)):
            # undo previous xor
            attempt[index] = chr(ord(attempt[index]) ^ 1)
            break
        index += 1
    n = block_size - index
    ptext = "".join(chr(ord(c) ^ n) 
                    for c in ''.join(attempt[index:target_byte + 1])) + known
    return solve_block(block, prev_block, block_size, ptext)

#E(iv xor plaintext)
#D(ctext) xor iv
#E(plaintext xor pCtext)
#D(ctxt) xor pCtext
block_size = 16
ciphertext = encrypt(listStrings)
old_block = ciphertext[1]
ciphertext = ciphertext[0]
solved = ''
for i in xrange(0, len(ciphertext), block_size):
    solved += solve_block(ciphertext[i:i+block_size], old_block, 
                          block_size, '')
    old_block = ciphertext[i:i+block_size]
print pkcs.validate_padding(solved)
