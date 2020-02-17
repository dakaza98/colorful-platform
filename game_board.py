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
    return map_xy


def move_plus():
    map_xy =map_cord(board_txt)
    move = []
    for cord in map_xy:
        if cord[0] == "+":
            move.append([cord[0],str(cord[1]),str(cord[2])])
    
    return move
print(move_plus())

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

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(move)-1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            quit()
        #print_choice(screen,current_row,move)
        print_choice(screen,current_row,move)


