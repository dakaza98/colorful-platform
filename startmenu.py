import curses
import time

menu = ["start", "quit"]

title = open('title.txt', 'r')
titletext = title.read()
title.close()

def print_menu_title(screen):
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
    screen.addstr(0, 0, "Game will now start")
    screen.refresh()
    time.sleep(3)

def main(screen):
    # Disable blinking cursor
    curses.curs_set(0)  

    current_row = 0
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    print_menu(screen, current_row)

    while True:
        pressed_key = screen.getch()

        if pressed_key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif pressed_key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        # KEY_ENTER might not always work because some computers sends the value 10 or 13 instead
        elif pressed_key == curses.KEY_ENTER or pressed_key in [10, 13]:
            if current_row == 0:
                screen.clear()
                start_game(screen)
                break
            elif current_row == 1:
                break

        print_menu(screen, current_row)

curses.wrapper(main)
