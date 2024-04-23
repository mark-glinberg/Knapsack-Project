import glob
import os

"""
Script to generate the average time, best solution, and relative error generated across all trace files for all instances of a given local search algorithm
"""

alg = "ls1" # Modify for ls1 or ls2

# All problem instances
small_files = ["small_{}".format(i) for i in range(1,11)]
large_files = ["large_{}".format(i) for i in range(1,22)]
files = small_files + large_files
# Output list
lines = ["File\t\tTime(s)\t\t\tValue\t\t\t\tRelErr\n"]

# Iterate through all instances
for file in files:
    # Collect all trace files generated for given problem instance (and given alg)
    paths = glob.glob("../output/our_trace_files/{}_{}*".format(file, alg))
    traces = [path.replace("\\", "/") for path in paths]

    # Initialize averages
    avg_time = 0
    avg_value = 0
    # Iterate through all trace files collected
    for trace in traces:
        # Open trace file
        with open(trace, "r") as f:
            # Read the last output (best solution found)
            last_line = f.readlines()[-1]
            time, value = map(float, last_line.split(","))
            # Add latest timestamp and best value found to averages
            avg_time += time
            avg_value += value

    # Calculate averages
    avg_time /= 10
    avg_value /= 10

    # Open solution file to get optimal solution
    if "large" in file:
        sol_path = "../DATASET/large_scale_solution/{}".format(file)
        with open(sol_path, "r") as f:
            sol_value = float(f.read())
        
        # Calculate average error
        rel_err = (sol_value - avg_value) / sol_value
        # Append new values to output list
        lines.append("{}:\t{:.6f},\t\t{:.2f},\t\t\t{:.4f}\n".format(file, avg_time, avg_value, rel_err))
    else:
        sol_path = "../DATASET/small_scale_solution/{}".format(file)
        with open(sol_path, "r") as f:
            sol_value = float(f.read())

        # Calculate average error
        rel_err = (sol_value - avg_value) / sol_value
        # Append new values to output list
        lines.append("{}:\t{:.5f},\t\t{:.4f},\t\t\t{:.4f}\n".format(file, avg_time, avg_value, rel_err))
    
# Change directory to main directory
os.chdir("..")
# Output list to file in main directory
with open("{}_averages.trace".format(alg), "w") as f:
    f.writelines(lines)