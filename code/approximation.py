import time
import pandas as pd

"""
Approximation algorithm for the 0-1 knapsack problem using a greedy approach. Calculates the ratio 
of value to weight for each item and sorts in descending order based on ratio. Selects the item with 
the largest ratio at each iteration until the knapsack is filled.

Parameters:
    values (list(float)): Values for each item
    weights (list(float)): Weights for each item
    capacity (int): Maximum weight allowed for knapsack
    cutoff (int): Maximum time algorithm can run

Returns:
    cur_value (float): Maximum value for solution found by algorithm
    cur_value list(int): List of items chosen by the solution found by the algorithm
    alg_time (float): Time taken to run the algorithm
"""

def approximation(values, weights, capacity, cutoff):
    start = time.time()

    # Init list of ratios
    ratio_list = []
    for value, weight in zip(values, weights):
        ratio_list.append(float(value / weight))

    # Store ratios, values, and weights as dataframe
    item_frame = pd.DataFrame({'values': values, 'weights': weights, 'ratios': ratio_list})
    item_frame = item_frame.sort_values(by=['ratios'], ascending=False)

    # Init vars for greedy algorithm
    solution = []
    cur_weight = 0
    cur_value = 0
    cutoff_reached = False

    for idx, item in item_frame.iterrows():
        if time.time() - start >= cutoff:
            cutoff_reached = True
            break

        if item['weights'] + cur_weight < capacity:
            cur_value += item['values']
            cur_weight += item['weights']
            solution.append(idx)

    if item_frame['values'].max() > cur_value:
        solution = [item_frame['values'].idxmax()]
        cur_value = item_frame['values'].max()

    alg_time = time.time() - start
    if cutoff_reached:
        alg_time = cutoff

    return cur_value, solution, alg_time