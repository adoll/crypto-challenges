class Rand:
    N = 624
    M = 397
    MASK32 = 2**32 - 1
    MASK31 = 2**31
    MULT1 = 1812433253
    SHIFT1 = 11
    SHIFT2 = 7
    SHIFT3 = 15
    SHIFT4 = 18
    AND1 = 2636928640
    AND2 = 4022730752
    ODDXOR = 2567483615
    def __init__(s, seed=None, state=[]):
        s.index = 0
        s.MT = list(state)
        if seed != None:
            s.MT.append(seed)
            for i in xrange(1, s.N):
                # last thirty two bits
                num = s.MASK32 & (s.MULT1 * (s.MT[i-1] ^ (s.MT[i-1] >> 30)) + i)
                s.MT.append(num)
    def number(s):
        if s.index == 0:
            s.generate_numbers()
        y = s.MT[s.index]
        y ^= (y >> s.SHIFT1)
        y ^= ((y << s.SHIFT2) & s.AND1)
        y ^= ((y << s.SHIFT3) & s.AND2)
        y ^= (y >> s.SHIFT4)
        s.index = (s.index + 1) % s.N
        return y

    def generate_numbers(s):
        for i in range(s.N):
            y = (s.MT[i] & s.MASK31) + (s.MT[(i+1) % s.N] & (s.MASK31 - 1))
            s.MT[i] = s.MT[(i + s.M) % s.N] ^ (y >> 1)
            if (y % 2) != 0:
                s.MT[i] = s.MT[i] ^ s.ODDXOR
