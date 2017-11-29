import argparse
import copy
import random

sol = []
def solve(num_wizards, num_constraints, wizards, constraints):
    constraints_copy = copy.copy(constraints)
    # constraints_by_key = {}
    # for i in range(len(constraints)):
    #     already_added = False
    #     for j in range(3):
    #         if constraints[i][j] in constraints_by_key:
    #             if (not already_added):
    #                 constraints_by_key[constraints[i][j]] += constraints[i]
    #                 already_added = True
    #         else:
    #             constraints_by_key[constraints[i][j]] = constraints[i]
    #             already_added = True
    random_num = random.randint(0, len(constraints_copy)-1)
    current_clause = constraints_copy[random_num]
    subproblems = possible_orders(current_clause)
    for subproblem in subproblems:
        current_three_clauses = find_three_clauses(subproblem, constraints_copy) # Changed this to up here so we don't calculate it as much. Clauses that include 3 wizards in common
        result = solver(subproblem, constraints_copy, current_three_clauses)
        if result:
            sol = result
            return result
    return False


def solver(subproblem, constraints_copy): #recursive function that returns the subproblem that satisfies constraints, False if none
    # for constraint in constraints_copy: (Don't think we need this outer loop. We're only looking at the three_clauses here, not all constraints)
    three_clauses = find_three_clauses(subproblem, constraints_copy)
    for three_clause in three_clauses:
        if violates_clause(subproblem, three_clause):
            return False                                    # stop pursuing this subproblem
    
    two_common = True
    constraint = find_clause(subproblem, constraints_copy, 2) # first clause where 2 seen wizards in common
    left_index, right_index = -1, -1
    if constraint == []:
        two_common = False
        constraint = find_clause(subproblem, constraints_copy, 1) # just in case we can't find a cause with 2 in common
        curr_wiz = None
        for wiz in constraint:
            if wiz not in subproblem:
                curr_wiz = wiz
                break
        left_index = subproblem.index(curr_wiz)
    else:
        curr_wiz = constraint[2] # generate subproblems, use a constraint with 3rd wizard that's not in current subproblem
        # find the indices of the interval (1st and 2nd wizards in constraint)
        if subproblem.index(constraint[0]) < subproblem.index(constraint[1]):
            left_index = subproblem.index(constraint[0])
            right_index = subproblem.index(constraint[1])
        else:
            left_index = subproblem.index(constraint[1])
            right_index = subproblem.index(constraint[0])

    new_subproblems = []
    if two_common: #constraint has 2 wizards in common with subproblem
        index = 0
        while index < range(len(subproblem)):       # find possible placements for this wizard, which is anywhere not in the interval given by constraint
            new_subproblem = list(subproblem)
            new_subproblem.insert(index, curr_wiz)
            new_subproblems.append(new_subproblem)  # adds new subproblem to list of subproblems
            if index + 1 > left_index:
                index = right_index + 1
            else:
                index += 1
    else: #case where constraint only has 1 wizard in common w subproblem
        for index in range(len(subproblem)):
            if index != left_index:
                new_subproblem = list(subproblem)
                new_subproblem.insert(index, curr_wiz)
                new_subproblems.append(new_subproblem)

    for new_subproblem in new_subproblems:          # recursively searches down branches of each subproblem
        result = solver(new_subproblem, constraints_copy)
        if result:
            return result
    return False

def violates_clause(subproblem, clause): #returns true if a subproblem violates a given clause.
    w1 = subproblem.index(clause[0])
    w2 = subproblem.index(clause[1])
    w3 = subproblem.index(clause[2])
    return (w3 > w1 and w3 < w2) or (w3 > w2 and w3 < w1)


def possible_orders(clause):
    return [[clause[0], clause[1], clause[2]], 
            [clause[1], clause[0], clause[2]],
            [clause[2], clause[0], clause[1]],
            [clause[2], clause[1], clause[0]]]

def clause_test(subproblem, clause): # gives count: all wizards in common (3), first two in common, or [one... but where]
    result = 0
    ind = 4     # placeholder
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

def find_three_clauses(subproblem, clauses): # finds all clauses with 3 wizards in common
    three_clauses = []
    for clause in clauses:
        if clause_test(subproblem, clause) == 3:
            three_clauses += clause
    return three_clauses

def find_clause(subproblem, clauses, num):  # finds clause with a specific number in common
    for clause in clauses:
        if clause_test(subproblem, clause) == num:
            return clause
    return []




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


if __name__=="__main__":
    parser = argparse.ArgumentParser(description = "Constraint Solver.")
    parser.add_argument("input_file", type=str, help = "___.in")
    # parser.add_argument("output_file", type=str, help = "___.out")
    args = parser.parse_args()

    num_wizards, num_constraints, wizards, constraints = read_input(args.input_file)
    solution = solve(num_wizards, num_constraints, wizards, constraints)
    # write_output(args.output_file, solution)
    print(sol)

# just commented a few things out in the main function so I could run 'python3 170_project_solver.py input_test.in' in terminal.



