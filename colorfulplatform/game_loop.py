import colorfulplatform.Board_map as Board_map
import colorfulplatform.Player as Player
import curses
import os
import time
import random
import numpy as np
import itertools

#screen = curses.initscr()
#curses.start_color()
class Game:
    def __init__(self,game_manager,player1_name,player2_name,is_player2_AI, AI_difficulty):
        self.screen = curses.initscr()

        self.start_color = curses.start_color()
        self.amount_turns = 0
        self.game_manager = game_manager
        self.player1= Player.player(self.screen,1,player1_name,"X",3,False)
        self.player2= Player.player(self.screen,2,player2_name,"O",2,is_player2_AI)
        self.list_players  = [self.player1,self.player2]
        self.which_player = 0
        self.current_player = self.list_players[self.which_player]
        self.AI_difficulty = AI_difficulty

        self.stone_removed = True
        self.is_game_over = False
        self.is_game_draw = False
        self.winner_name = str
        self.is_stone_selected = False
        self.json = {}
        
        
    def check_has_player_won(self,player):
        if (player.get_player_lose() == True):
            self.winner_name = player.player_name
            self.is_game_over = True

    def update_json(self,new_json):
        self.json = new_json
         
    def check_game_draw(self):
        if(self.amount_turns >= 500):
            self.is_game_draw = True
            self.is_game_over = True
    def get_game_info(self):
        return self.winner_name,self.is_game_draw
    def switch_turn(self):

        self.amount_turns +=1
        if self.which_player == 0:
            self.which_player = 1
            #self.list_players [1].move_index = self.list_players [0].move_index
            self.current_player= self.list_players[1]
            return
        elif self.which_player == 1:
            self.which_player =0
            #self.list_players[0].move_index = self.list_players[1].move_index gör så move_index för spelare är lika som i den gamla versionen av spelet

            self.current_player= self.list_players[0]
            return

    def get_amount_turns(self):
        return self.amount_turns

    def game_loop(self,screen):
        """ The self loop used by curses.

        Keyword arguments:
        screen -- the curses screen
        player1_name -- The name of player1 as a string
        player2_name -- The name of player2 as a string
        
        """
        # turn off cursor blinking
        curses.curs_set(0)  

        # color scheme for selected row player1
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)
        
        # color scheme for selected row player2
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)


        # color scheme for player1        
        curses.init_pair(3,curses.COLOR_RED,curses.COLOR_BLACK)
        
        # color scheme for player2
        curses.init_pair(2,curses.COLOR_YELLOW,curses.COLOR_BLACK)

        # color scheme for phase Not needed atm
        #curses.init_pair(5,curses.COLOR_CYAN,curses.COLOR_BLACK)        
    
        #Prints _player start text once
        print_once = 0

        #If _player has removed a stone = True else False

    #Menu object
        #start_menu = menu_start.startMenu(screen)
        #Map object
        #map_board.read_map()
        map_board = Board_map.board_map(self.screen)
        map_board.read_map()
        map_board.convert_map_to_coordinates()
        map_board.make_stone_list()
        map_board.stone_list_to_matrix()
        

        #_player list

        
        #test 
        self.json = map_board.convert_stone_list_to_json()
        while self.is_game_over == False:
            self.screen.clear()

        
                    
            if print_once == 0: 
                map_board.print_player_start(self.player1)
                print_once += 1    

            if self.stone_removed == False:
               self.current_player.print_player_remove()

            if self.is_stone_selected == False and self.stone_removed == True and self.current_player.phase == 2:
               self.current_player.print_player_move()

            self.current_player.switch_to_phase()
            map_board.stone_list_to_matrix()

            self.current_player.has_player_lost(map_board.get_stone_pos_list(),map_board.get_matrix())
            self.check_game_draw()
            self.check_has_player_won(self.current_player)
     
            map_board.print_map()
            map_board.print_player_names(self.player1,self.player2)
            map_board.print_choice(self.current_player)
            map_board.print_remaining_stone(self.list_players )
            map_board.print_phase(self.current_player)
            map_board.print_player_stone_pool(self.list_players )
            self.screen.refresh()
            
            # switch phases should maybe be done is a different way    

            
        

            
            if self.current_player.is_Ai == False:        
                key = screen.getch()
        
            if key == curses.KEY_LEFT and self.current_player.is_Ai == False:
               self.current_player.move_left(map_board.stone_pos_list)  

            elif key == curses.KEY_RIGHT and self.current_player.is_Ai == False: 
               self.current_player.move_right(map_board.stone_pos_list)
            
            elif key == curses.KEY_DOWN and self.current_player.is_Ai == False:
               self.current_player.move_down(map_board.stone_pos_list)
            
            elif key == curses.KEY_UP and self.current_player.is_Ai == False:
               self.current_player.move_up(map_board.stone_pos_list)
            
            elif(self.current_player.is_Ai == True):
                # -1 => "+" , 0 => "X", 1 = > "O"
                self.json = map_board.convert_stone_list_to_json()

                if self.current_player.phase == 1:
                    self.current_player.stone_pool -= 1
                self.json = self.game_manager.make_move_test(self.json['Board'], self.current_player.player_num - 1, self.amount_turns, self.AI_difficulty)

                map_board.convert_json_to_stone_list(self.json ,self.current_player,self.list_players[0])
                map_board.stone_list_to_matrix()

                self.switch_turn()
            
            elif (key == curses.KEY_ENTER or key in [10, 13] and self.current_player.is_Ai == False):
                    
                #phase1
                if (self.current_player.phase == 1):
                    
                    if self.current_player.can_player_act(map_board.stone_pos_list) == True and self.stone_removed == True:
                        new_stone_list =self.current_player.place_stone(map_board.get_stone_pos_list())
                        map_board.set_stone_pos_list(new_stone_list)
                        map_board.stone_list_to_matrix()
                        
                        map_board.check_both(self.current_player)
                        
                        if self.current_player.has_3_in_row  == True:
                            self.stone_removed = False
                        else:
                            self.switch_turn()
                    elif self.current_player.has_3_in_row  == True  and self.stone_removed == False and self.current_player.can_player_remove(map_board.stone_pos_list)  == True:
                                            
                        
                        new_stone_list =self.current_player.remove_stone_player(map_board.get_stone_pos_list(),self.list_players  )
                        map_board.set_stone_pos_list(new_stone_list)
                        map_board.stone_list_to_matrix()
                        
                        map_board.remove_old_3(self.current_player)
                        
                        
                        self.switch_turn()

                        self.stone_removed = True

                
                #phase 2
                
                elif (self.current_player.phase == 2):
                    self.current_player.find_all_neighbours(map_board.get_stone_pos_list(),map_board.get_matrix())
                    
                    if  self.current_player.can_player_move_stone(map_board.get_stone_pos_list()) and self.stone_removed == True and self.is_stone_selected == False:
                        selected_stone_index = self.current_player.get_selected_stone_index()
                        self.is_stone_selected = True
                        map_board.stone_list_to_matrix()
                        map_board.remove_old_3(self.current_player)
                    elif  self.is_stone_selected == True and self.stone_removed == True:
                        #had to move this if statement inside because selected stone index
                        
                        if self.current_player.is_neighbour_a_plus(map_board.get_stone_pos_list()) == True:

                            map_board.stone_list_to_matrix()
                            new_stone_list =self.current_player.move_stone(map_board.get_stone_pos_list())
                            map_board.set_stone_pos_list(new_stone_list)
                            #this makes it too op to just move in and out from a three in a row 
                            map_board.remove_old_3(self.current_player)

                            
                            
                            map_board.stone_list_to_matrix()
                            
                            map_board.check_both(self.current_player)
                            self.is_stone_selected = False
                
                            if self.current_player.has_3_in_row  == True:
                                self.stone_removed = False
                            elif self.is_stone_selected == False:
                                self.switch_turn()
                                
                                
                    elif self.current_player.has_3_in_row  == True  and self.stone_removed == False and self.current_player.can_player_remove(map_board.stone_pos_list) == True and self.is_stone_selected == False:

                        new_stone_list =self.current_player.remove_stone_player(map_board.get_stone_pos_list(),self.list_players )
                        map_board.set_stone_pos_list(new_stone_list)
                        map_board.stone_list_to_matrix()
                        
                        map_board.remove_old_3(self.current_player)
                        
                        
                        self.switch_turn()

                        self.stone_removed = True

                
                #phase 3
                elif (self.current_player.phase == 3):
                    self.current_player.find_all_neighbours(map_board.get_stone_pos_list(),map_board.get_matrix())
                    
                    if self.current_player.can_player_move_stone(map_board.get_stone_pos_list()) and self.stone_removed == True and self.is_stone_selected == False:
                        selected_stone_index =self.current_player.get_selected_stone_index()
                        self.is_stone_selected = True
                        map_board.stone_list_to_matrix()
                        map_board.remove_old_3(self.current_player)
                    elif  self.is_stone_selected == True and self.stone_removed == True:
                        #had to move this if statement inside because selected stone index
                        
                        if self.current_player.is_neighbour_a_plus(map_board.get_stone_pos_list()) == True:

                            map_board.stone_list_to_matrix()
                            new_stone_list =self.current_player.move_stone(map_board.get_stone_pos_list())
                            map_board.set_stone_pos_list(new_stone_list)
                            #this makes it too op to just move in and out from a three in a row 
                            map_board.remove_old_3(self.current_player)

                            
                            
                            map_board.stone_list_to_matrix()
                            
                            map_board.check_both(self.current_player)
                            self.is_stone_selected = False
                
                            if self.current_player.has_3_in_row  == True:
                                self.stone_removed = False
                            elif self.is_stone_selected == False:
                                self.switch_turn()
                                 
                                
                    elif self.current_player.has_3_in_row  == True  and self.stone_removed == False and self.current_player.can_player_remove(map_board.stone_pos_list) == True and self.is_stone_selected == False:

                        new_stone_list =self.current_player.remove_stone_player(map_board.get_stone_pos_list(),self.list_players )
                        map_board.set_stone_pos_list(new_stone_list)
                        map_board.stone_list_to_matrix()
                        
                        map_board.remove_old_3(self.current_player)
                        
                        
                        self.switch_turn()

                        self.stone_removed = True

                            
            # 27 = Escape key
            elif key == 27:     
                quit()
            
            # Prevent the screen from repainting to often
            time.sleep(0.01)
        #return self.winner_name,self.is_game_draw
        
def runGame(game_manager, player1_name,player2_name,is_player2_AI, AI_difficulty):
    game = Game(game_manager, player1_name,player2_name,is_player2_AI,AI_difficulty)
    curses.wrapper(game.game_loop)
    return game.get_game_info()