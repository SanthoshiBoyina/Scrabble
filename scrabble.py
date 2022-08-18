import random
import mysql.connector

TILE_POINTS = {"A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4, "I": 1, "J": 8, "K": 5, "L": 1, "M": 3, "N": 1, "O": 1, "P": 3,
               "Q": 10, "R": 1, "S": 1, "T": 1, "U": 1, "V": 4, "W": 4, "X": 8, "Y": 4, "Z": 10, "1": 0}
bag_of_tiles = ['A', 'C', 'B', 'I', 'A', 'P', 'Q', 'C', 'I', 'P', 'A', 'R', 'D', 'E', 'U', 'A', 'H', 'N', 'B', 'G', 'A',
              'R', 'E', 'D', 'N', 'A', 'E', 'G', 'D', 'A', 'E', 'I', 'D', 'R', 'A', 'U', 'E', 'T', 'O', 'A', 'N', 'I',
              'R', 'E', 'O', 'M', 'I', 'L', 'M', 'E', 'I', 'L', 'G', 'R', 'E', 'L', 'R', 'L', 'I', 'O', 'E', 'S', 'I',
              'O', 'E', 'T', 'U', 'J', 'K', 'E', 'N', 'S', 'I', 'F', 'U', 'S', 'W', 'V', 'E', 'N', 'H', 'O', 'W', 'F',
              'S', 'N', 'T', 'V', 'O', 'T', 'X', 'Y', 'Z', 'O', 'Y', 'T', '1', 'O', 'T', '1']


def game_board_construction() :
    # Constructing Scrabble Game Board
    global board
    board = [["|   |" for column in range(17)] for row in range(17)]
    board[0][0] = board[0][16] = board[16][0] = board[16][16] = "     "
    board[8][8] = "| * |"
    for i in range(1, 10) :
        board[0][i] = board[i][0] = board[i][16] = board[16][i] = "  " + str(i) + "  "
    for i in range(10, 16) :
        board[0][i] = board[i][0] = board[i][16] = board[16][i] = " " + str(i) + "  "

    board[1][1] = board[8][1] = board[15][1] = board[1][8] = board[15][8] = board[1][15] = board[8][15] = board[15][15] = "|tws|"
    board[2][2] = board[3][3] = board[4][4] = board[5][5] = board[2][14] = board[3][13] = board[4][12] = board[5][11] = board[14][2] = board[13][3] = board[12][4] = board[11][5] = board[14][14] = board[13][13] = board[12][12] = board[11][11] = "|dws|"
    board[2][6] = board[2][10] = board[6][2] = board[6][6] = board[6][10] = board[6][14] = board[10][2] = board[10][6] = board[10][10] = board[10][14] = board[14][6] = board[14][10] = "|tls|"
    board[1][4] = board[1][12] = board[3][7] = board[3][9] = board[4][1] = board[4][8] = board[4][15] = board[7][3] = board[7][7] = board[7][9] = board[7][13] = board[8][4] = board[8][12] = board[9][3] = board[9][7] = board[9][9] = board[9][13] = board[12][1] = board[12][8] = board[12][15] = board[13][7] = board[13][9] = board[15][4] = board[15][12] = "|dls|"

def board_display():
    #Displaying Scrabble Game Board
    global board

    print("  ".join(board[0]))
    for row in range(1, 16):
        print("       _____  _____  _____  _____  _____  _____  _____  _____  _____  _____  _____  _____  _____  _____  _____  ")
        print("  ".join(board[row]))
        print("       _____  _____  _____  _____  _____  _____  _____  _____  _____  _____  _____  _____  _____  _____  _____  ")
    print("  ".join(board[16]))


def player_details():
    # Acquiring Player Details
    global num_of_players, player_names
    player_names = [""]

    num_of_players = int(input("Enter Number of Players (2-4) : "))
    while not(2 <= num_of_players and num_of_players <= 4) :
        num_of_players = int(input("Enter Number of Players (2-4) : "))

    for player in range(num_of_players) :
        player_names.append(input(f"Enter Player {player + 1} name: ").upper())
    print()

def is_rack(turn) :
    global player_tiles
    for tile in range(7) :
        if(player_tiles[turn][tile] != '') :
            return False
    return True


def is_any_rack() :
    global num_of_players
    for turn in range(1, num_of_players+1) :
        if(is_rack(turn) == True) :
            return True
    return False


def game_over() :
    global bag_of_tiles, player_skips
    return (is_any_rack() and len(bag_of_tiles) == 0) or (6 in player_skips)


def replacing_blank_tiles(no_of_blank_tiles) :
    global word
    first_blank = input("What do you want to replace 1 with (A-Z) : ").upper()
    while not ('A' <= first_blank and first_blank <= 'Z' and len(first_blank) == 1):
        first_blank = input("What do you want to replace  1 with (A-Z) : ").upper()

    word = word.replace('1', first_blank, 1)
    if (no_of_blank_tiles == 2):
        second_blank = input("What do you want to replace second 1 with (A-Z) : ").upper()
        while not ('A' <= second_blank and second_blank <= 'Z' and len(second_blank) == 1):
            second_blank = input("What do you want to replace second 1 with (A-Z) : ").upper()
        word = word.replace('1', second_blank, 1)

def game_commencement() :
    global num_of_players, player_skips, player_tiles, player_scores, bag_of_tiles

    player_tiles = [[] for player in range(num_of_players+1)]
    player_skips = [0 for player in range(num_of_players+1)]
    player_scores = [0 for player in range(num_of_players+1)]
    player_scores[0] = -1000

    # Intially, each player is provided with 7 tiles to start the game
    for player_turn in range(1, num_of_players+1) :
        player_tiles[player_turn].extend(random.sample(bag_of_tiles, 7))
        for tile in player_tiles[player_turn] :
            bag_of_tiles.remove(tile)

    turn = 2
    first_player_turn()
    while not(game_over()) :
        players_turn(turn)
        if(player_skips[turn] == 6 or input(f"Press 'E' to exit the game : ").upper() == 'E') :
            break
        turn += 1
        if(turn == num_of_players+1) :
            turn = 1

    if(len(bag_of_tiles) == 0) :
        print("The Game has reached an End! As we are short of Tiles")
    if(6 in player_skips) :
        print(f"The Game has reached an End! As {player_names[player_skips.index(6)]} has performed 6 Succesive Skips")

def first_player_turn() :
    global player_names, player_tiles, word, player_scores, player_skips, org_word

    print(f"{player_names[1]} form a word using these letters : {', '.join(player_tiles[1])}")
    while input(f"{player_names[1]} to get a new set of Words, enter 'N' : ").upper() == "N":
        bag_of_tiles.extend(player_tiles[1])
        player_tiles[1].clear()
        player_tiles[1] = random.sample(bag_of_tiles, 7)
        for tile in player_tiles[1]:
            bag_of_tiles.remove(tile)
        print(f"{player_names[1]} form a word using these letters : {', '.join(player_tiles[1])}")
    word = input(f"{player_names[1]} enter your Word : ").upper()
    org_word = word
    no_of_blank_tiles = word.count('1')
    if(1 == no_of_blank_tiles or no_of_blank_tiles == 2) :
        replacing_blank_tiles(no_of_blank_tiles)

    while not(is_start_valid_word(word)) :
        print(f"OOPS! {word} is not a Convincing Word")
        print(f"{player_names[1]}, Please enter a Credible Word using {', '.join(player_tiles[1])} : ")
        while input(f"{player_names[1]} to get a new set of Words, enter 'N' : ").upper() == "N":
            bag_of_tiles.extend(player_tiles[1])
            player_tiles[1].clear()
            player_tiles[1] = random.sample(bag_of_tiles, 7)
            for tile in player_tiles[1]:
                bag_of_tiles.remove(tile)
            print(f"{player_names[1]} form a word using these letters : {', '.join(player_tiles[1])}")
        word = input(f"{player_names[1]} enter your Word : ").upper()
        org_word = word
        no_of_blank_tiles = word.count('1')
        if (1 == no_of_blank_tiles or no_of_blank_tiles == 2):
            replacing_blank_tiles(no_of_blank_tiles)

    # Only when the word is valid, we calculate its score and place it on the board
    tile_score = tiles_score(org_word)
    player_scores[1] = tile_score + premium_tiles_score(org_word, tile_score)
    player_scores[1] = 2 * player_scores[1]
    if(len(org_word) == 7) :
        player_scores[1] += 50
    print(f"{player_names[1]}'s score is {player_scores[1]}")
    place_word_on_board(org_word)
    board_display()

def is_start_valid_word(word) :
    global player_names, row_number, column_number, direction, org_word
    if(word.count('1') > 2) :
        return False
    if not(2 <= len(word) and len(word) <= 7) :
        print("Length of word should be in the range (2-7)")
        return False

    dictionary_file = open('dictionary.txt', 'r').read()
    dictionary_file = dictionary_file.split()
    if not(word in dictionary_file) :
        return False

    board_display()

    direction = input(f"{player_names[1]}, please enter direction (right or down): ").upper()
    while(not(direction == "RIGHT" or direction == "DOWN")) :
        direction = input(f"{player_names[1]}, please enter direction (right or down): ").upper()

    if(direction == "RIGHT") :
        row_number = int(input(f"{player_names[1]} enter Row Number (1-15) : "))
        while not (row_number == 8) :
            row_number = int(input(f"{player_names[1]} enter Row Number (1-15) : "))
        column_number = int(input(f"{player_names[1]} enter Column Number (1-15) : "))
        while not(column_number<=8 and 8 <= column_number+len(word)-1) :
            column_number = int(input(f"{player_names[1]} enter Column Number (1-15) : "))
    elif(direction == "DOWN") :
        row_number = int(input(f"{player_names[1]} enter Row Number (1-15) : "))
        while not(row_number <= 8 and 8 <= row_number+len(word)-1) :
            row_number = int(input(f"{player_names[1]} enter Row Number (1-15) : "))
        column_number = int(input(f"{player_names[1]} enter Column Number (1-15) : "))
        while not(column_number == 8) :
            column_number = int(input(f"{player_names[1]} enter Column Number (1-15) : "))

    return start_word_corresponds_board(org_word, row_number, column_number, direction)

def start_word_corresponds_board(word, row_number, column_number, direction) :
    global board, player_tiles

    temp_rack = [tile for tile in player_tiles[1]]
    if(direction == "RIGHT") :
        idx = column_number
        while (idx <= 15 and (idx-column_number) < len(word)) :
            if(word[idx-column_number] not in temp_rack) :
                return False
            tile_index = temp_rack.index(word[idx-column_number])
            temp_rack[tile_index] = ''
            idx += 1

        if (idx-column_number) < len(word) :
            return False

    elif direction == "DOWN" :
        idx = row_number
        while(idx <= 15 and (idx-row_number) < len(word)) :
            if(word[idx-row_number] not in temp_rack) :
                return False
            tile_index = temp_rack.index(word[idx-row_number])
            temp_rack[tile_index] = ''
            idx += 1

        if (idx-row_number) < len(word) :
            return False

    for tile_index in range(7) :
        if(temp_rack[tile_index] == '') :
            player_tiles[1][tile_index] = random.sample(bag_of_tiles, 1)[0]
            bag_of_tiles.remove(player_tiles[1][tile_index])
    return True

def players_turn(turn) :
    global player_names, player_tiles, word, player_scores, player_skips, org_word

    print(f"{player_names[turn]} form a word using these letters : {', '.join(player_tiles[turn])}")
    while input(f"{player_names[turn]} to get a new set of Words, enter 'N' : ").upper() == "N":
        if(len(bag_of_tiles) == 0) :
            print("Exchange of Tiles is not possible, as we are short of tiles in the bag!!")
        else :
            for tile in range(7) :
                if(player_tiles[turn][tile] != '') :
                    bag_of_tiles.append(player_tiles[turn][tile])
            for tile in range(7) :
                if(player_tiles[turn][tile] != '') :
                    player_tiles[turn][tile] = random.sample(bag_of_tiles, 1)[0]
            player_skips[turn] += 1
        if(player_skips[turn] == 6) :
            return
        print(f"{player_names[turn]} form a word using these letters : {', '.join(player_tiles[turn])}")
    player_skips[turn] = 0
    word = input(f"{player_names[turn]} enter your Word : ").upper()
    org_word = word
    no_of_blank_tiles = word.count('1')
    if (1 == no_of_blank_tiles or no_of_blank_tiles == 2):
        replacing_blank_tiles(no_of_blank_tiles)

    while not(valid_word(word, turn)) :
        print(f"OOPS! {word} is not a Convincing Word")
        print(f"{player_names[turn]}, Please enter a Credible Word using {', '.join(player_tiles[turn])} : ")
        while input(f"{player_names[turn]} to get a new set of Words, enter 'N' : ").upper() == "N":
            if (len(bag_of_tiles) == 0):
                print("Exchange of Tiles is not possible, as we are short of tiles in the bag!!")
            else:
                for tile in range(7):
                    if (player_tiles[turn][tile] != ''):
                        bag_of_tiles.append(player_tiles[turn][tile])
                for tile in range(7):
                    if (player_tiles[turn][tile] != ''):
                        player_tiles[turn][tile] = random.sample(bag_of_tiles, 1)[0]
                player_skips[turn] += 1
            print(f"{player_names[turn]} form a word using these letters : {', '.join(player_tiles[turn])}")
        word = input(f"{player_names[turn]} enter your Word : ").upper()
        org_word = word
        no_of_blank_tiles = word.count('1')
        if (1 == no_of_blank_tiles or no_of_blank_tiles == 2):
            replacing_blank_tiles(no_of_blank_tiles)

    # Only when the word is valid, we calculate its score and place it on the board
    tile_score = tiles_score(word)
    player_scores[turn] += tile_score + premium_tiles_score(word, tile_score)
    print(f"{player_names[turn]}'s score is {player_scores[turn]}")
    place_word_on_board(org_word)
    board_display()


def valid_word(word, turn) :
    global player_names, row_number, column_number, direction, org_word
    if(word.count('1') > 2) :
        return False
    if not(2 <= len(word)) :
        print("Length of word should atleast be 2")
        return False

    dictionary_file = open('dictionary.txt', 'r').read()
    dictionary_file = dictionary_file.split()
    if not(word in dictionary_file) :
        return False

    board_display()

    direction = input(f"{player_names[turn]}, Please Enter Direction (right or down): ").upper()
    while(not(direction == "RIGHT" or direction == "DOWN")) :
        direction = input(f"{player_names[turn]}, Please Enter Direction (right or down): ").upper()

    if(direction == "RIGHT") :
        row_number = int(input(f"{player_names[turn]}, Enter Row Number (1-15) : "))
        while not ((1 <= row_number) and (row_number <= 15) ) :
            row_number = int(input(f"{player_names[turn]}, Enter Row Number (1-15) : "))
        column_number = int(input(f"{player_names[turn]}, Enter Column Number (1-15) : "))
        while not( (1 <= column_number) and (column_number+len(word)-1 <= 15) ) :
            column_number = int(input(f"{player_names[turn]}, Enter Column Number (1-15) : "))

    elif(direction == "DOWN") :
        row_number = int(input(f"{player_names[turn]}, Enter Row Number (1-15) : "))
        while not((1 <= row_number) and (row_number+len(word)-1 <= 15)) :
            row_number = int(input(f"{player_names[turn]}, Enter Row Number (1-15) : "))
        column_number = int(input(f"{player_names[turn]}, Enter Column Number (1-15) : "))
        while not( (1 <= column_number) and (column_number <= 15)) :
            column_number = int(input(f"{player_names[turn]}, Enter Column Number (1-15) : "))

    return word_corresponds_board(org_word, turn, row_number, column_number, direction)

def word_corresponds_board(word, turn, row_number, column_number, direction) :
    global board, player_tiles, player_names, tiles_scores

    intersect = False
    current_tile = 0
    temp_rack = [tile for tile in player_tiles[turn]]
    if(direction == "RIGHT") :
        idx = column_number
        while (idx <= 15 and (idx-column_number) < len(word)) :
            if (word[idx-column_number] == board[row_number][idx][2]) :
                intersect = True
            elif (board[row_number][idx][2].isupper() or (word[idx-column_number] not in temp_rack) ) :
                return False
            else :
                tile_index = temp_rack.index(word[idx-column_number])
                temp_rack[tile_index] = ''
                current_tile += 1
            idx += 1

        if (idx-column_number) < len(word) :
            return False
    elif direction == "DOWN" :
        idx = row_number
        while(idx <= 15 and (idx-row_number) < len(word)) :
            if (word[idx-row_number] == board[idx][column_number][2]) :
                intersect = True
            elif(board[idx][column_number][2].isupper() or (word[idx-row_number] not in temp_rack) ) :
                return False
            else :
                tile_index = temp_rack.index(word[idx-row_number])
                temp_rack[tile_index] = ''
                current_tile += 1
            idx += 1

        if (idx-row_number) < len(word) :
            return False

    if (intersect == False) :
        print(f"{player_names[turn]}, {word} has to be matched with cluster of tiles on the board!!")
        return False

    if (current_tile == False) :
        print(f"{player_names[turn]}, {word} should make use of atleast one tile in your current tile rack{', '.join(player_tiles[turn])}")
        return False
    for tile_index in range(7) :
        if(temp_rack[tile_index] == '' and len(bag_of_tiles) != 0) :
            player_tiles[turn][tile_index] = random.sample(bag_of_tiles, 1)[0]
            bag_of_tiles.remove(player_tiles[turn][tile_index])
        elif(temp_rack[tile_index] == '') :
            player_tiles[turn][tile_index] = ''
    if(current_tile == 7) :
        tiles_scores[turn] += 50
    return True


def place_word_on_board(word) :
    global board, row_number, column_number, direction

    if direction == "RIGHT":
        for idx in range(len(word)):
            board[row_number][column_number + idx] = "| " + word[idx] + " |"

    elif direction == "DOWN":
        for idx in range(len(word)):
            board[row_number + idx][column_number] = "| " + word[idx] + " |"

def tiles_score(word):
    tile_score = 0
    for TILE in word :
        tile_score += TILE_POINTS.get(TILE)
    return tile_score


def premium_tiles_score(word, tile_score):
    global board, row_number, column_number, direction
    premium_score = 0
    i = row_number
    j = column_number

    if direction == "RIGHT":
        for idx in range(len(word)):
            if board[i][j + idx] == "|tws|":
                premium_score += (2 * tile_score)
            elif board[i][j + idx] == "|dws|":
                premium_score += (1 * tile_score)
            elif board[i][j + idx] == "|tls|":
                premium_score += (2 * TILE_POINTS.get(word[idx]))
            elif board[i][j + idx] == "|dls|":
                premium_score += TILE_POINTS.get(word[idx])
    elif direction == "DOWN":
        for idx in range(len(word)):
            if board[i + idx][j] == "|tws|" :
                premium_score += (2 * tile_score)
            elif board[i + idx][j] == "|dws|" :
                premium_score += (1 * tile_score)
            elif board[i + idx][j] == "|tls|" :
                premium_score += (2 * TILE_POINTS.get(word[idx]))
            elif board[i + idx][j] == "|dls|" :
                premium_score += TILE_POINTS.get(word[idx])
    return premium_score


def calculate_final_score() :
    global num_of_players, player_scores, player_tiles
    remaining_tiles_scores = [0 for turn in range(num_of_players+1)]
    remaining_tiles_scores[0] = -1
    for turn in range(1, num_of_players+1) :
        sum_of_rem_tile_values = 0
        for tile in range(7) :
            if(player_tiles[turn][tile] != '') :
                sum_of_rem_tile_values += TILE_POINTS.get(player_tiles[turn][tile])
        remaining_tiles_scores[turn] = sum_of_rem_tile_values

    if(0 in remaining_tiles_scores) :
        player_scores[turn] += sum(remaining_tiles_scores) + 1
    for turn in range(1, num_of_players + 1):
        player_scores[turn] -= remaining_tiles_scores[turn]


def game_winner():
    global num_of_players, player_names, player_scores
    first_highest_index = second_highest_index = 0

    for player_num in range(1, num_of_players+1):
        if player_scores[first_highest_index] < player_scores[player_num]:
            second_highest_index = first_highest_index
            first_highest_index = player_num
        elif player_scores[second_highest_index] <= player_scores[player_num]:
            second_highest_index = player_num
    print(f"Winner of the Game is {player_names[first_highest_index]} with a Highest Score of {player_scores[first_highest_index]}")
    print(f"Runner of the Game is {player_names[second_highest_index]} with Second Highest Score of {player_scores[second_highest_index]}")


def connecting_database() :
    global num_of_players, player_names, player_scores
    mydb = mysql.connector.connect(host="localhost", user="santhoshi",passwd="1234", database="scrabble")
    mycursor = mydb.cursor()
    
    mycursor.execute("""select max(score) from scores""")
    for row in mycursor :
        highest_score = row[0]
    
    current_high_score = max(player_scores)
    if(highest_score < current_high_score) :
        print(f"Congratulations!! {player_names[player_scores.index(current_high_score)]} you made a High Score of {current_high_score}")
    
    for i in range(num_of_players) :
        sql = "INSERT INTO scores (name, score) VALUES (%s, %s)"
        val = (player_names[i], player_scores[i])
        mycursor.execute(sql, val)
    mydb.commit()
    mycursor.execute("""select max(score) from scores""")
    for row in mycursor :
        highest_score = row[0]
    
    
    sql = "SELECT * FROM scores WHERE score = %s"
    val = (highest_score, )
    mycursor.execute(sql, val)
    for row in mycursor:
        print(f"Highest Score in Scrabble Game is {row[1]} ({row[0]})")


def main() :
    print("Welcome to Scrabble Game!")
    game_board_construction()
    player_details()
    game_commencement()
    calculate_final_score()
    game_winner()
    connecting_database()

if(__name__ == "__main__") :
    main()

