from __future__ import print_function
import argparse
from collections import deque
import sys


def moving_average_filter(stream, window_size):
    """Return the moving average of stream with the given window_size."""
    window = deque()
    window.append(0.0)
    i = 0
    for x in stream:
        if i >= window_size:
            window.popleft()
        else:
            i += 1
        window.append(x)
        y = sum(window) / window_size
        yield y


def main(window_size, fp):
    """Run a moving average filter over the text stream fp."""
    stream = (float(line) for line in fp)
    for y in moving_average_filter(stream, window_size):
        print(y, file=sys.stdout)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("k", help="window size",
                        type=int, default=1, nargs='?')
    args = parser.parse_args()
    main(args.k, sys.stdin)
