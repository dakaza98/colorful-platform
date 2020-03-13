import os
import curses
import numpy as np
import itertools

#color scheme for player1


class player:
    def __init__(self,screen,player_number,player_name,stone_pool,stone_remaining,stone_marker,color,isAi):
        self.player_name = player_name
        self.stone_pool = stone_pool
        self.remaining_stones = stone_remaining
        self.stone_marker = stone_marker
        self.player_color = color
        #self.player1_turn = player1_turn
        self.is_Ai = isAi
        self.player_num = player_number
        self.phase = 1
        self.move_index = 0
        self.selected_stone_index = 0
        self.lose = False
        self.screen = screen
        self.turn = False
        self.neighbours = []
        self.has_3_in_row = False # if this is True player has 3 in a row

    
    def get_player_lose(self):
        return self.lose

    def switch_player_turn(self):
        
        self.turn = not (self.turn)

    def set_selected_stone_index(self):
        self.selected_stone_index = self.move_index

    def get_selected_stone_index(self):
        self.set_selected_stone_index()
        return self.selected_stone_index    

    def get_neighbours(self):
        
        return self.neighbours

    def print_player_stone_pool(self):
        h,w = self.screen.getmaxyx()
        stone_pool_player_x = -9 + w//3   
        stone_pool_player_y = 9
        if self.player_num == 2:
            stone_pool_player_x = 30  + w//3 
            stone_pool_player_y = 9
        for i in range(self.stone_pool):

            screen.addstr(stone_pool_player_y+i,stone_pool_player_x,self.stone_marker,curses.color_pair(self.player_color))

    def switch_to_phase(self):
        """ Switches to phase2 if both stone pools of the player are empty
        Return: Phase

        Keyword arguments:
        phase -- the current phase of the game 
        stone_pool_player1 -- The amount of stone player1 has left to place
        stone_pool_player2 -- The amount of stone player2 has left to place
        """
        if self.stone_pool == 0 and self.remaining_stones > 3:
            self.phase = 2 
        elif self.remaining_stones <= 3:
            self.phase = 3   

    def check_player_remaining_stones(self):
        if self.remaining_stones <= 2:
            return True
        else:
            return False
    ####
    def lose_find_stone_neighbour_row(self,plus_list,matrix,current_row):
        current_stone_y = int(plus_list[current_row][2])
        current_stone_x = int(plus_list[current_row][1])
        row = matrix[current_stone_y]
        neighbours = []

        # look a head and behind for neighbour
        for x in reversed(range(0,current_stone_x)):
            elem = matrix[current_stone_y][x]
            if elem == " ":
                break
            elif (elem[0] == "X" or elem[0] == "O" or elem[0] == "+") and x != current_stone_x:
                neighbours.append([elem[0],x,current_stone_y])
                break
                

        for x in range(current_stone_x,len(row)):
            elem = matrix[current_stone_y][x]
            if elem == " ":
                break
                
            elif(elem[0] == "X" or elem[0] == "O" or elem[0] == "+") and x != current_stone_x:
                neighbours.append([elem[0],x,current_stone_y])
                break
                    

        return neighbours                    


    def lose_find_stone_neighbour_col(self,plus_list,matrix,current_row):
        #flipps the matrix so row becomes the columns ande vice versa
        matrix = np.transpose(matrix)
        current_stone_y = int(plus_list[current_row][2])
        current_stone_x = int(plus_list[current_row][1])
        col = matrix[current_stone_x]
        neighbours = []
        # look a head for neighbor
        for y in reversed(range(0,current_stone_y)):
            elem = matrix[current_stone_x][y]
            if elem == " ":
                break   
            
            elif (elem[0] == "X" or elem[0] == "O" or elem[0] == "+") and y != current_stone_y :
                neighbours.append([elem[0],current_stone_x,y])
                break
                
        for y in range(current_stone_y,len(col)):
            elem = matrix[current_stone_x][y]
            if elem == " ":
                break

            elif (elem[0] == "X" or elem[0] == "O" or elem[0] == "+") and y != current_stone_y:
                neighbours.append([elem[0],current_stone_x,y])
                break
                
        return neighbours   

    #den andra find all neighbours funkar inte för att hitta om en spelare förlorat,då andra inte tar in index som input
    def lose_find_all_neighbours(self,plus_list,matrix,current_row):
        neighbour_row  = self.lose_find_stone_neighbour_row(plus_list,matrix,current_row)
        neighbour_col = self.lose_find_stone_neighbour_col(plus_list,matrix,current_row)
        neighbours = neighbour_row + neighbour_col
        return neighbours 

    def check_player_stuck(self,plus_list,matrix):

        if self.phase == 2:
            for index,elem in enumerate(plus_list):
                char = elem[0]
                if char == self.stone_marker:
                    neighbours = self.lose_find_all_neighbours(plus_list,matrix,index)

                    for neighbour in neighbours:
                        if neighbour[0] == "+":
                            return False
            return True                
        return False
    def has_player_lost(self,plus_list,matrix):
        if(self.check_player_remaining_stones()== True or self.check_player_stuck(plus_list,matrix) == True):
            self.lose = True
            
        
        
    def move_down(self,plus_list):
        """ Finds the "+" char that is above self.move_index. If the current "+" char is at a coordinate that
            that violates the rules for move_indexment, the position wont change.
        Returns the new x position of the "+"  


        self.move_index -- the currently selected position in the plus_list
        plus_list -- the lists of all the "+" and their positions
        middle -- middle of the map, the values of x range 4,8,12..,28 and the values of y range 0,2,4..,12.
        """
        new_location = self.move_index
        current_location = self.move_index

        middle = 12, 6
        step = 4, 2
        
        while True:
            new_location += 1
            if new_location == len(plus_list):
                new_location = 0
            
            current_x = plus_list[current_location][1]
            new_x = plus_list[new_location][1]

            current_y = plus_list[current_location][2]
            new_y = plus_list[new_location][2]
            if current_x == new_x and current_y != new_y:
                #Check if allowed to move_index down
                if (int(current_x) != middle[0] and int(current_y) <= middle[1]) or (int(current_x) == middle[0] and int(current_y) != middle[1]-step[1] and int(current_y) != middle[1]+step[1]*3):
                    self.move_index = new_location
                    break
                else:
                    self.move_index = current_location
                    break
               
 

    def move_up(self,plus_list):
        """ Finds the "+" char that is above self.move_index. If the current "+" char is at a coordinate that
            that violates the rules for move_indexment, the positiono wont change.
        Returns the new x position of the "+"  


        self.move_index -- the currently selected position in the plus_list
        plus_list -- the lists of all the "+" and their positions
        middle -- middle of the map, the values of x range 4,8,12..,28 and the values of y range 0,2,4..,12.
        """
        new_location = self.move_index
        current_location = self.move_index
        middle = 12, 6
        step = 4, 2

        while True:
            if new_location == 0:
                new_location = len(plus_list)

            new_location -= 1
            current_x = plus_list[current_location][1]
            new_x = plus_list[new_location][1]

            current_y = plus_list[current_location][2]
            new_y = plus_list[new_location][2]
            current_y = plus_list[self.move_index][2]
            new_y = plus_list[new_location][2]
            if current_x == new_x and current_y != new_y:
                if (int(current_x) != middle[0] and int(current_y) >= middle[1]) or int(current_x) == middle[0] and int(current_y) != middle[1]-step[1]*3 and int(current_y) != middle[1]+step[1]:
                    self.move_index = new_location
                    break

                else:
                    self.move_index = current_location
                    break

    def move_right(self,plus_list):
        """ Finds the "+" char that is right of self.move_index. If the current "+" char is at a coordinate that
            that violates the rules for move_indexment, the positiono wont change.
        Returns the new x position of the "+"  


        self.move_index -- the currently selected position in the plus_list
        plus_list -- the lists of all the "+" and their positions
        middle -- middle of the map, the values of x range 4,8,12..,28 and the values of y range 0,2,4..,12.
        """
        new_location = self.move_index
        current_location = self.move_index

        middle = 12, 6
        step = 4, 2
        
        while True:
            new_location += 1
            if new_location == len(plus_list):
                new_location = 0
            
            current_x = plus_list[current_location][1]
            new_x = plus_list[new_location][1]

            current_y = plus_list[current_location][2]
            new_y = plus_list[new_location][2]
            if current_y == new_y and current_x != new_x:
                #Check if allowed to move_index left
                if (int(current_y) != middle[1] and int(current_x) <= middle[0]) or (int(current_y) == middle[1] and int(current_x) != middle[0]-step[0] and int(current_x) != middle[0]+step[0]*3):
                    self.move_index = new_location
                    break

                else:
                    self.move_index = current_location
                    break
                    

                    


    def move_left(self,plus_list):
        """ Finds the "+" char that is left of self.move_index. If the current "+" char is at a coordinate that
            that violates the rules for move_indexment, the positiono wont change.
        Returns the new x position of the "+"  

        self.move_index -- the currently selected position in the plus_list
        plus_list -- the lists of all the "+" and their positions
        middle -- middle of the map, the values of x range 4,8,12..,28 and the values of y range 0,2,4..,12.
        """
        new_location = self.move_index
        current_location = self.move_index

        middle = 12, 6
        step = 4, 2
        
        while True:
            new_location -= 1
            if new_location == len(plus_list):
                new_location = 0
            
            current_x = plus_list[current_location][1]
            new_x = plus_list[new_location][1]

            current_y = plus_list[current_location][2]
            new_y = plus_list[new_location][2]
            if current_y == new_y and current_x != new_x:
                #Check if allowed to move_index left
                if (int(current_y) != middle[1] and int(current_x) >= middle[0]) or (int(current_y) == middle[1] and int(current_x) != middle[0]-step[0]*3 and int(current_x) != middle[0]+step[0]):
                    self.move_index = new_location
                    break

                else:
                    self.move_index = current_location
                    break





    def  move_stone(self,plus_list):
        
        plus_list[self.selected_stone_index][0] = "+"
        plus_list[self.move_index][0] = self.stone_marker
        return plus_list

    def remove_stone_player(self,plus_list,players):
        """ Places a removes on the map by changing the player stone to a "+"
        Returns the changed plus_list list

        self.move_index -- the currently selected row in the plus_list
        plus_list -- the lists of all the "+" and their positions
        stone_pool_player1 -- The amount of stone player1 has left to place
        stone_pool_player2 -- The amount of stone player2 has left to place
        
        """
        if self.stone_marker == "X": 
            remove_stone_marker = "O"
        
        elif self.stone_marker == "O":

            remove_stone_marker = "X" 
        OtherPlayer = players[1]
        if self.player_num == 2:
            OtherPlayer = players[0]

        OtherPlayer.remaining_stones -= 1
        

        if plus_list[self.move_index][0] == remove_stone_marker:    
            plus_list[self.move_index][0] = "+"
        

        return plus_list
    
    def place_stone(self,plus_list):
        """ Places a stone on the map by changing the "+" to "X" or "O"
        Returns the changed plus_list list

        self.move_index -- the currently selected row in the plus_list
        plus_list -- the lists of all the "+" and their positions
        stone_marker -- the char of the stone, should be either "X" or "O" 
        stone_pool_player1 -- The amount of stone player1 has left to place
        stone_pool_player2 -- The amount of stone player2 has left to place
        
        """
        
        self.stone_pool -= 1
        plus_list[self.move_index][0] = self.stone_marker
        return plus_list

    def print_player_remove(self):
        """ Prints the name of player who will be able to remove a stone at the top of the screen
        
        Keyword arguments:
        screen -- the curses screen
        player1_turn -- bool, True is player1 turn and False is player2 turn    
        player1_name -- player1 name as string
        player2_name -- player2 name as string

        """
        h,w = self.screen.getmaxyx()

        #position of text 
        text_x = 3  + w//3 
        text_y = 2
        player_txt = self.player_name
        if len(  self.player_name) ==0:
            player_txt = "Player" + str(self.player_num) 
        self.screen.addstr(text_y,text_x,player_txt.rstrip("\n")+" remove a stone!",curses.color_pair(self.player_color))


    def can_player_act(self,plus_list):
        """Determines if a player is allowed to act
        Returns bool -- Can player act = True else False

        Keyword argument 
        plus_list -- list of "+" and placed stones
        self.move_index --  currently selected row in the plus_list
        stone_pool_player1 -- the amount of stone player1 has
        stone_pool_player2 -- the amount of stone player2 has
        player1_turn -- bool, True is player1 turn and False is player2 turn    
            
        """
        current_char = plus_list[self.move_index][0]
      
        can_not_act= self.stone_pool <= 0 or current_char != "+" 
        if can_not_act == True:    
            return False

        return True

    def print_player_move(self):
        """ Prints the name of player who will be able to move a stone at the top of the screen
        
        Keyword arguments:
        screen -- the curses screen
        player1_turn -- bool, True is player1 turn and False is player2 turn    
        player1_name -- player1 name as string
        player2_name -- player2 name as string

        """
        h,w = self.screen.getmaxyx()

        #position of text 
        text_x = 1  + w//3 
        text_y = 2
        player_txt = self.player_name
        if len(  player_txt) ==0:
            player_txt = "Player" + str(self.player_num) 
        self.screen.addstr(text_y,text_x,player_txt.rstrip("\n")+" move a stone to a neighbour!",curses.color_pair(self.player_color))
       
    def can_player_remove(self,plus_list):
        """Determines if a player can remove a stone
        Returns bool -- Can player remove a stone = True else False

        Keyword argument 
        plus_list -- list of "+" and placed stones
        self.move_index --  currently selected row in the plus_list
        player1_turn -- bool, True is player1 turn and False is player2 turn    
        """
        current_car = plus_list[self.move_index][0]
        remove_stone_marker = "O"
        if self.stone_marker == "O":
            remove_stone_marker = "X"
        if current_car == remove_stone_marker:
            return True
        return False        

    def can_player_move_stone(self,plus_list):
        stone_marker = "X"
        if self.stone_marker == "O":
            stone_marker = "O"
        current_stone_y = plus_list[self.move_index][2]
        current_stone_x = plus_list[self.move_index][1]
        if self.phase == 3 and plus_list[self.move_index][0] == stone_marker:
            return True
        elif plus_list[self.move_index][0] == stone_marker and "+" in itertools.chain( *self.neighbours):
                return True
        return False
    

    """
    def get_selected_stone_index(self.move_index):
        return self.move_index
    """

    def find_stone_neighbour_row(self,plus_list,matrix):
        current_stone_y = int(plus_list[self.move_index][2])
        current_stone_x = int(plus_list[self.move_index][1])
        row = matrix[current_stone_y]
        neighbours = []

        # look a head and behind for neighbour
        for x in reversed(range(0,current_stone_x)):
            elem = matrix[current_stone_y][x]
            if elem == " ":
                break
            elif (elem[0] == "X" or elem[0] == "O" or elem[0] == "+") and x != current_stone_x:
                neighbours.append([elem[0],x,current_stone_y])
                break
                

        for x in range(current_stone_x,len(row)):
            elem = matrix[current_stone_y][x]
            if elem == " ":
                break
                
            elif(elem[0] == "X" or elem[0] == "O" or elem[0] == "+") and x != current_stone_x:
                neighbours.append([elem[0],x,current_stone_y])
                break
                    

        return neighbours                    


    def find_stone_neighbour_col(self,plus_list,matrix):
        #flipps the matrix so row becomes the columns ande vice versa
        matrix = np.transpose(matrix)
        current_stone_y = int(plus_list[self.move_index][2])
        current_stone_x = int(plus_list[self.move_index][1])
        col = matrix[current_stone_x]
        neighbours = []
        # look a head for neighbor
        for y in reversed(range(0,current_stone_y)):
            elem = matrix[current_stone_x][y]
            if elem == " ":
                break   
            
            elif (elem[0] == "X" or elem[0] == "O" or elem[0] == "+") and y != current_stone_y :
                neighbours.append([elem[0],current_stone_x,y])
                break
                
        for y in range(current_stone_y,len(col)):
            elem = matrix[current_stone_x][y]
            if elem == " ":
                break

            elif (elem[0] == "X" or elem[0] == "O" or elem[0] == "+") and y != current_stone_y:
                neighbours.append([elem[0],current_stone_x,y])
                break
                
        return neighbours   

    def find_all_neighbours(self,plus_list,matrix):
        neighbour_row  = self.find_stone_neighbour_row(plus_list,matrix)
        neighbour_col = self.find_stone_neighbour_col(plus_list,matrix)
        all_neighbours = neighbour_row + neighbour_col
        self.neighbours = all_neighbours

    def is_neighbour_a_plus(self,plus_list):
        elem = plus_list[self.move_index]
        selected_stone = plus_list[self.selected_stone_index]
        if elem[0] == "+" and self.phase ==3:
            return True
        elif elem[0] == "+" and selected_stone in self.neighbours and self.phase == 2:
            return True
        return False    

