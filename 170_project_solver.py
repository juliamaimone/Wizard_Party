import argparse

def solve(num_wizards, num_constraints, wizards, constraints):
    constraints_copy = constraints.copy()
    order = []
    constraints_by_key = {}
    for i in range(constraints):
        already_added = False
        for j in range(3):
            if constraints[i][j] in constraints_by_key:
                if (not already_added):
                    constraints_by_key[constraints[i][j]] += constraints[i]
                    already_added = True
            else:
                constraints_by_key[constraints[i]] = constraints[i]
                already_added = True
    while constraints_copy:
        random_num = random.randint(0, len(constraints_copy)-1)
        current_clause = constraints_copy[random_num]
        subproblems = possible_orders(current_clause)
        for subproblem in subproblems:
            result = solver(subproblem, constraints_copy)
            if result:
                return result
        return False

def solver(subproblem, constraints_copy): #recursive function that returns the subproblem that satisfies constraints, False if none
    for wizard in subproblem: #checking all constraints for each wizard present in the subproblem
        for constraint in constraints_copy:
            three_clauses = find_three_clauses(subproblem, constraints_copy) #clauses that include 3 wizards in common
            for three_clause in three_clauses:
                if subproblem not in possible_orders(constraint):  #don't explore this subproblem since it violates a constraint
                    return False
                else:
                    del constraints_copy[constraints_copy.index(constraint)]
    constraint = find_clause(subproblem, constraints_copy, 2) #first clause where 2 seen wizards in common
    curr_wiz = constraint[2] #generate subproblems, use a constraint with 3rd wizard that's not in current subproblem
    left_index, right_index = -1, -1    #find the indices of the interval (1st and 2nd wizards in constraint)
    if subproblem.index(constraint[0]) < subproblem.index(constraint[1]):
        left_index = subproblem.index(constraint[0])
        right_index = subproblem.index(constraint[1])
    else:
        left_index = subproblem.index(constraint[1])
        right_index = subproblem.index(constraint[0])
    new_subproblems = []
    index = 0
    while index < len(range(subproblem)):       #find possible placements for this wizard, which is anywhere not in the interval given by constraint
        new_subproblem = list(subproblem)
        new_subproblem.insert(index, curr_wiz)
        subproblems.append(new_subproblem)  #adds new subproblem to list of subproblems
        if index + 1 > left_index:
            index = right_index + 1
        else:
            index += 1
    for new_subproblem in new_subproblems:          #recursively searches down branches of each subproblem
        result = solver(new_subproblem, constraints_by_key)
        if result:
            return result
    return False

def possible_orders(current_clause):
    return [[current_clause[0], current_clause[1], current_clause[2]], 
            [current_clause[1], current_clause[0], current_clause[2]],
            [current_clause[2], current_clause[0], current_clause[1]],
            [current_clause[2], current_clause[1], current_clause[0]]]

def clause_test(subproblem, clause):
    result = 0
    ind = 4
    if clause[2] in list(subproblem) and clause[0] in list(subproblem) and clause[1] in list(subproblem):
        return 3
    for wizard in list(subproblem):
        if clause[0] == wizard and ind != 0:
            ind = 0
            result += 1
        elif clause[1] == wizard and ind != 1:
            ind = 1
            result += 1
    return result

def find_three_clauses(subproblem, clauses):
    three_clauses = []
    for clause in clauses:
        if clause_test(subproblem, clause) == 3:
            three_clauses += clause
    return three_clauses

def find_clause(subproblem, clauses, num):
    for clause in clauses:
        if clause_test(subproblem, clause) == num:
            return clause

def read_input(filename):
    with open(filename) as f:
        num_wizards = int(f.readline())
        num_constraints = int(f.readline())
        constraints = []
        wizards = set()
        for _ in range(num_constraints):
            c = f.readline().split()
            constraints.append(c)
            for w in c:
                wizards.add(w)
                
    wizards = list(wizards)
    return num_wizards, num_constraints, wizards, constraints

def write_output(filename, solution):
    with open(filename, "w") as f:
        for wizard in solution:
            f.write("{0} ".format(wizard))

""""

if __name__=="__main__":
    parser = argparse.ArgumentParser(description = "Constraint Solver.")
    parser.add_argument("input_file", type=str, help = "___.in")
    parser.add_argument("output_file", type=str, help = "___.out")
    args = parser.parse_args()

    num_wizards, num_constraints, wizards, constraints = read_input(args.input_file)
    solution = solve(num_wizards, num_constraints, wizards, constraints)
    write_output(args.output_file, solution)

"""


