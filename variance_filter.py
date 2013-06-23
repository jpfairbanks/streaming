import random as rand
from time import time
import sys
import math
import stream
from stream import repeatcall, Stream, item, filter, tee
import itertools


from pylab import hist

class zscore(Stream):
    def __init__(self, iterable=None):
	"""start a state with no data. all parameters are set to 0.0 """
        self.sumhat = 0.0
        self.varhat = 0.0
        self.count  = 0.0
	super(zscore, self).__init__(iterable)
    def mean(self):
        """returns the estimated mean so far
        :returns: @todo

        """
        return self.sumhat/self.count
    def sigma(self):
        """Returns the sigma estimate
        :returns: @todo

        """
        return math.sqrt(self.varhat/self.count)

    def push(self, datum):
        """Pushes a datum into the structure updating the state.

        :datum: a number type
        :returns: the z-score of the datum

        """
        self.sumhat += datum
        self.count  += 1
        muhat = self.mean()
        self.varhat += (datum - muhat)**2
        z = 0
        sigma = self.sigma()
        if sigma != 0:
            z = (datum - muhat)/sigma
        return z
    def __call__(self, iterator):
	"""Run an entire iterator through. Returns another iterator.
	We call push on each element.
	"""
        return itertools.imap(self.push, iterator)

    def zscore(self, datum):
        """Gets the zscore of an element without updating the parameters.

        :datum: a number type
        :returns: the z-score of datum

        """
        z = 0
        sigma = self.sigma()
        if sigma() != 0:
            z = (datum - muhat)/sigma()
        return z

    def __repr__(self):
        """print this as a string
        :returns: @todo

        """
        return "stream; sumhat:%f; varhat:%f, count:%f;"%(self.sumhat,self.varhat,self.count)

class threshold_tee(Stream):
    """A stream that converts a single stream into two streams
    it returns the stream of things abs(x) < threshold and puts
    x such that abs(x)>= threshold into named_stream.
    
    Currently this will give two handles for polling on.
    The test will be execute twice for each element that
    goes through the stream.
    
    Note: Calling named_stream >> item[:10]; threshold_tee >> item[:10]
    will probably access more than 20 items. it will scan for 10 items 
    that are within the threshold and then scan again for 10 items that 
    are outside of it. 

    This can be used for finding the first 100 inliers and the first 10 outliers.

         >>> outlier = (named_stream >> item[:10])
	 >>> inliers = (threshold_tee >> item[:100])

    """

    def __init__(self, named_stream, threshold=2):
        """@todo: to be defined """
	super(threshold_tee, self).__init__()
        self.thresh = threshold
	self.named_stream = named_stream

    def __pipe__(self, inpipe):
        accept_branch, reject_branch = itertools.tee(iter(inpipe))
	accept = lambda x: abs(x) <  self.thresh
	reject = lambda x: abs(x) >= self.thresh
	self.iterator = itertools.ifilter(accept, accept_branch)
	reject_branch = itertools.ifilter(reject, reject_branch)
	Stream.pipe(reject_branch, self.named_stream)
	return self
    
    def __call__(self, iterator):
        return itertools.imap(push, iter(inpipe))
    

if __name__ == "__main__":
    varstream = zscore()
    #repeatcall(rand.normalvariate, 0,1) >> varstream
    repeatcall(rand.random) >> varstream
    x = (varstream >> item[:500])
    print(varstream)
    #hist(x)
    thresh = 1
    #normal_accept = filter(lambda x : abs(x)<=thresh)
    #normal_reject = filter(lambda x : abs(x)>thresh)
    #varstream >> tee(normal_accept)
    #varstream >> normal_reject
    #hist(normal_accept >> item[:500])
    #hist(normal_reject >> item[:500])

    extremes = Stream()
    typicals = (varstream >> threshold_tee(extremes, 2))
    print(typicals >> item[:500])
    print(extremes >> item[:50])
