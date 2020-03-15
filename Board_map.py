import os 
import curses
import time
import numpy as np 
import itertools
import Player
import json

class board_map:
    def __init__(self,screen):
        self.matrix = []
        self.stone_pos_list = []
        self.board_txt = ""
        self.map_path = map_path = 'Ascii_board.txt'
        self.map_coordinates = []
        self.screen = screen
        self.is_three_row = False # this check for row
        self.is_three_col = False #this check for col

        self.list_3_row = []
        self.list_3_col = []

    
        self.neighbours = []

    def convert_stone_list_to_json(self):
        data = {}
        data['Board'] =  {}
        for i,stone  in enumerate( self.stone_pos_list,0):
            stone_marker = stone[0]
            if stone_marker == "+":
                data['Board'][str(i)] = -1
            elif stone_marker == "X":
                data['Board'][str(i)] = 0
            elif stone_marker == "O":
                data['Board'][str(i)] = 1
        return data
    
    def convert_json_to_stone_list(self,json_obj):
        data = json_obj
        board = data['Board']
        for i,stone in enumerate(self.stone_pos_list):
            if board.get(str(i)) == -1:
                self.stone_pos_list[i][0] = "+"
            elif board.get(str(i)) == 0:
                self.stone_pos_list[i][0] = "X"
            elif board.get(str(i)) == 1:
                self.stone_pos_list[i][0] = "O"         
    

    def read_map(self):
        """
        Reads a text file and returns it as a string


        Keyword arguments:
        path -- path of the file

        """
        try:        
           with open( self.map_path,'r') as board:
                self.board_txt = board.read()
                board.close() 
            
        except IOError:
            
            raise Exception("Can not find the file at this path => "+ self.map_path)
    
    def check_row(self,player):
        """Checks if the game board has three of the same stones in a row vertically.
        
        Returns self.list_3_row and is_three_row -- bool, will be True if a new three in a row has been found  
        Keyword arguments:
        matrix -- the matrix of the board
        player1_turn -- bool, True is player1 turn and False is player2 turn    
        self.list_3_row -- list of all the three in a row that has been found
        """
        player_stone = player.stone_marker
        opponent_stone = 'O'
        is_three_row = False
        
        if player.stone_marker == 'O':
            opponent_stone = 'X'
        
        for row in (self.matrix):
            check_player = []
            found_player_stone = False
            count = 0

            for item in row:
                
                if item[0] == player_stone:
                    found_player_stone = True
                    count += 1
        
                if item[0] == ' ' or item[0] == opponent_stone:# or item[0] == '|':
                    count = 0
                    #if item == ' ':
                    #    id_row += 1
                    
                    check_player = []
                    #found_player_stone = False     
        
                elif found_player_stone == True and item[0] == player_stone: #!= ' ':
                    check_player.append(item)
        
                amount_player_stone = check_player.count(player_stone) 
        
                if count == 3:
        
                    if (check_player) not in self.list_3_row:
                        self.is_three_row = True
                        self.list_3_row.append(check_player)
                        return
        self.is_three_row = False
    

                 
    def check_col(self,player):
        """Checks if the game board has three of the same stones in a row horizontally.
        
        Returns self.list_3_col  and is_three_column -- bool, will be True if a new three in a row in a column has been found  
        Keyword arguments:
        matrix -- the matrix of the board
        player1_turn -- bool, True is player1 turn and False is player2 turn    
        self.list_3_col -- list of all the three in a row in a column that has been found
        """    
        transponse_matrix = np.transpose(self.matrix)
        player_stone = player.stone_marker
        opponent_stone = 'O'
        
        
        
        if player.stone_marker == 'O':
            opponent_stone = 'X'
        
        for row in transponse_matrix:
            check_player = []
            found_player_stone = False
            count = 0
            for item in row:
                
                if item[0] == player_stone:
                    found_player_stone = True
                    count += 1
                    
        
                if item[0] == ' ' or item[0] == opponent_stone:# or item == '-':
        
                    #if item == ' ':
                        #id_col += 1
                    count = 0
                    check_player = []
                    #found_player_stone = False     

                elif found_player_stone == True and item[0] == player_stone:
                    check_player.append(item)
                
                
        
                amount_player_stone = check_player.count(player_stone) 
                
                if count == 3:
        
                    if (check_player) not in self.list_3_col:
                        self.is_three_col = True

                        self.list_3_col.append(check_player)
                        return
        self.is_three_col = False


    def check_both(self,player):
        """Checks if the game board has three of the same stones in a row either vertically or horizontally.
        
        Returns  self.list_3_row ,self.list_3_col,bool which will be True if a new three in a row has been found  
        Keyword arguments:
        matrix -- the matrix of the board
        player1_turn -- bool, True is player1 turn and False is player2 turn
        self.list_3_row -- list of all the three in a row that has been found
        self.list_3_col -- list of all the three in a row in a column that has been found
        """        
        self.check_row(player)
        self.check_col(player)
        

        if self.is_three_row == True or self.is_three_col == True:
            player.has_3_in_row = True
        else:
            player.has_3_in_row = False


    def remove_old_3(self,player):
        current_stone_x = self.stone_pos_list[player.move_index][1]
        current_stone_y = self.stone_pos_list[player.move_index][2]
     
        for r in self.list_3_row:
            for row in r:
                if current_stone_x == row[1] and current_stone_y == row[2] or row[0] == '+':
                    self.list_3_row.remove(r)
                    
        for c in self.list_3_col:
            for col in c:
                if current_stone_x == col[1] and current_stone_y == col[2] or col[0] == '+':
                    self.list_3_col.remove(c)      


    def set_stone_pos_list(self,new_list):
        self.stone_pos_list = new_list    

    def get_stone_pos_list(self):
        return self.stone_pos_list

    def get_matrix(self):
        return self.matrix
    def convert_map_to_coordinates(self):
        """
        Converts the string version of the map to coordinates
    
        Returns a list of lists where every list has [char,xPos,Ypos]
        Example "X  " => [['X', 0, 0], [' ', 1, 0], [' ', 2, 0]...,]

        Keyword arguments:
        str_board -- the string version of the map
        """
        self.matrix = [[x for x in line] for line in self.board_txt.split('\n')]

        y = 0
        for row in self.matrix:
            x = 0
            for c in row:
                char_xy = [c,x,y]    
                self.map_coordinates.append(char_xy)
                x += 1
            y += 1
        
    def make_stone_list(self):
        """
        Finds all the "+" chars in  map_coordinates 
        Returns a list of lists where every list has ["+",xPos,Ypos]
        Example [['X', 0, 0], [' ', 1, 0],...,['+', '4', '0']] => [['+', '4', '0'],...]
        """
        for cord in self.map_coordinates:
            if cord[0] == "+":
                self.stone_pos_list.append([cord[0],int(cord[1]),int(cord[2])])

    def print_player_names(self,player1,player2):
        """Prints the playernames in the self.screen 

        Keyword arguments:
        self.screen -- the curses self.screen
        player1_name -- player1 name as string
        player2_name -- player2 name as string
        """
        h,w = self.screen.getmaxyx()
        
        player1_name_x = -10 + w//3   
        player1_name_y = 4
        self.screen.addstr(player1_name_y,player1_name_x,"Player"+str(player1.player_num ),curses.color_pair(player1.player_color))
        self.screen.addstr(player1_name_y+1,player1_name_x,player1.player_name,curses.color_pair(player1.player_color))       
        
        player2_name_x = 29  + w//3 
        player2_name_y = 4
        self.screen.addstr(player2_name_y,player2_name_x,"Player"+str(player2.player_num),curses.color_pair(player2.player_color))
        self.screen.addstr(player2_name_y+1,player2_name_x,player2.player_name,curses.color_pair(player2.player_color))
      
    def which_color_pair(self,stone_marker):
        """Picks a which color that will be choosed for the stone,
        depening if its an "O" or "x" 
        Returns color which is an int that represents the color_pair
        
        Keyword arguments:
        stone_marker -- char of the stone

        """
        color = 0

        if stone_marker== "O":
            color = 2
        elif stone_marker == "X" :
            color = 3
        return color
    def print_map(self):
        """Prints the all the chars except "+" in map_coordinates at their specified coordinate and stone pools for both players.

        Keyword arguments:
        screen -- the curses screen
        
        map_coordinates -- A list of lists where every list has the form [char, xPos, yPos]
        stone_pool_player1 -- The amount of stone player1 has left to place
        stone_pool_player2 -- The amount of stone player2 has left to place
        """
        for cord in self.map_coordinates:

            char = cord[0]
            
            if char == "+":        
                continue

            h,w = self.screen.getmaxyx()

            #To place the game board in the center of the window  
            y = cord[2]+ 9
            x = cord[1] +  w//3    
        
            color = self.which_color_pair(char)

            self.screen.addstr(y,x,char,curses.color_pair(color))
    
    def print_player_stone_pool(self,players):
        h,w = self.screen.getmaxyx()
    
        
        for player in players:
            stone_pool_player_x = -9 + w//3   
            stone_pool_player_y = 9
            if player.player_num == 2:
                stone_pool_player_x = 30  + w//3 
                stone_pool_player_y = 9
            for i in range(player.stone_pool):

                self.screen.addstr(stone_pool_player_y+i,stone_pool_player_x,player.stone_marker,curses.color_pair(player.player_color))
    def print_phase(self,player):
            h,w = self.screen.getmaxyx()

            #To place the game board in the center of the window  
         
           
            #print phase
            phase_txt_y =  4
            phase_txt_x =  6 + w//3
            self.screen.addstr(phase_txt_y,phase_txt_x,"Phase: "+str(player.phase),curses.color_pair(player.player_color))

    def print_remaining_stone(self,players):
        """Prints the amount of stones left for player1 and player2 at the left and right side of the board

        Keyword arguments:
        screen -- the curses screen
        remaining_stones_player1 = the total amount of stones for player1
        remaining_stones_player2 = the total amount of stones for player2
        """
        h,w = self.screen.getmaxyx()
        for player in players:
        #Positions of the text showing the remaining stones for player1 ¨
            if player.player_num == 1:
                remaining_stones_player1_x = -22 + w//3   
                remaining_stones_player1_y = 7
                self.screen.addstr(remaining_stones_player1_y,remaining_stones_player1_x,"Remaining stones: "+str(player.remaining_stones),curses.color_pair(player.player_color))

            #Positions of the text showing the remaining stones for player2 
            remaining_stones_player2_x = 30 + w//3   
            remaining_stones_player2_y = 7
            self.screen.addstr(remaining_stones_player2_y,remaining_stones_player2_x,"Remaining stones: "+str(player.remaining_stones),curses.color_pair(player.player_color))

    def print_choice(self,player):
        """Prints all plusses in plus_list on the screen. The currently selected plus is colored.

        Keyword arguments:
        screen -- the curses screen
        selected_move_idx -- the currently selected row in the plus_list
        plus_list -- the lists of all the "+" and their positions
        player1_turn -- bool,True for player1  and False for player2
        """    
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_RED)


        h, w = self.screen.getmaxyx()
        for idx, row in enumerate(self.stone_pos_list):

            # To have  the game board in the center, 5 is added y and w//3 is added to x
            y = int(row[2])+ 9
            x = int(row[1]) +  w//3      
            color =self.which_color_pair(row[0])
            if idx == player.move_index:
                color_cursor = 1
                #cursor will now have the player colors
                if player.player_num == 2:
                    color_cursor = 4
                self.screen.attron(curses.color_pair(color_cursor))
                self.screen.addstr(y,x, row[0])
                self.screen.attroff(curses.color_pair(color_cursor))
            else:
                self.screen.addstr(y, x, row[0],curses.color_pair(color))
                
        
    
    
    def stone_list_to_matrix(self):
        """Converts plus_list to a matrix
    
        Returns: matrix

        Keyword arguments:
        matrix -- matrix of all  the chars is the string version of the map
        plus_list -- the lists of all the "+" and their positions    
        """    
        for row in self.stone_pos_list:
            x = int(row[1]) 
            y = int(row[2])
            self.matrix[y][x]= row

    def print_player_start(self,player):
        """ Prints the name of player who will start to act at the top of the screen
        
        Keyword arguments:
        screen -- the curses screen
        player1_turn -- bool, True is player1 turn and False is player2 turn    
        player1_name -- player1 name as string
        player2_name -- player2 name as string

        """
        h,w = self.screen.getmaxyx()

        #position of text 
        text_x = 4  + w//3 
        text_y = 1
        player_name_txt = player.player_name

        if len(player.player_name) == 0:
            player_name_txt = "Player" + str(player.player_num)     
  
        self.screen.addstr(text_y,text_x,player_name_txt.rstrip("\n")+" will start!",curses.color_pair(player.player_color))

"""
def runMap(screen):
    
    board_map1 = board_map(screen)
    board_map1.screen.clear()
    board_map1.read_map()
    board_map1.convert_map_to_coordinates()
    board_map1.make_stone_list()
    board_map1.print_map()
    #curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    curses.init_pair(3,curses.COLOR_RED,curses.COLOR_BLACK)
    # color scheme for player2
    curses.init_pair(2,curses.COLOR_YELLOW,curses.COLOR_BLACK)  

    # color scheme for player1        
    
    player1= Player.player(board_map1.screen,1,"kalle",9,9,"X",3,False)
    player1.print_player_names()
    player2= Player.player(board_map1.screen,2,"kalle",9,9,"O",2,False)
    player2.print_player_names()
    players = [player1,player2]
    print(player2.player_num)
    board_map1.print_player_start(player1)
    board_map1.print_choice(players)

    board_map1.screen.refresh()

    time.sleep(3)
    quit()

"""