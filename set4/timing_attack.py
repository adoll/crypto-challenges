import urllib
import time
from Crypto import Random
import numpy
import heapq
hex_chars = '0123456789abcdef'
target = 'http://127.0.0.1:8080/test'
filename = 'passwords'

def make_request(filename, sig):
    start_time = time.time()
    code = urllib.urlopen(target + '?file=' + filename + '&signature=' + sig).getcode()
    if code == 200:
        print 'Success, sig = ' + sig
    elapsed_time = time.time() - start_time
    return elapsed_time

def update_times(filename, sig, N):
    times = []
    total_elapsed = 0
    for i in xrange(0, N):
        elapsed_time = make_request(filename, sig)
        times.append(elapsed_time)
        total_elapsed += elapsed_time
    avg_time = elapsed_time/N
    return avg_time

def test_chars(N, sig):
    avgs = []
    sig_list = list(sig)
    for c in hex_chars:
        sig_list[i] = c
        sig = ''.join(sig_list)
        avg_time = update_times(filename, sig, N)
        avgs.append((avg_time, c))
    return avgs

sig = 'A'*40
for i in xrange(0, len(sig)):
    N = 20
    while True:
        avgs = test_chars(N, sig)
        std_dev = numpy.std(zip(*avgs)[0])
        largest = heapq.nlargest(2, avgs)
        if largest[0][0] - largest[1][0] > 2*std_dev:
            sig_list = list(sig)
            sig_list[i] = largest[0][1]
            sig = ''.join(sig_list)
            print sig
            break
        N *= 2
