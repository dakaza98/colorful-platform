import curses
import os
import time
import random

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
            plus_list.append([cord[0],str(cord[1]),str(cord[2])])
    return plus_list

def print_player_names(screen,player1_name,player2_name):
    """Prints the playernames in the screen 

    Keyword arguments:
    screen -- the curses screen
    player1_name -- player1 name as string
    player2_name -- player2 name as string
    """
    h,w = screen.getmaxyx()

    player1_name_x = -1 + w//3   
    player1_name_y = 2
    screen.addstr(player1_name_y,player1_name_x,"Player1",curses.color_pair(3))
    screen.addstr(player1_name_y+1,player1_name_x,player1_name,curses.color_pair(3))

    player2_name_x = 29  + w//3 
    player2_name_y = 2
    screen.addstr(player2_name_y,player2_name_x,"Player2",curses.color_pair(2))
    screen.addstr(player2_name_y+1,player2_name_x,player2_name,curses.color_pair(2))
    
         

def print_map(screen,map_coordinates):
    """Prints the all the chars except "+" in map_coordinates at their specified coordinate.

    Keyword arguments:
    screen -- the curses screen
    map_coordinates -- A list of lists where every list has the form [char, xPos, yPos]
    """
    for cord in map_coordinates:

        char = cord[0]
        
        if char == "+":        
            continue

        h,w = screen.getmaxyx()

        #To place the game board in the center of the window  
        y = cord[2]+ 5
        x = cord[1] +  w//3    
        
        color = which_color_pair(char)

        screen.addstr(y,x,char,curses.color_pair(color))

def print_choice(screen, selected_move_idx, plus_list,player_turn):
    """Prints all plusses in plus_list on the screen. The currently selected plus is colored.

    Keyword arguments:
    screen -- the curses screen
    selected_move_idx -- the currently selected row in the plus_list
    plus_list -- the lists of all the "+" and their positions
    """    
    h, w = screen.getmaxyx()
    for idx, row in enumerate(plus_list):

        # To have  the game board in the center, 5 is added y and w//3 is added to x
        y = int(row[2])+ 5
        x = int(row[1]) +  w//3      
        color =which_color_pair(row[0])
        if idx == selected_move_idx:
            color_cursor = 1
            #cursor will now have the player colors
            if player_turn == False:
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
    elif stone_marker == "X": 
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



def place_stone(plus_list,current_row,stone_marker):
    """ Places a stone on the map by changing the "+" to "X" or "O"
    Returns the changed plus_list list

    current_row -- the currently selected row in the plus_list
    plus_list -- the lists of all the "+" and their positions
    stone_marker -- the char of the stone, should be either "X" or "O" 
    """
    current_char = plus_list[current_row][0]
    if current_char == "+":
        plus_list[current_row][0] = stone_marker
    return plus_list

def remove_stone(map_coordinates,stone_marker):
    """ When you place a stone it removes the stone from the left or the right side
        depending on the stone_marker
    Returns map_coordinates 
    Keyword arguments:
    map_coordinates -- list of all chars in the string version of the map
    stone_marker -- Char version of the stone which can be a "X" or "O"     

    """
    for stone in map_coordinates:
        if stone[0] == stone_marker:
            stone[0] = ""
            break
    return  map_coordinates
def which_stone(player_turn):
    """Picks which char the stone marker should be based on which player is next to act
    Return stone_marker

    Keyword arguments:
    stone_marker -- char of the stone,which can be "X" or "O"
    """
    stone_marker = "X"
    if player_turn == False:
        stone_marker = "O"
    return stone_marker    

def switch_player_turn(player_turn):
    """Switches which player turn it is to act
    Return player_turn
    Keyword arguments:
    player_turn -- bool, True is player1 turn and False is player2 turn
    """
    if player_turn == True:
        player_turn = False
    elif player_turn == False:
        player_turn = True        
    return player_turn

def random_player_start():
    """Determine which player that will start to act. 
    Returns True or False , True for player1 and False for player2 
    """
    player_start = random.randint(1,2)
    if player_start == 1:
        return True
    return False

def print_player_start(screen,player_turn,player1_name,player2_name):
    """ Prints the name of player who will start to act
    
    Keyword arguments:
    screen -- the curses screen
    player_turn -- bool shows who's turn it is act
    player1_name -- player1 name as string
    player2_name -- player2 name as string

    """
    h,w = screen.getmaxyx()

    #position of text 
    text_x = 8  + w//3 
    text_y = 0
    
    if player_turn == True:
          if len(player1_name) ==0:
              player1_name = "Player1"   
          screen.addstr(text_y,text_x,player1_name.rstrip("\n")+" will start!",curses.color_pair(3))
    else:
        if len(player2_name) ==0:
            player2_name = "Player2"        
        screen.addstr(text_y,text_x,player2_name.rstrip("\n")+" will start!",curses.color_pair(2))


def can_player_act(plus_list,current_row,remaining_stones_p1, remaining_stones_p2,player_turn):
    """Determines if a player is allowed to act
    Returns Tuple (bool,remaining_stones_p1,remaining_stones_p2)

    Keyword argument 
    plus_list -- list of "+" and placed stones
    current_row --  currently selected row in the plus_list
    remaining_stone_p1 -- the amount of stone player1 has
    remaining_stone_p2 -- the amount of stone player2 ha
    player_turn -- which player is next to act
      
    """
    current_char = plus_list[current_row][0]
    can_not_act= (remaining_stones_p1 <=  0 and remaining_stones_p2 <= 0) or current_char != "+"
    if can_not_act == True:    
        return False,remaining_stones_p1,remaining_stones_p2
    elif player_turn == True and can_not_act == False :
        remaining_stones_p1 -= 1
    elif player_turn == False and can_not_act == False:
        remaining_stones_p2 -= 1        
    return True,remaining_stones_p1, remaining_stones_p2
                
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
            
    # specify the current selected row
    current_row = 0

    # The path of the textfile of the map
    map_path = 'Ascii board.txt'

    #string of the map
    map_string = read_map(map_path)
    
    #coordinates of the chars in the map
    map_coordinates =convert_map_to_coordinates(map_string)
    
    # plus_list, coordinates of the "+" chars in the map_coordinates list 
    plus_list = make_plus_list(map_coordinates)
    
    
    #player_turn will determine which player that will start ,True for player1
    player_turn = random_player_start()
    
    remaining_stones_p1 = 9
    remaining_stones_p2 = 9
    #Prints player start text once
    print_once = 0
    while 1:
        screen.clear()
        if print_once == 0: print_player_start(screen,player_turn,player1_name,player2_name)
        print_once += 1    
        
        print_map(screen,map_coordinates)
        print_player_names(screen,player1_name,player2_name)

        print_choice(screen,current_row,plus_list,player_turn)
        
        screen.refresh()    

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
            player_can_act, remaining_stones_p1, remaining_stones_p2= can_player_act(plus_list,current_row,remaining_stones_p1,remaining_stones_p2,player_turn) 
            if player_can_act == True:
                stone_marker=which_stone(player_turn)
                plus_list = place_stone(plus_list,current_row,stone_marker)
                map_coordinates = remove_stone(map_coordinates,stone_marker)
                player_turn = switch_player_turn(player_turn)
         
        # 27 = Escape key
        elif key == 27: 
            quit()


        # Prevent the screen from repainting to often
        time.sleep(0.01)
            
