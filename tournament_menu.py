import curses
from curses.textpad import Textbox

class tournament_menu():
    def __init__(self):
        self.screen = curses.initscr()
        self.player1_name = ""
        self.enter_keys = [curses.KEY_ENTER, 10, 13]
        self.player_amount = 0
        self.AI_amount = 99
        self.AI_difficulty = [] 
    
    def get_tournament_info(self):
        curses.wrapper(self.run_tournament_menu)
        return self.player1_name.rstrip("\n") ,self.player_amount,self.AI_amount,self.AI_difficulty

         

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

    def print_intro_ask_difficulty(self):
        self.screen.clear()
        intro_text = "To select High difficulty use: 'H'. Medium: 'M'. Low: 'L'"
        num_rows, num_cols = self.screen.getmaxyx()

        x = int(num_cols / 2) - int(len(intro_text) / 2)
        y = int(num_rows / 2) -3

        self.screen.addstr(y, x, intro_text)
        self.screen.refresh()
    def ask_for_AI_difficulty(self):

        self.print_intro_ask_difficulty()
        for AI in range(1,self.AI_amount+1):
            player1_text = "Set difficulty for AI player,#"+str(AI) + ": "

            # Enable blinking cursor when typing in names
            curses.curs_set(1)

            difficulty_text = self.get_user_input(player1_text).rstrip("\n").rstrip(" ").capitalize()
            curses.curs_set(0)
            self.screen.refresh()

            while difficulty_text != "H" and difficulty_text != "M" and difficulty_text != "L":
                self.print_intro_ask_difficulty()
                # Enable blinking cursor when typing in names
                curses.curs_set(1)

                difficulty_text = self.get_user_input(player1_text).rstrip("\n").rstrip(" ").capitalize()
               
                curses.curs_set(0)
                self.screen.refresh()
            
            self.AI_difficulty.append(difficulty_text)

    def ask_for_player_amount(self):
        self.screen.clear()

        while self.player_amount > 8 or self.player_amount < 3:

            player1_text = "Select total number of players, between 3 and 8: "

            # Enable blinking cursor when typing in names
            curses.curs_set(1)

            try :
                self.player_amount = int(self.get_user_input(player1_text).rstrip("\n"))
            except ValueError :
                self.ask_for_player_amount()
                
            curses.curs_set(0)
            self.screen.refresh()

    def ask_for_ai_amount(self):
        self.screen.clear()
        amount_txt = self.player_amount -1
        while self.AI_amount >= self.player_amount :
            player1_text = "Select number of AI players between 0-"+ str(amount_txt)+ ": "
                
            # Enable blinking cursor when typing in names
            curses.curs_set(1)

            try :
                self.AI_amount = int(self.get_user_input(player1_text).rstrip("\n"))
            except ValueError:
                self.ask_for_ai_amount()
            curses.curs_set(0)
            self.screen.refresh()
    

    def ask_for_player_names(self):
        self.screen.clear()

        player1_text = "Insert player 1's name: "

        # Enable blinking cursor when typing in names
        curses.curs_set(1)

        self.player1_name = self.get_user_input(player1_text)

        curses.curs_set(0)
        self.screen.refresh()

    def run_tournament_menu(self,screen):
        self.ask_for_player_names()
        self.ask_for_player_amount()
        self.ask_for_ai_amount()
        self.ask_for_AI_difficulty()
                
