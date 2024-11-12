import numpy as np

def read_sudoku_rules(rules):
    rule_set = []
    with open(rules, "r") as file:
        for line in file:
            if line.startswith("p"):
                continue 
            else:
                rule_set.append(line.strip())
    return rule_set

# read sudokus
def read(doc):
    sudokus = []
    with open(doc, "r") as file:
        for line in file:
            sudokus.append(line.strip())
    
    return sudokus

# extract the rows of a sudoku
def get_rows(sudoku, n):
    rows = []
    i = 0
    while i < len(sudoku):
        rows.append(sudoku[i:i+n])
        i += n
    return rows

# get problem constrains 
def get_constrains(rows):
    problem_constrains = []
    for ridx, row in enumerate(rows):
        for nidx, elem in enumerate(row):
            if elem.isnum():
                problem_constrains.append(f"{ridx + 1}{nidx +1}{elem}")
    
    return problem_constrains

# get final constrains for problem
def final_constrains(p_constrains, rules):
    problem_rules = rules.copy()
    for pc in p_constrains:
        for rule in rules:
            if pc in rule:
                problem_rules.remove(rule)
    return problem_rules

# representation
def sudoku_represent(sudoku, sudoku_rules):
    n_rows = np.sqrt(len(sudoku))
    rows = get_rows(sudoku, n_rows)
    hard_constrains = get_constrains(rows)
    problem_constrains = final_constrains(hard_constrains, sudoku_rules)

def dpll(rep):
    
    pass


    

