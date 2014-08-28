import string
import sys
import re
base64Alphabet = string.ascii_uppercase + string.ascii_lowercase
base64Alphabet = base64Alphabet + string.digits + '+' + '/' + '='
dict1 = dict((c, i) for i, c in enumerate(base64Alphabet))
# parse when there are 6 hex digits
def encodeParse24Bits(dataString):
    encoded = ""
    num = int(dataString[0], 16)
    num <<= 4
    
    num |= int(dataString[1], 16)
    num <<= 4
    
    num |= int(dataString[2], 16)
    num <<= 4

    num |= int(dataString[3], 16)
    num <<= 4
    
    num |= int(dataString[4], 16)
    num <<= 4
    
    num |= int(dataString[5], 16)

    num1 = num >> 18

    num2 = num >> 12
    num2 &= 0x3F

    num3 = num >> 6
    num3 &= 0x3F

    num4 = num & 0x3F

    encoded += base64Alphabet[num1]
    encoded += base64Alphabet[num2]
    encoded += base64Alphabet[num3]
    encoded += base64Alphabet[num4]
    return encoded
# parse last 2 or 4 hex digits
def encodeParseLessBits(dataString):
    encoded = ""
    if len(dataString) == 2:
        num = int(dataString[0], 16)
        num <<= 4
        
        num |= int(dataString[1], 16)

        num1 = num >> 2

        num2 = num << 4
        num2 &= 0x3F

        encoded += base64Alphabet[num1]
        encoded += base64Alphabet[num2]
        encoded += '='
        encoded += '='

    if len(dataString) == 4:
        num = int(dataString[0], 16)
        num <<= 4
        
        num |= int(dataString[1], 16)
        num <<= 4
        
        num |= int(dataString[2], 16)
        num <<= 4

        num |= int(dataString[3], 16)
        
        num1 = num >> 10

        num2 = num >> 4
        num2 &= 0x3F

        num3 = num << 2
        num3 &= 0x3F

        encoded += base64Alphabet[num1]
        encoded += base64Alphabet[num2]
        encoded += base64Alphabet[num3]
        encoded += '='
    return encoded


# convert hex to base64 string, return result
def toBase64(hexString):
    strip_nonHex = re.compile("([^a-fA-F0-9])")
    hexString = strip_nonHex.sub('', hexString)
    base64 = ""
    for i in xrange(0, len(hexString), 6):
        data = hexString[i:i+6]
        if len(data) != 6:
            base64 += encodeParseLessBits(data)
        else:
            base64 += encodeParse24Bits(data)
    base64 += '\n'
    return base64

# parse a set of 4
def parse24Bits(dataString):
    decode = ''
    data1 = dict1[dataString[0]]
    data2 = dict1[dataString[1]]
    data3 = dict1[dataString[2]]
    data4 = dict1[dataString[3]]

    data = data1
    data = data << 6
    data = data | data2
    data = data << 6
    data = data | data3
    data = data << 6
    data = data | data4

    char1 = data >> 16
    char1 = char1 & 0xFF

    char2 = data >> 8
    char2 = char2 & 0xFF

    char3 = data & 0xFF
    decode += hex(char1).replace('0x', '').zfill(2) + hex(char2).replace('0x', '').zfill(2) 
    decode += hex(char3).replace('0x', '').zfill(2)
    return decode
# parse when padding is present
def parseLessBits(dataString):
    decode = ''
    if len(dataString) == 1:
        return "Invalid input"
    if len(dataString) == 2:
        data1 = dict1[dataString[0]]
        data2 = dict1[dataString[1]]

        char = data1
        char = char << 6
        char = char | data2
        char = char >> 4
        return hex(char).replace('0x', '').zfill(2)
    if len(dataString) == 3:
        data1 = dict1[dataString[0]]
        data2 = dict1[dataString[1]]
        data3 = dict1[dataString[2]]

        data = data1
        data = data << 6
        data = data | data2
        data = data << 6
        data = data | data3

        char1 = data >> 10

        char2 = data >> 2
        char2 = char2 & 0xFF

        decode = hex(char1).replace('0x', '').zfill(2) +  hex(char2).replace('0x', '').zfill(2)
        return decode
# convert base64 string to hex, return result
def toHex(baseString):
    hexString = ''
    i = 0
    currentChars = ''
    for char in baseString:
        if char == '=':
            hexString += parseLessBits(currentChars)
            break
        if char in dict1:
            currentChars += char
            i = i + 1
            if i == 4:
                i = 0
                hexString += parse24Bits(currentChars)
                currentChars = ''
    return hexString
