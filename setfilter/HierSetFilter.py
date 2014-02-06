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
import random
import multiprocessing
from multiprocessing import Process, JoinableQueue as Queue

SIGOBJ = "signal"

def makeelts(lower:int, upper:int, numelts:int, outchan:Queue):
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
    morestuff = True
    while morestuff:
        x = inchan.get()
        logger.info("Leaf:%s" % x)
        if x not in sf:
            sf.add(x)
            outchan.put(x)
        inchan.task_done()
        if x == SIGOBJ:
            morestuff = False
    logger.info("leafdone")


def InternalSet(Achild:Queue, Bchild:Queue, outqueue:Queue):
    """Take the output of two LeafSet's and take the union."""
    logger = multiprocessing.log_to_stderr()
    logger.setLevel(logging.INFO)
    AminusB = set()
    BminusA = set()
    morestuff = True
    while morestuff:
        a = Achild.get()
        b = Bchild.get()
        logger.info("Internal:%s:%s" % (a, b))
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
        Achild.task_done()
        Bchild.task_done()
        if (a == SIGOBJ) or (b == SIGOBJ):
            outqueue.put(SIGOBJ)
            morestuff = False
    logger.info("internal done")


def printer(chan:Queue, fmt:str, destination:file):
    """A data sink that prints the contents of chan as strings to destination
    using a format string"""
    logger = multiprocessing.log_to_stderr()
    logger.setLevel(logging.INFO)
    logger.info("sink started")
    i = 0
    morestuff = True
    while morestuff:
        elt = chan.get()
        logger.info(fmt % (i, elt))
        i += 1
        chan.task_done()
        if elt == SIGOBJ:
            morestuff = False
    logger.info('printer done')


def main():
    """Starts all the processing elements and connects them."""
    q = [Queue() for i in range(5)]
    src1 = Process(target=makeelts, args=(0, 1 << 3, 20, q[0]))
    src2 = Process(target=makeelts, args=(1 << 2, 1 << 4, 20, q[1]))
    work1 = Process(target=LeafSet, args=(q[0], q[2]))
    work2 = Process(target=LeafSet, args=(q[1], q[3]))
    #internalwork = Process(target=LeafSet, args=(q[2], q[4]))
    internalwork = Process(target=InternalSet, args=(q[2], q[3], q[4]))
    sink = Process(target=printer, args=(q[4], "sink:%d:%s", sys.stderr))
    src1.start()
    src2.start()
    work1.start()
    work2.start()
    internalwork.start()
    sink.start()
    #JOINING
    src1.join()
    src2.join()
    print("sources joined", file=sys.stderr)
    work1.join()
    work2.join()
    print("leaves joined", file=sys.stderr)
    internalwork.join()
    print("root joined", file=sys.stderr)
    sink.join()
    print("procs joined")

    return 0

if __name__ == '__main__':
    main()
