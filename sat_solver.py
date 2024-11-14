import numpy as np

def read_sudoku_rules(rules):
    """Read sudoku rules and encode it as a list of set clauses"""
    rule_set = []
    with open(rules, "r") as file:
        for line in file:
            if line.startswith("p"):
                continue 
            else:
                clause_lit = line.strip().split()
                rule_set.append({rule for rule in clause_lit if rule != "0"})

    return rule_set

# read sudokus
def read(doc):
    """Read the sudoku to be solved """
    sudokus = []
    with open(doc, "r") as file:
        for line in file:
            sudokus.append(line.strip())
    
    return sudokus

# extract the rows of a sudoku
def get_rows(sudoku, n):
    """Extract the rows of the sudoku we aim to solve """
    rows = []
    i = 0
    while i < len(sudoku):
        rows.append(sudoku[i:i+n])
        i += n

    return rows

# get problem constrains 
def get_constrains(rows):
    """
    Extract the sudoku specific constrains and variables 
    and then turn them into a set  

    Return:
        proble_constrains = list[literals]
        problem_vars = dic{row_entry = [-1] * number_possible_values}
            * here -1 means unassigned 
    """

    problem_constrains = []
    problem_vars = {}
    for ridx, row in enumerate(rows):
        for nidx, elem in enumerate(row):
            if elem.isnum():
                problem_constrains.append(f"{ridx + 1}{nidx +1}{elem}")
            else:
                problem_vars[f"{ridx + 1}{nidx +1}"] = [None] * len(row) 
    
    return set(problem_constrains), problem_vars

# get final constrains for problem
def final_constrains(p_constrains, rules):
    """
    Extract final constrains of sudoku puzzle by joining
    the problem specific constrains and the rules
    """
    problem_rules = rules.copy()
    for pc in p_constrains:
        for rule in rules:
            if pc in rule:
                problem_rules.remove(rule)

    return problem_rules

########### DPLL #############

def set_var_value(lit, vars):
    """Set variable value for pure literals or unit clauses"""
    val_idx = int(lit[-1]) - 1
    if int(lit) > 0:
        vars[lit][val_idx] = True
    else:
        vars[np.abs(lit)][val_idx] = False

def check_unit_clause(rep, vars):
    """Check for unit clauses in the problem clasuse"""
    for clause in rep:

        if len(clause) == 1:
            lit = clause.pop()
            # set variable to desired value based on literal sign 
            set_var_value(lit, vars)
            rep.remove(clause)
    
    return rep, vars
    
def check_pure_lit(rep, vars):
    """Check for pure literals in the clauses"""

    set_lit = set()
    # get all literals in formula 
    for clause in rep:
        set_lit.union(clause)
    
    # find pure literals 
    for lit in set_lit:
        pure = False
        for clause in rep:
            if (int(lit) * -1) in clause:
                pure  = False 
                break 
            else:
                pure = True 
        
        # if pure literal set value and remove from clause
        if pure == True: 
            set_var_value(lit, vars)
            # remove pure literal from clauses
            for clause in rep:
                clause.discard(lit)
        

def dpll(rep):
    if len(rep) == 0:
        print()
    

# representation problem and solve
def represent_solve(sudoku, sudoku_rules):
    n_rows = np.sqrt(len(sudoku))
    rows = get_rows(sudoku, n_rows)
    hard_constrains = get_constrains(rows)
    # get final representation for problem at hand 
    problem_constrains = final_constrains(hard_constrains, sudoku_rules)
    
    # solve sudoku
    dpll(problem_constrains)


    

