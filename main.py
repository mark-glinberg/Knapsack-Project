import argparse
import random

def run_alg(args):
    # print(f"-i, --inst \t{args.filePath} (filePath)")
    # print(f"-a, --alg \t{args.alg} (alg)")
    # print(f"-t, --time \t{args.cutoff} (cutoff)")
    # print(f"-s, --seed \t{args.seed} (seed)")

    # Open input file 
    data = open(args.filePath, "r")

    # Sets the seed for random, when generating a random num later you must call random.seed(seed) before generating the random num
    # due to random being a pseudo-random generator
    if seed != 0:
        random.seed(seed)

    if args.alg == 'bnb':
        print("Executing Branch-and-Bound algorithm")
        # EXEC bnb algorithm
    elif args.alg == 'approx':
        print("Executing Approximation algorithm")
        # EXEC aprox algorithm
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
                        default=filePath)
    
    parser.add_argument('-a', '--alg', action="store",
                        type=str,
                        dest="alg",
                        default=alg)
    
    parser.add_argument('-t', '--time', action="store",
                        type=int,
                        dest="cutoff",
                        default=cutoff)
    
    parser.add_argument('-s', '--seed', action="store",
                        type=int,
                        dest="seed",
                        default=seed)
    
    # Store args
    args = parser.parse_args()

    run_alg(args)