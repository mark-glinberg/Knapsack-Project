import argparse
import random
import os

from approximation import approximation
from simulated_annealing import simulated_annealing
from hill_climbing import hill_climbing
from BnB import BnB_knapsack
from generate_plots import generate_plots
# import your python script here when you complete your algorithm

"""
Main file for handling command line arguments and calling various scripts. Parses input 
to genereate list of items by value and weight. Runs algorithms using command line arguments 
and calling corresponding scripts. Generates plots using separate script. 
"""

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
            opt_sol.append(float(line))
        f.close()
    else:
        # Grab optimal solution as an int for data files
        f = open(solutionPath, "r")
        opt_sol = float(f.read())
        f.close()
    
    # Whether to create a trace file
    trace_file = False
    # Calling different algorithms
    if args.alg == 'bnb':
        print("Executing Branch-and-Bound algorithm")
        # EXEC bnb algorithm
        best_value, best_solution, trace, tot_time = BnB_knapsack(inputPath, cutoff, "our_solutions", "our_trace_files")
        trace_file = True
        args.seed = None
        best_value = round(best_value, 4)
        print(best_solution)
        print(best_value)
        print(tot_time)
        if test:
            sol_val = 0
            for i in range(len(opt_sol)):
                if opt_sol[i] == 1.0:
                    sol_val += values[i]
            print(sol_val == best_value)
        else:
            print(opt_sol == best_value)
    elif args.alg == 'approx':
        print("Executing Approximation algorithm")
        best_value, best_solution, alg_time = approximation(values, weights, capacity, cutoff)

        # Create solution file
        print(best_solution)
        print(best_value)
    elif args.alg == 'ls1':
        print("Executing 1st Local Search algorithm (simulated annealing)")
        # EXEC 1st local search algorithm

        best_value, best_solution, trace = simulated_annealing(values, weights, capacity, 0, cutoff)

        trace_file = True
        # Create solution file
        
        print(best_solution)
        print(best_value)
    else:
        print("Executing 2nd Local Search algorithm (hill climbing)")
        # EXEC 2nd local search algorithm
        best_value, best_solution, trace = hill_climbing(values, weights, capacity, cutoff, seed)
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
        if args.seed:
            filename = "our_solutions/{}_{}_{}_{}.sol".format(args.dataPath, args.alg, args.cutoff, args.seed)
        else:
            filename = "our_solutions/{}_{}_{}.sol".format(args.dataPath, args.alg, args.cutoff)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            f.write(str(best_value) + "\n")
            f.write(", ".join(map(str, best_solution)))

        # Generate trace file if the algorithm calls for it
        if trace_file:
            if args.seed:
                filename = "our_trace_files/{}_{}_{}_{}.trace".format(args.dataPath, args.alg, args.cutoff, args.seed)
            else:
                filename = "our_trace_files/{}_{}_{}.trace".format(args.dataPath, args.alg, args.cutoff)
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "w") as f:
                for step in trace:
                    f.write(", ".join(map(str, step)) + "\n")

def plot(args):
    generate_plots(args.alg, args.generate)

if __name__ == '__main__':
    # Init default parameters
    dataPath = 'large_3'
    alg = 'ls1'
    cutoff = 500
    seed = 0

    # Init args
    parser = argparse.ArgumentParser(
        prog='main',
        add_help=True
    )

    parser.add_argument('-inst', action="store",
                        type=str,
                        dest="dataPath",
                        default=dataPath,
                        help="input file to read (ex: small_1)")
    
    parser.add_argument('-alg', action="store",
                        type=str,
                        dest="alg",
                        default=alg,
                        choices=['bnb', 'approx', 'ls1', 'ls2'],
                        help="select which algorithm to run")
    
    parser.add_argument('-time', action="store",
                        type=int,
                        dest="cutoff",
                        default=cutoff,
                        help="cutoff time for algorithms")
    
    parser.add_argument('-seed', action="store",
                        type=int,
                        dest="seed",
                        default=seed,
                        help="seed used to randomize")
    
    parser.add_argument('-p', '--plot', action="store_true",
                        dest="plot",
                        help="whether or not to plot local searches")
    
    parser.add_argument('-g', '--generate', action="store_true",
                        dest="generate",
                        help="whether or not to generate new trace files for plots")
    
    args = parser.parse_args()
    if args.plot:
        plot(args)
    else:
        run_alg(args)