import curses
from curses.textpad import Textbox

class single_menu():
    def __init__(self):
        self.screen = curses.initscr()
        self.player1_name = ""
        self.player2_name = ""
        self.enter_keys = [curses.KEY_ENTER, 10, 13]
    def get_player_names(self):
        curses.wrapper(self.run_single_menu)
        return self.player1_name.rstrip("\n").rstrip(" ") ,self.player2_name.rstrip("\n").rstrip(" ")

         

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

    def get_user_input(self, text):
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
        user_input = textbox.edit(self.validate_key_input)

        return user_input
  
    def ask_for_player_names(self):
        player1_text = "Insert player 1's name: "
        player2_text = "Insert player 2's name: "

        # Enable blinking cursor when typing in names
        curses.curs_set(1)

        self.player1_name = self.get_user_input(player1_text)
        self.player2_name = self.get_user_input(player2_text)

        curses.curs_set(0)
        self.screen.refresh()

    def run_single_menu(self,screen):
        self.screen.clear()
        self.ask_for_player_names()
                
