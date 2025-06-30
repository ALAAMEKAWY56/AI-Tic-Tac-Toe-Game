"""
Tic Tac Toe Player using Depth-First Search (DFS)
"""

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
        raise None




def dfs(board, depth=0):
    """
    Returns the optimal action for the current player on the board using Depth-First Search.
    """
    # Start time measurement
    start_time = time.perf_counter_ns()

    # Increment depth counter
    depth += 1

    # Calculate the branching factor
    empty_cells = sum(row.count(EMPTY) for row in board)
    possible_actions = len(actions(board))
    branching_factor = possible_actions / empty_cells if empty_cells > 0 else 0

    # no more moves
    if terminal(board):
        # Print time and space complexity
        end_time = time.perf_counter_ns()
        time_taken = end_time - start_time  # Time difference in nanoseconds
        print(f"Depth: {depth}, Time: {time_taken} nanoseconds, Branching Factor: {branching_factor},Space Complexity: O({depth})" )
        return None

    # Get all possible actions
    possible_actions = actions(board)

    # Iterate through all possible actions
    for action in possible_actions:
        # Get the result board after applying the action
        next_board = result(board, action)

        # Recursively search for the next move
        next_move = dfs(next_board, depth)

        # If the current move leads to a win for the current player, return it
        if next_move is not None:
            return action

    # If no winning move is found, return a random move
    return random.choice(list(possible_actions))


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) is not None or all(EMPTY not in row for row in board)


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

