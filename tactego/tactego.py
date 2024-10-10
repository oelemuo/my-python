"""
File:    tactego.py
Author:  Obinna Elemuo
Date:    11/29/23
Section: 26
E-mail:  so01811@umbc.edu
Description:
Project 2:
Simplified version of the game Stratego named Tactego. Program open and reads
files which includes element that will be used to draw the board, made by 2d list.
The goal of the game is to capture enemy flag, once this happens, program will print the
winner and end game.
"""
import random
def initialize_board(length, width, pieces_file):
    """
    Initialize the game board based on given parameters and piece file
    :param length: length of the board
    :param width: the width of the board
    :param pieces_file: file containing information about pieces
    :return: the game board, a 2d List representing
    """
    total_cells = length * width
    red_pieces = []
    blue_pieces = []
    board = [['' for _ in range(width)] for _ in range(length)]

    # read the file and process the pieces
    with open(pieces_file, 'r') as file:
        lines = file.readlines()
        # iterate through lines of the file
        for line in lines:
            line = line.strip().split()
            if len(line) == 2:
                num_pieces = int(line[1])
                # extend each pieces list with red player or blue player pieces from file
                # denote with prefixed letter
                red_pieces.extend([f"R{line[0]}"] * num_pieces)
                blue_pieces.extend([f"B{line[0]}"] * num_pieces)
    # check if board can fit all pieces
    if len(red_pieces) > total_cells / 2:
        print("Warning! The size of the board is too small for the number of pieces")
        print("The game may be invalid.")

    # shuffle pieces for both players
    random.shuffle(red_pieces)
    random.shuffle(blue_pieces)

    # add red player pieces to board
    for i in range(length):
        for j in range(width):
            if len(red_pieces) != 0:
                board[i][j] = red_pieces.pop()
    # add blue player pieces to the board
    for i in range(length - 1, -1, -1):
        for j in range(width):
            if len(blue_pieces) != 0:
                board[i][j] = blue_pieces.pop()

    # return initialized board
    return board
def get_player_move(board, player):
    """
    Get the player's move from the board for a specific player
    :param board: the game board
    :param player: the player whose move is being obtained
    :return: the updated game board after the player's move
    """
    # use boolean flag to get the chosen piece
    is_valid_start = False
    is_valid_end = False

    # Repeat until start position is correct
    while not is_valid_start:
        start_position = input("Select Piece to Move by Position >> ")

        # Check if the piece is valid
        indexes = start_position.strip().split(' ')
        if len(indexes) == 2:
            if player == 'blue':
                try:
                    if board[int(indexes[0])][int(indexes[1])] == '':
                        print('You must select a starting position with one of your pieces.')
                    elif board[int(indexes[0])][int(indexes[1])][1] == 'F':
                        print('You must select a starting position with one of your pieces. Not a flag')
                    elif board[int(indexes[0])][int(indexes[1])][0] == 'B':
                        start = (int(indexes[0]), int(indexes[1]))
                        is_valid_start = True
                    else:
                        print('You must select a starting position with one of your pieces.')
                except:
                    print('You must select a starting position with one of your pieces.')
            else:
                try:
                    if board[int(indexes[0])][int(indexes[1])] == '':
                        print('You must select a starting position with one of your pieces.')
                    elif board[int(indexes[0])][int(indexes[1])][0] == 'R':
                        start = (int(indexes[0]), int(indexes[1]))
                        is_valid_start = True
                    else:
                        print('You must select a starting position with one of your pieces.')
                except:
                    print('You must select a starting position with one of your pieces.')

    # Repeat until end position is correct
    while not is_valid_end:
        end_position = input("Select Position to move Piece >> ")
        indexes = end_position.strip().split(' ')

        if len(indexes) == 2:
            try:
                valid_piece = True
                if board[int(indexes[0])][int(indexes[1])] != '':
                    if player == 'blue':
                        if board[int(indexes[0])][int(indexes[1])][0] == 'B':
                            valid_piece = False
                    else:
                        if board[int(indexes[0])][int(indexes[1])][0] == 'R':
                            valid_piece = False

                if not valid_piece:
                    print(f'You must select a valid position to move your piece.')
                else:
                    stop = (int(indexes[0]), int(indexes[1]))
                    board = move_piece((start, stop), board)
                    is_valid_end = True
            except:
                print('You must select a valid position to move your piece.')

    return board

def move_piece(move, board):
    """
    Move a piece on the board from start position to stop position
    :param move: tuple containing start and stop positions of the move
    :param board: the game board
    :return: updated game board after a piece is moved
    """
    # get the move
    start, stop = move

    # get the piece
    piece = board[start[0]][start[1]]

    # get the destination
    dest = board[stop[0]][stop[1]]

    # handle combat
    if dest == "":
        board[stop[0]][stop[1]] = piece
        board[start[0]][start[1]] = ""
        return board
    elif dest[1] == 'F':
        board[stop[0]][stop[1]] = piece
        board[start[0]][start[1]] = ""
        return board

    else:
        if int(piece[1]) >= int(dest[1]):
            board[stop[0]][stop[1]] = piece
            board[start[0]][start[1]] = ""
            return board
        else:
            board[start[0]][start[1]] = ""
            return board


def get_winner(board):
    """
    Determine the winner based on the state of the game board
    :param board: the game board
    :return: "blue" if blue players wins, 'red' if red player wins, None if no winner
    """
    # Count Red Player Flags:
    red_flags = 0
    for row in board:
        for tile in row:
            if tile == "RF":
                red_flags += 1
    if red_flags == 0:
        return 'blue'

    # Count Blue Player Flags
    blue_flags = 0
    for row in board:
        for tile in row:
            if tile == "BF":
                blue_flags += 1

    if blue_flags == 0:
        return "red"

    # if no winner
    return None


def switch_player(player):
    """
    function to switch the current player
    :param player: the current player
    :return: the next player to take a turn
    """
    if player == "red":
        return "blue"
    else:
        return "red"


def draw_board(board):
    """
    function to display the game board
    :param board: the board
    """
    # display the column numbers
    # for loop iterates the length pf the columns
    print('   ', end=' ')
    for i in range(len(board[0])):
        print(f"{i:<5}", end=' ')
    print()

    # display the row numbers and the board
    # for loop iterates the length of the rows
    for i in range(len(board)):
        print(f"  {i:<3}", end='')
        for j in range(len(board[i])):
            print(f"{board[i][j]:<5}", end=' ')
        print()


def tactego(pieces_file, length, width):
    """
    The game loop for Tactego
    :param pieces_file: file containing information about pieces
    :param length: the length of the game board
    :param width: the width of the game board
    """
    # initial the game board
    board = initialize_board(length, width, pieces_file)
    player = 'red'

    # boolean flag for the game being over
    game_is_over = False

    while not game_is_over:
        # draw the board
        draw_board(board)
        # Get player move, move the pieces and handle combat
        board = get_player_move(board, player)

        # switch player
        player = switch_player(player)

        # check for a winner
        winner = get_winner(board)

        # if winner case
        if winner != None:
            if winner == 'red':
                print("R has won the game")
            else:
                print("B has won the game")
            game_is_over = True

# main method
if __name__ == "__main__":
    random.seed(input("What is the seed?"))
    file_name = input("What is the filename for the pieces?")
    length = int(input("What is the length?"))
    width = int(input("What is the width?"))
    tactego(file_name, length, width)
