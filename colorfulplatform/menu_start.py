import curses
import time 
import colorfulplatform.Player
import colorfulplatform.Board_map
import os
from curses.textpad import Textbox
#self.screen = curses.initscr()

#curses.start_color()
#curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
#test
import tournament_menu
import single_menu

class startMenu:
    def __init__(self):
        self.screen = curses.initscr()
        self.CHOICE_SINGLE = "Single"
        self.CHOICE_TOURNAMENT = "Tournament"
        self.CHOICE_QUIT = "Quit"
        self.current_CHOICE = ""
        self.menu = [self.CHOICE_SINGLE, self.CHOICE_TOURNAMENT, self.CHOICE_QUIT]      
        self.title_txt = ""
        self.color = 1
        self.player1_name = ""
        self.player2_name = ""
        self.enter_keys = [curses.KEY_ENTER, 10, 13]
        self.current_row = 0
        self.is_menu_finished = False
   
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
   
    def get_is_menu_finished(self):
        return self.is_menu_finished
   
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

     



    def get_menu_choice(self):
        curses.wrapper(self.runMenu)
        return self.current_CHOICE   

    def runMenu(self, screen):
        """The menu loop used by curses.

        Keyword arguments:
        self.screen -- the curses self.screen
        """
        # Disable blinking cursor

        curses.curs_set(0)

        #curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        curses.init_pair(3,curses.COLOR_RED,curses.COLOR_BLACK)
        # color scheme for player2
        curses.init_pair(2,curses.COLOR_YELLOW,curses.COLOR_BLACK)  

        self.print_menu(self.current_row)

        while True:
            pressed_key = self.screen.getch()
            if pressed_key == curses.KEY_UP and self.current_row > 0:
                self.current_row -= 1
            elif pressed_key == curses.KEY_DOWN and self.current_row < len(self.menu) - 1:
                self.current_row += 1
            elif pressed_key in self.enter_keys:
                if self.menu[self.current_row] == self.CHOICE_SINGLE:
                    self.current_CHOICE = self.CHOICE_SINGLE
                    self.screen.clear()
                    break
                elif self.menu[self.current_row] == self.CHOICE_TOURNAMENT:
                    self.current_CHOICE = self.CHOICE_TOURNAMENT
                    self.screen.clear()
                    break
                elif self.menu[self.current_row] == self.CHOICE_QUIT:
                    self.current_CHOICE = self.CHOICE_QUIT
                    self.screen.clear()
                    break

            self.print_menu(self.current_row)
#test
start = startMenu()
s = start.get_menu_choice()
if s == "Single":
    print(s)
    menu_single = single_menu.single_menu()
    player1_name ,player2_name = menu_single.get_player_names()
    print(player1_name,player2_name)
elif s == "Tournament":
    menu_tournament = tournament_menu.tournament_menu()
    player1_name,player_amount,AI_amount,AI_difficulty = menu_tournament.get_tournament_info()
    print(player1_name,player_amount,AI_amount,AI_difficulty)

