import curses
import time 
import Player
import Board_map
import game_board
import os
from curses.textpad import Textbox
#self.screen = curses.initscr()

#curses.start_color()
#curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)



class startMenu:
    def __init__(self,screen):
        self.CHOICE_START = "start"
        self.CHOICE_QUIT = "quit"
        self.current_CHOICE = ""
        self.menu = ["start", "quit"] 
        self.screen = screen
        self.title_txt = ""
        self.color = 1
        self.player1_name = ""
        self.player2_name = ""
        self.enter_keys = [curses.KEY_ENTER, 10, 13]
        self.current_row = 0
   
    def read_title(self):
        title = open('title.txt', 'r')
        self.title_txt = title.read()
        title.close()  

    def print_menu_title(self):
        self.read_title()
        splitted_title = self.title_txt.split("\n")
        first_line = splitted_title[0]

        _, num_cols = self.screen.getmaxyx()

        # Add some top margin on the title to get some space between the top and the title
        top_margin = 2

        # All lines start at the same x position so that the ascii art looks like intended
        x = int(num_cols / 2) - int(len(first_line) / 2)

        for index, line in enumerate(splitted_title):
            self.screen.addstr(index + top_margin, x, splitted_title[index])
    
    def get_menu_choice(self):
        return self.cu
    def print_menu(self, selected_row_index):
        """Prints the menu to the self.screen.

        Keyword arguments:
        self.screen             -- the curses self.screen
        selected_row_index -- the currently selected row in the menu
        """
        self.screen.clear()

        num_rows, num_cols = self.screen.getmaxyx()

        self.print_menu_title()

        for index, row in enumerate(self.menu):
            x = int(num_cols / 2) - int(len(row) / 2)
            y = int(num_rows / 2) - len(self.menu) + index

            if index == selected_row_index:
                self.screen.attron(curses.color_pair(self.color))
                self.screen.addstr(y, x, row.capitalize())
                self.screen.attroff(curses.color_pair(self.color))
            else:
                self.screen.addstr(y, x, row.capitalize())

        self.screen.refresh()
    

    def validate_key_input(self,key_input):
        """
        Callback function used by curses when a user types input.
        The function checks if the pressed key is one of the enter keys and
        signals curses to stop asking for input. Otherwise it lets the character through
        """
        if key_input in self.enter_keys:
            # 7 is a magic number that tells curses to stop asking for input
            return 7
        else:
            return key_input

    def get_player_name(self, text):
        """
        Prints and centers text on screen.
        Creates a new text input where the user enters the player name and returns it.

        Keyword arguments:
        self.screen             -- the curses self.screen.
        text               -- Text that appears before the input.

        Example:
        text = "Insert player 1's name" => Insert player 1's name: (user types here)

        Returns:
        The name of the player that the user entered.
        """

        # Centers the text
        num_rows, num_cols = self.screen.getmaxyx()

        x = int(num_cols / 2) - int(len(text) / 2)
        y = int(num_rows / 2)

        self.screen.addstr(y, x, text)
        self.screen.refresh()

        # We must create a new window becuase the edit function will return
        # everything that has been printed on the self.screen and not just the entered name
        win = curses.newwin(5, 10, y, x + len(text))
        textbox = Textbox(win)
        player_name = textbox.edit(self.validate_key_input)

        return player_name


  
    def ask_for_player_names(self):
        player1_text = "Insert player 1's name: "
        player2_text = "Insert player 2's name: "

        # Enable blinking cursor when typing in names
        curses.curs_set(1)

        self.player1_name = self.get_player_name(player1_text)
        self.player2_name = self.get_player_name(player2_text)

        curses.curs_set(0)
        self.screen.refresh()


screen_1 = curses.initscr()
curses.start_color()

def main(screen):
    
    """The menu loop used by curses.

    Keyword arguments:
    self.screen -- the curses self.screen
    """
    # Disable blinking cursor

    start1 = startMenu(screen)
    curses.curs_set(0)

    #curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    curses.init_pair(3,curses.COLOR_RED,curses.COLOR_BLACK)
    # color scheme for player2
    curses.init_pair(2,curses.COLOR_YELLOW,curses.COLOR_BLACK)  

    start1.print_menu(start1.current_row)
  
   

    while True:
        pressed_key = start1.screen.getch()
        if pressed_key == curses.KEY_UP and start1.current_row > 0:
            start1.current_row -= 1
        elif pressed_key == curses.KEY_DOWN and start1.current_row < len(start1.menu) - 1:
            start1.current_row += 1
        elif pressed_key in start1.enter_keys:
            if start1.menu[start1.current_row] == start1.CHOICE_START:
                start1.current_CHOICE = start1.CHOICE_START
                start1.screen.clear()
                start1.ask_for_player_names()

                #starts the game
                #game_board.main(start1.screen,start1.player1_name,start1.player2_name)
                Board_map.runMap(start1.screen)
                break
            elif start1.menu[start1.current_row] == start1.CHOICE_QUIT:
                start1.current_CHOICE = start1.CHOICE_QUIT
                break

        start1.print_menu(start1.current_row)


if __name__ == "__main__": 
    curses.wrapper(main)
