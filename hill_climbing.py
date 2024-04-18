import random
import time
import numpy as np


def hill_climbing(values, weights, capacity, cutoff, seed):
    np.random.seed(seed=seed)
    values = np.array(values)
    weights = np.array(weights)

    # Evaluation function for hill climbing
    def eval(solution):
        # Sum value using solution as one-hot indices
        value = np.sum(values * solution)
        # Sum weight using solution as one-hot indices
        weight = np.sum(weights * solution)
        # If the knapsack is overfilled, use the negative of the value
        if weight > capacity:
            value = -value
        return value
    
    # Number of items
    n = len(values)
    # Initialize solution to not include any item
    best_sol = np.zeros(n).astype('int32')
    best_val = eval(best_sol)
    # Initialize trace with first solution
    trace = [(0.0, best_val)]

    start = time.time()
    # Do random restarts until the cutoff time
    while time.time() - start < cutoff:
        # Randomly with some items included
        solution = np.random.choice(2, (n,), p=[0.99, 0.01]).astype('int32')
        sol_val = eval(solution)
        # Iterate until a better solution isn't found (a peak is reached)
        while True:
            # Initialize best neighbor as the smallest number
            largest_val = -np.inf
            largest_solution = []
            # Iterate through all neighbors to determine best improvement
            for i in range(n):
                # Generate a neighboring solution
                bit_flip = np.copy(solution)
                bit_flip[i] = 1 - bit_flip[i]
                bit_flip_val = eval(bit_flip)
                # Save the neighboring solution if it's the best one found so far
                if bit_flip_val > largest_val:
                    largest_val = bit_flip_val
                    largest_solution = np.copy(bit_flip)
            # If the best neighboring solution is better than the best solution
            # for the current random restart, use the neighboring solution
            if largest_val > sol_val:
                sol_val = largest_val
                solution = np.copy(largest_solution)
            # Otherwise a peak is reached
            else:
                break
        # If the peak found is higher than the current best peak, take new peak
        if sol_val > best_val:
            best_sol = solution
            best_val = sol_val
            trace.append((time.time() - start, best_val))
    return best_val, best_sol, trace