from Player import *
from Board_map import*

import curses
import os
import time
import random
import numpy as np
import itertools

class game_loop:
    def __init__(self,screen,player_name):
        self.screen = screen
        self.board = board_map(screen)
        self.players = []


