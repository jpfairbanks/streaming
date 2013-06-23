""" This module demonstrates some features of the libstreampy 
We take an iterable and split it into even and odd then scan it

Comparing a static implementation to the stream.py implementation"""
import sys
sys.path.append("~/Code/streaming/libstreampy/")
from time import time
import stream
from stream import fold
from stream import tee
from stream import filter
from stream import item
import operator as ops
import numpy

N = int(sys.argv[1])
instream = range(N)

#use a python scan impementation no cheating for static team
def scan(op, seq):
    """Compute the op-scan of seq"""
    l = []
    s = 0
    for x in seq:
	s = op(s,x)
	l.append(s)
    return l
#static
ts = time()
#filter, scan
evens = instream[::2]
odds = instream[1::2]
even_ans = scan(ops.add, evens)
odd_ans = scan(ops.add, odds )
static_time = time() - ts

#streaming
#these just create objects that are going to accept streams
cong_2 = lambda x: x%2==0
evens = filter(cong_2)
odds  = filter(lambda x: not cong_2(x))
ts = time()
#do the wiring
instream >> tee(evens)
instream >> odds
seans = evens >> fold(ops.add)
soans = odds  >> fold(ops.add)
#seans = evens >> stream.reduce(ops.add)
#soans = odds  >> stream.reduce(ops.add)

# trigger execution
seans = seans >> item[:]
soans = soans >> item[:]
stream_time = time() - ts
#print(even_ans)
#print(seans >> item[:])
#print(odd_ans)
#print(soans >> item[:])


#make sure we got the right answer
assert ( seans == list(even_ans))
assert ( soans == list(odd_ans))
#show us what the performance penalty for using streams was.
print("we got the same answer using the streams")
print("static_time: %f, ips: %f" % (static_time, N//static_time))
print("stream_time: %f, ips: %f" % (stream_time, N//stream_time))
print("streaming/static: %f" % (stream_time/static_time))
