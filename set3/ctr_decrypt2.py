from Crypto import Random
import sys
import base64
import ctrmode
import string
from set1 import xor
from set1 import decoderepeatingxor
from set1 import repeatingKeyXor
key = Random.new().read(16)
shortest = 100000
ciphertexts = []
for line in sys.stdin:
    #print line.decode('base64')
    ciphertext = ctrmode.encrypt(base64.b64decode(line), key, 0).encode('hex')
    if len(ciphertext) < shortest:
        shortest = len(ciphertext)
    ciphertexts.append(ciphertext)
concat = ''
for ciphertext in ciphertexts:
    ciphertext = ciphertext[:shortest]
    concat += ciphertext
# this gets a plaintext that is a littled mangled, but close
# ie, the first part was 'I'm rated "P"... this ks a uarlhne,'
guess = decoderepeatingxor.solveForKeysize(shortest, concat)
print guess[0]
