from Crypto.Util import number

class RSA:

    def __init__(s, numBits, e):
        s.e = e
        coprime = False
        while (not coprime):
            p = number.getPrime(numBits)
            q = number.getPrime(numBits)
            et = (p-1) * (q-1)
            s.d = number.inverse(s.e, et)
            coprime = s.d != 1
        s.n = p * q
        
        
    
    def encrypt(s, msg):
        m = int(msg.encode("hex"), 16)
        return str(pow(m, s.e, s.n))

    def decrypt(s, ctext):
        ctext = int(ctext)
        hexString = hex(pow(ctext, s.d, s.n)).replace('0x', '').replace('L', '')
        if (len(hexString) % 2 == 1):
            hexString = "0" + hexString
        m = hexString.decode('hex')
        return m

def main():
    #print modinv(17, 3120)
    rsa = RSA(512, 3)
    encrypted = rsa.encrypt("ABCdafad")
    decrypted = rsa.decrypt(encrypted)
    print encrypted
    print decrypted
if __name__ == "__main__":
    main()
