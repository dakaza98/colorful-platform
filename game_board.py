import curses
import os
import time


def read_map(path):
    """
    Reads a text file and returns it as a string


    Keyword arguments:
    path -- path of the file

    """
    try:        
        board = open( path,'r')
        board_txt = board.read()
        board.close 
        
        return board_txt
    except IOError:
        
        raise Exception("Can not find the file at this path => "+ path)

def convert_map_to_coordinates(str_board):
    """
    Reads the string from left to right and appends every char to list with its x any y pos
    the top of the menu. 
    Returns a list of lists where every list has [char,xPos,Ypos]
    Example "X  " => [['X', 0, 0], [' ', 1, 0], [' ', 2, 0]...,]

    Keyword arguments:
    str_board -- the string of the map
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
    """Prints the playernames in screen 

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
    """Reads the map_coordinates list  and prints the chars in the Screen

    Keyword arguments:
    screen -- the curses screen
    """
    for cord in map_coordinates:
        h,w = screen.getmaxyx()

        #To place the game board in the center of the window  
        y = cord[2]+ 5
        x = cord[1] +  w//3    
        
        char = cord[0]
        if char == "O":
            
            screen.addstr(y,x,char,curses.color_pair(2))
        elif char == "X": 

            screen.addstr(y,x,char,curses.color_pair(3))
        elif char != "+" and char != "O" and char !="X":
            screen.addstr(y,x,char)

      
          



def print_choice(screen,selected_move_idx,plus_list,player1_name,player2_name,map_coordinates):
    """Reads the plus_list list  and prints the chars in the Screen. If selected

    Keyword arguments:
    screen -- the curses screen
    selected_move_idx -- the currently selected row in the plus_list
    plus_list -- the lists of all the "+" and their positions
    map_coordinates -- The coordinates of the chars in the map
    """    
    screen.clear()
    print_map(screen,map_coordinates)
    print_player_names(screen,player1_name,player2_name)
    h, w = screen.getmaxyx()
    for idx, row in enumerate(plus_list):
        y = int(row[2])+ 5
        x = int(row[1]) +  w//3      
        if idx == selected_move_idx:
            screen.attron(curses.color_pair(1))
            screen.addstr(y,x, row[0])
            screen.attroff(curses.color_pair(1))
        else:
            screen.addstr(y, x, row[0])
   
    screen.refresh()    


def move_down(plus_list,current_row):
    """ Finds the "+" char that is below the current_row. If the current "+" char is at the bottom, 
        it finds the "+" char at the top with the same x position

    current_row -- the currently selected row in the plus_list
    plus_list -- the lists of all the "+" and their positions
    """
    
    new_row = current_row
    
    while True:
        new_row += 1
        if new_row == len(plus_list):
            new_row = 0
        
        if plus_list[current_row][1] == plus_list[new_row][1] and plus_list[current_row][2] != plus_list[new_row][2]:
     
          return new_row 

def move_up(plus_list,current_row):
    """ Finds the "+" char that is above the current_row. If the current "+" char is at the top, 
        it finds the "+" char at the top with the same x position


    current_row -- the currently selected row in the plus_list
    plus_list -- the lists of all the "+" and their positions
    """
    
    new_row = current_row
    
    while True:
        if new_row == 0:
            new_row = len(plus_list)
        
        new_row -= 1
        
        if plus_list[current_row][1] == plus_list[new_row][1] and plus_list[current_row][2] !=   plus_list[new_row][2]:
     
          return new_row  

def change_plus_to_X (plus_list,current_row):
    """ Changes the "+" to a "X" of the current_row in the plus_list list
    Returns the changed plus_list list


    current_row -- the currently selected row in the plus_list
    plus_list -- the lists of all the "+" and their positions
    """

    plus_list[current_row][0] = "X"
    return plus_list
def change_plus_to_O (plus_list,current_row):
    """ Changes the "+" to a "O" of the current_row in the plus_list list
    Returns the changed plus_list list


    current_row -- the currently selected row in the plus_list
    plus_list -- the lists of all the "+" and their positions
    """

    plus_list[current_row][0] = "O"
    return plus_list
 
def main(screen,player1_name,player2_name):
    """ The game loop used by curses.

    Keyword arguments:
    screen -- the curses screen
    player1_name -- The name of player1 as a string
    player2_name -- The name of player2 as a string
    """
    # turn off cursor blinking
    curses.curs_set(0)

    # color scheme for selected row
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)

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
    # plus_list 
    
    # plus_list, coordinates of the "+" chars in the map_coordinates list 
    plus_list = make_plus_list(map_coordinates)
     
    while 1:
        print_choice(screen,current_row,plus_list,player1_name,player2_name,map_coordinates)
        
        key = screen.getch()

        if key == curses.KEY_LEFT and current_row > 0:  
            current_row -= 1
            time.sleep(0.08)
        elif key == curses.KEY_RIGHT and current_row < len(plus_list)-1:
            current_row += 1
            time.sleep(0.08)
        elif key == curses.KEY_DOWN:
            current_row = move_down(plus_list,current_row)

        elif key == curses.KEY_UP:
            current_row = move_up(plus_list,current_row)

        elif key == curses.KEY_ENTER or key in [10, 13]:
            plus_list = change_plus_to_X(plus_list,current_row)
        
        # 27 = Escape key
        elif key == 27: 
            quit()
            
