import time
import random
import rng

time.sleep(random.randint(40, 1000))
seed = int(time.mktime(time.gmtime()))
gen = rng.Rand(seed)
time.sleep(random.randint(40, 1000))
number = gen.number()
print number
# just guess an approximate time and brute force
approxtime = int(time.mktime(time.strptime('2013 8 28 12', '%Y %m %d %H')))
for guess in range(approxtime, approxtime + 365*24*60*60):
    num = rng.Rand(guess).number()
    if number == num:
        print 'Success, seed= ' + str(guess)
        print 'Actual seed= ' + str(seed)
        break
    guess += 1
