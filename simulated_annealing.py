import random
import math
import time

def simulated_annealing(values, weights, capacity, initial_temp, cooling_rate, stopping_temp):
    start = time.time()
    solution_trace = []
    # Utility function to calculate the total weight and value of the current knapsack
    def knapsack_value(knapsack):
        total_weight = sum(weights[i] for i in range(len(knapsack)) if knapsack[i])
        total_value = sum(values[i] for i in range(len(knapsack)) if knapsack[i])
        if total_weight > capacity:
            return 0  #exceeds capacity
        return total_value

    # Initialize a random solution
    n = len(values)
    current_solution = [random.choice([True, False]) for _ in range(n)]
    current_value = knapsack_value(current_solution)

    best_solution = current_solution[:]
    best_value = current_value

    # Begin with initial temperature
    temperature = initial_temp

    # Decrease temperature until stop
    while temperature > stopping_temp and time.time() - start < 300:
        # Generate a neighboring solution (flip one bit)
        neighbor = current_solution[:]
        bit_to_flip = random.randint(0, n - 1)
        neighbor[bit_to_flip] = not neighbor[bit_to_flip]

        # Evaluate the new solution
        neighbor_value = knapsack_value(neighbor)

        # Calculate the change in value
        delta_value = neighbor_value - current_value

        # Determine if we should accept the new solution
        if delta_value > 0 or random.random() < math.exp(delta_value / temperature):
            current_solution = neighbor[:]
            current_value = neighbor_value

            # Check if the new solution is the best we've found so far
            if current_value > best_value:
                best_solution = current_solution[:]
                best_value = current_value
                timestamp = time.time() - start
                solution_trace.append((timestamp, best_value))

        # Decrease the temperature
        temperature -= cooling_rate

    best_solution_indices = [i for i, selected in enumerate(best_solution) if selected]


    with open('solution_trace.csv', 'w') as f:
        for timestamp, value in solution_trace:
            f.write(f"{timestamp:.5f}, {value}\n")
    return best_value, best_solution_indices