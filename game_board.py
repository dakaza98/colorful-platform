import curses
import os
import time

# The path of the textfile of the map
map_path = 'Ascii board.txt'

def read_map(path):
    try:        
        board = open( path,'r')
        board.close 

        board_txt = board.read()
        return board_txt
    except IOError:
        print("Can not find the file" )




def map_cord(str_board):
    """
    Reads the string from left to right and appends every char to list with its x any y pos
    the top of the menu. 
    Returns a list of lists where every list has [char,xPos,Ypos]
    Example "X  " => [['X', 0, 0], [' ', 1, 0], [' ', 2, 0]...,]

    Keyword arguments:
    str_board -- the string of the map
    """
 
    matrix = [[x for x in line] for line in str_board.split('\n')]
    map_xy = []
    y = 0
    for row in matrix:
        x = 0
        for c in row:
            char_xy = [c,x,y]    
            map_xy.append(char_xy)
            x += 1
        y += 1
    return map_xy

def move_plus():
    """
    Finds all the "+" chars in the map_xy 
    Returns a list of lists where every list has ["+",xPos,Ypos]
    Example [['X', 0, 0], [' ', 1, 0],...,['+', '4', '0']] => [['+', '4', '0'],...]
    """
    map_xy =map_cord(read_map(map_path))
    move = []
    for cord in map_xy:
        if cord[0] == "+":
            move.append([cord[0],str(cord[1]),str(cord[2])])
    return move

def print_map(screen):
    """Reads the map_xy list  and prints the chars in the Screen

    Keyword arguments:
    screen -- the curses screen
    map_xy -- list of lists the chars and their positions 
    """
    map_xy = map_cord(read_map(map_path))
    for cord in map_xy:
        h,w = screen.getmaxyx()
        y = cord[2]+ 5
        x = cord[1] +  w//3    
        char = cord[0]
        if char == "O":
            curses.init_pair(2,curses.COLOR_YELLOW,curses.COLOR_BLACK)
                        
            screen.addstr(y,x,char,curses.color_pair(2))
        elif char == "X": 
            curses.init_pair(3,curses.COLOR_RED,curses.COLOR_BLACK)

            screen.addstr(y,x,char,curses.color_pair(3))
        elif char != "+" and char != "O" and char !="X":
            screen.addstr(y,x,char)

      
          


def print_choice(screen,selected_move_idx,move):
    """Reads the move list  and prints the chars in the Screen. If selected

    Keyword arguments:
    screen -- the curses screen
    selected_move_idx -- the currently selected row in the move
    move -- the lists of all the "+" and their positions
    """    
    screen.clear()
    print_map(screen)
    h, w = screen.getmaxyx()
    for idx, row in enumerate(move):
        y = int(row[2])+ 5
        x = int(row[1]) +  w//3      
        if idx == selected_move_idx:
            screen.attron(curses.color_pair(1))
            screen.addstr(y,x, row[0])
            screen.attroff(curses.color_pair(1))
        else:
            screen.addstr(y, x, row[0])
   
    screen.refresh()    


def move_down(move,current_row):
    """ Finds the "+" char which has the same xpos but an other Ypos in the move list
    return the index of the new "+"

    current_row -- the currently selected row in the move
    move -- the lists of all the "+" and their positions
    """
    
    new_row = current_row
    
    while True:
        new_row += 1
        if new_row == len(move):
            new_row = 0
        
        if move[current_row][1] == move[new_row][1] and move[current_row][2] != move[new_row][2]:
     
          return new_row 

def move_up(move,current_row):
    """ Finds the "+" char which has the same xpos but an other Ypos in the move list
    return the index of the new "+"

    current_row -- the currently selected row in the move
    move -- the lists of all the "+" and their positions
    """
    
    new_row = current_row
    
    while True:
        if new_row == 0:
            new_row = len(move)
        
        new_row -= 1
        
        if move[current_row][1] == move[new_row][1] and move[current_row][2] !=   move[new_row][2]:
     
          return new_row  

def stone_change(move,current_row):
    """ Changes the "+" to a "X" of the current_row in the move list
    returns the changed move list


    current_row -- the currently selected row in the move
    move -- the lists of all the "+" and their positions
    """

    move[current_row][0] = "X"
    return move

def main(screen):
    # turn off cursor blinking
    curses.curs_set(0)

    # color scheme for selected row
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)

    # specify the current selected row
    current_row = 0

    # move list
    move = move_plus()
     
    
    print_choice(screen,current_row,move)
    while 1:
        key = screen.getch()
        if key == curses.KEY_LEFT and current_row > 0:  
            current_row -= 1
            print_choice(screen,current_row,move)
            time.sleep(0.08)
        elif key == curses.KEY_RIGHT and current_row < len(move)-1:
            current_row += 1
            print_choice(screen,current_row,move)
            time.sleep(0.08)
        elif key == curses.KEY_DOWN:
            current_row = move_down(move,current_row)
            print_choice(screen,current_row,move)

        elif key == curses.KEY_UP:
            current_row = move_up(move,current_row)
            print_choice(screen,current_row,move)

        elif key == curses.KEY_ENTER or key in [10, 13]:
            move = stone_change(move,current_row)
            print_choice(screen,current_row,move)
            time.sleep(3)
            
            quit()

