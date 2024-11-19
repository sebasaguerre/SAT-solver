import numpy as np
import os
import sys
from pathlib import Path

# global var -> folder where script is located
folder_path = os.path.dirname(os.path.abspath(__file__))

def read_sudoku_rules(rules):
    """Read sudoku rules and encode it as a list of set clauses"""
    rule_set = []
    file = os.path.join(folder_path, rules)
    with open(file, "r") as file:
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
    file = os.path.join(folder_path, doc)
    with open(file, "r") as file:
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
            if elem.isdigit():
                problem_constrains.append(f"{ridx + 1}{nidx +1}{elem}")
            else:
                problem_vars[f"{ridx + 1}{nidx +1}"] = [None

    return problem_constrains, problem_vars

# get final constrains for problem
def final_constrains(p_constrains, rules):
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

########### DPLL #############

def remove_clauses(lit, rep):
    return [clause for clause in rep if lit not in clause]

def remove_lits(lit, rep):
    return [clause.discard(lit) for clause in rep]


def set_var_value(lits, rep, vars, sudoku_num):
    """Set variable value for pure literals or unit clauses"""
    for lit in lits:
        val_idx = int(lit[-1]) - 1
        if int(lit) > 0:
            vars[lit][val_idx] = True
            #remove all clause that contain lit
            rep = remove_clauses(lit, rep)
            
        else:
            vars[np.abs(lit)][val_idx] = False
            # remove lit from all caluses 
            rep = remove_lits(lit, rep)
    
    dpll(rep, vars, sudoku_num)

def check_unit_clause(rep, vars, sudoku_num):
    """Check for unit clauses in the problem clasuse"""
    unit_clauses = []
    
    # extract unit clauses 
    for clause in rep:
        if len(clause) == 1:
            unit_clauses.append(clause)
    for unit in unit_clauses:
        rep.remove(unit)

    set_var_value(unit_clauses, rep, vars, sudoku_num)
    
    return rep, vars
    
def check_pure_lit(rep, vars, sudoku_num):
    """Check for pure literals in the clauses"""

    pure_lits = []
    set_lit = set()
    # get all literals in formula 
    for clause in rep:
        set_lit.update(clause)
    
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
            pure_lits.append(lit)
            # remove pure literal from clauses
            for clause in rep:
                clause.discard(lit) 
    
    set_var_value(pure_lits, rep, vars, sudoku_num)

def check_empty(rep, sudoku_num):
    for clause in rep:
        if len(clause) == 0: 
            with open("sudoku_results.txt", "a+") as file:
                file.write(f"UNSAT sudoku# {sudoku_num}")
            return True

    return False 

def return_model(vars, sudoku_num):
    model = {}
    for key in vars.keys():
        model[key] = vars[key].index(True) + 1

    with open("sudoku_results.txt", "a+") as file:
        file.write(f"SAT sudoku# {sudoku_num} model {model}")
    return 0

def split(rep, vars, sudoku_num):
    for key in vars.keys():
        # if any(value is None for value in vars[key]):
            for idx in range(len(vars[key])):
                vars2 = vars.copy()
                rep2 = rep.copy()
                lit = key + str(idx +1)
                # set lit to true 
                vars[key][idx] = True
                # remove clauses with literal and remove the negated literal from clauses 
                remove_clauses(lit, rep)
                remove_lits("-" + lit, rep)

                if dpll(rep, vars, sudoku_num) == True:
                    return_model(vars, sudoku_num) 
                else:
                    vars[key][idx] = False
                    # remove clasuses with tliteral and remove the non negatred literal from clauses 
                    remove_lits(lit, rep)
                    remove_clauses("-" + lit, rep)

                    if dpll(rep2, vars2, sudoku_num) == True:
                        return_model(vars, sudoku_num)
    
            
def dpll(rep, vars, sudoku_num):
    if len(rep) == 0:
        return_model(vars, sudoku_num)
        return True
    if check_empty(rep, sudoku_num):
        return False
    rep = check_unit_clause(rep, vars, sudoku_num)
    rep = check_pure_lit(rep, vars, sudoku_num)
    print("*"*100)
    if split(rep, vars, sudoku_num): return True
    else: 
        return False

# representation problem and solve
def represent_solve(sudoku, sudoku_rules, sudoku_num):
    sudoku_num = sudoku_num
    n_rows = int(np.sqrt(len(sudoku)))
    rows = get_rows(sudoku, n_rows)
    hard_constrains, vars  = get_constrains(rows)
    # get final representation for problem at hand 
    problem_constrains = final_constrains(hard_constrains, sudoku_rules)
    # solve sudoku
    dpll(problem_constrains, vars, sudoku_num)

def solve_problems(file, rule_file):
    sudokus = read(file)
    sudoku_rules = read_sudoku_rules(rule_file)
    print("*"*20 + "Read Successfully" + "*"*20)

    for idx, sudoku in enumerate(sudokus):
        represent_solve(sudoku, sudoku_rules, idx + 1)

def main():
    test = input("Test? ")
    if test.lower() == "y":
        file = "4x4.txt"
        rule_file = "sudoku-rules-4x4.txt"
    else:
        file = input("Give sudoku file: ")
        rule_file = input("Give sudoku rule-file: ")
    solve_problems(file, rule_file)

if "__main__":
    main()