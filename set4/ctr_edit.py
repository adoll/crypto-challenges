from set3 import ctrmode
from set1 import xor
from Crypto import Random
import sys

# wasn't sure if I should have the edit function 'insert' new text
# or overwrite the old text past the offset, I ended up going with the
# latter, as far as I can tell this only changes the execution of the atack
# slightly
def edit(ciphertext, key, offset, new_text):
    # just gonna go with a nonce of 0 to make things simpler, if I understand
    # this attack correctly, changing nonces on every edit would be enough to
    # make it not work
    plaintext = ctrmode.decrypt(ciphertext, key, 0)
    ciphertext = ctrmode.encrypt(plaintext[0:offset] + new_text, key, 0)
    return ciphertext

input = sys.stdin.read()
key = Random.new().read(16)
target = ctrmode.encrypt(input, key, 0)
ctr_stream = ''
for i, c in reversed(list(enumerate(target))):
    ctext = edit(target, key, i, 'A')
    ctr_stream = chr(ord(ctext[i]) ^ ord('A')) + ctr_stream
print xor.charXor(target, ctr_stream).decode('hex')

