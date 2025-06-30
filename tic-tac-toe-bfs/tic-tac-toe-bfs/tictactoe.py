"""
Tic Tac Toe Player
"""

import math
import copy
import random 
import time

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
    counter = {"X":0, "O":0}

    for i in board:
        for j in i:
            if j is not None:
                counter[j] +=1
            
    return X if counter['X'] == counter['O'] else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_moves = set()
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == EMPTY:
                possible_moves.add((i, j))
    return possible_moves            


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    result_board = copy.deepcopy(board)
    
    if action is not None and result_board[action[0]][action[1]] == EMPTY:
        next_player = player(board)
        result_board[action[0]][action[1]] = next_player
        return result_board
    else:    
        raise ImpossibleMoveError # type: ignore


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    win_states = win_indexes(len(board))
    for indexes in win_states:
        if all(board[r][c] == X for r, c in indexes):
            return X
        if all(board[r][c] == O for r, c in indexes):
            return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    for i in board:
        if i.count(EMPTY) > 0:
            return False

    # no more moves
    return True



from collections import deque

def bfs(board):
    """
    Returns the optimal action for the current player on the board using BFS.
    """
    start_time = time.perf_counter_ns()
    # Queue for BFS
    queue = deque([(board, None)])

    empty_cells = sum(row.count(EMPTY) for row in board)
    possible_actions = len(actions(board))
    depth = 9 - possible_actions
    branching_factor = depth / empty_cells if empty_cells > 0 else 0

    while queue:
        current_board, prev_action = queue.popleft()

        # Check if current board is terminal
        if terminal(current_board):
            end_time = time.perf_counter_ns()
            time_taken = end_time - start_time  # Time difference in nanoseconds
            print(f"Depth: {depth}, Time: {time_taken} nanoseconds, Branching Factor: {branching_factor},Space Complexity: O({depth**int(branching_factor)})" )
            return prev_action

        # Generate possible actions
        possible_actions = actions(current_board)

        # Iterate over possible actions
        for action in possible_actions:
            next_board = result(current_board, action)
            # Add next board and action to queue
            queue.append((next_board, action))

    return None


def win_indexes(n):
    # Rows
    for r in range(n):
        yield [(r, c) for c in range(n)]
    # Columns
    for c in range(n):
        yield [(r, c) for r in range(n)]
    # Diagonal top left to bottom right
    yield [(i, i) for i in range(n)]
    # Diagonal top right to bottom left
    yield [(i, n - 1 - i) for i in range(n)]


def player_goal(player):
     return 1 if player == X else -1

def get_random_move(max):
    i = random.randrange(max)
    j = random.randrange(max)
    return (i, j)