from Crypto.Cipher import AES
from Crypto import Random
import sys
import string
import base64
text = sys.stdin.read()
key = b'YELLOW SUBMARINE'
cipher = AES.new(key, AES.MODE_ECB, b'0')
plaintext = cipher.decrypt(base64.standard_b64decode(text))
plaintext = plaintext[:-ord(plaintext[-1])]
print plaintext
