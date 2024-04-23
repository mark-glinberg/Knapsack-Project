import time
import numpy as np

"""
Local search algorithm for the 0-1 knapsack problem using hill climbing.
While within the cutoff time, the algorithm geneartes a random solution (with most of the items not being selected).
Then with 20% probability it chooses a neighbor (flips a bit) at random and saves that neighbor as the solution.
The other 80% of the time, the algorithm iterates through all possible neighbors to find the one that has the largest evaluation.
If the neighbor is better than the current solution, then the current solution is replaced with the neighbor.
Once no neighbor can replace the current solution, a peak (local max) is reached.
The resulting peak will replace the best solution if it has a higher evaluation, otherwise the algorithm will restart with another random solution.

Parameters:
    values (list(float)): Values for each item
    weights (list(float)): Weights for each item
    capacity (int): Maximum weight allowed for knapsack
    cutoff (int): Maximum time algorithm can run
    seed (int): Seed for random number generation

Returns:
    best_val (float): Maximum value for solution found by algorithm
    best_sol list(int): List of items chosen by the solution found by the algorithm
    trace (list(float, float)): List of tuples for timestamps and values of each better solution found
"""
def hill_climbing(values, weights, capacity, cutoff, seed):
    # Set seed
    np.random.seed(seed=seed)
    # Convert inputs to np arrays for faster processing
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
            # With 20% likelihood, flip a random bit (pick a random neighbor)
            if np.random.rand() < 0.2:
                rand_idx = int(np.random.rand() * n)
                solution[rand_idx] = 1 - solution[rand_idx]
                sol_val = eval(solution)
            # Otherwise pick the best neighbor (steepest ascent)
            else:
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
    return best_val, np.nonzero(best_sol)[0], trace