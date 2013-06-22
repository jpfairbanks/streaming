from __future__ import print_function
import sys
import random

fp = sys.stdout
#while True:
for i in range(10000):
    num = random.random()
    print(str(num), file=fp)
