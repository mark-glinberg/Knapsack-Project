import argparse
import random

from approximation import approximation
from simulated_annealing import simulated_annealing
# import your python script here when you complete your algorithm


def run_alg(args):
    if "small" in args.dataPath:
        inputPath = "DATASET/small_scale/" + args.dataPath
        solutionPath = "DATASET/small_scale_solution/" + args.dataPath
    elif "large" in args.dataPath:
        inputPath = "DATASET/large_scale/" + args.dataPath
        solutionPath = "DATASET/large_scale_solution/" + args.dataPath
    else:
        inputPath = "DATASET/test/" + args.dataPath
        solutionPath = "DATASET/test_solution/" + args.dataPath

    if seed != 0:
        random.seed(seed)

    # Parse input file and init lists for values and weights
    values = []
    weights = []
    f = open(inputPath, "r")
    _, capacity = map(int, f.readline().split())
    for line in f.readlines():
        value, weight = line.split()
        values.append(float(value))
        weights.append(float(weight))
    f.close()

    # Get optimal solution from file
    f = open(solutionPath, "r")
    opt_sol = int(f.read())
    f.close()

    # Skeleton for calling algorithms
    if args.alg == 'bnb':
        print("Executing Branch-and-Bound algorithm")
        # EXEC bnb algorithm
    elif args.alg == 'approx':
        alg_sol, items, alg_time = approximation(values, weights, capacity, cutoff)

        # Create solution file
        rel_error = (abs(opt_sol - alg_sol)) / opt_sol
        f = open(f"{args.dataPath}_{args.alg}_{args.cutoff}_{args.seed}.sol", "w")
        f.write("{}\n".format(rel_error))
        f.write(", ".join(map(str, items)))
        f.close()
    elif args.alg == 'ls1':
        print("Executing 1st Local Search algorithm (simulated annealing)")
        # EXEC 1st local search algorithm
        initial_temp = 1000
        cooling_rate = 0.03
        stopping_temp = 1

        best_value, best_solution = simulated_annealing(values, weights, capacity, initial_temp, cooling_rate, stopping_temp)

        print(best_solution)
        print(best_value)

    else:
        print("Executing 2nd Local Search algorithm")
        # EXEC 2nd local search algorithm
    
if __name__ == '__main__':
    # Init default parameters
    dataPath = 'small_1'
    alg = 'ls1'
    cutoff = 500
    seed = 0

    # Init args
    parser = argparse.ArgumentParser(
        prog='main',
        add_help=True
    )

    parser.add_argument('-i', '--inst', action="store",
                        type=str,
                        dest="dataPath",
                        default=dataPath,
                        help="input file to read (ex: small_1)")
    
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