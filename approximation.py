import pandas as pd

def approximation(values, weights, capacity):
    # Init list of ratios
    ratio_list = []

    for value, weight in zip(values, weights):
        ratio_list.append(float(value / weight))

    # Store ratios, values, and weights as dataframe
    item_frame = pd.DataFrame({'values': values, 'weights': weights, 'ratios': ratio_list})
    item_frame = item_frame.sort_values(by=['ratios'], ascending=False)

    cur_weight = 0
    cur_value = 0

    # Greedy algorithm
    for _, item in item_frame.iterrows():
        if item['weights'] + cur_weight < capacity:
            cur_value += item['values']
            cur_weight += item['weights']

    if int(cur_value) == cur_value:
        print(int(cur_value))
    else:
        print("{:.4f}".format(cur_value))