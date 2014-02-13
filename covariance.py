#!/usr/bin/env python
"""covariance.py computes the covariance on a stream of numbers.
The input must be lines of text representing floating point numbers.
The dimensionality is passed as the first argument.
Every line must have the same number of records separated by the delimiter sep.

This file also provides a class CovarianceEstimator for reusability.
"""

from __future__ import print_function
import sys
import argparse
import numpy as np


class CovarianceEstimator():
    """Estimates teh covariance of a multivariate data set.
    Each update must contain an observation for every varialble"""
    def __init__(self, dim):
        """Initialize for observations with dimension dim."""
        self.sums = np.zeros([dim, dim])
        self.totals = np.zeros(dim)
        self.count = 0
        self.dim = dim

    def update(self, observation):
        """Update the data structure with a single observation"""
        self.count += 1
        for j in range(self.dim):
            self.totals[j] += observation[j]
            for k in range(self.dim):
                self.sums[j, k] += observation[j] * observation[k]

    def query(self):
        """Get the covariance matrix as a numpy array.
        Performs a malloc for the output."""
        n = self.count
        cov = (self.sums - np.outer(self.totals, self.totals/n)) / (n-1)
        return cov


class LineParser():
    def __init__(self, len):
        self.space = np.empty(len, dtype=np.float64)
        self.len = len
        self.err = 0

    def parse(self, line):
        """Parse a line into an array of floats of length dim.
        Recycles memory for output buffer, so you need to copy out
        in concurrent situations."""
        split = line.split(" ")
        if len(split) != self.len:
            raise Exception(
                "wrong line length check self.err for observed length.")
            self.err = len(split)
        for i in range(self.len):
            self.space[i] = float(split[i])
        return self.space

if __name__ == '__main__':
    print('starting covariance computation', file=sys.stderr)
    parser = argparse.ArgumentParser()
    parser.add_argument("dim", help="number of dimensions", type=int)
    args = parser.parse_args()
    state = CovarianceEstimator(args.dim)
    linereader = LineParser(args.dim)
    for line in sys.stdin:
        observation = linereader.parse(line)
        state.update(observation)
        out = state.query()
        oline = str(out)
        sys.stdout.write(oline)
        sys.stdout.write("\n")
