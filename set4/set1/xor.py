def hexXor(buf1, buf2):
    result = ""
    for (x,y) in zip(buf1, buf2):
        c = hex(int(x, 16) ^ int(y, 16)).replace('0x', '')
        result += c
    return result

def charXor(buf1, buf2):
    result = ""
    for (x,y) in zip(buf1, buf2):
        c = hex(ord(x) ^ ord(y)).replace('0x','').zfill(2)
        result += c
    return result
