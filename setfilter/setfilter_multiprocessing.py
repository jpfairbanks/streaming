"""setfilter.py runs a hierarchical set filter for removing duplicates from
an infinite stream of data.

Author: James Fairbanks
Email: jpfairbanks@gmail.com
Date: 2014-01-28

"""
import sys
import random
from multiprocessing import Process, JoinableQueue as Queue


class SetFilter:
    def __init__(self):
        self.state = set()

    def insert(self, elt):
        if elt in self.state:
            return None
        else:
            self.state.add(elt)
            return elt


def makeelts(lower, upper, numelts, outqueue):
    for i in range(numelts):
        n = random.randint(lower, upper)
        outqueue.put(n)
        fp = sys.stdout
        if i % 10 == 0:
            fp.write(".")
    outqueue.put(None)


def makeset(inqueue, outqueue):
    sf = SetFilter()
    while True:
        x = inqueue.get()
        if x is None:
            break
        y = sf.insert(x)
        if y is not None:
            outqueue.put(y)
        inqueue.task_done()
    outqueue.put(None)


def printer(queue, fmt, destination):
    i = 0
    while True:
        elt = queue.get()
        if elt is None:
            break
        print(fmt % (i, elt), file=destination)
        i += 1
        queue.task_done()

def main():
    """Starts all the processing elements and connects them."""
    q1, q2 = Queue(), Queue()
    src = Process(target=makeelts, args=(0, 1 << 12, 100000, q1))
    work = Process(target=makeset, args=(q1, q2))
    sink = Process(target=printer, args=(q2, "%d:%d", sys.stdout))
    src.start()
    work.start()
    sink.start()
    print("joining")
    q2.join()
    print("joined")
    src.join()
    work.join()
    sink.join()
    print("procs joined")

    return 0

if __name__ == '__main__':
    main()
