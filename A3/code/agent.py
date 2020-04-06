"""
An AI player for Othello. 
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

caching_table = {}

def eprint(*args, **kwargs): #you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)
    
# Method to compute utility value of terminal state
def compute_utility(board, color):
    score_p1, score_p2 = get_score(board)
    if color == 1:
        return score_p1 - score_p2
    else: 
        return score_p2 - score_p1


# Better heuristic value of board
def compute_heuristic(board, color): #not implemented, optional
    #IMPLEMENT
    return 0 #change this!

############ MINIMAX ###############################
def minimax_min_node(board, color, limit, caching = 0):
    if color == 1:
        oppo = 2 # light
    else:
        oppo = 1 # dark

    moves = get_possible_moves(board, oppo)

    if len(moves) == 0 or limit == 0: # no moves or out of limit
        return (None, compute_utility(board, color))

    minimax_min = float('inf')
    best_move = None

    for move in moves:
        next_state = play_move(board, oppo, move[0], move[1])


        if caching == 0:
            child = minimax_max_node(next_state, color, limit - 1, caching)
        elif next_state in caching_table:
            child = caching_table[next_state]
        else:
            child = minimax_max_node(next_state, color, limit - 1, caching)
            caching_table[next_state] = child

        if child[1] < minimax_min:
            minimax_min = child[1]
            best_move = move

    return (best_move, minimax_min)

def minimax_max_node(board, color, limit, caching = 0): #returns highest possible utility

    moves = get_possible_moves(board, color)

    if len(moves) == 0 or limit == 0: # no moves or out of limit
        return (None, compute_utility(board, color))

    minimax_max = -float('inf')
    best_move = None

    for move in moves:
        next_state = play_move(board, color, move[0], move[1])

        if caching == 0:
            child = minimax_min_node(next_state, color, limit - 1, caching)
        elif next_state in caching_table:
            child = caching_table[next_state]
        else:
            child = minimax_min_node(next_state, color, limit - 1, caching)
            caching_table[next_state] = child


        if child[1] > minimax_max:
            minimax_max = child[1]
            best_move = move

    return (best_move, minimax_max)

def select_move_minimax(board, color, limit, caching = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    """

    move = minimax_max_node(board, color, limit, caching)[0]
    return move

############ ALPHA-BETA PRUNING #####################
def alphabeta_min_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    if color == 1:
        oppo = 2 # light
    else:
        oppo = 1 # dark

    moves = get_possible_moves(board, oppo)

    if len(moves) == 0 or limit == 0:
        return (None, compute_utility(board, color))

    min_uti = float('inf')
    best_move = None

    if ordering != 0:
        moves.sort(key = lambda m: compute_utility(play_move(board, oppo, m[0], m[1]), color))

    for move in moves:
        next_state = play_move(board, oppo, move[0], move[1])

        if caching == 0:
            child = alphabeta_max_node(next_state, color, alpha, beta, limit - 1, caching, ordering)
        elif next_state in caching_table:
            child = caching_table[next_state]
        else:
            child = alphabeta_max_node(next_state, color, alpha, beta, limit - 1, caching, ordering)
            caching_table[next_state] = child

        if child[1] < min_uti:
            min_uti = child[1]
            best_move = move
        
        if beta > min_uti:
            beta = min_uti
        if beta <= alpha:
            return (best_move, min_uti)

    return (best_move, min_uti)

def alphabeta_max_node(board, color, alpha, beta, limit, caching = 0, ordering = 0):
    moves = get_possible_moves(board, color)

    if len(moves) == 0 or limit == 0:
        return (None, compute_utility(board, color))

    max_uti = -float('inf')
    best_move = None

    if ordering != 0:
        moves.sort(key = lambda m: compute_utility(play_move(board, color, m[0], m[1]), color))

    for move in moves:
        next_state = play_move(board, color, move[0], move[1])

        if caching == 0:
            child = alphabeta_min_node(next_state, color, alpha, beta, limit - 1, caching, ordering)
        elif next_state in caching_table:
            child = caching_table[next_state]
        else:
            child = alphabeta_min_node(next_state, color, alpha, beta, limit - 1, caching, ordering)
            caching_table[next_state] = child

        if child[1] > max_uti:
            max_uti = child[1]
            best_move = move
        
        if alpha < max_uti:
            alpha = max_uti
        if beta <= alpha:
            return (best_move, max_uti)


    return (best_move, max_uti)

def select_move_alphabeta(board, color, limit, caching = 0, ordering = 0):
    """
    Given a board and a player color, decide on a move. 
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.  

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic 
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.    
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations. 
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations. 
    """
    alpha = -float('inf')
    beta = float('inf')
    move = alphabeta_max_node(board, color, alpha, beta, limit, caching, ordering)[0]
    return move

####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Othello AI") # First line is the name of this AI
    arguments = input().split(",")
    
    color = int(arguments[0]) #Player color: 1 for dark (goes first), 2 for light. 
    limit = int(arguments[1]) #Depth limit
    minimax = int(arguments[2]) #Minimax or alpha beta
    caching = int(arguments[3]) #Caching 
    ordering = int(arguments[4]) #Node-ordering (for alpha-beta only)

    if (minimax == 1): eprint("Running MINIMAX")
    else: eprint("Running ALPHA-BETA")

    if (caching == 1): eprint("State Caching is ON")
    else: eprint("State Caching is OFF")

    if (ordering == 1): eprint("Node Ordering is ON")
    else: eprint("Node Ordering is OFF")

    if (limit == -1): eprint("Depth Limit is OFF")
    else: eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1): eprint("Node Ordering should have no impact on Minimax")

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1): #run this if the minimax flag is given
                movei, movej = select_move_minimax(board, color, limit, caching)
            else: #else run alphabeta
                movei, movej = select_move_alphabeta(board, color, limit, caching, ordering)
            
            print("{} {}".format(movei, movej))

if __name__ == "__main__":
    run_ai()
