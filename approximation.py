import time
import pandas as pd

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
    solution = [0 for _ in range(len(values))]
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
            solution[idx] = 1

    alg_time = time.time() - start
    if cutoff_reached:
        alg_time = cutoff

    return cur_value, solution, alg_time