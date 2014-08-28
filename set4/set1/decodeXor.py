import string
import xor

def scoreString(someString):
    someString = string.lower(someString)
    chars = {}
    totalChars = 0
    for char in someString:
        if char in string.ascii_letters:
            if char in chars:
                chars[char] += 1
            else:
                chars[char] = 1
            totalChars += 1
    score = 0
    for char in string.ascii_lowercase:
        if char in chars:
            count = chars[char]
            percent = count/float(totalChars)
            score += percent*percent
    non_ascii = 0.0
    for c in someString:
        if c not in string.ascii_letters + ' \n.!\',\"-;':
            non_ascii += 1
    # squared sum of frequences is .066
    score = abs(score - .065) + non_ascii/(2*totalChars)
    return score

# takes hex encoding of encrypted string, returns sorted list of likely results
def decodeString(someString):
    results = []
    for i in range(0, 256):
        testString = ""
        for c in someString.decode('hex'):
            testString += chr(i)
        testString = testString.encode('hex')
        result = xor.hexXor(testString, someString)
        decoded = result.decode('hex')
        non_ascii = 0.0
        if all(c in string.printable for c in decoded):
            for c in decoded:
                if c not in string.ascii_letters + ' \n.!\',\"-;':
#                    print c
                    non_ascii += 1
            if non_ascii < 10:
                score = scoreString(decoded)
                info = score, decoded, chr(i)
                results.append(info)
    results = sorted(results)
    return results
def main():
    #Cooking MC's like a pound of bacon
    result = decodeString('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')
    print result[0]
if __name__ == "__main__":
    main()

