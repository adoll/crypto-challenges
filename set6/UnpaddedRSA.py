from Crypto.Util import number
from set6 import RSA

def attack(r, ciphertext):
    random = number.getRandomInteger(100)
    while (random % r.n == 1):
        print random
        print r.n
        random = number.getRandomInteger(100)
        
    randomInv = number.inverse(random, r.n)
    randomEnc = pow(random, r.e, r.n)
    serverDecryption = r.decrypt(int(ciphertext) * randomEnc)
    targetMessage = (int(serverDecryption.encode('hex'), 16) * randomInv) % r.n
    return hex(targetMessage).replace('0x', '').replace('L', '').decode('hex')

def main():
    r = RSA.RSA(512, 3)
    encrypted = r.encrypt("ABCdafaddsffsfsdsgdd")
    print encrypted
    decrypted = attack(r, encrypted)
    print decrypted
if __name__ == "__main__":
    main()

    
