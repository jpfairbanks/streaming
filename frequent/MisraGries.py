"""MisraGries.py: Implements the Misra Gries algorithm for finding frequent
stream elements"""
import random
import collections
import argparse


class MisraGriesSketch:
    """MisraGriesSketch: supports iterating over a stream of data
    estimating the frequency of high frequency items.
    Instantiating the class initializes the structure.
    Call process on each element to insert it.
    Call query to achieve an estimate on the frequency of an item.
    Given a second pass over the data we can return the elements
    with frequency at least m/k
    """
    def __init__(self, k):
        self.candidates = dict()
        self.m = 0
        self.k = k
        self.counter = collections.Counter()

    def process(self, j):
        """insert a single element and update the structure"""
        self.m += 1
        candidates = self.candidates
        if j in candidates:
            candidates[j] += 1
        elif len(candidates) < self.k - 1:
            #available slots to add a candidate
            candidates[j] = 1
        else:
            #no slot for j try and evict
            for l in list(candidates.keys()):
                candidates[l] += -1
                if candidates[l] == 0:
                    #self.dellist.append(l)
                    del candidates[l]
            #self.dellist = []
        return 0

    def query(self, j):
        """An estimate of the frequency of j. At least f[j] - m/k."""
        if j in self.candidates:
            return self.candidates[j]
        else:
            return 0

    @property
    def thresh(self):
        """Defines the threshold of how frequent is frequent enough."""
        return self.m / self.k

    def secondpass(self, seq):
        """Run the sequence through again tracking the candidates
        to see which are frequent."""
        for j in seq:
            if j in self.candidates:
                self.counter[j] += 1
        #take all elements where true count exceeds thresh
        return (j for j, c in self.counter.items() if c >= self.thresh)

    def validate(self):
        """After you have run the data through for the second pass,
        it is possible to test that the data structure had no false negatives.
        We check that any element that should be considered frequent was
        in fact a candidate. We have no logical implication
        between candidates and their true values."""
        for j, c in self.counter.items():
            if c > self.thresh and j not in self.candidates:
                return False
        return True

    def __str__(self):
        return "MisraGriesSketch m:%d, k:%d" % (self.m, self.k)


def main(m, k):
    """Generate the random input and get the two pass frequent items
    using MG algorithm.

    - m: length of stream.
    - k: fraction of elts desired."""
    MG = MisraGriesSketch(k)
    instream = [int(random.paretovariate(1)) for i in range(m)]
    for j in instream:
        MG.process(j)
        #print("m:%d; j:%d; state:%s" % (MG.m, j, MG.candidates))
    frequentItems = list(MG.secondpass(instream))
    print(MG.validate())
    return MG,  frequentItems

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", type=int,
                        dest="m", help="the length of stream to make")
    parser.add_argument("-k", type=int,
                        dest="k",
                        help="the fraction of elements to consider frequent")
    args = parser.parse_args()
    print("%s,%s" % main(args.m, args.k))
