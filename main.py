import argparse
import random
import pandas as pd
from approximation import approximation
# import your python script here when you complete your algorithm


def run_alg(args):
    # Sets the seed for random, when generating a random num later you must call random.seed(seed) before generating the random num
    # due to random being a pseudo-random generator
    if seed != 0:
        random.seed(seed)

    # Parse input file and init lists for values and weights
    values = []
    weights = []

    data = open(args.filePath, "r")
    _, capacity = map(int, data.readline().split())

    for line in data.readlines():
        value, weight = line.split()
        values.append(float(value))
        weights.append(float(weight))

    # Skeleton for calling algorithms
    if args.alg == 'bnb':
        print("Executing Branch-and-Bound algorithm")
        # EXEC bnb algorithm
    elif args.alg == 'approx':
        print("Executing Approximation algorithm")
        approximation(values, weights, capacity)
    elif args.alg == 'ls1':
        print("Executing 1st Local Search algorithm")
        # EXEC 1st local search algorithm
    else:
        print("Executing 2nd Local Search algorithm")
        # EXEC 2nd local search algorithm


if __name__ == '__main__':
    # Init default parameters
    filePath = 'DATASET/small_scale/small_1'
    alg = 'bnb'
    cutoff = 1000
    seed = 0

    # Init args
    parser = argparse.ArgumentParser(
        prog='main',
        add_help=True
    )

    parser.add_argument('-i', '--inst', action="store",
                        type=str,
                        dest="filePath",
                        default=filePath,
                        help="path to input file")
    
    parser.add_argument('-a', '--alg', action="store",
                        type=str,
                        dest="alg",
                        default=alg,
                        choices=['bnb', 'approx', 'ls1', 'ls2'],
                        help="select which algorithm to run")
    
    parser.add_argument('-t', '--time', action="store",
                        type=int,
                        dest="cutoff",
                        default=cutoff,
                        help="cutoff time for algorithms")
    
    parser.add_argument('-s', '--seed', action="store",
                        type=int,
                        dest="seed",
                        default=seed,
                        help="seed used to randomize")
    
    args = parser.parse_args()

    run_alg(args)