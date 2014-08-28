import sys
import string

def my_range(start,end,step):
    i = start
    while i < end:
        yield i
        i+=step

def isEcb(ciphertext):
    count = 0
    for i in range(0, len(ciphertext)):
        if ciphertext[i:i+16] in ciphertext[i+16:]:
            count += 1
    return count > 0
