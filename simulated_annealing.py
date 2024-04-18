import random
import math
import time

def knapsack_value(knapsack, weights, values):
    total_weight = sum(weights[i] for i, included in enumerate(knapsack) if included)
    total_value = sum(values[i] for i, included in enumerate(knapsack) if included)
    return total_value, total_weight

def initialize_solution(weights, capacity):
    solution = [False] * len(weights)
    current_weight = 0
    items = list(range(len(weights)))
    random.shuffle(items)  # Randomize the order of items to consider for adding
    for item in items:
        if current_weight + weights[item] <= capacity:
            solution[item] = True
            current_weight += weights[item]
    return solution

def simulated_annealing(values, weights, capacity, stopping_temp):
    start = time.time()
    initial_temp = 100 + len(values) * 5
    cooling_rate = 1 / (10 + 0.1 * len(values))
    current_solution = initialize_solution(weights, capacity)
    current_value, current_weight = knapsack_value(current_solution, weights, values)
    
    best_solution = current_solution[:]
    best_value = current_value

    temperature = initial_temp

    while temperature > stopping_temp and time.time() - start < 300:
        # Create random solution
        item_to_flip = random.randint(0, len(weights) - 1)
        neighbor = current_solution[:]
        neighbor[item_to_flip] = not neighbor[item_to_flip]
        neighbor_value, neighbor_weight = knapsack_value(neighbor, weights, values)

        if neighbor_weight <= capacity:
            # Find delta
            delta_value = neighbor_value - current_value

            # Consider cases
            if delta_value > 0 or random.random() < math.exp(delta_value / temperature):
                current_solution = neighbor[:]
                current_value = neighbor_value
                current_weight = neighbor_weight

                if current_value > best_value:
                    best_solution = current_solution[:]
                    best_value = current_value

        # Cool down temperature
        temperature -= cooling_rate

    return best_value, best_solution
