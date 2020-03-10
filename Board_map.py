import os 
import curses
import time
import numpy as np 
import itertools
import Player


class board_map:
    def __init__(self,screen):
        self.matrix = []
        self.stone_pos_list = []
        self.board_txt = ""
        self.map_path = map_path = 'Ascii_board.txt'
        self.map_coordinates = []
        self.screen = screen
       
    def read_map(self):
        """
        Reads a text file and returns it as a string


        Keyword arguments:
        path -- path of the file

        """
        try:        
            board = open( self.map_path,'r')
            self.board_txt = board.read()
            board.close() 
            
        except IOError:
            
            raise Exception("Can not find the file at this path => "+ self.map_path)

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
        stone_pool_player_x = -9 + w//3   
        stone_pool_player_y = 9
        if self.player_num == 2:
            stone_pool_player_x = 30  + w//3 
            stone_pool_player_y = 9
        
        for player in players:
            for i in range(self.stone_pool):

                self.screen.addstr(stone_pool_player_y+i,stone_pool_player_x,player.stone_marker,curses.color_pair(player.color))
    def print_phase(self,player):
            h,w = screen.getmaxyx()

            #To place the game board in the center of the window  
         
           
            #print phase
            phase_txt_y =  4
            phase_txt_x =  6 + w//3
            self.screen.addstr(phase_txt_y,phase_txt_x,"Phase: "+str(player.phase),curses.color_pair(player.color))

    def print_remaining_stone(self,players):
        """Prints the amount of stones left for player1 and player2 at the left and right side of the board

        Keyword arguments:
        screen -- the curses screen
        remaining_stones_player1 = the total amount of stones for player1
        remaining_stones_player2 = the total amount of stones for player2
        """
        h,w = screen.getmaxyx()
        for player in players:
        #Positions of the text showing the remaining stones for player1 ¨
            if player.player_num == 1:
                remaining_stones_player1_x = -22 + w//3   
                remaining_stones_player1_y = 7
                screen.addstr(remaining_stones_player1_y,remaining_stones_player1_x,"Remaining stones: "+str(player.remaining_stones),curses.color_pair(player.color))

            #Positions of the text showing the remaining stones for player2 
            remaining_stones_player2_x = 30 + w//3   
            remaining_stones_player2_y = 7
            screen.addstr(remaining_stones_player2_y,remaining_stones_player2_x,"Remaining stones: "+str(player.remaining_stones),curses.color_pair(player.color))

    def print_choice(self,players):
        """Prints all plusses in plus_list on the screen. The currently selected plus is colored.

        Keyword arguments:
        screen -- the curses screen
        selected_move_idx -- the currently selected row in the plus_list
        plus_list -- the lists of all the "+" and their positions
        player1_turn -- bool,True for player1  and False for player2
        """    
        h, w = self.screen.getmaxyx()
        for player in players:
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
                    
            
    
    
    def plus_list_to_matrix(self):
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
        
       
  
        self.screen.addstr(text_y,text_x,player.player_name.rstrip("\n")+" will start!",curses.color_pair(player.player_color))


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

