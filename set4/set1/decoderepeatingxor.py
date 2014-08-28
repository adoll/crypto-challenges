import xor
import sys
import convert
import decodeXor
import repeatingKeyXor

def my_range(start, end, step):
    while start <= end:
        yield start
        start += step

def hammingDistance(hexBuf1, hexBuf2):
    xorString = xor.hexXor(hexBuf1, hexBuf2)
    binaryStr = bin(int(xorString, 16))[2:]
    count = 0
    for char in binaryStr:
        if char == '1':
            count += 1
    return count

def solveForKeysize(keysize, hexString):
    blocks = []
    #create blocks of keysize bytes
    for i in my_range(0, len(hexString), 2*keysize):
        blocks.append(hexString[i:i + 2*keysize])   
    #print len(blocks)
    key = ""
    for i in my_range(0, 2*keysize, 2):
        singleXor = ""
        cutoff = len(blocks)-1
        for block in blocks[0:cutoff]:
            singleXor += block[i:i+2]
        if len(singleXor) == 0:
            break
        decoded = decodeXor.decodeString(singleXor)
        # if there weren't any with printable chars
        if len(decoded) == 0:
            print 'empty'
            return ''
        # guess most likely 
        key += decoded[0][2]
        temp = (hexString).decode('hex')
    #print key so we can fill in the gaps
    print 'Key'
    print repr(key)
    print '-----------------------------------------'
    return (repeatingKeyXor.encode(temp, key)).decode('hex'), key

def main():
    data = sys.stdin.read()
    data = data.replace('\n', '')
    hexData = convert.toHex(data)
#print (repeatingKeyXor.encode(hexData.decode('hex'), 'Terminator X: Bring the noise')).decode('hex')
    values = {}
    for keysize in range(2, 41):
        string1 = hexData[0:2*keysize]
        string2 = hexData[2*keysize:4*keysize]
        string3 = hexData[4*keysize:6*keysize]
        string4 = hexData[6*keysize:8*keysize]
        hamming = hammingDistance(string1, string2)
        hamming2 = hammingDistance(string3, string4)
        normalized = hamming/float(keysize)
        normalized2 = hamming2/float(keysize)
        avg = (normalized + normalized2)/2
        values[keysize] = avg

    i = 0
#print solveForKeysize(29, hexData)
    for potentialKeysize in sorted(values, key=values.get, reverse=False):
        print potentialKeysize, values[potentialKeysize]
        print solveForKeysize(potentialKeysize, hexData)[0]
        print '----------------------------------------------------'
        i += 1
        if i >= 10:
            break

if __name__ == "__main__":
    main()
