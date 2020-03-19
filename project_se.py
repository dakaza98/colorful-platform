
""" Highest level and entrypoint of the ProjectSE / UU-game application """
import os
from projectse.player import *
from projectse.configuration import *
from projectse.game_manager import *
from projectse.tournament import *

from colorfulplatform.menu_start import startMenu
import colorfulplatform.game_loop as game_loop
from colorfulplatform.single_menu import SingleMenu
from colorfulplatform.tournament_menu import TournamentMenu


class MockPlatform:

    def initialize(self):
        """ Used to setup the Platform if necessary.
        returns none """

        return None

    def get_menu_choice(self):
        """ Called by ProjectSE to make the Platform present a menu and gather user choice to decide what kind of
         game to play: tournament, singleplayer, or simply quitting the application

          returns: A single word string which corresponds to a legal choice. """

        return "Singleplayer"

    def play(self, board):
        """ Called by ProjectSE to let the Platform make operations on the BoardState-object and then return it once
        it is finished with it (which occurs once it's the AI's turn to move OR match between humans is finished and there is a winner

        Parameters: board - BoardState object on which to make a move

        Returns: a BoardState object with the latest positions """
        board.finished = True
        return board

    def setup(self, black_name, white_name):
        """ Called by ProjectSE to let the platform initialize a new match with settings from
        a Match-instance, that is, player names, player types (Human/AI);player color.

         returns: None """
        print("Setting up platform with player infos")

        return BoardState()

    def get_player(self, color):
        if color=="black":
            return ("CPU", "L")
        else:
            return ("Olle","")


class ProjectSE:
    def __init__(self,cb=ConfigurationBuilder(),pltfrm=MockPlatform(),gm=GameManager()):
        self.cb = cb
        self.platform = pltfrm
        self.game_mgr = gm
        #TODO: wait with this, if no connection we cant play
        # self.game_mgr.connect()

    def intro_menu_choice(self):
        """ Get user input to determine if to start
        new tournament, singleplayer or exit"""
        print("Welcome to the UU-game press 'T' to start tournament, 'S' for single or 'Q' to quit")
        while True:
            key_hit = input()
            if (key_hit == 'T'):
                return "Tournament"
            elif (key_hit == 'S'):
                print("Singleplayer!")
                return "Single"
            elif (key_hit == 'Q'):
                print("See you next time!")
                return "Quit"
            else:
                print("You pressed", key_hit,
                "This is not a valid key, press T or Q to start or quit")

    def init(self):
        menu = startMenu()
        choice = menu.get_menu_choice()

        if choice == "Tournament":
            tournament_menu = TournamentMenu()
            player_names, amount_of_players, amount_of_ai, ai_difficulties = tournament_menu.get_tournament_info()

            players_cfg = self.cb.set_tournament_settings(player_names, amount_of_ai, ai_difficulties)
            retry = True
            while retry:
                tournament = Tournament(players_cfg)
                self.play_tournament(tournament)
                retry = tournament.ask_retry()
        elif choice == "Single":
            single_menu = SingleMenu()
            player1_name,player2_name = single_menu.get_player_names()
            game_loop.runGame(player1_name,player2_name, is_player2_AI=False)
        elif choice == "Quit":
            quit()
        else:
            raise NotImplementedError("No such choice")

    def setup_platform(self, match):
        """ Interface to Platform to set type of players and names """
        return self.platform.setup(match.get_black_player_name(),match.get_white_player_name())

    def which_player_won(self,match,is_game_draw,winner_name) :
        if match.get_black_player_name() == winner_name and is_game_draw == False:
            return match.get_black_player(),match.get_white_player()
        elif is_game_draw == False and match.get_white_player_name() == winner_name:
            return match.get_white_player(),match.get_black_player()
        #game is_draw
        print(is_game_draw)
        

    def play_tournament(self, tournament):
        """ Decides and makes call to start the matches inside all rounds of the tournament sequentially
        Starting with the first rounds matches. AIvsAI matches are determined by chance """
        round = tournament.get_current_round()
        tournament.print_round()
        while round is not None:
            match = tournament.get_current_match()
            while match is not None:
                # AI vs AI is determined by tournament and not actually played.
                match.print_playing()
                match.print_play_match()
                if match.only_ai():
                    winner = tournament.aiplay(match)
                else:
                    winner_name,is_game_draw = game_loop.runGame(match.get_black_player_name(), match.get_white_player_name(), match.is_player2_ai())
                    print(winner_name,is_game_draw)
                    winner,loser= self.which_player_won(match,is_game_draw,winner_name)
                    match.set_winner(winner)
                    match.set_loser(loser)
                tournament.set_result(winner,is_game_draw)
                tournament.tournamentdrawer.drawResultTable()
                match = tournament.get_next_match()
            round = tournament.get_next_round()
        return tournament.stop_tournament()

    def play_match(self, match) -> Player:
        """
        Used to play a game by first initializing the platform with
        information about the match and then playing until the match is finished.
        return : Winning player is returned, if draw None is returned.
        """
        board_state = self.setup_platform(match)
        while not board_state.is_finished():
            current_player = match.get_player_by_color(board_state.get_player_color())
            if current_player.is_ai():
                board_state = self.game_mgr.make_move(board_state)
            else:
                board_state = self.platform.play(board_state)
        # We have either a winner or a tie now
        if board_state.is_draw:
            return None
        else:
            winner = match.get_player_by_color(board_state.get_player_color())
            return winner

    def main_loop(self):
        print("Get ready to rumble!!!")

    def exit(self):
        print("Game exited")


if __name__ == "__main__":
    ProjectSE().init()
