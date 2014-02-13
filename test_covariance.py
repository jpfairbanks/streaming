from covariance import CovarianceEstimator
import numpy as np
from numpy import random


def check_CovarianceEstimator(cove, n):
    assert cove.dim == n
    assert len(cove.totals) == n
    assert cove.count == 0
    assert cove.sums.shape == (n, n)


def testInit():
    """Test that the initialization happens correctly"""
    n = 4
    cove = CovarianceEstimator(n)
    check_CovarianceEstimator(cove, n)


def makerand(nsamples, ndim):
    mat = np.array([[1, .5], [.5, 1]])
    mu = np.arange(ndim)
    sample = random.multivariate_normal(mean=mu, cov=mat, size=nsamples)
    return sample


def testCov():
    """Generate a random sample with known covariance and compare to numpy.cov."""
    cove = CovarianceEstimator(2)
    sample = makerand(10, 2)
    print('sample:\n {0}'.format(sample))
    for row in range(10):
        x = sample[row][:]
        cove.update(x)
    ans = cove.query()
    print('ans:\n {0}'.format(ans))
    rans = np.cov(sample.T)
    print('rans:\n {0}'.format(rans))
    assert np.allclose(ans, rans)
