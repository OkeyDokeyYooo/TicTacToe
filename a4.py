#Assignment 4 CMPT310
# Author : Allen Huang 301280711
import time
import random
import math
#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
#global value

random_playouts_time = 500
win_grade = 1
# full_win_grad = 1
loss_grade = 0
tie_grade = 0.5

noughts = u"\u2B55"
crosses = u"\u274C"

TRED =  '\033[31;1m' # BOLD RED Text
ENDC = '\033[m' # reset to the defaults


board = [[" "," "," "],
        [" "," "," "],
        [" "," "," "]]

vaild_position = [[0,0], [0,1], [0,2],
                  [1,0], [1,1], [1,2],
                  [2,0], [2,1], [2,2]]

#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
#check stats functions
def is_finish(input_board):
    if is_win(input_board) or is_tie(input_board):
        return True
    else: 
        return False

def is_tie(input_board):
    if not any(" " in subl for subl in input_board) and not is_win(input_board):
        return True
    else:
        return False

def is_full_win(input_board):
    if not any(" " in subl for subl in input_board) and is_win(input_board):
        return True
    else:
        return False

def is_win(input_board):
    row_list = generate_row_list(input_board)
    column_list = generate_column_list(input_board)
    diagonal_list = generate_diagonal_list(input_board)
    
    if check_has_win(row_list) or check_has_win(column_list) or check_has_win(diagonal_list):
        return True

    return False

def generate_row_list(lst):
    row_list = []
    for i in range(len(lst)):
        row_list.append(lst[i])
    return row_list


def generate_column_list(lst):
    column_list = []
    for column in range(len(lst)):
        temp_list = []
        for row in range(len(lst[column])):
            temp_list.append(lst[row][column])
        column_list.append(temp_list)
    return column_list


def generate_diagonal_list(lst):
    diagonal_list = []
    temp = []
    for i in range(len(lst)):
        temp.append(lst[i][i])
    diagonal_list.append(temp)

    temp = []
    i = 0
    for j in range(len(lst) - 1, -1, -1):
        temp.append(lst[i][j])
        i += 1
    diagonal_list.append(temp)
    return diagonal_list

def check_has_win(twoD_lst):
    for i in range(len(twoD_lst)):
        if is_all_same(twoD_lst[i]):
            return True
    return False

def is_all_same(lst):
    current = lst[0]
    if current == "noughts":
        for i in range(1, len(lst)):
            if current != lst[i]:
                return False
        return True
    elif current == "crosses":
        for i in range(1, len(lst)):
            if current != lst[i]:
                return False
        return True
    else:
        return False
#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
#helper function, display the board
def display_board(input_board):
    for i in range(len(input_board)):
        print("\t\t       |       |       ")
        print("\t\t", end='')
        for j in range(len(input_board[i])):
            if j == len(input_board[i]) - 1:
                if input_board[i][j] == "crosses":
                    print("   " + crosses, end='   ')
                elif input_board[i][j] == "noughts":
                    print("   " + noughts, end='   ')
                else:
                    print("   " + " ",     end='   ')
            else:
                if input_board[i][j] == "crosses":
                    print("   " + crosses, end='   |')
                elif input_board[i][j] == "noughts":
                    print("   " + noughts, end='   |')
                else:
                    print("   " + " ",     end='   |')

            if j == len(input_board[i]) - 1 and i < 2:
                print("\n\t\t       |       |       ", end='')
                print("\n\t\t–––––––|–––––––|–––––––")
            if j == 2 and i == 2:
                print("\n\t\t       |       |       ")

def display_sample():
    print("\n\t\t       |       |       ")
    print("\t\t (0,0) | (0,1) | (0,2) ")
    print("\t\t       |       |       ")
    print("\t\t–––––––|–––––––|–––––––")
    print("\t\t       |       |       ")
    print("\t\t (1,0) | (1,1) | (1,2) ")
    print("\t\t       |       |       ")
    print("\t\t–––––––|–––––––|–––––––")
    print("\t\t       |       |       ")
    print("\t\t (2,0) | (2,1) | (2,2) \n")



#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# AI Helper Function
def change_board_stat(x , y, piece):
    board[x][y] = piece

def change_AI_board_stat(x, y, piece, input_board):
    temp_board = list(map(list, input_board))
    temp_board[x][y] = piece
    return temp_board

def find_opponent_choice(opponent_choice):
    if opponent_choice == "noughts":
        return "crosses"
    else:
        return "noughts"

def filp_fair_coin():
    if random.random() > 0.5:
        return win_grade
    else :
        return loss_grade

# def is_AI_lose(input_board, player_choice):
    
#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
#AI: using pure Monte Carlo Tree Search (pMCTS)
def AI_turn(AI_choice):
    AI_leagl_move = list(map(list, vaild_position))
    
    if len(AI_leagl_move) == 1:
        the_AI_move = AI_leagl_move.pop()
        print("AI choose:" + str(the_AI_move))
        vaild_position.remove(the_AI_move)
        change_board_stat(the_AI_move[0], the_AI_move[1], AI_choice)
        display_board(board)
        return 

    AI_board = list(map(list, board)) # deep copy the board
    AI_grade_list = [0] * len(vaild_position)
    player_choice = find_opponent_choice(AI_choice)
    index = 0

    for next_move in AI_leagl_move:

        temp_board = list(map(list, AI_board))
    
        total_win = 0
        total_depth = 0
        for i in range(random_playouts_time):
            temp_leagl_move = list(map(list, AI_leagl_move))
            temp_leagl_move.remove(next_move)
            total_win += make_rand_move(temp_leagl_move,temp_board, AI_choice, player_choice, next_move)

        
        AI_grade_list[index] = (total_win) 
        # / total_depth  + 2 * math.sqrt(math.log(total_depth)/random_playouts_time) 
        index += 1
    
    # print("AI GRADE LIST:   " + str(AI_grade_list))
    # print("AI POSSIBLE LIST:" + str(AI_leagl_move))

    the_AI_move = AI_leagl_move[AI_grade_list.index(max(AI_grade_list))]
    print("AI choose:" + str(the_AI_move))
    vaild_position.remove(the_AI_move)
    change_board_stat(the_AI_move[0], the_AI_move[1], AI_choice)
    display_board(board)
        

#random playouts
def make_rand_move(leagl_move,input_board, AI_choice, player_choice, AI_move):
    input_board = change_AI_board_stat(AI_move[0], AI_move[1],  AI_choice, input_board)
    if is_win(input_board):
        return win_grade
    if is_tie(input_board):
        return filp_fair_coin()
    # if is_full_win(input_board):
    #     return full_win_grad

    while True:

        player_next_move = leagl_move.pop(random.randint(0, len(leagl_move) - 1))
        # print("user choice: " + str(player_next_move))
        input_board = change_AI_board_stat(player_next_move[0], player_next_move[1], player_choice, input_board)
        # print("user move: ")
        # display_board(input_board)
        # time.sleep(1)

        if is_win(input_board):
            return loss_grade
        if is_tie(input_board):
            return tie_grade
        
        AI_next_move = leagl_move.pop(random.randint(0, len(leagl_move) - 1))
        # print("AI choice: " + str(AI_next_move))
        input_board = change_AI_board_stat(AI_next_move[0], AI_next_move[1], AI_choice, input_board)
        # print("AI move: ")
        # display_board(input_board)
        # time.sleep(1)

        # if is_full_win(input_board):
        #     return full_win_grad, depth
        if is_win(input_board):
            return win_grade
        if is_tie(input_board):
            return tie_grade

#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
#play_a_new_game
def init_game():
    print("Starting a New Game...")
    display_sample()
    player_choice = input("Pick a Piece ( x or o )\n : ")
    while player_choice not in ["x", "o"]:
            player_choice = input("Wrong input, must be x or o: ")
    player_order = input("Choose Digit: 1 -> Go first , 2 -> Go after\n : ")
    while player_order not in ["1", "2"]:
        player_order = input("Wrong input, must be digit 1 or 2: ")
    
    if player_choice == "x":
        player_choice = "crosses"
    else:
        player_choice = "noughts"
    
    if player_order == "1":
        player_order = "first"
    else:
        player_order = "seconde"
    return player_choice, player_order

def right_form():
    player_move = input("you want put your piece to where, choose from below\n" + str(vaild_position) + "\n example format : 0 0 \n :")
    player_move = player_move.split(' ')
    while len(player_move) != 2 or player_move[0] not in ['0', '1', '2'] or player_move[1] not in ['0', '1', '2']:
        player_move = input("Not the right format, please type like the example format : 0 0 \n :")
        player_move = player_move.split(' ') 
    return player_move  

def player_turn(player_choice):
        player_move = right_form()
        player_x = int(player_move[0])
        player_y = int(player_move[1])
        while [player_x, player_y] not in vaild_position:
                player_move = input("Not vaild position, choose from below\n" + str(vaild_position) + "\n example format : 0 0")
                player_move = right_form()  
                player_x = int(player_move[0])
                player_y = int(player_move[1])

        vaild_position.remove([player_x, player_y])
        change_board_stat(player_x, player_y, player_choice)
        display_board(board)

def play_a_new_game():
    player_choice, player_order = init_game()
    AI_choice = find_opponent_choice(player_choice)
    if player_order == "first":
        while True:
            player_turn(player_choice)
            if is_win(board):
                print(TRED+"\nGame Over, You Win!!!",ENDC)
                return
            if is_tie(board):
                print(TRED+"\nGame Over, Tie Game!!!",ENDC)
                return
            AI_turn(AI_choice)
            if is_win(board):
                print(TRED+"\nGame Over, You Lose!!!",ENDC)
                return
            if is_tie(board):
                print(TRED+"\nGame Over, Tie Game!!!",ENDC)
                return
    else:
        while True:
            AI_turn(AI_choice)
            if is_win(board):
                print(TRED+"\nGame Over, You Lose!!!",ENDC)
                return
            if is_tie(board):
                print(TRED+"\nGame Over, Tie Game!!!",ENDC)
                return
            player_turn(player_choice)
            if is_win(board):
                print(TRED+"\nGame Over, You Win!!!",ENDC)
                return
            if is_tie(board):
                print(TRED+"\nGame Over, Tie Game!!!",ENDC)
                return 


#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# minimax alg
def make_change(board, x, y, chess):
    board[x][y] = chess

def remove_element(lst , ele):
    for element in lst:
        if element == ele:
            

def minimax_alg (game_board, vaild_position, MIN_or_MAX):
    grade_list[len(vaild_position)] = {0}
    for move in vaild_position:
        temp_move_list = list(map(list, vaild_position));
        temp_move_list.pop(move);

        
    


#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
#Main Function
if __name__ == '__main__':
    # minimax_alg(board);
    # play_a_new_game()
