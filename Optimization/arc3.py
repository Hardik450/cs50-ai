class CSP:
    def __init__(self, variables, domains, neighbors, constraints):
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints

from collections import deque

def AC3(csp):
    queue = deque()

    for X in csp.variables:
        for Y in csp.neighbors[X]:
            queue.append((X,Y))
    
    while queue:
        x, y = queue.popleft()
        print(x, y)
        if REVISE(csp, x, y):
            if not csp.domains[x]:
                return False
            for z in csp.neighbors[x]:
                if z != y and (z, x) not in queue:
                    queue.append((z, x))
    
    return True

def REVISE(csp, x, y):
    revised = False
    to_remove = []
    for i in csp.domains[x][:]:
        if not any(csp.constraints(i, j) for j in csp.domains[y]):
            to_remove.append(i)
    for i in to_remove:
        csp.domains[x].remove(i)
        revised = True
    return revised

def less_than(x, y):
    return x < y

variables = ["X", "Y"]

domains = {
    "X": [1, 2, 3],
    "Y": [0, 2]
}

neighbors = {
    "X": ["Y"],
    "Y": ["X"]
}

csp = CSP(variables, domains, neighbors, less_than)
print(csp.domains)
result = AC3(csp)

print("Arc Consistent:", result)
print("Domains after AC-3:", csp.domains)
