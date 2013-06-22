from __future__ import print_function
import sys
import random
import collections

window = collections.deque()
window.append(0.0)
window_size = 10
fp = sys.stdin
a_0 = 1.0/2
i = 0
for line in fp:
    x = float(line)
    if i >= window_size:
        window.popleft()
    i += 1
    window.append(x)
    y = sum(window) / window_size
    print(y)
