import curses
import time

import game_board
from curses.textpad import Textbox


CHOICE_START = "start"
CHOICE_QUIT = "quit"

menu = [CHOICE_START, CHOICE_QUIT]

# KEY_ENTER might not always work because some computers sends the value 10 or 13 instead
enter_keys = [curses.KEY_ENTER, 10, 13]

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





def validate_key_input(key_input):
    """
    Callback function used by curses when a user types input.
    The function checks if the pressed key is one of the enter keys and
    signals curses to stop asking for input. Otherwise it lets the character through
    """
    if key_input in enter_keys:
        # 7 is a magic number that tells curses to stop asking for input
        return 7
    else:
        return key_input


def get_player_name(screen, text):
    """
    Prints and centers text on screen.
    Creates a new text input where the user enters the player name and returns it.

    Keyword arguments:
    screen             -- the curses screen.
    text               -- Text that appears before the input.

    Example:
    text = "Insert player 1's name" => Insert player 1's name: (user types here)

    Returns:
    The name of the player that the user entered.
    """

    # Centers the text
    num_rows, num_cols = screen.getmaxyx()

    x = int(num_cols / 2) - int(len(text) / 2)
    y = int(num_rows / 2)

    screen.addstr(y, x, text)
    screen.refresh()

    # We must create a new window becuase the edit function will return
    # everything that has been printed on the screen and not just the entered name
    win = curses.newwin(5, 10, y, x + len(text))
    textbox = Textbox(win)
    player_name = textbox.edit(validate_key_input)

    return player_name



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

    while True:
        pressed_key = screen.getch()

        if pressed_key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif pressed_key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif pressed_key in enter_keys:
            if menu[current_row] == CHOICE_START:
                screen.clear()

                player1_text = "Inset player 1's name: "
                player2_text = "Insert player 2's name: "

                # Enable blinking cursor when typing in names
                curses.curs_set(1)

                player1_name = get_player_name(screen, player1_text)
                player2_name = get_player_name(screen, player2_text)

                curses.curs_set(0)

                #starts the game
                game_board.main(screen,player1_name,player2_name)
                break
            elif menu[current_row] == CHOICE_QUIT:
                break

        print_menu(screen, current_row)

curses.wrapper(main)
