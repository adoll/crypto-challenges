from Crypto import Random
import sys
import base64
import ctrmode
import string
from set1 import xor
from set1 import repeatingKeyXor
ciphertexts = []
key = 'F+29jCe2TtGOzccY4tM69Q=='
i = 0
for line in sys.stdin:
    ciphertext = ctrmode.encrypt(base64.b64decode(line), base64.b64decode(key), 0)
    ciphertexts.append(ciphertext.encode('hex'))
    print '--------------------------------------------'
    print  str(i) + " " + ciphertext.encode('hex')
    i += 1
# see what we get when we try searching for the
#potentialKey = repeatingKeyXor.encode(ciphertexts[4].decode('hex'), 'the ')

#8
potentialKey = xor.charXor(ciphertexts[8].decode('hex'), 
                           'And though 2345678901234567890123456 day')
#10
#potentialKey = xor.charXor(ciphertexts[10].decode('hex'), 
 #                         'To please 678901234567890123456 day')
#3
potentialKey = xor.charXor(ciphertexts[3].decode('hex'), 
                           'Eighteenth-century 901234567890123456 day')
#2
potentialKey = xor.charXor(ciphertexts[2].decode('hex'), 
                           'From counter or desk 67890123 grey')
#1
potentialKey = xor.charXor(ciphertexts[1].decode('hex'), 
                           'Coming with vivid faces')
# 0
potentialKey = xor.charXor(ciphertexts[0].decode('hex'), 
                           'I have met them at close of day')
#6
potentialKey = xor.charXor(ciphertexts[6].decode('hex'), 
                           'Or have lingered awhile and said')
#4
potentialKey = xor.charXor(ciphertexts[4].decode('hex'), 
                           'I have passed with a nod of the head')
#37
potentialKey = xor.charXor(ciphertexts[37].decode('hex'), 
                           'He, too, has been changed in his turn')

# Easter, 1916 by William Butler Yeats
i = 0
for ciphertext in ciphertexts:
    print str(i) + " " + repr(xor.hexXor(ciphertext, potentialKey).decode('hex'))
    i += 1
