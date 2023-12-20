"""
Tic Tac Toe Player
"""

import math
import copy

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
    turns = 0

    for i in range(len(board)):
        for j in range(len(board[1])):
            if board[i][j] != EMPTY:
                turns += 1

    if turns % 2 == 0:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                moves.update([(i,j)])

    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action in actions(board):
        new = copy.deepcopy(board)
        new[action[0]][action[1]] = player(board)
        return new
    else:
        raise Exception("Invalid move")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    win = None
    p = X if player(board) == O else O
    for i in range(len(board)):
        if board[i][0] and all(play == board[i][0] for play in board[i]):
            win = p

    for j in range(len(board[0])):
        col_values = []
        for k in range(len(board)):
            col_values.append(board[k][j])
        if col_values[0] and all(play == col_values[0] for play in col_values):
            win = p

    if board[0][0] and board[0][0] == board[1][1] and board[0][0] == board[2][2]:
        win = p
    
    if board[0][2] and board[0][2] == board[1][1] and board[0][2] == board[2][0]:
        win = p

    return win


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) or len(actions(board)) < 1:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def max_value(board):
    if terminal(board):
        return utility(board)

    v = -math.inf
    for a in actions(board):
        v = max(v, min_value(result(board, a)))
    return v
    

def min_value(board):
    if terminal(board):
        return utility(board)

    v = math.inf
    for a in actions(board):
        v = min(v, max_value(result(board, a)))
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    else:
        moves = []
        p = player(board)
        acts = actions(board)
        if p == X:
            for a in acts:
                moves.append([a, min_value(result(board, a))])
            moves = sorted(moves, key = lambda x: x[1], reverse = True)
        elif p == O:
            for a in acts:
                moves.append([a, max_value(result(board, a))])
            moves = sorted(moves, key = lambda x: x[1])
        
        return moves[0][0]
