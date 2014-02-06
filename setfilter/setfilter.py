"""HierSetFilter.py runs a hierarchical set filter for removing duplicates from
an infinite stream of data. We use multiprocessing and two implementations one
for leaf nodes and one for internal nodes.
The system will stop after a finite number of
elements are generated then processed. We use logging to stderr in order
to show the concurrency of the system.

The convention is the function arguments are (input, application, output)

Author: James Fairbanks
Email: jpfairbanks@gmail.com
Date: 2014-01-31

"""
import time
import math
import logging
import sys
import scipy.stats
from scipy.stats import zipf
import random
import multiprocessing
from multiprocessing import Process, JoinableQueue as Queue
import itertools
from itertools import zip_longest

SIGOBJ = "signal"

def IterChan(chan):
    while True:
        elt = chan.get()
        chan.task_done()
        reply = (yield elt)
        if elt == SIGOBJ:
            break


def makeelts(lower: int, upper: int, numelts: int, outchan: Queue):
    """Make a stream of integers uniformly at random between lower and upper
    if numelts is negative go for ever. Put then into the outchan."""
    for i in range(numelts):
        n = random.randint(lower, upper)
        outchan.put(n)
        fp = sys.stdout
    outchan.put(SIGOBJ)


def LeafSet(inchan:Queue, outchan:Queue):
    """Report the distinct elements of inchan on outchan."""
    sf = set()
    logger = multiprocessing.log_to_stderr()
    logger.setLevel(logging.INFO)
    for x in IterChan(inchan):
        #logger.info("Leaf:%s" % x)
        if x not in sf:
            sf.add(x)
            outchan.put(x)
    logger.info("Leaf done")


def InternalSet(Achild: Queue, Bchild: Queue, outqueue: Queue):
    """Take the output of two LeafSet's and take the union."""
    logger = multiprocessing.log_to_stderr()
    logger.setLevel(logging.INFO)
    AminusB = set()
    BminusA = set()
    for a,b in zip_longest(IterChan(Achild), IterChan(Bchild), fillvalue=None):
        #logger.info("Internal:%s:%s" % (a, b))
        if a in BminusA:
            BminusA.remove(a)
        elif a not in AminusB:
            AminusB.add(a)
            outqueue.put(a)
        if b in AminusB:
            AminusB.remove(b)
        elif b not in BminusA:
            BminusA.add(b)
            outqueue.put(b)
    logger.info("Internal done")


def printer(chan: Queue, fmt: str, destination:str):
    """A data sink that prints the contents of chan as strings to destination
    using a format string the first argument to the format string is the number
    of elements seen so far."""
    logger = multiprocessing.log_to_stderr()
    logger.setLevel(logging.INFO)
    logger.info("sink started")
    i = 0
    for elt in IterChan(chan):
        print(fmt % (i, elt), file=destination)
        i += 1
    logger.info('Printer done')


def makeLeaf(lower: int, upper: int, number: int):
    """Start the leaf processes and returns the channel on which to communicate."""
    q0, q1 = Queue(), Queue()
    src = Process(target=makeelts, args=(lower, upper, number, q0))
    work = Process(target=LeafSet, args=(q0, q1))
    src.start()
    work.start()
    return q1

def makeInternal(height: int, numelts: int) -> Queue:
    """Recursively Start the internal node processes and returns the channel on which to communicate."""
    outchan = Queue()
    assert height >= 0,  "down too far in tree"
    if height == 0: #base case
        left = makeLeaf(0, 1<<7, numelts)
        right = makeLeaf(1<<3, 1<<9, numelts)
    else: #not at the leaves yet
        left = makeInternal(height-1, numelts)
        right = makeInternal(height-1, numelts)
    internal= Process(target=InternalSet, args=(left, right, outchan))
    internal.start()
    return outchan


def main():
    """Starts all the processing elements and connects them."""
    n = 100000
    height = 3
    root = makeInternal(height, n)
    sink = Process(target=printer, args=(root, "sink:%d:%s", sys.stdout))
    sink.start()
    #JOINING
    sink.join()
    print("procs joined")
    return 0

if __name__ == '__main__':
    main()


class Worker(Process):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        """Call the super class constructor and assign the channels"""
        Process.__init__(self, group, target, name, args, kwargs)
        self.inchan = None
        self.outchan = None

    def attach(self, inchan, outchan):
        """Attach the two channels to the process."""
        self.inchan = inchan
        self.outchan = outchan
