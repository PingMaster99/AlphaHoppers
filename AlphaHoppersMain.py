"""
    AlphaHoppersMain.py

    Utilizes Pygame and Minimax to generate a game of Hoppers

    Pablo Ruiz 18259 (PingMaster99)
    Version 1.0
    Updated February 9, 2020

    Controls:

    Click   -   Select initial and final square for the hopper
    Space   -   Reset the selected coordinates
"""

import GameMechanics as Mechanics
import AI as AI
import pygame as p


hopper_engine = Mechanics.Hoppers()
p.init()
WIDTH = HEIGHT = 520
DIMENSION = 10
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 144
COLORS = {1: [p.Color("yellowgreen"), SQ_SIZE], 2: [p.Color("cyan"), SQ_SIZE]}

"""
User input and updating the graphics
"""

hopper_engine.get_board().print_board()


def main():
    """
    Main method to run the Hoppers game
    """
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    winner = None
    current_selection = []
    ai_turn = False
    game_playing = True
    while game_playing:

        for e in p.event.get():
            if e.type == p.QUIT:
                winner = -1
                game_playing = False

            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                row = location[1] // SQ_SIZE
                column = location[0] // SQ_SIZE
                selected_coordinate = [row, column]
                current_selection.append(selected_coordinate)
                if len(current_selection) == 2:
                    if not ai_turn:
                        winner, ai_turn = make_human_move(1, current_selection)
                    current_selection.clear()

            elif e.type == p.MOUSEBUTTONUP:
                if ai_turn:
                    winner = make_ai_move(2, 1)
                    ai_turn = False

            elif e.type == p.KEYDOWN:
                if e.key == p.K_SPACE:
                    current_selection.clear()

        draw_game(screen, hopper_engine)
        clock.tick(MAX_FPS)
        p.display.flip()

        if winner is not None and winner != -1:
            print(f"Gano el jugador {winner}")
            break


def initialize_game():
    """
    Generates a new game
    :return: hoppers game
    """
    return Mechanics.Hoppers()


def draw_game(screen, game):
    """
    Draws the game in the window
    :param screen: screen to draw on
    :param game: game that is being played
    """
    draw_board(screen, game)  # squares on the board
    draw_pieces(screen, game.get_board().board)   # pieces


def draw_board(screen, game):
    """
    Draws the Hoppers board
    :param screen: screen to draw on
    :param game: game that is being played
    """
    colors = [p.Color("white"), p.Color("lightgray")]
    green_zome = [p.Color("darkgreen"), p.Color("green")]
    blue_zone = [p.Color("darkblue"), p.Color("blue")]
    hopper_zones = game.hopper_zones
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            if hopper_zones[row][column] == 0:
                color = colors[(row + column) % 2]
            elif hopper_zones[row][column] == 1:
                color = green_zome[(row + column) % 2]
            else:
                color = blue_zone[(row + column) % 2]
            p.draw.rect(screen, color, p.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
    """
    Draws the hopper pieces
    :param screen: screen to draw on
    :param board: Hoppers board
    """
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece == 0:
                continue
            else:
                p.draw.circle(screen, COLORS[piece][0], (column * SQ_SIZE + SQ_SIZE / 2, row * SQ_SIZE + SQ_SIZE / 2),
                              SQ_SIZE / 3.2)


def make_human_move(player, move):
    """
    Processes human input and makes a move
    :param player: player one or two
    :param move: move made
    :return: if there is a game winner and if the movement was valid
    """
    initial_coordinate = move[0]
    final_coordinate = move[1]

    initial_row, initial_column = initial_coordinate[0], initial_coordinate[1]
    final_row, final_column = final_coordinate[0], final_coordinate[1]

    valid_movement, path = hopper_engine.make_move([initial_row, initial_column], [final_row, final_column], player)
    winner = hopper_engine.check_win()

    if not valid_movement:
        print("No es un movimiento valido")
    else:
        print(hopper_engine.get_board().evaluate(), "Evaluacion actual")
        print(path, "recorrido")
        hopper_engine.get_board().print_board()

    return winner, valid_movement


def make_ai_move(player, depth):
    """
    Makes an AI move
    :param player: player one or two
    :param depth: depth of the AI analysis
    :return: if there is a game winner
    """
    value, new_board = AI.minimax(hopper_engine.get_board(), depth, player, hopper_engine)

    move = new_board.get_last_move()
    initial_row, initial_column = move[0][0], move[0][1]
    final_row, final_column = move[1][0], move[1][1]

    path = hopper_engine.make_move([initial_row, initial_column], [final_row, final_column], player)[1]
    winner = hopper_engine.check_win()

    print(new_board.evaluate(), "Evaluacion actual")
    print(path, "recorrido\n")
    hopper_engine.get_board().print_board()

    return winner


if __name__ == "__main__":
    main()






