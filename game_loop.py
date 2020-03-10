import Board_map
import Player
import menu_start
import curses
import os
import time
import random
import numpy as np
import itertools

class game_loop:
    def __init__(self,screen,player_name):
        self.screen = screen
        self.board = Board_map(screen)
        self.players = []




def main(screen,player1_name,player2_name):
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
   
    # specify the current selected row
    current_row = 0

    # The path of the textfile of the map
    map_path = 'Ascii_board.txt'
    #string of the map
    map_string = read_map(map_path)
    
    #test
    matrix = convert_map_matrix(map_string)
    #test_ends

    #coordinates of the chars in the map
    map_coordinates =convert_map_to_coordinates(map_string)
    
    # plus_list, coordinates of the "+" chars in the map_coordinates list 
    plus_list = make_plus_list(map_coordinates)
    
    #player1_turn will determine which player that will start ,True for player1
    player1_turn = random_player_start()
    
    #The amount of stones left to be placed,if these amounts = 0 phase1 ends
    stone_pool_player1 = 9
    stone_pool_player2 = 9

    #The total amount of stones, if one of these amounts <= 2 that player loses
    remaining_stones_player1 = 9
    remaining_stones_player2 = 9
    
    #Prints player start text once
    print_once = 0
    list_3_row = []
    list_3_col = []
   
    #If player has removed a stone = True else False
    stone_removed = True

    #Which phase
    player1_phase = 1
    player2_phase = 1

    #phase 2 stuff
    is_stone_selected = False

    while 1:
        
        screen.clear()

    
                
        if print_once == 0: 
            print_player_start(screen,player1_turn,player1_name,player2_name)
            print_once += 1    

        if stone_removed == False:
            print_player_remove(screen,player1_turn,player1_name,player2_name)

        if is_stone_selected == False and stone_removed == True:
            if (player1_phase == 2 and player1_turn == True) or (player2_phase == 2 and player1_turn == False):
                print_player_move(screen,player1_turn,player1_name,player2_name)

        print_map(screen,map_coordinates,stone_pool_player1,stone_pool_player2)            
        print_player_names(screen,player1_name,player2_name)
        print_choice(screen,current_row,plus_list,player1_turn)
        print_remaining_stone(screen,remaining_stones_player1,remaining_stones_player2)
        print_phase(screen,player1_turn,player1_phase,player2_phase)
        screen.refresh()    
        
        # switch phases should maybe be done is a different way    
        player1_phase,player2_phase = switch_to_phase(player1_phase,player2_phase,stone_pool_player1,stone_pool_player2,remaining_stones_player1,remaining_stones_player2)
        
        if check_looser(remaining_stones_player1):
            winner = player2_name
            quit()             
        elif check_looser(remaining_stones_player2):
            winner = player1_name
            quit()
        

        if player1_phase == 2 or player2_phase == 2:
            if check_invalid_move(plus_list,matrix,player1_turn) == False:
                if player1_turn == True: 
                    print( player1_name+" lost")
                else:
                    print( player2_name+" lost")

                quit()
                
        key = screen.getch()
        
        if key == curses.KEY_LEFT:  
            current_row = move_left(plus_list, current_row)
        
        elif key == curses.KEY_RIGHT: 
            current_row = move_right(plus_list, current_row)
        
        elif key == curses.KEY_DOWN:
            current_row = move_down(plus_list,current_row)

        elif key == curses.KEY_UP:
            current_row = move_up(plus_list,current_row)
        
        elif key == curses.KEY_ENTER or key in [10, 13]:
            #phase1
            if ((player1_phase == 1 and player1_turn == True) or (player2_phase == 1 and player1_turn == False)) == True:
                player_can_act = can_player_act(plus_list,current_row,stone_pool_player1,stone_pool_player2,player1_turn) 
                
                if player_can_act == True and stone_removed == True:

                    stone_marker = which_stone(player1_turn)
                    plus_list, stone_pool_player1, stone_pool_player2 = place_stone(plus_list, current_row, stone_marker, stone_pool_player1, stone_pool_player2)
                    matrix = plus_list_to_matrix(plus_list,matrix)
                    

                    
                    list_3_row, list_3_col, has_player_3_row = check_both(matrix,list_3_row,list_3_col,player1_turn)
                    
                    if has_player_3_row == True:
                        stone_removed = False
                    else:
                        player1_turn = switch_player_turn(player1_turn)  

                elif has_player_3_row == True  and stone_removed == False and can_player_remove(plus_list,current_row ,player1_turn)  == True:
                                        
                    plus_list,remaining_stones_player1,remaining_stones_player2= remove_stone_player( plus_list,current_row,player1_turn,remaining_stones_player1,remaining_stones_player2)
                    
                    
                    list_3_row,list_3_col = remove_old_3(plus_list,current_row,list_3_row,list_3_col)
                    #list_3_row = []
                    #list_3_col = []

                    matrix = plus_list_to_matrix(plus_list,matrix)
                    player1_turn = switch_player_turn(player1_turn)
                    stone_removed = True
            #phase 2
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
                        list_3_row,list_3_col,has_player_3_row = check_both(matrix,list_3_row,list_3_col,player1_turn)
                        is_stone_selected = False
            
                        if has_player_3_row == True:
                            stone_removed = False
                        elif is_stone_selected == False:
                            player1_turn = switch_player_turn(player1_turn)
                            
                elif has_player_3_row == True  and stone_removed == False and can_player_remove(plus_list,current_row ,player1_turn)  == True and is_stone_selected == False:
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

                        list_3_row,list_3_col,has_player_3_row = check_both(matrix,list_3_row,list_3_col,player1_turn)
                        is_stone_selected = False
            
                        if has_player_3_row == True:
                            stone_removed = False
                        elif is_stone_selected == False:
                            player1_turn = switch_player_turn(player1_turn)

                        
                elif has_player_3_row == True  and stone_removed == False and can_player_remove(plus_list,current_row ,player1_turn)  == True and is_stone_selected == False:
                    plus_list,remaining_stones_player1,remaining_stones_player2= remove_stone_player( plus_list,current_row,player1_turn,remaining_stones_player1,remaining_stones_player2)
                    matrix = plus_list_to_matrix(plus_list,matrix)
                    list_3_row,list_3_col = remove_old_3(plus_list,current_row,list_3_row,list_3_col)
                    #list_3_row = []
                    #list_3_col = []
                    
                    player1_turn = switch_player_turn(player1_turn)
                    stone_removed = True                     

        # 27 = Escape key
        elif key == 27:     
            quit()
        
        # Prevent the screen from repainting to often
        time.sleep(0.01)
    
