import argparse
import copy
import random


def solve(num_wizards, num_constraints, wizards, constraints):
    constraints_copy = copy.copy(constraints)
    random_num = random.randint(0, len(constraints_copy)-1)
    current_clause = constraints_copy[random_num]
    subproblems = possible_orders(current_clause)
    for subproblem in subproblems:
        #print("current_subproblem = " + str(subproblem))
        current_three_clauses = find_three_clauses(subproblem, constraints_copy) # Changed this to up here so we don't calculate it as much. Clauses that include 3 wizards in common
        result = solver(subproblem, constraints_copy)
        if result:
            return result
    return False


def solver(subproblem, constraints_copy): #recursive function that returns the subproblem that satisfies constraints, False if none
    # for constraint in constraints_copy: (Don't think we need this outer loop. We're only looking at the three_clauses here, not all constraints)
    three_clauses = find_three_clauses(subproblem, constraints_copy)
    for three_clause in three_clauses:
        if violates_clause(subproblem, three_clause):
            return False                                    # stop pursuing this subproblem
    if len(subproblem) == num_wizards:
        return subproblem
    two_common = True
    constraint = find_clause(subproblem, constraints_copy, 2) # first clause where 2 seen wizards in common
    left_index, right_index = -1, -1
    if constraint == []:
        two_common = False
        constraint = find_clause_one_in_common(subproblem, constraints_copy) # just in case we can't find a cause with 2 in common
        if not constraint:
            constraint = find_clause_with_zero(subproblem, constraints_copy)
        curr_wiz = None
        if constraint:
            for wiz in constraint:
                if wiz not in subproblem:
                    curr_wiz = wiz
                if wiz in subproblem:
                    left_index = subproblem.index(wiz)

            


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
        for index in range(len(subproblem)):
            if not (index < right_index and index > left_index) or (index > right_index and index < left_index):
                new_subproblem = list(subproblem)
                new_subproblem.insert(index, curr_wiz)
                new_subproblems.append(new_subproblem)  # adds new subproblem to list of subproblems
    else: #case where constraint only has 1 wizard in common w subproblem
        for index in range(len(subproblem)):
            new_subproblem = list(subproblem)
            new_subproblem.insert(index, curr_wiz)
            new_subproblems.append(new_subproblem)
    for new_subproblem in new_subproblems:          # recursively searches down branches of each subproblem
        #print("curent new subproblem = " + str(new_subproblem))
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

def find_three_clauses(subproblem, clauses):
    return_clauses = []
    #print(subproblem)
    for clause in clauses:
        add_curr_clause = True
        for i in range(3):
            if clause[i] not in subproblem:
                add_curr_clause = False
        if add_curr_clause:
            return_clauses.append(clause)
    return return_clauses


def find_clause(subproblem, clauses, num):  # finds clause with a specific number in common
    for clause in clauses:
        if clause_test(subproblem, clause) == num:
            return clause
    return []

def find_clause_one_in_common(subproblem, clauses):
    for clause in clauses:
        common_count = 0
        for i in range(len(clause)):
            if clause[i] in subproblem:
                common_count += 1
        if common_count == 1:
            return clause
    return []
    

def find_clause_with_zero(subproblem, clauses):
    for clause in clauses:
        no_common = True
        for i in range(len(clause)):
            if clause[i] in subproblem:
                no_common = False
        if no_common:
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
    parser.add_argument("output_file", type=str, help = "___.out")
    args = parser.parse_args()

    num_wizards, num_constraints, wizards, constraints = read_input(args.input_file)
    solution = solve(num_wizards, num_constraints, wizards, constraints)
    write_output(args.output_file, solution)
    print(solution)

# just commented a few things out in the main function so I could run 'python3 170_project_solver.py input_test.in' in terminal.



