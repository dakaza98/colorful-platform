import os
import curses
#color scheme for player1


class player:
    def __init__(self,screen,player_number,player_name,stone_pool,stone_remaining,stone_marker,color,isBot):
        self.player_name = player_name
        self.stone_pool = stone_pool
        self.remaining_stones = stone_remaining
        self.stone_marker = stone_marker
        self.player_color = color
        #self.player1_turn = player1_turn
        self.is_bot = isBot
        self.player_num = player_number
        self.phase = 1
        self.move_index = 0
        self.lose = False
        self.screen = screen
        

    def print_player_names(self):
        """Prints the playernames in the self.screen 

        Keyword arguments:
        self.screen -- the curses self.screen
        player1_name -- player1 name as string
        player2_name -- player2 name as string
        """
        h,w = self.screen.getmaxyx()
        
        player_name_x = -10 + w//3   
        player_name_y = 4
        if self.player_num == 2:
            player_name_x = 29  + w//3 
            player_name_y = 4
        self.screen.addstr(player_name_y,player_name_x,"Player"+str(self.player_num == 2),curses.color_pair(self.player_color))
        self.screen.addstr(player_name_y+1,player_name_x,self.player_name,curses.color_pair(self.player_color))

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

    def check_looser(self):
        if self.remaining_stones <= 2:
            self.lose = True
        else:
            self.lose = False 

    def has_player_lost(self,plus_list,matrix,player1_turn):
        self.check_looser()
        for index,elem in enumerate(plus_list):
            char = elem[0]
            if char == self.stone_marker:
                neighbours = find_all_neighbours(plus_list,matrix,index)
                for neighbour in neighbours:
                    if neighbour[0] == "+":
                        self.lose = True 
        self.lose = False

    def move_index_down(self,plus_list):
        """ Finds the "+" char that is above self.move_index. If the current "+" char is at a coordinate that
            that violates the rules for move_indexment, the position wont change.
        Returns the new x position of the "+"  


        self.move_index -- the currently selected position in the plus_list
        plus_list -- the lists of all the "+" and their positions
        middle -- middle of the map, the values of x range 4,8,12..,28 and the values of y range 0,2,4..,12.
        """
        new_location = self.move_index
        middle = 12, 6
        step = 4, 2
        
        while True:
            new_location += 1
            if new_location == len(plus_list):
                new_location = 0
            
            current_x = plus_list[self.move_index][1]
            new_x = plus_list[new_location][1]

            current_y = plus_list[self.move_index][2]
            new_y = plus_list[new_location][2]
            if current_x == new_x and current_y != new_y:
                #Check if allowed to move_index down
                if (int(current_x) != middle[0] and int(current_y) <= middle[1]) or (int(current_x) == middle[0] and int(current_y) != middle[1]-step[1] and int(current_y) != middle[1]+step[1]*3):
                    self.move_index = new_location
                else:
                    self.move_index


    def move_index_up(self,plus_list):
        """ Finds the "+" char that is above self.move_index. If the current "+" char is at a coordinate that
            that violates the rules for move_indexment, the positiono wont change.
        Returns the new x position of the "+"  


        self.move_index -- the currently selected position in the plus_list
        plus_list -- the lists of all the "+" and their positions
        middle -- middle of the map, the values of x range 4,8,12..,28 and the values of y range 0,2,4..,12.
        """
        new_location = self.move_index
        middle = 12, 6
        step = 4, 2

        while True:
            if new_location == 0:
                new_location = len(plus_list)

            new_location -= 1
            current_x = plus_list[self.move_index][1]
            new_x = plus_list[new_location][1]

            current_y = plus_list[self.move_index][2]
            new_y = plus_list[new_location][2]
            if current_x == new_x and current_y != new_y:
                if (int(current_x) != middle[0] and int(current_y) >= middle[1]) or int(current_x) == middle[0] and int(current_y) != middle[1]-step[1]*3 and int(current_y) != middle[1]+step[1]:
                    self.move_index = new_location
                else:
                    self.move_index

    def move_index_right(self,plus_list):
        """ Finds the "+" char that is right of self.move_index. If the current "+" char is at a coordinate that
            that violates the rules for move_indexment, the positiono wont change.
        Returns the new x position of the "+"  


        self.move_index -- the currently selected position in the plus_list
        plus_list -- the lists of all the "+" and their positions
        middle -- middle of the map, the values of x range 4,8,12..,28 and the values of y range 0,2,4..,12.
        """
        new_location = self.move_index
        middle = 12, 6
        step = 4, 2
        
        while True:
            new_location += 1
            if new_location == len(plus_list):
                new_location = 0
            
            current_x = plus_list[self.move_index][1]
            new_x = plus_list[new_location][1]

            current_y = plus_list[self.move_index][2]
            new_y = plus_list[new_location][2]
            if current_y == new_y and current_x != new_x:
                #Check if allowed to move_index left
                if (int(current_y) != middle[1] and int(current_x) <= middle[0]) or (int(current_y) == middle[1] and int(current_x) != middle[0]-step[0] and int(current_x) != middle[0]+step[0]*3):
                    self.move_index = new_location
                else:
                    self.move_index


    def move_index_left(self,plus_list):
        """ Finds the "+" char that is left of self.move_index. If the current "+" char is at a coordinate that
            that violates the rules for move_indexment, the positiono wont change.
        Returns the new x position of the "+"  

        self.move_index -- the currently selected position in the plus_list
        plus_list -- the lists of all the "+" and their positions
        middle -- middle of the map, the values of x range 4,8,12..,28 and the values of y range 0,2,4..,12.
        """
        new_location = self.move_index
        middle = 12, 6
        step = 4, 2
        
        while True:
            new_location -= 1
            if new_location == len(plus_list):
                new_location = 0
            
            current_x = plus_list[self.move_index][1]
            new_x = plus_list[new_location][1]

            current_y = plus_list[self.move_index][2]
            new_y = plus_list[new_location][2]
            if current_y == new_y and current_x != new_x:
                #Check if allowed to move_index left
                if (int(current_y) != middle[1] and int(current_x) >= middle[0]) or (int(current_y) == middle[1] and int(current_x) != middle[0]-step[0]*3 and int(current_x) != middle[0]+step[0]):
                    self.move_index = new_location
                else:
                    self.move_index



def check_row(matrix, player1_turn, list_3_row):
    """Checks if the game board has three of the same stones in a row vertically.
    
    Returns list_3_row and is_three_row -- bool, will be True if a new three in a row has been found  
    Keyword arguments:
    matrix -- the matrix of the board
    player1_turn -- bool, True is player1 turn and False is player2 turn    
    list_3_row -- list of all the three in a row that has been found
    """
    player_stone = 'X'
    opponent_stone = 'O'
    pre_list_3_row = list_3_row
    is_three_row = False
    
    if player1_turn == False:
        player_stone = 'O'
        opponent_stone = 'X'
    
    for row in (matrix):
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
    
                if (check_player) not in list_3_row:
                    is_three_row = True
                    list_3_row.append(check_player)

    return list_3_row, is_three_row    
    
    

                 
def check_col(matrix,player1_turn,list_3_col):
    """Checks if the game board has three of the same stones in a row horizontally.
    
    Returns list_3_col  and is_three_column -- bool, will be True if a new three in a row in a column has been found  
    Keyword arguments:
    matrix -- the matrix of the board
    player1_turn -- bool, True is player1 turn and False is player2 turn    
    list_3_col -- list of all the three in a row in a column that has been found
    """    
    transponse_matrix = np.transpose(matrix)
    player_stone = 'X'
    opponent_stone = 'O'
    is_three_col = False
    pre_list_3_col = list_3_col
    
    if player1_turn == False:
        player_stone = 'O'
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
    
                if (check_player) not in list_3_col:
                    is_three_col = True

                    list_3_col.append(check_player)
    
    return list_3_col,is_three_col
                
def check_both(matrix,list_3_row,list_3_col,player1_turn):
    """Checks if the game board has three of the same stones in a row either vertically or horizontally.
    
    Returns  list_3_row ,list_3_col,bool which will be True if a new three in a row has been found  
    Keyword arguments:
    matrix -- the matrix of the board
    player1_turn -- bool, True is player1 turn and False is player2 turn
    list_3_row -- list of all the three in a row that has been found
    list_3_col -- list of all the three in a row in a column that has been found
    """        
    list_3_row, is_three_row = check_row(matrix, player1_turn, list_3_row)
    list_3_col, is_three_col = check_col(matrix, player1_turn, list_3_col)
    

    if is_three_row == True or is_three_col == True:
        return list_3_row,list_3_col,True
    
    return list_3_row,list_3_col,False
def place_stone(plus_list,current_row,stone_marker,stone_pool_player1,stone_pool_player2):
    """ Places a stone on the map by changing the "+" to "X" or "O"
    Returns the changed plus_list list

    current_row -- the currently selected row in the plus_list
    plus_list -- the lists of all the "+" and their positions
    stone_marker -- the char of the stone, should be either "X" or "O" 
    stone_pool_player1 -- The amount of stone player1 has left to place
    stone_pool_player2 -- The amount of stone player2 has left to place
    
    """
    if stone_marker == "X":
        stone_pool_player1 = stone_pool_player1 - 1
    elif stone_marker == "O":
        stone_pool_player2 = stone_pool_player2 - 1    

    plus_list[current_row][0] = stone_marker
    return plus_list, stone_pool_player1, stone_pool_player2

def  move_stone(plus_list,current_row,player1_turn,selected_stone_index):
    stone_marker = "X"
    if player1_turn == False:
        stone_marker = "O"
    plus_list[selected_stone_index][0] = "+"
    plus_list[current_row][0] = stone_marker
    return plus_list

def remove_stone_player(plus_list,current_row,player1_turn,stone_pool_player1,stone_pool_player2):
    """ Places a removes on the map by changing the player stone to a "+"
    Returns the changed plus_list list

    current_row -- the currently selected row in the plus_list
    plus_list -- the lists of all the "+" and their positions
    stone_pool_player1 -- The amount of stone player1 has left to place
    stone_pool_player2 -- The amount of stone player2 has left to place
    
    """
    if player1_turn == True: 
        remove_stone_marker = "O"
        stone_pool_player2 = stone_pool_player2 -1
    
    elif player1_turn == False:

        remove_stone_marker = "X" 
        stone_pool_player1 = stone_pool_player1 -1

    if plus_list[current_row][0] == remove_stone_marker:    
        plus_list[current_row][0] = "+"
    

    return plus_list,stone_pool_player1,stone_pool_player2

def print_player_remove(screen,player1_turn,player1_name,player2_name):
    """ Prints the name of player who will be able to remove a stone at the top of the screen
    
    Keyword arguments:
    screen -- the curses screen
    player1_turn -- bool, True is player1 turn and False is player2 turn    
    player1_name -- player1 name as string
    player2_name -- player2 name as string

    """
    h,w = screen.getmaxyx()

    #position of text 
    text_x = 3  + w//3 
    text_y = 2
    
    if player1_turn == True:
          if len(player1_name) ==0:
              player1_name = "Player1"   
          screen.addstr(text_y,text_x,player1_name.rstrip("\n")+" remove a stone!",curses.color_pair(3))
    else:
        if len(player2_name) ==0:
            player2_name = "Player2"        
        screen.addstr(text_y,text_x,player2_name.rstrip("\n")+" remove a stone!",curses.color_pair(2))

def can_player_act(plus_list,current_row,stone_pool_player1, stone_pool_player2,player1_turn):
    """Determines if a player is allowed to act
    Returns bool -- Can player act = True else False

    Keyword argument 
    plus_list -- list of "+" and placed stones
    current_row --  currently selected row in the plus_list
    stone_pool_player1 -- the amount of stone player1 has
    stone_pool_player2 -- the amount of stone player2 has
    player1_turn -- bool, True is player1 turn and False is player2 turn    
        
    """
    current_char = plus_list[current_row][0]
    can_not_act= (stone_pool_player1 <=  0 and stone_pool_player2 <= 0) or current_char != "+"
    if can_not_act == True:    
        return False

    return True


def can_player_remove(plus_list,current_row,player1_turn):
    """Determines if a player can remove a stone
    Returns bool -- Can player remove a stone = True else False

    Keyword argument 
    plus_list -- list of "+" and placed stones
    current_row --  currently selected row in the plus_list
    player1_turn -- bool, True is player1 turn and False is player2 turn    
    """
    current_car = plus_list[current_row][0]
    remove_stone_marker = "O"
    if player1_turn == False:
        remove_stone_marker = "X"
    if current_car == remove_stone_marker:
        return True
    return False        

def can_player_move_stone(plus_list,current_row,player1_turn,neighbours):
    stone_marker = "X"
    if player1_turn == False:
        stone_marker = "O"
    current_stone_y = plus_list[current_row][2]
    current_stone_x = plus_list[current_row][1]
    if neighbours == None and plus_list[current_row][0] == stone_marker:
        return True
    elif plus_list[current_row][0] == stone_marker and "+" in itertools.chain( *neighbours):
            return True
    return False



def get_selected_stone_index(current_row):
    return current_row


def find_stone_neighbour_row(plus_list,matrix,current_row):
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


def find_stone_neighbour_col(plus_list,matrix,current_row):
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

def find_all_neighbours(plus_list,matrix,current_row):
    neighbour_row  = find_stone_neighbour_row(plus_list,matrix,current_row)
    neighbour_col = find_stone_neighbour_col(plus_list,matrix,current_row)
    neighbours = neighbour_row + neighbour_col
    return neighbours 

def is_neighbour_a_plus(plus_list,current_row,neighbours,selected_stone_index):
    elem = plus_list[current_row]
    selected_stone = plus_list[selected_stone_index]
    
    if elem[0] == "+" and selected_stone in neighbours:
        return True
    return False    

def remove_old_3(plus_list,current_row,list_3_row,list_3_col):
    current_stone_x = plus_list[current_row][1]
    current_stone_y = plus_list[current_row][2]

    for r in list_3_row:
        for row in r:
            if current_stone_x == row[1] and current_stone_y == row[2] or row[0] == '+':
                list_3_row.remove(r)
    for c in list_3_col:
        for col in c:
            if current_stone_x == col[1] and current_stone_y == col[2] or col[0] == '+':
                list_3_col.remove(c)      

    return list_3_row,list_3_col
