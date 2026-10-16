class CSP:
    def __init__(self, variables, domains, neighbors, constraints):
        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints

def backtracking_search(csp):
    return backtrack({}, csp)

def backtrack(assignment, csp):
    if len(assignment) == len(csp.variables):
        return assignment
    
    var = select_unassigned_variable(assignment, csp)

    for value in csp.domains[var]:
        if consistent(var, value, assignment, csp):
            assignment[var] = value
            result = backtrack(assignment, csp)
            if result is not None:
                return result
            del assignment[var]
    return None

def select_unassigned_variable(assignment, csp):
    for var in csp.variables:
        if var not in assignment:
            return var
    return None

def consistent(var, value, assignment, csp):
    for neighbor in csp.neighbors[var]:
        if neighbor in assignment:
            if not csp.constraints(value, assignment[neighbor]):
                return False
    if not count_slot(assignment, value):
        return False
    return True

variables = ["Math", "Physics", "Chemistry", "Biology", "English", "History", "Geography", "Political Science", "Computer Science", "Physical Education", "Economics", "Art", "Music", "Drama", "Philosophy", "Sociology", "Psychology", "Anthropology", "Statistics", "Environmental Science"]
value = ["Monday1", "Tuesday1", "Wednesday1", "Thursday1", "Friday1", "Monday2", "Tuesday2", "Wednesday2", "Thursday2", "Friday2"]
domains = {key : value for key in variables}
neighbors = {}
for i, var in enumerate(variables):
    neighbors[var] = []
    if i > 0:
        neighbors[var].append(variables[i-1])
    if i < len(variables) - 1:
        neighbors[var].append(variables[i+1])
    if i == 0:
        neighbors[var].append(variables[-1])
    elif i == len(variables) - 1:
        neighbors[var].append(variables[0])

def different_timeslot(x, y):
    return x != y 

def count_slot(x, y):
    count = 0
    for var in x:
        if x[var] == y:
            count += 1
    if count >= 2:
        return False
    return True

csp = CSP(variables, domains, neighbors, different_timeslot)
result = backtracking_search(csp)
print("Schedule Assignment:", result)