from __future__ import print_function
import sys

ifp = sys.stdin
ofp = sys.stdout
state = 0.0
weight = 0.5
for line in ifp:
    x = float(line)
    state = weight * state + x
    print(state, file=ofp)
