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

# def futoshiki_csp1(n):
#     '''
#     Return a csp model for futoshiki with size n and row and column constraints.
#     '''
#     dom = []
#     i = 0
#     for i in range(n): # domain
#         dom.append(i+1)

#     vars = []
#     for i in dom: # variables i - col, j - row
#         for j in dom:
#             vars.append(Variable('{},{}'.format(i, j), dom))
    
#     cons = []
#     #not equal constraint
#     for var in vars:
#         v_col = int(var.name[0]) - 1
#         v_row = int(var.name[2]) - 1
#         for col in range(v_col + 1, n): # constraints for row
#             con = Constraint("C(({},{}), ({},{}))".format(v_col + 1, v_row + 1, col + 1, v_row + 1),[vars[v_col + n * v_row], vars[col + n * v_row]])
#             sat_tuples = []
#             for t in itertools.product(dom, dom):
#                 if t[0] != t[1]:
#                     sat_tuples.append(t)
#             con.add_satisfying_tuples(sat_tuples)
#             cons.append(con)

#         for row in range(v_row + 1, n): # constraints for col
#             con = Constraint("C(({},{}), ({},{}))".format(v_col + 1, v_row + 1, v_col + 1, row + 1),[vars[v_col + n * v_row], vars[v_col + n * row]])
#             sat_tuples = []
#             for t in itertools.product(dom, dom):
#                 if t[0] != t[1]:
#                     sat_tuples.append(t)
#             con.add_satisfying_tuples(sat_tuples)
#             cons.append(con)

#     csp = CSP("{}-futoshiki".format(n), vars)
#     for c in cons:
#         csp.add_constraint(c)
#     return csp


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
                row.append(Variable('{},{}'.format(i, int(j/2)), [futo_grid[i][j]]))
            else:
                row.append(Variable('{},{}'.format(i, int(j/2)), dom))
        V.append(row)

    V_1d = []
    for i in V:
        V_1d.extend(i)

    
    cons = []
    #not equal constraint
    for i in range(n):
        for j in range(n): 
            for col in range(j + 1, n):
                con = Constraint("C(({},{}), ({},{}))".format(i, j, i, col),[V[i][j], V[i][col]])
                sat_tuples = []
                for t in itertools.product(dom, dom):
                    if t[0] != t[1]:
                        sat_tuples.append(t)
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)

            for row in range(i + 1, n):
                con = Constraint("C(({},{}), ({},{}))".format(i, j, row, j),[V[i][j], V[row][j]])
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
                con = Constraint("C(({},{}), ({},{}))".format(row_num, col_num, \
                    row_num, col_num + 1),[V[row_num][col_num], V[row_num][col_num+1]])
                sat_tuples = []
                for t in itertools.product(dom, dom):
                    if t[0] > t[1]:
                        sat_tuples.append(t)
                con.add_satisfying_tuples(sat_tuples)
                cons.append(con)

            elif row[i] == '<':
                con = Constraint("C(({},{}), ({},{}))".format(row_num, col_num, \
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

# board_1 = [[1,'<',0,'.',0],[0,'.',0,'.',2],[2,'.',0,'>',0]]
# csp, v = futoshiki_csp_model_1(board_1)

# solver = BT(csp)
# solver.bt_search(prop_BT)
# # for i in range(len(v)):
# #     for j in range(len(v)):
# #         print(v[i][j].get_assigned_value())




def futoshiki_csp_model_2(futo_grid):
    ##IMPLEMENT 
    
    return
