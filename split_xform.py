#!/usr/bin/env python
""" This module demonstrates some features of the libstreampy
We take an iterable and split it into even and odd then scan it

Comparing a static implementation to the stream.py implementation

Depends on the stream module from https://github.com/aht/stream.py.
"""

from __future__ import print_function
import sys
sys.path.append("~/Code/streaming/libstreampy/")
from time import time
import math
import stream
from stream import fold
from stream import tee
from stream import filter
from stream import item
import operator as ops

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: ./split_xform.py N", file=sys.stderr)
        sys.exit(1)
    N = int(sys.argv[1])
    instream = [float(i) for i in range(N)]

    def scan(op, seq):
        """Compute the op-scan of seq"""
        l = []
        s = 0
        for x in seq:
            s = op(s,x)
            l.append(s)
        return l

    def my_sqrt(x):
        for i in x:
            yield math.sqrt(i)
    #static computation in a time block
    ts = time()
    evens = instream[::2]
    odds  = instream[1::2]
    evens = map(math.sqrt, evens)
    odds  = map(math.sqrt, odds)
    even_ans = scan(ops.add, evens)
    odd_ans  = reduce(ops.add, odds )
    static_time = time() - ts

    #streaming computation

    # create our filters
    cong_2 = lambda x: x%2==0
    evens = filter(cong_2)
    odds  = filter(lambda x: not cong_2(x))
    ts = time()
    # wire the split into the filters
    instream >> tee(evens)
    instream >> odds

    # wire up the map and fold (scan/accumulate)
    foldedevens = (evens >> stream.map(math.sqrt) >> fold(ops.add))
    print(time() - ts)
    sqrtodds = odds >> (stream.Processor(my_sqrt))
    print("established the sqrter %f" % (time() - ts))
    foldedodd = sqrtodds >> stream.fold(ops.add)
    print("made odd folder: %f" % (time() - ts))
    # force execution
    soans = foldedodd >> item[-1:]
    print(soans)
    print(time() - ts)
    seans = foldedevens >> item[:]
    print(time() - ts)
    stream_time = time() - ts

    #print(even_ans)
    #print(seans >> item[:])
    #print(odd_ans)
    #print(soans >> item[:])

    #check the answers

    #assert ( seans == (even_ans))
    #assert ( soans == (odd_ans))
    assert ( seans == list(even_ans))
    #assert ( soans == list(odd_ans))

    # display the timing information
    print("we got the same answer using the streams")
    print("static_time: %f, ips: %f" % (static_time, N//static_time))
    print("stream_time: %f, ips: %f" % (stream_time, N//stream_time))
    print("streaming/static: %f" % (stream_time/static_time))
