import os 
import curses
import time
class board_map:
    def __init__(self,screen):
        self.matrix = []
        self.stone_pos_list = []
        self.board_txt = str
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
        
                

    def runMap(self):
        self.screen.clear()
        self.read_map()
        self.convert_map_to_coordinates()
        self.make_stone_list()
        self.print_map()
        # color scheme for player1        
        curses.init_pair(3,curses.COLOR_RED,curses.COLOR_BLACK)
        #player1= player.player(self.screen,1,"kalle",9,9,"X",3)
        self.player.print_player_names(player1)
        self.screen.refresh()

        time.sleep(3)
