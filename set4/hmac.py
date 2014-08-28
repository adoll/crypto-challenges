from hashlib import sha1
from set1 import xor
block_size = 64
def hmac_sha1(key, message):    
    if len(key) > block_size:
        key = sha1(key).digest()
    if len(key) < block_size:
        key += '\x00'*(block_size - len(key))
    o_key_pad = xor.charXor('\x5c' * block_size, key).decode('hex')
    i_key_pad = xor.charXor('\x36' * block_size, key).decode('hex')
    temp = sha1(i_key_pad + message).digest()
    return sha1(o_key_pad + temp).hexdigest()

