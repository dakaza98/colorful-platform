import curses
import time

CHOICE_START = "start"
CHOICE_QUIT = "quit"

menu = [CHOICE_START, CHOICE_QUIT]

title = open('title.txt', 'r')
titletext = title.read()
title.close()

def print_menu_title(screen):
    """Reads the menu title from a text file and prints it to
    the top of the menu.

    Keyword arguments:
    screen -- the curses screen
    """

    splitted_title = titletext.split("\n")
    first_line = splitted_title[0]

    _, num_cols = screen.getmaxyx()

    # Add some top margin on the title to get some space between the top and the title
    top_margin = 2

    # All lines start at the same x position so that the ascii art looks like intended
    x = int(num_cols / 2) - int(len(first_line) / 2)

    for index, line in enumerate(splitted_title):
        screen.addstr(index + top_margin, x, splitted_title[index])

def print_menu(screen, selected_row_index):
    """Prints the menu to the screen.

    Keyword arguments:
    screen             -- the curses screen
    selected_row_index -- the currently selected row in the menu
    """
    screen.clear()

    num_rows, num_cols = screen.getmaxyx()

    print_menu_title(screen)

    for index, row in enumerate(menu):
        x = int(num_cols / 2) - int(len(row) / 2)
        y = int(num_rows / 2) - len(menu) + index
        
        if index == selected_row_index:
            screen.attron(curses.color_pair(1))
            screen.addstr(y, x, row.capitalize())
            screen.attroff(curses.color_pair(1))
        else:
            screen.addstr(y, x, row.capitalize())

    screen.refresh()

def start_game(screen):
    """Temporary functions that 'starts' the game.

    Keyword arguments:
    screen -- the curses screen
    """
    screen.addstr(0, 0, "Game will now start")
    screen.refresh()
    time.sleep(3)

def main(screen):
    """The menu loop used by curses.
    
    Keyword arguments:
    screen -- the curses screen
    """
    # Disable blinking cursor
    curses.curs_set(0)  

    current_row = 0
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    print_menu(screen, current_row)

    # KEY_ENTER might not always work because some computers sends the value 10 or 13 instead
    enter_keys = [curses.KEY_ENTER, 10, 13]

    while True:
        pressed_key = screen.getch()

        if pressed_key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif pressed_key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif pressed_key in enter_keys:
            if menu[current_row] == CHOICE_START:
                screen.clear()
                start_game(screen)
                break
            elif menu[current_row] == CHOICE_QUIT:
                break

        print_menu(screen, current_row)

curses.wrapper(main)
