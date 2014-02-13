from __future__ import print_function
import sys
import argparse
import numpy.random as random


def vetdist(candidate):
    """Maps string description of a Distribution to np.random Distribution"""
    if candidate == "uniform":
        return random.uniform
    if candidate == "normal":
        return random.normal
    if candidate == "exponential":
        return random.exponential
    raise argparse.ArgumentTypeError(
        "Distribution <{0}> not found".format(candidate))


def sprintln(sep, nums):
    """Print the numbers with a seperator"""
    if len(nums) == 1:
        return str(nums[0])
    else:
        return sep.join(map(str, nums))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("nsamples", help="number of samples to produce",
                        type=int, nargs="?", default=100)
    parser.add_argument("-d",
                        help="delimiter",
                        type=str,
                        nargs="?",
                        default=" ")
    parser.add_argument("-f",
                        help="number of dimensions (fields)",
                        type=int,
                        nargs="?",
                        default=1)
    parser.add_argument("--dist",
                        help="a sampling distribution uniform (default), normal, exponential",
                        type=vetdist,
                        default="uniform",
                        nargs="?")
    args = parser.parse_args()
    fp = sys.stdout
    #while True:
    for i in range(args.nsamples):
        nums = args.dist(size=args.f)
        print(sprintln(args.d, nums), file=fp)
