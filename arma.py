import sys
import random

def arma_gen(stream:iter, consts):
    """Generator function that produces an ARMA stream."""
    state = 0
    for line in stream:
        x = float(line)
        state = a_0 * state + x
        yield state

if __name__ == '__main__':
    fp = sys.stdin
    ofp = sys.stdout
    for y in arma_gen(fp, -1.0/2):
        print(y, file=ofp)
