import math as m 
import numpy as np

# Read Sudoku rules
def read_sudoku_rules(rules):
    rule_set = []
    with open(rules, "r") as file:
        for line in file:
            if line.startswith("p"):
                continue 
            else:
                clause_lit = line.strip().split()
                rule_set.append({rule for rule in clause_lit if rule != "0"})

    return rule_set

# Read Sudokus
def read(doc):
    sudokus = []
    with open(doc, "r") as file:
        for line in file:
            sudokus.append(line.strip())

    return sudokus

# Extract the rows of a Sudoku
def get_rows(sudoku, n):
    return [sudoku[i:i+n] for i in range(0, len(sudoku), n)]


def get_constraints(rows):
    problem_constrains = []
    problem_vars = {}
    for ridx, row in enumerate(rows):
        for nidx, elem in enumerate(row):
            if elem.isdigit():
                problem_constrains.append(f"{ridx + 1}{nidx +1}{elem}")

    return problem_constrains, problem_vars

def final_constraints(p_constrains, rules):
    """
    Extract final constrains of sudoku puzzle by joining
    the problem specific constrains and the rules
    """
    problem_rules = rules.copy()
    # iterate over constrains in probelm constrains 
    for pc in p_constrains:
        for rule in rules:
            if pc in rule:
                problem_rules.remove(rule)

    return problem_rules

# Representation
def sudoku_represent(sudoku, sudoku_rules):
    n_rows = int(np.sqrt(len(sudoku)))
    rows = get_rows(sudoku, n_rows)
    hard_constraints = get_constraints(rows)
    return final_constraints(hard_constraints, sudoku_rules)

def find_unit_cluase(rep):
    # find the clauses which are unit clauses
    return [next(iter(rep)) for clause in rep if len(clause) == 1]

def fin_pure_literals(rep):
    # get all literals in problem 
    literals = {literal for clause in rep for literal in clause}
    # return all pute literals 
    return [literal for literal in literals if str((-1)*int(literal)) not in literals]

def reduce_rep(rep, vars):
    new_rep = []
    for clause in rep:
        new_clause = set()
        for literal in clause:
            if vars.get(literal.strip("-")) != str((-1)*int(literal)):
                new_clause.update(literal)
        for literal in clause:
            if vars.get(literal.lstrip("-")) == False:
                
        


def dpll(rep, variables):
    rep = rep.copy()
    variables = variables.copy()