import Board_map
import Player
import menu_start
import curses
import os
import time
import random
import numpy as np
import itertools

screen = curses.initscr()
curses.start_color()


def switch_turn(players,playerNumber):
    if playerNumber == 0:
        playerNumber = 1
        return players[1],playerNumber
    elif playerNumber == 1:
        playerNumber =0
        return players[0],playerNumber    

def main(screen):
    """ The game loop used by curses.

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
    stone_removed = True

    is_stone_selected = False

    PlayerNumber = 0
   #Menu object
    start_menu = menu_start.startMenu(screen)

    #Map object
    map_board = Board_map.board_map(screen)
    #map_board.read_map()
    map_board.convert_map_to_coordinates()
    map_board.make_stone_list()
    map_board.stone_list_to_matrix()
    print(map_board.stone_pos_list)
    

    #_player list
    players = []
    
    if start_menu.get_is_menu_finished() == False:
        start_menu.runMenu()
    player1_name = start_menu.player1_name
    player2_name = start_menu.player2_name
    player1= Player.player(map_board.screen,1,player1_name,9,9,"X",3,False)
    players.append(player1)
    player2= Player.player(map_board.screen,2,player2_name,9,9,"O",2,False)
    players.append(player2)
    
    _player = players[0] #player1
    
    while 1:
        map_board.screen.clear()

    
                
        if print_once == 0: 
            map_board.print_player_start(player1)
            print_once += 1    

        if stone_removed == False:
            _player.print_player_remove()

        if is_stone_selected == False and stone_removed == True and _player.phase == 2:
            _player.print_player_move()

        map_board.print_map()
        map_board.print_player_names(player1,player2)
        map_board.print_choice(_player)
        map_board.print_remaining_stone(players)
        map_board.print_phase(_player)
        map_board.print_player_stone_pool(players)
        map_board.screen.refresh()    
        
        # switch phases should maybe be done is a different way    
        _player.switch_to_phase()
        _player.check_looser()            
        if _player.lose:
            winner = player2_name
            print("hej")
            quit()             
    
        map_board.stone_list_to_matrix()

        print(PlayerNumber)
                
        key = screen.getch()
    
        if key == curses.KEY_LEFT:
            _player.move_left(map_board.stone_pos_list)  

        elif key == curses.KEY_RIGHT: 

            _player.move_right(map_board.stone_pos_list)
        elif key == curses.KEY_DOWN:
            _player.move_down(map_board.stone_pos_list)
        elif key == curses.KEY_UP:
            _player.move_up(map_board.stone_pos_list)
        
        elif key == curses.KEY_ENTER or key in [10, 13]:
                
            #phase1
            if (_player.phase == 1):
                
                if _player.can_player_act(map_board.stone_pos_list) == True and stone_removed == True:
                    print(map_board.stone_pos_list)
                    new_stone_list = _player.place_stone(map_board.get_stone_pos_list())
                    map_board.set_stone_pos_list(new_stone_list)
                    map_board.stone_list_to_matrix()
                    
                    _player.check_both(map_board.get_matrix())
                    
                    
                    if _player.has_3_in_row  == True:
                        stone_removed = False
                    else:
                        print("lol")
                        _player,PlayerNumber = switch_turn(players,PlayerNumber)
                elif _player.has_3_in_row  == True  and stone_removed == False and _player.can_player_remove(map_board.stone_pos_list)  == True:
                                        
                    map_board.set_stone_pos_list(_player.remove_stone_player(map_board.stone_pos_list))
                    
                    
                    _player.remove_old_3(map_board.stone_pos_list)
                    #list_3_row = []
                    #list_3_col = []
                    _player,PlayerNumber = switch_turn(players,PlayerNumber)

                    stone_removed = True
            #phase 2
            """
            elif ((player1_phase == 2 and player1_turn == True) or (player2_phase == 2 and player1_turn == False)) == True:
                neighbours = find_all_neighbours(plus_list,matrix,current_row)
                player_can_move_stone = can_player_move_stone(plus_list,current_row,player1_turn,neighbours)
                
                if player_can_move_stone == True and stone_removed == True and is_stone_selected == False:
                    stone_marker=which_stone(player1_turn)
                    selected_stone_index = get_selected_stone_index(current_row)
                    is_stone_selected = True
                    matrix = plus_list_to_matrix(plus_list,matrix)
                    list_3_row,list_3_col = remove_old_3(plus_list,selected_stone_index,list_3_row,list_3_col)

                elif  is_stone_selected == True and stone_removed == True:
                    #had to move this if statement inside because selected stone index
                    
                    if is_neighbour_a_plus(plus_list,current_row,neighbours,selected_stone_index) == True:

                        matrix = plus_list_to_matrix(plus_list,matrix)

                        plus_list = move_stone(plus_list,current_row,player1_turn,selected_stone_index)
                        #this makes it too op to just move in and out from a three in a row 
                        list_3_row,list_3_col = remove_old_3(plus_list,selected_stone_index,list_3_row,list_3_col)
                        #list_3_row = []
                        #list_3_col = []
                        
                        matrix = plus_list_to_matrix(plus_list,matrix)
                        list_3_row,list_3_col,has_3_in_row  = check_both(matrix,list_3_row,list_3_col,player1_turn)
                        is_stone_selected = False
            
                        if has_3_in_row  == True:
                            stone_removed = False
                        elif is_stone_selected == False:
                            player1_turn = switch_player_turn(player1_turn)
                            
                elif has_3_in_row  == True  and stone_removed == False and can_player_remove(plus_list,current_row ,player1_turn)  == True and is_stone_selected == False:
                    plus_list,remaining_stones_player1,remaining_stones_player2= remove_stone_player( plus_list,current_row,player1_turn,remaining_stones_player1,remaining_stones_player2)
                    matrix = plus_list_to_matrix(plus_list,matrix)
                    list_3_row,list_3_col = remove_old_3(plus_list,current_row,list_3_row,list_3_col)
                    #list_3_row = []
                    #list_3_col = []
                    
                    player1_turn = switch_player_turn(player1_turn)
                    stone_removed = True
            #phase 3
            elif ((player1_phase == 3 and player1_turn == True) or (player2_phase == 3 and player1_turn == False)) == True:
                player_can_move_stone = can_player_move_stone(plus_list,current_row,player1_turn,neighbours =None)
                
                if player_can_move_stone == True and stone_removed == True and is_stone_selected == False:
                    stone_marker=which_stone(player1_turn)
                    selected_stone_index = get_selected_stone_index(current_row)
                    is_stone_selected = True
                    matrix = plus_list_to_matrix(plus_list,matrix)


                elif  is_stone_selected == True and stone_removed == True:
                    #had to move this if statement inside because selected stone index
                    #if is_neighbour_a_plus(plus_list,current_row,neighbours,selected_stone_index) == True:
                    if plus_list[current_row][0] == "+":
                        plus_list = move_stone(plus_list,current_row,player1_turn,selected_stone_index)
                        #this makes it too op to just move in and out from a three in a row 
                            
                        list_3_row,list_3_col = remove_old_3(plus_list,selected_stone_index,list_3_row,list_3_col)
                        #list_3_row = []
                        #list_3_col = []
                        
                        matrix = plus_list_to_matrix(plus_list,matrix)

                        list_3_row,list_3_col,has_3_in_row  = check_both(matrix,list_3_row,list_3_col,player1_turn)
                        is_stone_selected = False
            
                        if has_3_in_row  == True:
                            stone_removed = False
                        elif is_stone_selected == False:
                            player1_turn = switch_player_turn(player1_turn)

                        
                elif has_3_in_row  == True  and stone_removed == False and can_player_remove(plus_list,current_row ,player1_turn)  == True and is_stone_selected == False:
                    plus_list,remaining_stones_player1,remaining_stones_player2= remove_stone_player( plus_list,current_row,player1_turn,remaining_stones_player1,remaining_stones_player2)
                    matrix = plus_list_to_matrix(plus_list,matrix)
                    list_3_row,list_3_col = remove_old_3(plus_list,current_row,list_3_row,list_3_col)
                    #list_3_row = []
                    #list_3_col = []
                    
                    player1_turn = switch_player_turn(player1_turn)
                    stone_removed = True                     
            """
        # 27 = Escape key
        elif key == 27:     
            quit()
        
        # Prevent the screen from repainting to often
        time.sleep(0.01)
    

    
    

curses.wrapper(main)