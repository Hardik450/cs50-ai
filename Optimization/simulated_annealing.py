import random
import math

def value(x):
    return x * math.sin(x)

def get_neighbors(x, step=0.4):
    return [
        max(0, x - step),
        min(10, x + step)
    ]

def simulated_annealing(state, get_neighbors, value, initial_temperature = 100, cooling_rate=0.95, min_temp=0.01):
    current = state
    temperature = initial_temperature
    while temperature > min_temp:
        neighbors = get_neighbors(current)
        neighbor = random.choice(neighbors)
        delta = value(neighbor) - value(current)

        if delta >= 0:
            current = neighbor
        else:
            acceptance_probability = math.exp(delta/temperature)
            if random.random() < acceptance_probability:
                current = neighbor
        temperature *= cooling_rate
    return current

start = random.uniform(0, 10)
result = simulated_annealing(start, get_neighbors, value)

print("Start x:", start)
print("Final x:", result)
print("Maximum value:", value(result))
