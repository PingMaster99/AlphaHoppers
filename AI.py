"""
    AI.py

    Uses a minimax algorithm to play the Hoppers game

    Pablo Ruiz 18259 (PingMaster99)
    Version 1.0
    Updated February 9, 2020
"""

from copy import deepcopy
import Board as Bd
import GameMechanics as Gme


def minimax(position: Bd, depth, max_player, game: Gme, alpha=float('-inf'), beta=float('inf')):
    """
    Minimax algorithm with alpha beta pruning for the AI player
    :param position: current board position
    :param depth: maximum analysis depth
    :param max_player: player who is being analyzed
    :param game: current game in play
    :param alpha: alpha value for pruning
    :param beta: beta value for pruning
    :return: evaluation and best move
    """
    if depth == 0 or position.game_won() is not None:
        return position.evaluate(), position
    if max_player == 1:
        max_evaluation = float('-inf')
        best_move = None

        for move in get_all_moves(position, 1, game):
            evaluation = minimax(move, depth - 1, 2, game, alpha, beta)[0]
            max_evaluation = max(max_evaluation, evaluation)
            if max_evaluation == evaluation:
                best_move = move
            alpha = max(alpha, max_evaluation)
            if alpha >= beta:
                break
        return max_evaluation, best_move

    else:
        min_evaluation = float('inf')
        best_move = None

        for move in get_all_moves(position, 2, game):
            evaluation = minimax(move, depth - 1, 1, game, alpha, beta)[0]
            min_evaluation = min(min_evaluation, evaluation)
            if min_evaluation == evaluation:
                best_move = move
            beta = min(beta, min_evaluation)
            if alpha >= beta:
                break
        return min_evaluation, best_move


def get_all_moves(position, player, game: Gme):
    """
    Gets all the moves in a position
    :param position: current board position
    :param player: player who is going to move
    :param game: current game in play
    :return: a list of all the boards with the new moves
    """
    moves = []
    for piece in position.get_pieces(player):
        valid_moves = position.get_valid_moves(piece)
        for move in valid_moves:
            temp_board = deepcopy(position)
            new_board = simulate_move(piece, move, temp_board, game, player)
            moves.append(new_board)
    return moves


def simulate_move(piece, move, board, game, player):
    """
    Simulates a move on one of the analysis boards
    :param piece: current piece to be moved
    :param move: move to be made
    :param board: board in which the move will be made
    :param game: current game in play
    :param player: player who has to move
    :return: board with the move
    """
    board.direct_move(piece, move, player)
    return board

