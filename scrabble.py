import random
LETTER_VALUES = {"A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4, "I": 1, "J": 1, "K": 5, "L": 1, "M": 3, "N": 1, "O": 1, "P": 3, "Q": 10, "R": 1, "S": 1, "T": 1, "U": 1, "V": 4, "W": 4, "X": 8, "Y": 4, "Z": 10, "1": 0}
tiles_list = ['A', 'C', 'B', 'I', 'A', 'P', 'Q', 'C', 'I', 'P', 'A', 'R', 'D', 'F', 'U', 'A', 'H', 'N', 'B', 'G', 'A',
              'R', 'E', 'D', 'N', 'A', 'E', 'G', 'D', 'A', 'E', 'I', 'D', 'R', 'A', 'U', 'E', 'T', 'O', 'A', 'N', 'I',
              'R', 'E', 'O', 'M', 'I', 'L', 'M', 'E', 'I', 'L', 'G', 'R', 'E', 'L', 'R', 'L', 'I', 'O', 'E', 'S', 'I',
              'O', 'E', 'T', 'U', 'J', 'K', 'E', 'N', 'S', 'I', 'F', 'U', 'S', 'W', 'V', 'E', 'N', 'V', 'O', 'W', 'F',
              'S', 'N', 'T', 'V', 'O', 'T', 'X', 'Y', 'Z', 'O', 'Y', 'T', '1', 'O', 'T', '1']

print('Welcome to Scrabble Game!')

def player_details():
    global num_of_players, player_name
    player_name = []
    while 1:
        num_of_players = int(input("Enter Number of Players (2-4) : "))
        if (num_of_players >= 2 and num_of_players <= 4):
            break
    for member in range(num_of_players):
        player_name.append(input(f"Enter Player {member + 1} name: "))

def letter_generation() :
    global num_of_players, word, letters, player_turn
    while len(tiles_list) != 0 :
        for player_turn in range(num_of_players):
            letters = ', '.join(random.sample(tiles_list, 7))
            print(f"{player_name[player_turn]} form a word using these letters : {letters}")
            while (1) :
                new_keys = input('If you are unable to form a word press "N" to get a new set of words or else press any key : ').upper()
                if (new_keys == 'N'):
                    letters = ', '.join(random.sample(tiles_list, 7))
                    print(f"{player_name[player_turn]} form a word using these letters : {letters}")
                else :
                    break

            word = input("Enter your Word : ").upper()
            valid_word()
        end = input('To Exit the game press "e" or else to continue the game press any key : ').upper()
        if (end == 'E'):
            game_winner()
            exit()


def valid_word() :
    global word, letters, start, blank_count, blank_word
    word_list = list(word)
    letters_list = list(letters)
    dictionary_file = open('dictionary.txt', 'r')
    file_of_dictionary = dictionary_file.read()
    file_of_dictionary = file_of_dictionary.split()

    blank_count = 0
    blank = "1"

    for letter in word_list :
        if (letter == blank) :
            blank_count += 1

    if blank_count == 1:
        choose = input("What do you want to replace with 1 : ").upper()
        blank_word = word
        word = word.replace(blank, choose)

    if blank_count == 2:
        blank_letter1 = input("What do you want to replace the first 1 with : ").upper()
        blank_word = word
        word = word.replace(blank, blank_letter1, 1)
        blank_letter2 = input("What do you want to replace the second 1 with : ").upper()
        word = word.replace(blank, blank_letter2)

    if start == 0:
        if (word in file_of_dictionary) and len(word) < 8 and (all(i in letters_list for i in word_list)):
            print('The word is valid')
            board_display()
            game_play()
        else :
            word = input("Invalid. Enter a Valid Word: ").upper()
            valid_word()
    else :
        if (word in file_of_dictionary) and len(word) < 8:
            print('The word is valid')
            board_display()
            game_play()
        else :
            word = input("Invalid. Enter a Valid Word: ").upper()
            valid_word()



def game_board():
    # Defining Scrabble Game Board
    global board
    board = [["|   |" for row in range(15)] for column in range(15)]
    board[7][7] = "| * |"
    board[0][0] = board[7][0] = board[14][0] = board[0][7] = board[14][7] = board[0][14] = board[7][14] = board[14][14] = "|tws|"
    board[1][1] = board[2][2] = board[3][3] = board[4][4] = board[1][13] = board[2][12] = board[3][11] = board[4][10] = board[13][1] = board[12][2] = board[11][3] = board[10][4] = board[13][13] = board[12][12] = board[11][11] = board[10][10] = "|dws|"
    board[1][5] = board[1][9] = board[5][1] = board[5][5] = board[5][9] = board[5][13] = board[9][1] = board[9][5] = board[9][9] = board[9][13] = board[13][5] = board[13][9] = "|tls|"
    board[0][3] = board[0][11] = board[2][6] = board[2][8] = board[3][0] = board[3][7] = board[3][14] = board[6][2] = board[6][6] = board[6][8] = board[6][12] = board[7][3] = board[7][11] = board[8][2] = board[8][6] = board[8][8] = board[8][12] = board[11][0] = board[11][7] = board[11][14] = board[12][6] = board[12][8] = board[14][3] = board[14][11] = "|dls|"


def board_display():
    #Displaying Scrabble Game Board
    global board
    row = 1
    print("     1      2     3      4      5      6       7     8      9      10     11     12     13     14   15")
    for column in board:
        print("  _____  _____  _____  _____  _____  _____  _____  _____  _____  _____  _____  _____  _____  _____  _____  ")
        if row < 10:
            print(row, end = " ")
        else:
            print(row, end = "")
        print("  ".join(column))
        print("  _____  _____  _____  _____  _____  _____  _____  _____  _____  _____  _____  _____  _____  _____  _____  ")
        row += 1


start = 0
def game_play() :
    global start, word, letters, board, direction, row_number, column_number, blank_count, blank_word, player_turn
    if start == 0:
        print("Start your game from Centre of the Board.")
    while 1 :
        row_number = int(input("Enter Row Number : "))
        column_number = int(input("Enter Column Number : "))
        if (row_number-1 + len(word) <= 14) and (column_number-1 + len(word) <= 14) :
            break
    if start == 0:
        while (row_number != 8 or column_number != 8) :
            print("Invalid. Start from Centre of the Board.")
            row_number = int(input("Enter Row Number : "))
            column_number = int(input("Enter Column Number : "))


    # Player should Enter Correct Direction Right or Down
    while 1:
        direction = input("Enter Right or Down : ").upper()
        if (direction == "RIGHT" or direction == "DOWN") :
            break

    board_list = []
    word_list = list(word)
    letter_count = 0
    if start != 0:
        if direction == "RIGHT":
            for column in range(column_number-1, (len(word) + column_number-1)):
                board_list.extend(list(board[row_number - 1][column]))
            for letter in word_list:
                if letter in board_list:
                    letter_count += 1
                    word_list.remove(letter)

        if direction == "DOWN":
            for row in range(row_number-1, (len(word) + row_number-1)):
                board_list.extend(list(board[row][column_number - 1]))
            for letter in word_list:
                if letter in board_list:
                    letter_count += 1
                    word_list.remove(letter)
    else:
        letter_count = 1
    if (letter_count != 0) :
        score()
        if direction == "RIGHT":
            for next_col in range(len(word)):
                board[row_number - 1][(column_number - 1) + next_col] = "| " + word[next_col] + " |"

        if direction == "DOWN":
            for next_row in range(len(word)):
                board[(row_number - 1) + next_row][column_number - 1] = "| " + word[next_row] + " |"
        start = 1
        if (blank_count != 0) :
            blank_list = list(blank_word)
            for letter in blank_list :
                tiles_list.remove(letter)
        if (blank_count == 0) :
            for letter in word_list :
                tiles_list.remove(letter)

        board_display()

    else :
        print('The word has no common letter in the board')
        word = input('Enter a valid word : ').upper()
        valid_word()

players_scores = [0, 0, 0, 0]
def score():
    global player_turn, player_name, players_scores, word, carry
    word_list = list(word)
    if len(word) == 7:
        carry = 50
        for LETTER in word_list:
            carry += LETTER_VALUES.get(LETTER)
    elif len(word) > 0 and len(word) < 8:
        carry = 0
        for LETTER in word_list:
            carry += LETTER_VALUES.get(LETTER)
    players_scores[player_turn] += (carry + update_score())
    print(f"{player_name[player_turn]}'s score is {players_scores[player_turn]}")


def update_score():
    global word, board, carry, row_number, column_number, direction
    update_carry = 0

    if direction == "RIGHT":
        for col_index in range(len(word)):
            if board[row_number - 1][(column_number - 1) + col_index] == "|tws|":
                update_carry += (2 * carry)
            elif board[row_number - 1][(column_number - 1) + col_index] == "|dws|":
                update_carry += (1 * carry)
            elif board[row_number - 1][(column_number - 1) + col_index] == "|tls|":
                update_carry += (2 * LETTER_VALUES.get(word[col_index]))
            elif board[row_number - 1][(column_number - 1) + col_index] == "|dls|":
                update_carry += (LETTER_VALUES.get(word[col_index]))
            else:
                update_carry += 0
    if direction == "DOWN":
        for row_index in range(len(word)):
            if board[(row_number - 1) + row_index][column_number - 1] == "|tws|":
                update_carry += (2 * carry)
            elif board[(row_number - 1) + row_index][column_number - 1] == "|dws|":
                update_carry += (1 * carry)
            elif board[(row_number - 1) + row_index][column_number - 1] == "|tls|":
                update_carry += (2 * LETTER_VALUES.get(word[row_index]))
            elif board[(row_number - 1) + row_index][column_number - 1] == "|dls|":
                update_carry += (LETTER_VALUES.get(word[row_index]))
            else:
                update_carry += 0
    return update_carry


def game_winner():
    global player_name, players_scores, num_of_players
    first_highest = second_highest = 0
    first_player = second_player = 0
    for player in range(num_of_players):
        if players_scores[player] > first_highest:
            second_player = first_player
            first_player = player
            second_highest = first_highest
            first_highest = players_scores[player]
        elif second_highest < players_scores[player]:
            second_highest = players_scores[player]
            second_player = player
    print("Winner of the Game is", player_name[first_player], "with a Highest Score of ", first_highest)
    print("Runner of the Game is", player_name[second_player], "with Second Highest Score of ", second_highest)


game_board()
player_details()
letter_generation()
game_winner()
