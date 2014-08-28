import aes
import base64
from Crypto import Random
from set1 import findecb

key = Random.new().read(16)
unknownString = 'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK'

def ecb_oracle(plaintext, target_string):
    plaintext = plaintext + target_string
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

def padding_attack(target_string, block_size, target_byte, plaintext):
    block = target_byte/block_size + 1
    offset = target_byte % block_size + 1
    my_string = 'a'*int(block_size-offset)
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

def decrypt_ecb(target_string, block_size):
    plaintext = ''
    for i in range(0, len(ecb_oracle('', target_string))):
         char = padding_attack(target_string, block_size, i, plaintext)
         if char == None:
             break
         plaintext += char
    return plaintext[:-ord(plaintext[-1])]

unknownString = base64.b64decode(unknownString)
ecbTest = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
block_size = find_block_size(unknownString)
if findecb.isEcb(ecb_oracle(ecbTest, unknownString)):
    print decrypt_ecb(unknownString, block_size) 
