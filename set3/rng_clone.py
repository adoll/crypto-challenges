import struct
import random
import rng
# python doesn't have unsigned right shifts
def rshift(val, n): 
    return (val % 0x100000000) >> n

def right(value, shift):
    i = 0
    original = 0
    while (i * shift) < 32:
        mask = rshift((-1 << (32 - shift)), shift*i)
        part = value & mask
        value ^= rshift(part, shift)
        original |= part
        i += 1
    return original

def left(value, shift, mask):
    i = 0
    original = 0
    while (i * shift) < 32:
        mask1 = rshift(-1, 32 - shift) << (shift * i)
        part = value & mask1
        value ^= (part << shift) & mask
        original |= part
        i += 1
    return original

gen = rng.Rand(random.randint(0, 2**32-1))
state = []
for i in range(0, 624):
    value = right(gen.number(), gen.SHIFT4)
    value = left(value, gen.SHIFT3, gen.AND2)
    value = left(value, gen.SHIFT2, gen.AND1)
    value = right(value, gen.SHIFT1)
    state.append(value)

clone = rng.Rand(state=state)
if clone.number() == gen.number():
    print 'success', clone.number(), gen.number()
