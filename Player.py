import os


class player:
    def __init__(self,screen,player_num,player_name,stone_pool,stone_remaining,stone_marker,color,isBot):
        self.player_name = player_name
        self.stone_pool = stone_pool
        self.remaining_stones = stone_remaining
        self.stone_marker = stone_marker
        self.player_color = color
        #self.player1_turn = player1_turn
        self.bot = isBot
        self.num = player
        self.phase = 1
        self.move = 0
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
        
        player1_name_x = -10 + w//3   
        player1_name_y = 4
        if self.player_type == 2:
            player2_name_x = 29  + w//3 
            player2_name_y = 4
        self.screen.addstr(player1_name_y,player1_name_x,"Player"+str(self.player_type),self.player_color)
        self.screen.addstr(player1_name_y+1,player1_name_x,self.player_name,self.player_color)


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

    def move_down(self,plus_list):
        """ Finds the "+" char that is above self.move. If the current "+" char is at a coordinate that
            that violates the rules for movement, the position wont change.
        Returns the new x position of the "+"  


        self.move -- the currently selected position in the plus_list
        plus_list -- the lists of all the "+" and their positions
        middle -- middle of the map, the values of x range 4,8,12..,28 and the values of y range 0,2,4..,12.
        """
        new_location = self.move
        middle = 12, 6
        step = 4, 2
        
        while True:
            new_location += 1
            if new_location == len(plus_list):
                new_location = 0
            
            current_x = plus_list[self.move][1]
            new_x = plus_list[new_location][1]

            current_y = plus_list[self.move][2]
            new_y = plus_list[new_location][2]
            if current_x == new_x and current_y != new_y:
                #Check if allowed to move down
                if (int(current_x) != middle[0] and int(current_y) <= middle[1]) or (int(current_x) == middle[0] and int(current_y) != middle[1]-step[1] and int(current_y) != middle[1]+step[1]*3):
                    self.move = new_location
                else:
                    self.move


    def move_up(self,plus_list):
        """ Finds the "+" char that is above self.move. If the current "+" char is at a coordinate that
            that violates the rules for movement, the positiono wont change.
        Returns the new x position of the "+"  


        self.move -- the currently selected position in the plus_list
        plus_list -- the lists of all the "+" and their positions
        middle -- middle of the map, the values of x range 4,8,12..,28 and the values of y range 0,2,4..,12.
        """
        new_location = self.move
        middle = 12, 6
        step = 4, 2

        while True:
            if new_location == 0:
                new_location = len(plus_list)

            new_location -= 1
            current_x = plus_list[self.move][1]
            new_x = plus_list[new_location][1]

            current_y = plus_list[self.move][2]
            new_y = plus_list[new_location][2]
            if current_x == new_x and current_y != new_y:
                if (int(current_x) != middle[0] and int(current_y) >= middle[1]) or int(current_x) == middle[0] and int(current_y) != middle[1]-step[1]*3 and int(current_y) != middle[1]+step[1]:
                    self.move = new_location
                else:
                    self.move

    def move_right(self,plus_list):
        """ Finds the "+" char that is right of self.move. If the current "+" char is at a coordinate that
            that violates the rules for movement, the positiono wont change.
        Returns the new x position of the "+"  


        self.move -- the currently selected position in the plus_list
        plus_list -- the lists of all the "+" and their positions
        middle -- middle of the map, the values of x range 4,8,12..,28 and the values of y range 0,2,4..,12.
        """
        new_location = self.move
        middle = 12, 6
        step = 4, 2
        
        while True:
            new_location += 1
            if new_location == len(plus_list):
                new_location = 0
            
            current_x = plus_list[self.move][1]
            new_x = plus_list[new_location][1]

            current_y = plus_list[self.move][2]
            new_y = plus_list[new_location][2]
            if current_y == new_y and current_x != new_x:
                #Check if allowed to move left
                if (int(current_y) != middle[1] and int(current_x) <= middle[0]) or (int(current_y) == middle[1] and int(current_x) != middle[0]-step[0] and int(current_x) != middle[0]+step[0]*3):
                    self.move = new_location
                else:
                    self.move


    def move_left(self,plus_list):
        """ Finds the "+" char that is left of self.move. If the current "+" char is at a coordinate that
            that violates the rules for movement, the positiono wont change.
        Returns the new x position of the "+"  

        self.move -- the currently selected position in the plus_list
        plus_list -- the lists of all the "+" and their positions
        middle -- middle of the map, the values of x range 4,8,12..,28 and the values of y range 0,2,4..,12.
        """
        new_location = self.move
        middle = 12, 6
        step = 4, 2
        
        while True:
            new_location -= 1
            if new_location == len(plus_list):
                new_location = 0
            
            current_x = plus_list[self.move][1]
            new_x = plus_list[new_location][1]

            current_y = plus_list[self.move][2]
            new_y = plus_list[new_location][2]
            if current_y == new_y and current_x != new_x:
                #Check if allowed to move left
                if (int(current_y) != middle[1] and int(current_x) >= middle[0]) or (int(current_y) == middle[1] and int(current_x) != middle[0]-step[0]*3 and int(current_x) != middle[0]+step[0]):
                    self.move = new_location
                else:
                    self.move