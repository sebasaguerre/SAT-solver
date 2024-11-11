import numpy as np

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

# representation
def represent(sudoku):
    n_rows = np.sqrt(len(sudoku))
    rows = get_rows(sudoku, n_rows)
    problem_constrains = get_constrains(rows)


