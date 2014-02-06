import math
import sys
import scipy.stats
from scipy.stats import zipf
import random
STDIN = sys.stdin
STDIN.recv = STDIN.readline

STDOUT = sys.stdout
STDOUT.send = lambda x: STDOUT.write(str(x))

#Zipf = Source()
#Zipf.connect(lambda: zipf.rvs(2, size=10), STDOUT)

class Filter:
    "Generic filter class."
    def __init__(self):
        self.inchan = None
        self.f = None
        self.outchan = None

    def connect(self, inchan, f, outchan):
        self.inchan = inchan
        self.f = f
        self.outchan = outchan

    def Spawn(self):
        "Start an loop receiving from in and sending the result of f to out."
        while True:
            self.outchan.put(self.f(self.inchan.get()))


class Source(Filter):
    "Generate data similar to one sided filter"
    def connect(self, f, outchan):
        self.f = f
        self.outchan = outchan

    def Spawn(self):
        "Start an loop receiving from in and sending the result of f to out."
        while True:
            self.outchan.send(self.f())


class Sink:
    """Consume data similar to one sided filter.
    f can update the state of an object that will support queries."""
    def __init__(self):
        self.state = None
        self.f = None
        self.inchan = None

    def connect(self, inchan, f):
        self.inchan = inchan
        self.f = f

    def Spawn(self):
        "Start an loop receiving from in and applying f."
        while True:
            self.f(self.inchan.recv())


def compose(f:Filter, g:Filter) -> Filter:
    """Composes f,g into a new filter performing g of f."""
    h = Filter()
    h.inchan = f.inchan
    h.outchan = g.outchan
    h.f = lambda x: g.f(f.f(x))
    return h


def Sourceify(generator, channel):
    source = Source()
    source.connect(generator, channel)
    return source

