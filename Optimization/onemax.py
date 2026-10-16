import random
import math

N = 8

def generate_random_state():
    return [random.choice([0,1]) for _ in range(N)]

def value(state):
    return sum(state)

def get_neighbors(state):
    neighbors = []
    for i in range(len(state)):
        neighbor = state.copy()
        neighbor[i] = 1 - neighbor[i]
        neighbors.append(neighbor)
    return neighbors

def stochastic_hill_climbing(Initial_state, get_neighbors, value):
    current = Initial_state
    while True:
        neighbors = get_neighbors(current)
        better_neighbors = [
            state for state in neighbors
            if value(state) > value(current)
        ]

        if not better_neighbors:
            return current

        current = random.choice(better_neighbors)
    
def random_restart_hill_climbing(generate_random_state, get_neighbors, value, restarts = 10):
    best_state = None
    best_value = -math.inf

    for _ in range(restarts):
        state = generate_random_state()
        final = stochastic_hill_climbing(state, get_neighbors, value)

        if value(final) > best_value:
            best_state = final
            best_value = value(final)
    
    return best_state

if __name__ == "__main__":
    state = generate_random_state()
    final = stochastic_hill_climbing(state, get_neighbors, value)
    print("Final state (Stochastic Hill Climbing):", final)
    print("Value:", value(final))
    state_rr = random_restart_hill_climbing(generate_random_state, get_neighbors, value, restarts=20)
    print("Final state (Random Restart Hill Climbing):", state_rr)
    print("Value:", value(state_rr))