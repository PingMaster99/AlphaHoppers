"""
    GameMechanics.py

    Builds a Hoppers game

    Pablo Ruiz 18259 (PingMaster99)
    Version 1.0
    Updated February 9, 2020
"""

import Board as Bd


class Hoppers:
    """
    Hoppers game class
    """
    def __init__(self):
        """
        Initializes the game
        """
        self.board = Bd.Board()
        self.hopper_zones = [
            [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
            [0, 0, 0, 0, 0, 0, 0, 2, 2, 2],
            [0, 0, 0, 0, 0, 0, 2, 2, 2, 2],
            [0, 0, 0, 0, 0, 2, 2, 2, 2, 2]
        ]

    def process_input(self, coordinate, player):
        """
        Processes the input of a player (currently inactive because of GUI implementation)
        :param coordinate: coordinate introduced
        :param player: currant player
        :return: True if the input was valid, else: False
        """
        valid = False
        while not valid:
            try:
                coordinate = input(f"[Jugador {player}] Introduzca la coordenada de {coordinate} separada por un espacio: fila columna:\n>>  ")
                coordinate = list(map(int, coordinate.split()))
                if 0 < coordinate[0] < 11 and 0 < coordinate[1] < 11:
                    coordinate[0] -= 1
                    coordinate[1] -= 1
                    valid = True
                else:
                    print("Recuerde que son numeros enteros del 1 al 10")

            except (IndexError, ValueError):
                print("Recuerde que son numeros enteros del 1 al 10 con un espacio entre las coordenadas")

        return coordinate

    def make_move(self, initial_coordinate, final_coordinate, player_turn):
        """
        Makes a move on the board
        :param initial_coordinate: initial coordinate
        :param final_coordinate: final coordinate
        :param player_turn: current player
        :return: if the move was valid and the path
        """
        return self.board.make_move(initial_coordinate, final_coordinate, player_turn)

    def check_win(self):
        """
        Checks if the game is won
        :return: 1 if player one won, 2 if player two won, or None
        """
        return self.board.game_won()

    def get_board(self):
        """
        Gets the current board
        :return: the board
        """
        return self.board

    def restart(self):
        self.__init__()

    def get_possible_moves(self, piece):
        return self.board.get_valid_moves(piece)
