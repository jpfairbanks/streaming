import sys
import random

fp = sys.stdin
a_0 = 1.0/2
for line in fp:
    x = float(line)
    state = a_0 * state + x
    print(state)
