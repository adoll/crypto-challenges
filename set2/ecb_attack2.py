
from Crypto import Random
import oracle
import random
import base64
import aes
import string
from set1 import findecb

random.seed()
num_bytes = random.randint(5, 256)
key = Random.new().read(16)
unknownString = 'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK'
append_string = oracle.append_begin('', num_bytes)
def my_range(start,end,step):
    i = start
    while i < end:
        yield i
        i+=step

def ecb_oracle(plaintext, target_string):
    plaintext = append_string + plaintext + target_string
    return aes.ecbEncrypt(plaintext, key)

def find_block_size(target_string):
    last_ctext = ecb_oracle('', target_string)
    for i in range(1, 255):
        my_string = 'a'*int(i)
        new_ctext = ecb_oracle(my_string, target_string)
        diff = len(new_ctext) - len(last_ctext)
        if  diff != 0:
            return diff
        last_ctext = new_ctext

# attack extended to start from arbitary point
def padding_attack(target_string, block_size, target_byte, plaintext, 
                   last_repeat, padding):
    block = (last_repeat+target_byte)/block_size + 1
    offset = target_byte % block_size + 1
    my_string = 'a'*int(padding-offset)
    target = ecb_oracle(my_string, target_string)[:block_size*block]
    possibles = {}
    for i in range(0, 256):
        temp = my_string + plaintext + chr(i)
        ctext = ecb_oracle(temp, target_string)[:block*block_size]
        possibles[ctext] = chr(i)
    if target in possibles:
        return possibles[target]
    else:
        return None

def decrypt_ecb(target_string, block_size, last_repeat, padding):
    plaintext = ''
    for i in range(0, len(ecb_oracle('', target_string))):
         char = padding_attack(target_string, block_size, i, plaintext, 
                               last_repeat, padding)
         if char == None:
             break
         plaintext += char
    return plaintext[:-ord(plaintext[-1])]

unknownString = base64.b64decode(unknownString)
ecbTest = 'a'*int(64)
block_size = find_block_size(unknownString)
ciphertext = ecb_oracle(ecbTest, unknownString)
if findecb.isEcb(ciphertext):
    last_repeat = -1
    repeat = ''
    # find last repeating block
    for i in my_range(0, len(ciphertext), block_size):
        if ciphertext[i:i+block_size] in ciphertext[i+block_size:]:
            last_repeat = string.rfind(ciphertext, ciphertext[i:i+block_size])
            repeat = ciphertext[i:i+block_size]
            break
    i = 64
    # remove extraneous bytes till we know where target starts
    while last_repeat == string.rfind(ciphertext, repeat):
        i -= 1
        ecbTest = 'a'*int(i)
        ciphertext = ecb_oracle(ecbTest, unknownString)
    print decrypt_ecb(unknownString, block_size, last_repeat, i+1)
