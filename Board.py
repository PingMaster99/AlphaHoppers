"""
    Board.py

    Boards used for analysis and play of the
    Hoppers game

    Pablo Ruiz 18259 (PingMaster99)
    Version 1.0
    Updated February 9, 2020
"""

from copy import deepcopy


class Board:

    def __init__(self):
        """
            Initializes the board
        """
        self.board = [
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

        self.explored_coordinates = []
        self.last_jump_path = []
        self.visited_path = []

    def is_adjacent(self, initial_coordinate, final_coordinate):
        """
        Calculates if two coordinates are adjacent
        :param initial_coordinate: initial coordinate
        :param final_coordinate: final coordinate
        :return: True if adjacent, else: False
        """
        if abs(initial_coordinate[0] - final_coordinate[0]) <= 1 and abs(initial_coordinate[1] - final_coordinate[1]) <= 1 \
                and initial_coordinate != final_coordinate:
            return True
        else:
            return False

    def check_jump(self, current_coordinate, row_direction=0, column_direction=0, row_delimiter=-1, column_delimiter=-1,
                   positive=True, down_right_diagonal=False, up_left_diagonal=False):
        """
        Checks if a piece can jump in a certain direction
        :param current_coordinate: piece coordinate
        :param row_direction: row direction
        :param column_direction: column direction
        :param row_delimiter: maximum or minimum row number
        :param column_delimiter: maximum or minimum column number
        :param positive: if the direction is positive
        :param down_right_diagonal: if the jump is in this direction
        :param up_left_diagonal: if the jump is in this direction
        :return: landing coordinate of the hopper if a jump is possible
        """
        if positive and not down_right_diagonal and not up_left_diagonal:
            if current_coordinate[0] > row_delimiter and current_coordinate[1] < column_delimiter and \
                    self.board_item(current_coordinate, row_direction, column_direction) != 0 and \
                    self.board_item(current_coordinate, row_direction * 2, column_direction * 2) == 0:
                return [current_coordinate[0] + 2 * row_direction, current_coordinate[1] + 2 * column_direction]

        elif not up_left_diagonal and not down_right_diagonal:
            if current_coordinate[0] < row_delimiter and current_coordinate[1] > column_delimiter and \
                    self.board_item(current_coordinate, row_direction, column_direction) != 0 and \
                    self.board_item(current_coordinate, row_direction * 2, column_direction * 2) == 0:
                return [current_coordinate[0] + 2 * row_direction, current_coordinate[1] + 2 * column_direction]

        elif down_right_diagonal:
            if current_coordinate[0] < row_delimiter and current_coordinate[1] < column_delimiter and \
                    self.board_item(current_coordinate, row_direction, column_direction) != 0 and \
                    self.board_item(current_coordinate, row_direction * 2, column_direction * 2) == 0:
                return [current_coordinate[0] + 2 * row_direction, current_coordinate[1] + 2 * column_direction]

        elif up_left_diagonal:
            if current_coordinate[0] > row_delimiter and current_coordinate[1] > column_delimiter and \
                    self.board_item(current_coordinate, row_direction, column_direction) != 0 and \
                    self.board_item(current_coordinate, row_direction * 2, column_direction * 2) == 0:
                return [current_coordinate[0] + 2 * row_direction, current_coordinate[1] + 2 * column_direction]

        return None

    def board_item(self, position, offset_row=0, offset_column=0):
        """
        Returns a board item with the specified coordinates
        :param position: coordinate
        :param offset_row: offset
        :param offset_column: offset
        :return: the item
        """
        return self.board[position[0] + offset_row][position[1] + offset_column]

    def can_jump(self, initial_coordinate, final_coordinate):
        """
        Checks if a hopper can move between two coordinates
        :param initial_coordinate: initial coordinate
        :param final_coordinate: final coordinate
        :return: if it can jump and the path it took
        """
        self.last_jump_path = [initial_coordinate, final_coordinate]
        # Did not select a piece
        if self.board[initial_coordinate[0]][initial_coordinate[1]] == 0:
            return False, None

        # Adjacent movement
        elif self.is_adjacent(initial_coordinate, final_coordinate):
            if self.board[final_coordinate[0]][final_coordinate[1]] == 0:
                return True, self.last_jump_path
            else:
                return False, None

        # Jump over other pieces
        else:
            self.hopper_jump(initial_coordinate, final_coordinate)
            if len(self.last_jump_path) > 1:
                return True, self.last_jump_path

        return False, None

    def adjacent_jumps(self, current_coordinate):
        """
        Gets all the possible adjacent jumps of a hopper
        :param current_coordinate: current coordinate
        :return: list with the adjacent jumps
        """
        adjacent_jumps = []

        # clockwise check starting with up
        up = self.check_jump(current_coordinate, -1, 0, 1, 10)
        if up is not None:
            adjacent_jumps.append(up)

        right_diagonal = self.check_jump(current_coordinate, -1, 1, 1, 8)
        if right_diagonal is not None:
            adjacent_jumps.append(right_diagonal)

        right = self.check_jump(current_coordinate, 0, 1, -1, 8)
        if right is not None:
            adjacent_jumps.append(right)

        down_right_diagonal = self.check_jump(current_coordinate, 1, 1, 8, 8, down_right_diagonal=True)
        if down_right_diagonal is not None:
            adjacent_jumps.append(down_right_diagonal)

        down = self.check_jump(current_coordinate, 1, 0, 8, -1, False)
        if down is not None:
            adjacent_jumps.append(down)

        down_left_diagonal = self.check_jump(current_coordinate, 1, -1, 8, 1, False)
        if down_left_diagonal is not None:
            adjacent_jumps.append(down_left_diagonal)

        left = self.check_jump(current_coordinate, 0, -1, 10, 1, False)
        if left is not None:
            adjacent_jumps.append(left)

        up_left_diagonal = self.check_jump(current_coordinate, -1, -1, 1, 1, up_left_diagonal=True)
        if up_left_diagonal is not None:
            adjacent_jumps.append(up_left_diagonal)

        return adjacent_jumps

    def recursive_hopper_path(self, initial_coordinate, final_coordinate, visited, path):
        """
        Gets the path a hopper takes on jumps
        :param initial_coordinate: initial coordinate
        :param final_coordinate: final coordinate
        :param visited: visited coordinates
        :param path: path tanken
        """
        self.visited_path.append(initial_coordinate)
        path.append(initial_coordinate)

        if initial_coordinate == final_coordinate:
            print("here for the jump", final_coordinate)
            self.last_jump_path = deepcopy(path)

        else:
            for coordinate in self.adjacent_jumps(initial_coordinate):
                if coordinate not in self.visited_path:
                    self.recursive_hopper_path(coordinate, final_coordinate, self.visited_path, path)
        path.pop()
        visited.pop()

    def hopper_jump(self, initial_coordinate, final_coordinate):
        """
        Auxiliary function to call the recursive hopper jump.
        Resets the jump path and the visited coordinates of the board class
        :param initial_coordinate: initial coordinate
        :param final_coordinate: final coordinate
        """
        self.last_jump_path.clear()
        visited = self.visited_path = []
        path = []
        self.recursive_hopper_path(initial_coordinate, final_coordinate, visited, path)

    def make_move(self, initial_coordinate, final_coordinate, player_turn):
        """
        Makes a move on the board
        :param initial_coordinate: initial coordinate
        :param final_coordinate: final coordinate
        :param player_turn: the player who made the move
        :return: if the move was valid and its path
        """
        can_jump, path = self.can_jump(initial_coordinate, final_coordinate)
        if can_jump and self.board[initial_coordinate[0]][initial_coordinate[1]] == player_turn:
            self.board[initial_coordinate[0]][initial_coordinate[1]] = 0
            self.board[final_coordinate[0]][final_coordinate[1]] = player_turn
            self.last_move = [initial_coordinate, final_coordinate]

            return True, path
        else:
            return False, None

    def direct_move(self, initial_coordinate, final_coordinate, player):
        """
        Makes a move without validation (used for the AI)
        :param initial_coordinate: initial coordinate
        :param final_coordinate: final coordinate
        :param player: player who made the move
        :return: True
        """
        self.board[initial_coordinate[0]][initial_coordinate[1]] = 0
        self.board[final_coordinate[0]][final_coordinate[1]] = player
        self.last_move = [initial_coordinate, final_coordinate]
        return True

    def check_win_player_two(self):
        """
        Checks if player two has won the game
        :return: True if the player two won, else: False
        """
        element_number = 5
        win_chance = False
        for row in range(5):
            for element in range(element_number):
                if self.board[row][element] == 0:
                    return False
                elif not win_chance and self.board[row][element] == 2:
                    win_chance = True
            element_number -= 1
        return win_chance

    def check_win_player_one(self):
        """
        Checks if player one has won
        :return: True if player one won, else: False
        """
        element_offset = 0
        win_chance = False

        for row in range(5, 10):
            for element in range(9 + element_offset, 10):
                if self.board[row][element] == 0:
                    return False
                elif not win_chance and self.board[row][element] == 1:
                    win_chance = True
            element_offset -= 1
        return win_chance

    def game_won(self):
        """
        Checks if any of the players has won the game
        :return: 1 if player one won, 2 if player two won, or None
        """
        if self.check_win_player_one():
            return 1
        elif self.check_win_player_two():
            return 2
        else:
            return None

    def evaluate(self):
        """
        Evaluates the board to see who has an advantage
        :return: valuation
        """
        if self.game_won() == 1:
            return float('inf')
        elif self.game_won() == 2:
            return float('-inf')

        first_score = 0
        second_score = 0
        for row in range(10):
            for column in range(10):
                item = self.board[row][column]
                if item == 0:
                    continue
                elif item == 1:
                    first_score += ((row - 9) ** 2 + (column - 9) ** 2) ** 0.5

                else:
                    second_score += (row ** 2 + column ** 2) ** 0.5

        return (1 / (first_score / 15)) - (1 / (second_score / 15))

    def spaces_in_zone_two(self):
        """
        Gets the number of free spaces in player one's zone
        :return: True if player one won, else: False
        """
        space_count = 0
        element_offset = 0

        for row in range(5, 10):
            for element in range(9 + element_offset, 10):
                if self.board[row][element] == 0:
                    space_count += 1
            element_offset -= 1
        return space_count

    def spaces_in_zone_one(self):
        """
        Gets the number of free spaces in zone one
        :return: Number of free spaces in zone one
        """
        element_offset = 0
        free_spaces = 0
        for row in range(5, 10):
            for element in range(9 + element_offset, 10):
                if self.board[row][element] == 0:
                    free_spaces += 1
            element_offset -= 1
        return free_spaces

    def get_pieces(self, player_turn):
        """
        Gets all the pieces of a specified player
        :param player_turn: current player
        :return: list with all the piece positions
        """
        piece_positions = []
        for row in range(10):
            for column in range(10):

                item = self.board[row][column]
                if item == 0:
                    continue

                elif self.board[row][column] == player_turn:
                    piece_positions.append([row, column])

        return piece_positions

    def get_board(self):
        """
        Gets the board
        :return: current board
        """
        return self.board

    def get_valid_moves(self, initial_coordinate):
        """
        Gets all valid moves in a position
        :param initial_coordinate: initial coordinate
        :return: list with all valid moves
        """
        moves = []
        for row in range(10):
            for column in range(10):
                if self.board[row][column] == 0:
                    if self.can_jump(initial_coordinate, [row, column])[0]:
                        moves.append([row, column])
        return moves

    def print_board(self):
        """
        Prints the board
        """
        for row in self.board:
            print(row)
        print()

    def get_last_move(self):
        """
        Gets the last move made on the board
        """
        return self.last_move



















