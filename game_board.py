import curses
import numpy as np
import os
import time
#sh, sw = s.getmaxyx()

# Creates a new window
#w = curses.newwin(sh, sw, 0, 0)

# Setting for accepting the keypad
#w.keypad(1) 

# For refreshing the window every 100 miliseconds
#w.timeout(100)
#screen = curses.initscr()
MAP_WIDTH = 34
MAP_HEIGHT = 13

map_txt = 'Ascii board.txt'
board = open( map_txt,'r')
board.close 

board_txt = board.read()


#board_matrix = np.matrix(board_txt)


"""
Input a string,in this case string of the map
Reads the string from left to right and appends every char to list with its x any y pos
Returns a list of lists where every list has [char,xPos,Ypos]
 example map_xy = [['X', 0, 0], [' ', 1, 0], [' ', 2, 0]...,]
 """
def map_cord(str_board): 
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
    #print(map_xy)    
    return map_xy

"""
Finds all the "+" chars in the map_xy 
Returns a list of lists where every list has ["+",xPos,Ypos]
 example move = [['+', '4', '0'], ['+', '16', '0'],...]
 """ 
def move_plus():
    map_xy =map_cord(board_txt)
    move = []
    for cord in map_xy:
        if cord[0] == "+":
            move.append([cord[0],str(cord[1]),str(cord[2])])
    
    return move
#print(move_plus())

def print_map(screen):
    
    map_xy = map_cord(board_txt)
    for cord in map_xy:
        h,w = screen.getmaxyx()
        y = cord[2]+ 5
        x = cord[1] +  w//3    
        char = cord[0]
        print(x,y)
        if char == "O":
            curses.init_pair(2,curses.COLOR_YELLOW,curses.COLOR_BLACK)
                        
            screen.addstr(y,x,char,curses.color_pair(2))
        elif char == "X": 
            curses.init_pair(3,curses.COLOR_RED,curses.COLOR_BLACK)

            screen.addstr(y,x,char,curses.color_pair(3))
        elif char != "+" and char != "O" and "X":
            screen.addstr(y,x,char)

      
          


def print_choice(screen,selected_move_idx,move):
    screen.clear()
    print_map(screen)
    h, w = screen.getmaxyx()
    for idx, row in enumerate(move):
        y = int(row[2])+ 5
        x = int(row[1]) +  w//3      
        print(x,y)
        print(move)      
        if idx == selected_move_idx:
            screen.attron(curses.color_pair(1))
            screen.addstr(y,x, row[0])
            screen.attroff(curses.color_pair(1))
        else:
            screen.addstr(y, x, row[0])
   
    screen.refresh()    


"""
input current_row(index) and move list 
finds the "+" char which has the same xpos but an other Ypos in the move list
return the index of the new "+"
"""
def move_down(move,current_row):
    new_row = current_row
    
    while True:
        new_row += 1
        if new_row == len(move):
            new_row = 0
        
        if move[current_row][1] == move[new_row][1] and move[current_row][2] != move[new_row][2]:
     
          return new_row 

"""
input current_row(index) and move list 
finds the "+" char which has the same xpos but an other Ypos in the move list
return the index of the new "+"
"""
def move_up(move,current_row):
    new_row = current_row
    
    while True:
        if new_row == 0:
            new_row = len(move)
        
        new_row -= 1
        
        if move[current_row][1] == move[new_row][1] and move[current_row][2] !=   move[new_row][2]:
     
          return new_row  
"""
input current_row(index) and move list
changes the "+" to a "X" of the current_row in the move list
returns the changed move list
"""
def stone_change(move,current_row):
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
    # print the 
    
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

