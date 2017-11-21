import argparse

def solve(num_wizards, num_constraints, wizards, constraints): 
	constraints_copy = constraints.copy()                   # copy of constraints since we'll be reducing
    order = []                                              # the working order to be returned
	constraints_by_key = {}									# maps wizards to the clauses they are in
	for i in range(constraints):
		already_added = False
			for j in range(3):
				if constraints[i][j] in constraints_by_key:
					if (!already_added):
						constraints_by_key[constraints[i][j]] += constraints[i]
						already_added = True
				else:
					constraints_by_key[constraints[i]] = constraints[i]
					already_added = True
    while constraints_copy:
		random_num = random.randint(0, len(constraints_copy)-1)
        current_clause = constraints_copy[random_num]
        subproblems = [[current_clause[0], current_clause[1], current_clause[2]],
            [current_clause[1], current_clause[0], current_clause[2]],
            [current_clause[2], current_clause[0], current_clause[1]],
            [current_clause[2], current_clause[1], current_clause[0]]]
		for subproblem in subproblems:
			result = solver(subproblem, constraints_by_key)
			if result != False:
				return result
		return False

def solver(subproblem, constraints_by_key): #recursive function that returns the subproblem that satisfies constraints, False if none
	for wizard in subproblem: #checking all constraints for each wizard present in the subproblem
		for constraint in constraints_copy:
			if all 3 wizards in constraint are in subproblem list:
				if constraint is not satisfied:  #don't explore this subproblem since it violates a constraint
					return False
				else:
					remove this constraint from constraints_copy
	generate constraint - heuristic: wizard that has least num of constraints? 
	curr_wiz = constraint[2] #generate subproblems, use a constraint with 3rd wizard that's not in current subproblem
	left_index, right_index = -1, -1 	#find the indices of the interval (1st and 2nd wizards in constraint)
	if subproblem.index(constraint[0]) < subproblem.index(constraint[1]):
		left_index = subproblem.index(constraint[0])
		right_index = subproblem.index(constraint[1])
	else:
		left_index = subproblem.index(constraint[1])
		right_index = subproblem.index(constraint[0])
	new_subproblems = []
	index = 0
	while index < len(range(subproblem)):		#find possible placements for this wizard, which is anywhere not in the interval given by constraint
		new_subproblem = list(subproblem)
		new_subproblem.insert(index, curr_wiz)
		subproblems.append(new_subproblem)	#adds new subproblem to list of subproblems
		if index + 1 > left_index:
			index = right_index + 1
		else:
			index += 1
	for new_subproblem in new_subproblems: 			#recursively searches down branches of each subproblem
		result = solver(new_subproblem, constraints_by_key)
		if result != False
			return result
	return False


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


