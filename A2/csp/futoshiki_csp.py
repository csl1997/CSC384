#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = futoshiki_csp_model_1(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the Futoshiki puzzle.

1. futoshiki_csp_model_1 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only 
      binary not-equal constraints for both the row and column constraints.

2. futoshiki_csp_model_2 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only n-ary 
      all-different constraints for both the row and column constraints. 

'''
from cspbase import *
import itertools
from propagators import *

def futoshiki_csp_model_1(futo_grid):
    ##IMPLEMENT
    n = len(futo_grid)

    dom = []
    i = 0
    for i in range(n): # domain
        dom.append(i+1)

    V = []
    for i in range(n): # variables i - row, j - col
        row = []
        for j in range(0, len(futo_grid[i]), 2):
            if futo_grid[i][j] != 0:
                row.append(Variable('Cell: {},{}'.format(i, int(j/2)), [futo_grid[i][j]]))
            else:
                row.append(Variable('Cell: {},{}'.format(i, int(j/2)), dom))
        V.append(row)

    V_1d = []
    for i in V:
        V_1d.extend(i)

    
    cons = []
    #not equal constraint
    for i in range(n):
        for j in range(n): 
            for col in range(j + 1, n):
                con = Constraint("C((Cell: {},{}), (Cell: {},{}))".format(i, j, i, col),[V[i][j], V[i][col]])
                sat_tuples = []
                for t in itertools.product(dom, dom):
                    if t[0] != t[1]:
                        sat_tuples.append(t)
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)

            for row in range(i + 1, n):
                con = Constraint("C((Cell: {},{}), (Cell: {},{}))".format(i, j, row, j),[V[i][j], V[row][j]])
                sat_tuples = []
                for t in itertools.product(dom, dom):
                    if t[0] != t[1]:
                        sat_tuples.append(t)
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)

    # binary inequality constraints
    row_num = 0
    for row in futo_grid:
        col_num = 0
        for i in range(1, len(row) , 2):
            # constraints
            if row[i] == '>':
                con = Constraint("C((Cell: {},{}), (Cell: {},{}))".format(row_num, col_num, \
                    row_num, col_num + 1),[V[row_num][col_num], V[row_num][col_num+1]])
                sat_tuples = []
                for t in itertools.product(dom, dom):
                    if t[0] > t[1]:
                        sat_tuples.append(t)
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)

            elif row[i] == '<':
                con = Constraint("C((Cell: {},{}), (Cell: {},{}))".format(row_num, col_num, \
                    row_num, col_num + 1), [V[row_num][col_num], V[row_num][col_num+1]])
                sat_tuples = []
                for t in itertools.product(dom, dom):
                    if t[0] < t[1]:
                        sat_tuples.append(t)
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)
            col_num += 1
        row_num += 1


    csp = CSP("{}-futoshiki".format(n), V_1d)
    for c in cons:
        csp.add_constraint(c)

    return csp, V



def futoshiki_csp_model_2(futo_grid):
    ##IMPLEMENT 
    n = len(futo_grid)

    dom = []
    i = 0
    for i in range(n): # domain
        dom.append(i+1)

    V = []
    for i in range(n): # variables i - row, j - col
        row = []
        for j in range(0, len(futo_grid[i]), 2):
            if futo_grid[i][j] != 0:
                row.append(Variable('Cell: {},{}'.format(i, int(j/2)), [futo_grid[i][j]]))
            else:
                row.append(Variable('Cell: {},{}'.format(i, int(j/2)), dom))
        V.append(row)

    V_1d = []
    for i in V:
        V_1d.extend(i)

    cons = []
    # n-ary all-different constraints
    for row in range(n):
        # row constraints
        con = Constraint("C(Row {})".format(row), V[row])
        sat_tuples = []
        for t in list(itertools.product(dom, repeat = n)):
            val_list = []
            for temp_v in t:
                if temp_v not in val_list:
                    val_list.append(temp_v)
            # no repeat in the tuple
            if len(val_list) == len(t):
                sat_tuples.append(t)
        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)

    # col constraints
    for col in range(n):
        col_list = []
        for row in range(n):
            col_list.append(V[row][col])
        con = Constraint("C(Col {})".format(col), col_list)
        sat_tuples = []
        for t in list(itertools.product(dom, repeat = n)):
            val_list = []
            for temp_v in t:
                if temp_v not in val_list:
                    val_list.append(temp_v)
            # no repeat in the tuple
            if len(val_list) == len(t):
                sat_tuples.append(t)
        con.add_satisfying_tuples(sat_tuples)
        cons.append(con)

    # binary inequality constraints
    row_num = 0
    for row in futo_grid:
        col_num = 0
        for i in range(1, len(row) , 2):
            # constraints
            if row[i] == '>':
                con = Constraint("C((Cell: {},{}), (Cell: {},{}))".format(row_num, col_num, \
                    row_num, col_num + 1),[V[row_num][col_num], V[row_num][col_num+1]])
                sat_tuples = []
                for t in itertools.product(dom, dom):
                    if t[0] > t[1]:
                        sat_tuples.append(t)
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)

            elif row[i] == '<':
                con = Constraint("C((Cell: {},{}), (Cell: {},{}))".format(row_num, col_num, \
                    row_num, col_num + 1), [V[row_num][col_num], V[row_num][col_num+1]])
                sat_tuples = []
                for t in itertools.product(dom, dom):
                    if t[0] < t[1]:
                        sat_tuples.append(t)
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)
            col_num += 1
        row_num += 1

    csp = CSP("{}-futoshiki".format(n), V_1d)
    for c in cons:
        csp.add_constraint(c)

    return csp, V


