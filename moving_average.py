from __future__ import print_function
""" 
This module produces a stream of random variables from a moving average model.

The first command line argument is the number of samples negative means infinite.
The second argument is the window size. The moving average is uniform over the window.
The third argument is the file destination for the data it should be a filename.


the output to the user goes on stderr and the data generated goes onto a variable fp, 
which defaults to stdout.
"""
import sys
from time import time
import stream
import random as rand
from stream import chop, repeatcall, item

# handle command line flags
view_len = int(sys.argv[1])
print("num_samples: %d" % view_len, file=sys.stderr)
if view_len < 0:
    print("infinite samples", file=sys.stderr)
win_len = int(sys.argv[2])
print("window_length: %d" % win_len, file=sys.stderr)

if len(sys.argv) < 4 :
    fp = sys.stdout
else:
    try:
        fp = open(sys.argv[3], 'w')
    except IOError:
        print("couldn't open file; using stdout")
        fp = sys.stdout
print(str(fp), file=sys.stderr)

#define what we need to do moving averages
weights = [1.0/win_len for i in range(win_len)]
def inner(window):
    """ Computes the inner product of window and weights.
    weights must be defined outside to avoid a useless rezipping 
    when using this in a stream.
    """
    acc =  sum((i*w for i,w in zip(window, weights)))
    return acc

#get an infinite stream of uniform random floats
zsource   = repeatcall(rand.random)

# WIRING
# make our moving average window
winstream = ( zsource >> chop(win_len)  )
# compute the windowed average
xstream   = ( winstream >> stream.map(inner) )

# EXECUTING
if view_len > 0:
    ts = time()
    for i in range(view_len):
        fp.write(str(next(xstream.iterator))+'\n')
    print("time: %f" % (time()-ts), file=sys.stderr)
    print("items_per_sec: %f" % (view_len/(time()-ts)), file=sys.stderr)
if view_len < 0:
    while True:
        fp.write(str(next(xstream.iterator))+'\n')
