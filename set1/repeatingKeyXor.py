import string
import sys
import xor

def my_range(start, end, step):
    while start <= end:
        yield start
        start += step

def encode(plaintext, key):
    keyLen = len(key)
    textLen = len(plaintext)
    ciphertext = ""
    for i in my_range(0, textLen, keyLen):
        overshoot = i+keyLen - textLen 
        if (overshoot > 0):
            endKey = keyLen - overshoot
        else:
            endKey = keyLen
        ciphertext += xor.charXor(plaintext[i:i+keyLen], key[0:endKey])
    return ciphertext
#cipher = encode("Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal", "ICE")
#compare = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"
#if (cipher == compare):
 #   print "success"
  #  print cipher
