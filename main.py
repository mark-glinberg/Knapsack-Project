import argparse
import random
import os

from approximation import approximation
from simulated_annealing import simulated_annealing
from hill_climbing import hill_climbing
# import your python script here when you complete your algorithm

def run_alg(args):
    # Find path of file and determine whether it's a test file
    if "small" in args.dataPath:
        test = False
        inputPath = "DATASET/small_scale/" + args.dataPath
        solutionPath = "DATASET/small_scale_solution/" + args.dataPath
    elif "large" in args.dataPath:
        test = False
        inputPath = "DATASET/large_scale/" + args.dataPath
        solutionPath = "DATASET/large_scale_solution/" + args.dataPath
    else:
        test = True
        inputPath = "DATASET/test/" + args.dataPath
        solutionPath = "DATASET/test_solution/" + args.dataPath

    # Take input seed
    if args.seed != 0:
        random.seed(args.seed)
    
    # Take cutoff input or a default of 30 secs
    if args.cutoff > 0:
        cutoff = args.cutoff
    else:
        cutoff = 30

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
    if test:
        # Turn full solution into an array for test files
        opt_sol = []
        f = open(solutionPath, "r")
        for line in f.readlines():
            opt_sol.append(int(line))
        f.close()
    else:
        # Grab optimal solution as an int for data files
        f = open(solutionPath, "r")
        opt_sol = int(f.read())
        f.close()
    
    # Whether to create a trace file
    trace_file = False
    # Calling different algorithms
    if args.alg == 'bnb':
        print("Executing Branch-and-Bound algorithm")
        # EXEC bnb algorithm
    elif args.alg == 'approx':
        print("Executing Approximation algorithm")
        best_value, best_solution, alg_time = approximation(values, weights, capacity, cutoff)

        # Create solution file
        print(best_solution)
        print(best_value)
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
        print("Executing 2nd Local Search algorithm (hill climbing)")
        # EXEC 2nd local serach algorithm
        best_value, best_solution, trace = hill_climbing(values, weights, capacity, cutoff)
        # Flag to generate a trace file
        trace_file = True

        print(best_solution)
        print(best_value)
        if test:
            print(opt_sol == best_solution)
        else:
            print(opt_sol == best_value)

    # Generate output file if not testing our code
    if not test:
        filename = "our_solutions/{}_{}_{}_{}.sol".format(args.dataPath, args.alg, args.cutoff, args.seed)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            f.write(str(best_value) + "\n")
            f.write(", ".join(map(str, best_solution)))

        # Generate trace file if the algorithm calls for it
        if trace_file:
            filename = "our_trace_files/{}_{}_{}_{}.trace".format(args.dataPath, args.alg, args.cutoff, args.seed)
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "w") as f:
                for step in trace:
                    f.write(", ".join(map(str, step)) + "\n")

    
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