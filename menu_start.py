import curses
import time 
import player
import board_map
import game_board
import os
from curses.textpad import Textbox
#screen = curses.initscr()

#curses.start_color()
#curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
screen = curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
CHOICE_START = "start"
CHOICE_QUIT = "quit"
menu = ["start", "quit"] 
class startMenu:
    def __init__(self):
       

        self.title_txt = ""
        self.color = 1
        self.player1_name = ""
        self.player2_name = "" 
   
    def read_title(self):
        title = open('title.txt', 'r')
        self.title_txt = title.read()
        title.close()  

    def print_menu_title(self,screen):
        self.read_title()
        splitted_title = self.title_txt.split("\n")
        first_line = splitted_title[0]

        _, num_cols = screen.getmaxyx()

        # Add some top margin on the title to get some space between the top and the title
        top_margin = 2

        # All lines start at the same x position so that the ascii art looks like intended
        x = int(num_cols / 2) - int(len(first_line) / 2)

        for index, line in enumerate(splitted_title):
            screen.addstr(index + top_margin, x, splitted_title[index])
    
    def print_menu(self, screen,selected_row_index):
        """Prints the menu to the screen.

        Keyword arguments:
        screen             -- the curses screen
        selected_row_index -- the currently selected row in the menu
        """
        screen.clear()

        num_rows, num_cols = screen.getmaxyx()

        self.print_menu_title(screen)

        for index, row in enumerate(menu):
            x = int(num_cols / 2) - int(len(row) / 2)
            y = int(num_rows / 2) - len(menu) + index

            if index == selected_row_index:
                screen.attron(curses.color_pair(self.color))
                screen.addstr(y, x, row.capitalize())
                screen.attroff(curses.color_pair(self.color))
            else:
                screen.addstr(y, x, row.capitalize())

        screen.refresh()
    

    def validate_key_input(self,key_input):
        """
        Callback function used by curses when a user types input.
        The function checks if the pressed key is one of the enter keys and
        signals curses to stop asking for input. Otherwise it lets the character through
        """
        enter_keys = [curses.KEY_ENTER, 10, 13]
        if key_input in enter_keys:
            # 7 is a magic number that tells curses to stop asking for input
            return 7
        else:
            return key_input




    def get_player_name(self,screen, text):
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
        player_name = textbox.edit(self.validate_key_input)

        return player_name
    def ask_for_player_names(self,screen):
        player1_text = "Insert player 1's name: "
        player2_text = "Insert player 2's name: "

        # Enable blinking cursor when typing in names
        curses.curs_set(1)

        self.player1_name= self.get_player_name(screen,player1_text)
        self.player2_name = self.get_player_name(screen, player2_text)

        curses.curs_set(0)
        screen.refresh()


def runMenu(screen):
    
    """The menu loop used by curses.

    Keyword arguments:
    screen -- the curses screen
    """
    # Disable blinking cursor
    start1 = startMenu()
    curses.curs_set(0)

    current_row = 0
    #curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    start1.print_menu(screen,current_row)
    enter_keys = [curses.KEY_ENTER, 10, 13]
    

    while True:
        pressed_key = screen.getch()

        if pressed_key == curses.KEY_UP and current_row > 0:
            print("hej")
            current_row -= 1
        elif pressed_key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif pressed_key in enter_keys:
            print(menu[current_row],"je")
            if menu[current_row] == CHOICE_START:
                start1.current_CHOICE = CHOICE_START
                screen.clear()
                start1.ask_for_player_names(screen)

                #starts the game
                game_board.main(screen,start1.player1_name,start1.player2_name)
                #board_map.board_map(screen).runMap()
                break
            elif menu[current_row] == CHOICE_QUIT:
                start1.current_CHOICE = CHOICE_QUIT
                break

        start1.print_menu(current_row)



curses.wrapper(runMenu(screen))
