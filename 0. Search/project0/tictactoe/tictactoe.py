"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    if terminal(board):
        # teminal state
        return None

    # how many X's and O's
    Xs = Os = 0
    for row in board:
        Xs += row.count(X)
        Os += row.count(O)

    # If game starts with X then
    # its X turn if number of X's are equals to O's
    return X if Xs == Os else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    if terminal(board):
        # teminal state
        return None

    actions = set()    
    for i in range(len(board)):
        for j in range(len(board[i])):
            # Available cell
            if board[i][j] == EMPTY:
                actions.add((i, j))

    return actions            


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    i, j = action
    # checks if is a valid action
    if i >= len(board) or j >= len(board) or board[i][j] is not EMPTY:
        raise Exception("Invalid action for the board")

    # copy the current board
    new_board = deepcopy(board)

    # make action
    new_board[i][j] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    # checks if there are mathing player horizontally, vertically, or diagonally
    for k in range(len(board)):
        for player in [X, O]:
            # horizontal
            if board[k][0] == board[k][1] == board[k][2] == player:
                return player
            # vertical    
            if board[0][k] == board[1][k] == board[2][k] == player:
                return player

    for player in [X, O]:
        # diagonal
        if board[0][0] == board[1][1] == board[2][2] == player:
            return player
        if board[0][2] == board[1][1] == board[2][0] == player:
            return player    
            
    # otherwise, there are no winner
    return None        


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # checks if there are winner or the board is full
    if winner(board) or not any([cell == EMPTY for row in board for cell in row]):
        return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # check winners
    w = winner(board)

    if w is X:
        return 1
    elif w is O:
        return -1
    else:
        # Tie
        return 0        


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    if terminal(board):
        # teminal state
        return None

    next_player = player(board)
    if next_player == X:
        score, action = max_value(board)
    
    elif next_player == O:
        score, action = min_value(board)

    return action
    
def max_value(board, alpha=-99, beta=99):
    """
    Returns the optimal score and action for the maximizer player on the board.
    """
    # base case
    if terminal(board):
        return utility(board), None

    value = -99
    best_action = None
    
    for action in actions(board):

        score, _ = min_value(result(board, action), alpha, beta)

        if score > value:
            value = score
            best_action = action
        # alpha - beta pruning
        alpha = max(alpha, score)
        if alpha >= beta:
            break    

    return value, best_action  

def min_value(board, alpha=-99, beta=99):
    """
    Returns the optimal score for the minmizer player on the board.
    """

    # base case
    if terminal(board):
        return utility(board), None

    value = 99
    best_action = None
    
    for action in actions(board):
        score, _ = max_value(result(board, action), alpha, beta)

        if score < value:
            value = score
            best_action = action
        # alpha - beta pruning
        beta = min(beta, score)
        if alpha >= beta:
            break

    return value, best_action       