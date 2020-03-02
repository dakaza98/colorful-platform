import curses
import os
import time
import random
import numpy as np
import itertools

def read_map(path):
    """
    Reads a text file and returns it as a string


    Keyword arguments:
    path -- path of the file

    """
    try:        
        board = open( path,'r')
        board_txt = board.read()
        board.close() 
        
        return board_txt
    except IOError:
        
        raise Exception("Can not find the file at this path => "+ path)

def convert_map_to_coordinates(str_board):
    """
    Converts the string version of the map to coordinates
 
    Returns a list of lists where every list has [char,xPos,Ypos]
    Example "X  " => [['X', 0, 0], [' ', 1, 0], [' ', 2, 0]...,]

    Keyword arguments:
    str_board -- the string version of the map
    """
 
    matrix = [[x for x in line] for line in str_board.split('\n')]

    map_coordinates = []
    y = 0
    for row in matrix:
        x = 0
        for c in row:
            char_xy = [c,x,y]    
            map_coordinates.append(char_xy)
            x += 1
        y += 1
    
    return map_coordinates

          
def make_plus_list(map_coordinates):
    """
    Finds all the "+" chars in  map_coordinates 
    Returns a list of lists where every list has ["+",xPos,Ypos]
    Example [['X', 0, 0], [' ', 1, 0],...,['+', '4', '0']] => [['+', '4', '0'],...]
    """
    plus_list = []
    for cord in map_coordinates:
        if cord[0] == "+":
            plus_list.append([cord[0],int(cord[1]),int(cord[2])])
    return plus_list

def print_player_names(screen,player1_name,player2_name):
    """Prints the playernames in the screen 

    Keyword arguments:
    screen -- the curses screen
    player1_name -- player1 name as string
    player2_name -- player2 name as string
    """
    h,w = screen.getmaxyx()

    player1_name_x = -10 + w//3   
    player1_name_y = 4
    screen.addstr(player1_name_y,player1_name_x,"Player1",curses.color_pair(3))
    screen.addstr(player1_name_y+1,player1_name_x,player1_name,curses.color_pair(3))

    player2_name_x = 29  + w//3 
    player2_name_y = 4
    screen.addstr(player2_name_y,player2_name_x,"Player2",curses.color_pair(2))
    screen.addstr(player2_name_y+1,player2_name_x,player2_name,curses.color_pair(2))
    
         

def print_map(screen,map_coordinates,stone_pool_player1,stone_pool_player2,phase):
    """Prints the all the chars except "+" in map_coordinates at their specified coordinate,
    the current the phase and stone pools for both players.

    Keyword arguments:
    screen -- the curses screen
    
    map_coordinates -- A list of lists where every list has the form [char, xPos, yPos]
    stone_pool_player1 -- The amount of stone player1 has left to place
    stone_pool_player2 -- The amount of stone player2 has left to place
    phase -- the current phase of the game
    """
    for cord in map_coordinates:

        char = cord[0]
        
        if char == "+":        
            continue

        h,w = screen.getmaxyx()

        #To place the game board in the center of the window  
        y = cord[2]+ 9
        x = cord[1] +  w//3    
       
        color = which_color_pair(char)

        screen.addstr(y,x,char,curses.color_pair(color))

        #print phase
        phase_y =  4
        phase_x =  6 + w//3
        screen.addstr(phase_y,phase_x,"Phase: "+str(phase),curses.color_pair(5))

        #Posistions of the stones showing on the left and right side of the game board
        stone_pool_player1_x = -9 + w//3   
        stone_pool_player1_y = 9

        for i in range(stone_pool_player1):

            screen.addstr(stone_pool_player1_y+i,stone_pool_player1_x,"X",curses.color_pair(3))

        stone_pool_player2_x = 30  + w//3 
        stone_pool_player2_y = 9
        for i in range(stone_pool_player2):
            screen.addstr(stone_pool_player2_y+i,stone_pool_player2_x,"O",curses.color_pair(2))

def print_remaining_stone(screen,remaining_stones_player1,remaining_stones_player2):
    """Prints the amount of stones left for player1 and player2 at the left and right side of the board

    Keyword arguments:
    screen -- the curses screen
    remaining_stones_player1 = the total amount of stones for player1
    remaining_stones_player2 = the total amount of stones for player2
    """
    h,w = screen.getmaxyx()

    #Positions of the text showing the remaining stones for player1 
    remaining_stones_player1_x = -22 + w//3   
    remaining_stones_player1_y = 7
    screen.addstr(remaining_stones_player1_y,remaining_stones_player1_x,"Remaining stones: "+str(remaining_stones_player1),curses.color_pair(3))

    #Positions of the text showing the remaining stones for player2 
    remaining_stones_player2_x = 30 + w//3   
    remaining_stones_player2_y = 7
    screen.addstr(remaining_stones_player2_y,remaining_stones_player2_x,"Remaining stones: "+str(remaining_stones_player2),curses.color_pair(2))


def print_choice(screen, selected_move_idx, plus_list,player1_turn):
    """Prints all plusses in plus_list on the screen. The currently selected plus is colored.

    Keyword arguments:
    screen -- the curses screen
    selected_move_idx -- the currently selected row in the plus_list
    plus_list -- the lists of all the "+" and their positions
    player1_turn -- bool,True for player1  and False for player2
    """    
    h, w = screen.getmaxyx()
    for idx, row in enumerate(plus_list):

        # To have  the game board in the center, 5 is added y and w//3 is added to x
        y = int(row[2])+ 9
        x = int(row[1]) +  w//3      
        color =which_color_pair(row[0])
        if idx == selected_move_idx:
            color_cursor = 1
            #cursor will now have the player colors
            if player1_turn == False:
                color_cursor = 4
            screen.attron(curses.color_pair(color_cursor))
            screen.addstr(y,x, row[0])
            screen.attroff(curses.color_pair(color_cursor))
        else:
            screen.addstr(y, x, row[0],curses.color_pair(color))
   

def which_color_pair(stone_marker):
    """Picks a which color that will be choosed for the stone,
    depening if its an "O" or "x" 
    Returns color which is an int that represents the color_pair
    
    Keyword arguments:
    stone_marker -- char of the stone

    """
    color = 0

    if stone_marker== "O":
        color = 2
    elif stone_marker == "X" :
        color = 3
    return color

def move_down(plus_list,current_row):
    """ Finds the "+" char that is below the current_row. If the current "+" char is at the bottom, 
        it finds the "+" char at the top with the same x position
    Returns the new y position of the "+" 

    Keyword arguments:
    current_row -- the currently selected row in the plus_list
    plus_list -- the lists of all the "+" and their positions
    """
    
    new_row = current_row
    
    while True:
        new_row += 1
        if new_row == len(plus_list):
            new_row = 0
        
        current_x = plus_list[current_row][1]
        new_x = plus_list[new_row][1]

        current_y = plus_list[current_row][2]
        new_y = plus_list[new_row][2]
        if current_x == new_x and current_y != new_y:
          return new_row 

def move_up(plus_list,current_row):
    """ Finds the "+" char that is above the current_row. If the current "+" char is at the top, 
        it finds the "+" char at the bottom with the same x position
    Returns the new y position of the "+" 


    current_row -- the currently selected row in the plus_list
    plus_list -- the lists of all the "+" and their positions
    """
    
    new_row = current_row
    
    while True:
        if new_row == 0:
            new_row = len(plus_list)
        
        new_row -= 1
        current_x = plus_list[current_row][1]
        new_x = plus_list[new_row][1]

        current_y = plus_list[current_row][2]
        new_y = plus_list[new_row][2]
        if current_x == new_x and current_y != new_y:
     
          return new_row  



def place_stone(plus_list,current_row,stone_marker,stone_pool_player1,stone_pool_player2):
    """ Places a stone on the map by changing the "+" to "X" or "O"
    Returns the changed plus_list list

    current_row -- the currently selected row in the plus_list
    plus_list -- the lists of all the "+" and their positions
    stone_marker -- the char of the stone, should be either "X" or "O" 
    stone_pool_player1 -- The amount of stone player1 has left to place
    stone_pool_player2 -- The amount of stone player2 has left to place
    
    """
    if stone_marker == "X":
        stone_pool_player1 = stone_pool_player1-1
    elif stone_marker == "O":
        stone_pool_player2 = stone_pool_player2 -1    

    plus_list[current_row][0] = stone_marker
    return plus_list,stone_pool_player1,stone_pool_player2


def which_stone(player1_turn):
    """Picks which char the stone marker should be based on which player is next to act
    Return stone_marker, which can either be a "X" or "O" depending on who is placing the stone

    Keyword arguments:
    player1_turn -- bool,True for player1  and False for player2

    """
    stone_marker = "X"
    if player1_turn == False:
        stone_marker = "O"
    return stone_marker    

def switch_player_turn(player1_turn):
    """Switches which player turn it is to act
    Return player1_turn , which boolean value get switched to let the other player act
    Keyword arguments:
    player1_turn -- bool, True is player1 turn and False is player2 turn
    
    """
    return not player1_turn

def random_player_start():
    """Determine which player that will start to act. 
    Returns a bool , True for player1 and False for player2 
    """
    player_start = random.randint(1,2)
    if player_start == 1:
        return True
    return False

    
def print_player_start(screen,player1_turn,player1_name,player2_name):
    """ Prints the name of player who will start to act at the top of the screen
    
    Keyword arguments:
    screen -- the curses screen
    player1_turn -- bool, True is player1 turn and False is player2 turn    
    player1_name -- player1 name as string
    player2_name -- player2 name as string

    """
    h,w = screen.getmaxyx()

    #position of text 
    text_x = 4  + w//3 
    text_y = 1
    
    if player1_turn == True:
          if len(player1_name) ==0:
              player1_name = "Player1"   
          screen.addstr(text_y,text_x,player1_name.rstrip("\n")+" will start!",curses.color_pair(3))
    else:
        if len(player2_name) ==0:
            player2_name = "Player2"        
        screen.addstr(text_y,text_x,player2_name.rstrip("\n")+" will start!",curses.color_pair(2))

def print_player_remove(screen,player1_turn,player1_name,player2_name):
    """ Prints the name of player who will be able to remove a stone at the top of the screen
    
    Keyword arguments:
    screen -- the curses screen
    player1_turn -- bool, True is player1 turn and False is player2 turn    
    player1_name -- player1 name as string
    player2_name -- player2 name as string

    """
    h,w = screen.getmaxyx()

    #position of text 
    text_x = 3  + w//3 
    text_y = 2
    
    if player1_turn == True:
          if len(player1_name) ==0:
              player1_name = "Player1"   
          screen.addstr(text_y,text_x,player1_name.rstrip("\n")+" remove a stone!",curses.color_pair(3))
    else:
        if len(player2_name) ==0:
            player2_name = "Player2"        
        screen.addstr(text_y,text_x,player2_name.rstrip("\n")+" remove a stone!",curses.color_pair(2))


def can_player_act(plus_list,current_row,stone_pool_player1, stone_pool_player2,player1_turn):
    """Determines if a player is allowed to act
    Returns bool -- Can player act = True else False

    Keyword argument 
    plus_list -- list of "+" and placed stones
    current_row --  currently selected row in the plus_list
    stone_pool_player1 -- the amount of stone player1 has
    stone_pool_player2 -- the amount of stone player2 has
    player1_turn -- bool, True is player1 turn and False is player2 turn    
      
    """
    current_char = plus_list[current_row][0]
    can_not_act= (stone_pool_player1 <=  0 and stone_pool_player2 <= 0) or current_char != "+"
    if can_not_act == True:    
        return False

    return True



def can_player_remove(plus_list,current_row,player1_turn):
    """Determines if a player can remove a stone
    Returns bool -- Can player remove a stone = True else False

    Keyword argument 
    plus_list -- list of "+" and placed stones
    current_row --  currently selected row in the plus_list
    player1_turn -- bool, True is player1 turn and False is player2 turn    
    """
    current_car = plus_list[current_row][0]
    remove_stone_marker = "O"
    if player1_turn == False:
        remove_stone_marker = "X"
    if current_car == remove_stone_marker:
        return True
    return False        


def convert_map_matrix(str_board):
    """
    Converts the string version of the map to a matrix

    Returns a matrix of all  the chars is the string version of the map

    Keyword arguments:
    str_board -- the string version of the map
    """
    matrix = [[x for x in line] for line in str_board.split('\n')]
    return matrix



def check_row(matrix,player1_turn,list_3_row):
    """Checks if the game board has three of the same stones in a row vertically.
    
    Returns list_3_row and is_three_row -- bool, will be True if a new three in a row has been found  
    Keyword arguments:
    matrix -- the matrix of the board
    player1_turn -- bool, True is player1 turn and False is player2 turn    
    list_3_row -- list of all the three in a row that has been found
    """
    player_stone = 'X'
    opponent_stone = 'O'
    pre_list_3_row = list_3_row
    is_three_row = False
    if player1_turn == False:
        player_stone = 'O'
        opponent_stone = 'X'
    for id_row,row in enumerate(matrix):
        check_player = []
        found_player_stone = False
        for item in row:
            if item == player_stone:
                found_player_stone = True
            if item == ' ' or item == opponent_stone or item == '|':
                check_player = []
                found_player_stone = False     
            if found_player_stone == True and item != ' ':
                check_player.append(item)
            amount_player_stone = check_player.count(player_stone) 
            if check_player and all(elem ==player_stone or elem == '-' for elem in check_player ) and amount_player_stone == 3:
                if ([id_row]+check_player) not in list_3_row:
                    is_three_row = True
                    list_3_row.append([id_row]+check_player)

    return list_3_row,is_three_row    
    
    

                 
def check_col(matrix,player1_turn,list_3_col):
    """Checks if the game board has three of the same stones in a row horizontally.
    
    Returns list_3_col  and is_three_column -- bool, will be True if a new three in a row in a column has been found  
    Keyword arguments:
    matrix -- the matrix of the board
    player1_turn -- bool, True is player1 turn and False is player2 turn    
    list_3_col -- list of all the three in a row in a column that has been found
    """    
    transponse_matrix = np.transpose(matrix)
    player_stone = 'X'
    opponent_stone = 'O'
    is_three_col = False
    pre_list_3_col = list_3_col
    if player1_turn == False:
        player_stone = 'O'
        opponent_stone = 'X'
    for id_col,row in enumerate(transponse_matrix):
        check_player = []
        found_player_stone = False
        for item in row:
            if item == player_stone:
                found_player_stone = True
            if item == ' ' or item == opponent_stone or item == '-':
                check_player = []
                found_player_stone = False     
            if found_player_stone == True and item != ' ':
                check_player.append(item)
            amount_player_stone = check_player.count(player_stone) 
            if check_player and all(elem ==player_stone or elem == '|' for elem in check_player ) and amount_player_stone == 3:
                if ([id_col]+check_player) not in list_3_col:
                    is_three_col = True
                    list_3_col.append([id_col]+check_player)
 
    return list_3_col,is_three_col
                
def check_both(matrix,list_3_row,list_3_col,player1_turn):
    """Checks if the game board has three of the same stones in a row either vertically or horizontally.
    
    Returns  list_3_row ,list_3_col,bool which will be True if a new three in a row has been found  
    Keyword arguments:
    matrix -- the matrix of the board
    player1_turn -- bool, True is player1 turn and False is player2 turn
    list_3_row -- list of all the three in a row that has been found
    list_3_col -- list of all the three in a row in a column that has been found
    """        
    list_3_row,is_three_row = check_row(matrix,player1_turn,list_3_row)
    list_3_col,is_three_col = check_col(matrix,player1_turn,list_3_col)
    if is_three_row == True or is_three_col == True:
        return list_3_row,list_3_row,True
    
    return list_3_row,list_3_row,False

    

def plus_list_to_matrix(plus_list,matrix):
    """Converts plus_list to a matrix
 
    Returns: matrix

    Keyword arguments:
    matrix -- matrix of all  the chars is the string version of the map
    plus_list -- the lists of all the "+" and their positions    
    """    
    for row in plus_list:
        x = int(row[1]) 
        y = int(row[2])
        matrix[y][x]= row[0]
    
    return matrix        


def remove_stone_player(plus_list,current_row,player1_turn,stone_pool_player1,stone_pool_player2):
    """ Places a removes on the map by changing the player stone to a "+"
    Returns the changed plus_list list

    current_row -- the currently selected row in the plus_list
    plus_list -- the lists of all the "+" and their positions
    stone_pool_player1 -- The amount of stone player1 has left to place
    stone_pool_player2 -- The amount of stone player2 has left to place
    
    """
    if player1_turn == True: 
        remove_stone_marker = "O"
        stone_pool_player2 = stone_pool_player2 -1
    
    elif player1_turn == False:

        remove_stone_marker = "X" 
        stone_pool_player1 = stone_pool_player1 -1

    if plus_list[current_row][0] == remove_stone_marker:    
        plus_list[current_row][0] = "+"
    

    return plus_list,stone_pool_player1,stone_pool_player2

def switch_to_phase2(phase,stone_pool_player1,stone_pool_player2):
    """ Switches to phase2 if both stone pools of the player are empty
    Return: Phase

    Keyword arguments:
    phase -- the current phase of the game 
    stone_pool_player1 -- The amount of stone player1 has left to place
    stone_pool_player2 -- The amount of stone player2 has left to place
    """
    if stone_pool_player1 == 0 and stone_pool_player2 == 0:
        phase = 2
    return phase

def can_player_move_stone(plus_list,current_row,player1_turn):
    stone_marker = "X"
    if player1_turn == False:
        stone_marker = "O"
    current_stone_y = plus_list[current_row][2]
    current_stone_x = plus_list[current_row][1]
    
    if plus_list[current_row][0] == stone_marker and "+" in itertools.chain( *neighbours):
        return True
    return False

def get_selected_stone_index(current_row):
    return current_row    

def  move_stone(plus_list,current_row,player1_turn,selected_stone_index):
    stone_marker = "X"
    if player1_turn == False:
        stone_marker = "O"
    plus_list[selected_stone_index][0] = "+"
    plus_list[current_row][0] = stone_marker
    return plus_list

def find_stone_neighbour_row(plus_list,matrix,current_row):
    current_stone_y = int(plus_list[current_row][2])
    current_stone_x = int(plus_list[current_row][1])
    row = matrix[current_stone_y]
    neighbours = []

    # look a head for neighbour
    for x in reversed(range(0,current_stone_x)):
        elem = matrix[current_stone_y][x]
        if elem == " ":
            break
        elif (elem == "X" or elem == "O" or elem == "+") and x != current_stone_x:
            neighbours.append([elem,x,current_stone_y])

            break

    for x in range(current_stone_x,len(row)):
        elem = matrix[current_stone_y][x]
        if elem == " ":
            break
        elif (elem == "X" or elem == "O" or elem == "+") and x != current_stone_x:
            neighbours.append([elem,x,current_stone_y])
            
            break
   
    return neighbours                    


def find_stone_neighbour_col(plus_list,matrix,current_row):
    #flipps the matrix so row becomes the columns ande vice versa
    matrix = np.transpose(matrix)
    current_stone_y = int(plus_list[current_row][2])
    current_stone_x = int(plus_list[current_row][1])
    col = matrix[current_stone_x]
    neighbours = []
    # look a head for neighbor
    for y in reversed(range(0,current_stone_y)):
        elem = matrix[current_stone_x][y]
        if elem == " ":
            break
        elif (elem == "X" or elem == "O" or elem == "+") and y != current_stone_y:
            neighbours.append([elem,current_stone_x,y])
            
            break

    for y in range(current_stone_y,len(col)):
        elem = matrix[current_stone_x][y]
        if elem == " ":
            break
        elif (elem == "X" or elem == "O" or elem == "+") and y != current_stone_y:
            neighbours.append([elem,current_stone_x,y])

            break
    return neighbours   

def find_all_neighbours(plus_list,matrix,current_row):
    neighbour_row  = find_stone_neighbour_row(plus_list,matrix,current_row)
    neighbour_col = find_stone_neighbour_col(plus_list,matrix,current_row)
    neighbours = neighbour_row + neighbour_col
    return neighbours 

def is_neighbour_a_plus(plus_list,current_row,neighbours):
    elem = plus_list[current_row]
    print(True)   
    if elem[0] == "+" and elem in neighbours:
        return True
    return False    

def remove_old_3(plus_list,current_row,list_3_row,list_3_col):
    current_stone_x = plus_list[current_row][1]
    current_stone_y = plus_list[current_row][2]
    for row in list_3_row:
        if current_stone_x == row[0]:
            list_3_row.remove(row)
    for col in list_3_col:
        if current_stone_y == col[0]:
            list_3_col.remove(col)        

    return list_3_row,list_3_col
        
def print_player_move(screen,player1_turn,player1_name,player2_name):
    """ Prints the name of player who will be able to move a stone at the top of the screen
    
    Keyword arguments:
    screen -- the curses screen
    player1_turn -- bool, True is player1 turn and False is player2 turn    
    player1_name -- player1 name as string
    player2_name -- player2 name as string

    """
    h,w = screen.getmaxyx()

    #position of text 
    text_x = 1  + w//3 
    text_y = 2
    
    if player1_turn == True:
        if len(player1_name) ==0:
            player1_name = "Player1"   
        screen.addstr(text_y,text_x,player1_name.rstrip("\n")+" move a stone to a neighbour!",curses.color_pair(3))
    else:
        if len(player2_name) ==0:
            player2_name = "Player2"        
        screen.addstr(text_y,text_x,player2_name.rstrip("\n")+" move a stone to a neighbour!",curses.color_pair(2))

def main(screen,player1_name,player2_name):
    """ The game loop used by curses.

    Keyword arguments:
    screen -- the curses screen
    player1_name -- The name of player1 as a string
    player2_name -- The name of player2 as a string
    
    """
    # turn off cursor blinking
    curses.curs_set(0)  

    # color scheme for selected row player1
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)
    
    # color scheme for selected row player2
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)


    # color scheme for player1        
    curses.init_pair(3,curses.COLOR_RED,curses.COLOR_BLACK)
    
    # color scheme for player2
    curses.init_pair(2,curses.COLOR_YELLOW,curses.COLOR_BLACK)

    # color scheme for phase 
    curses.init_pair(5,curses.COLOR_CYAN,curses.COLOR_BLACK)        
    # specify the current selected row
    current_row = 0

    # The path of the textfile of the map
    map_path = 'Ascii_board.txt'
    #string of the map
    map_string = read_map(map_path)
    
    #test
    matrix = convert_map_matrix(map_string)
    #test_ends

    #coordinates of the chars in the map
    map_coordinates =convert_map_to_coordinates(map_string)
    
    # plus_list, coordinates of the "+" chars in the map_coordinates list 
    plus_list = make_plus_list(map_coordinates)
    
    #player_1turn will determine which player that will start ,True for player1
    player1_turn = random_player_start()
    
    #The amount of stones left to be placed,if these amounts = 0 phase1 ends
    stone_pool_player1 = 9
    stone_pool_player2 = 9

    #The total amount of stones, if one of these amounts <= 2 that player loses
    remaining_stones_player1 = 9
    remaining_stones_player2 = 9
    
    #Prints player start text once
    print_once = 0
    list_3_row = []
    list_3_col = []
   
    #If player has removed a stone = True else False
    stone_removed = True

    #Which phase
    phase = 1


    #phase 2 stuff
    is_stone_selected = False
    while phase == 1 :
        phase = switch_to_phase2(phase,stone_pool_player1,stone_pool_player2)
        # switch phases should maybe be done is a different way    
        if phase != 1 : 
            break

        screen.clear()
    
                
        if print_once == 0: 
            print_player_start(screen,player1_turn,player1_name,player2_name)
            print_once += 1    

        if stone_removed == False:
            print_player_remove(screen,player1_turn,player1_name,player2_name)

        
        print_map(screen,map_coordinates,stone_pool_player1,stone_pool_player2,phase)            
        print_player_names(screen,player1_name,player2_name)
        print_choice(screen,current_row,plus_list,player1_turn)
        print_remaining_stone(screen,remaining_stones_player1,remaining_stones_player2)
        screen.refresh()    
        
        phase = switch_to_phase2(phase,stone_pool_player1,stone_pool_player2)
        # switch phases should maybe be done is a different way    
        if phase != 1:
            break

        key = screen.getch()
        if key == curses.KEY_LEFT and current_row > 0:  
            current_row -= 1
        elif key == curses.KEY_RIGHT and current_row < len(plus_list)-1:
            current_row += 1
        elif key == curses.KEY_DOWN:
            current_row = move_down(plus_list,current_row)

        elif key == curses.KEY_UP:
            current_row = move_up(plus_list,current_row)

        elif key == curses.KEY_ENTER or key in [10, 13]:
           
            player_can_act = can_player_act(plus_list,current_row,stone_pool_player1,stone_pool_player2,player1_turn) 
            if player_can_act == True and stone_removed == True:

                stone_marker=which_stone(player1_turn)
                plus_list,stone_pool_player1,stone_pool_player2 = place_stone(plus_list,current_row,stone_marker,stone_pool_player1,stone_pool_player2)
                matrix = plus_list_to_matrix(plus_list,matrix)
                 
                list_3_row,list_3_col,has_player_3_row = check_both(matrix,list_3_row,list_3_col,player1_turn)
                
                if has_player_3_row == True:
                    stone_removed = False
                else:
                    player1_turn = switch_player_turn(player1_turn)  

            elif has_player_3_row == True  and stone_removed == False and can_player_remove(plus_list,current_row ,player1_turn)  == True:
                                    
                plus_list,remaining_stones_player1,remaining_stones_player2= remove_stone_player( plus_list,current_row,player1_turn,remaining_stones_player1,remaining_stones_player2)
                matrix = plus_list_to_matrix(plus_list,matrix)
                list_3_row,list_3_col = remove_old_3(plus_list,current_row,list_3_row,list_3_col)
                player1_turn = switch_player_turn(player1_turn)
                stone_removed = True
        # 27 = Escape key
        elif key == 27:     
            quit()
        
        # Prevent the screen from repainting to often
        time.sleep(0.01)
    
    #phase2
    while phase == 2:
        #here should phase 2 be
        screen.clear()
                
        if stone_removed == False:
            print_player_remove(screen,player1_turn,player1_name,player2_name)

        if is_stone_selected == False and stone_removed == True:
            print_player_move(screen,player1_turn,player1_name,player2_name)
        
        print_map(screen,map_coordinates,stone_pool_player1,stone_pool_player2,phase)            
        print_player_names(screen,player1_name,player2_name)
        print_choice(screen,current_row,plus_list,player1_turn)
        print_remaining_stone(screen,remaining_stones_player1,remaining_stones_player2)
        screen.refresh()    
        
        # switch phases should maybe be done is a different way    
        

        key = screen.getch()
        if key == curses.KEY_LEFT and current_row > 0:  
            current_row -= 1
        elif key == curses.KEY_RIGHT and current_row < len(plus_list)-1:
            current_row += 1
        elif key == curses.KEY_DOWN:
            current_row = move_down(plus_list,current_row)

        elif key == curses.KEY_UP:
            current_row = move_up(plus_list,current_row)

        elif key == curses.KEY_ENTER or key in [10, 13]:
            player_can_move_stone = can_player_move_stone(plus_list,current_row,player1_turn)
            if player_can_move_stone == True and stone_removed == True and is_stone_selected == False:
                stone_marker=which_stone(player1_turn)
                selected_stone_index = get_selected_stone_index(current_row)
                is_stone_selected = True
                matrix = plus_list_to_matrix(plus_list,matrix)
                neighbours = find_all_neighbours(plus_list,matrix,current_row)
                list_3_row,list_3_col,has_player_3_row = check_both(matrix,list_3_row,list_3_col,player1_turn)
                
                if has_player_3_row == True:
                    stone_removed = False
                elif is_stone_selected == False:
                    player1_turn = switch_player_turn(player1_turn)

            elif is_neighbour_a_plus(plus_list,current_row,neighbours) == True and is_stone_selected == True and stone_removed == True:
                plus_list = move_stone(plus_list,current_row,player1_turn,selected_stone_index)
                matrix = plus_list_to_matrix(plus_list,matrix)
                list_3_row,list_3_col = remove_old_3(plus_list,current_row,list_3_row,list_3_col)
                list_3_row,list_3_col,has_player_3_row = check_both(matrix,list_3_row,list_3_col,player1_turn)
                is_stone_selected = False
                neighbours = []
                if has_player_3_row == True:
                    stone_removed = False
                elif is_stone_selected == False:
                    player1_turn = switch_player_turn(player1_turn)  
                    
            elif has_player_3_row == True  and stone_removed == False and is_stone_selected == False  and can_player_remove(plus_list,current_row ,player1_turn)  == True:
                plus_list,remaining_stones_player1,remaining_stones_player2= remove_stone_player( plus_list,current_row,player1_turn,remaining_stones_player1,remaining_stones_player2)
                matrix = plus_list_to_matrix(plus_list,matrix)
                list_3_row,list_3_col = remove_old_3(plus_list,current_row,list_3_row,list_3_col)
                player1_turn = switch_player_turn(player1_turn)
                stone_removed = True
        # 27 = Escape key
        elif key == 27:     
            quit()
        # Prevent the screen from repainting to often
        time.sleep(0.01)
