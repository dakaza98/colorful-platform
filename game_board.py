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



def print_map(screen):
    screen.clear()

    map_xy = map_cord(board_txt)
    for cord in map_xy:
        h,w = screen.getmaxyx()
        y = cord[2]+ 5
        x = cord[1] +  w//3
        char = cord[0]
        screen.addstr(y,x,char)

    screen.refresh()    


"""
def main(screen):
    # turn off cursor blinking
    curses.curs_set(0)

    # get height and width of screen
    h, w = screen.getmaxyx()

    # create a new color scheme
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_YELLOW)

    # text to be written in center

    # find coordinates for centered text
    print_map(screen)
    
    # set color scheme
    screen.attron(curses.color_pair(1))

    # write text on screen

    # unset color scheme
    screen.attroff(curses.color_pair(1))

    # update the screen
    screen.refresh()

    # wait for 3 sec before exit
    time.sleep(3)

curses.wrapper(main)    
"""