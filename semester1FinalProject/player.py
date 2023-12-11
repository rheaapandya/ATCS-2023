# player.py
from fsm import FSM
import pygame
import time

class Player:
     # STATES
    HIKE = "h"
    REST = "r"
    GAMEOVER = "go"

    # INPUTS
    FOOD_UP = "fu"
    FULLY_LOADED = "fl"
    FOOD_ZERO = "fz"
    REST_OVER = "ro"

    def __init__(self, x, y, width, height, path_width):
        self.x = x
        self.y = y
        self.fsm = FSM(self.REST)
        self.init_fsm()
        self.food = 3
        self.last_food_update_time = time.time()
        self.zero_food_timer = 0  # Timer for tracking how long the food value has been at 0
        self.width = width
        self.height = height
        self.path_width = path_width

       

    def init_fsm(self):
        """
        Adds all states to the FSM
        """
        self.fsm.add_transition(self.FOOD_UP, self.REST, self.turn_hike, self.HIKE)
        self.fsm.add_transition(self.FOOD_UP, self.HIKE, self.turn_rest, self.REST)
        self.fsm.add_transition(self.FULLY_LOADED, self.REST, self.turn_hike, self.HIKE)
        self.fsm.add_transition(self.FULLY_LOADED, self.HIKE, self.turn_hike, self.HIKE)
        self.fsm.add_transition(self.FOOD_ZERO, self.HIKE, self.turn_game_over, self.GAMEOVER)
        self.fsm.add_transition(self.FOOD_ZERO, self.REST, self.turn_game_over, self.GAMEOVER)
        self.fsm.add_transition(self.FOOD_ZERO, self.GAMEOVER, self.turn_game_over, self.GAMEOVER)
        self.fsm.add_transition(self.FULLY_LOADED, self.GAMEOVER, self.turn_game_over, self.GAMEOVER)
        self.fsm.add_transition(self.FOOD_UP, self.GAMEOVER, self.turn_game_over, self.GAMEOVER)
        self.fsm.add_transition(self.REST_OVER, self.REST, self.turn_hike, self.HIKE)
        self.fsm.add_transition(self.REST_OVER, self.HIKE, self.turn_hike, self.HIKE)
        
    def update(self, keys):
        # Update food every 2 seconds
        current_time = time.time()
        if current_time - self.last_food_update_time >= 2:
            if self.get_state() == "r":
                self.food = min(self.food + 1, 4)  # Recharge by 1 every 2 seconds while resting, up to 4
            elif self.get_state() == "h":
                self.food -= 1

            # Check if food is at 0 and update the zero food timer
            if self.food == 0:
                self.zero_food_timer += 2  # Increase timer by 2 seconds every update
            else:
                self.zero_food_timer = 0  # Reset the timer if food is not at 0

            self.last_food_update_time = current_time

        if self.zero_food_timer >= 2:
            self.fsm.process(self.FOOD_ZERO)

        if self.food < 0:
            self.food = 0  # Ensure food doesn't go below 0

        

        if keys[pygame.K_SPACE]:
            if self.get_state() == self.HIKE:
                # If the space bar is held, transition to "rest"
                self.fsm.process(self.FOOD_UP)
            if self.food > 3:
                self.fsm.process(self.REST_OVER)
        else:
            # If the space bar is not held, transition to "hike"
            self.fsm.process(self.FULLY_LOADED)
            # Arrow key movement with bounds checking
            if keys[pygame.K_LEFT] and self.x > ((self.width - self.path_width)/2):
                self.x -= 8  # Adjust player's position to ensure it doesn't go past the left edge
            elif keys[pygame.K_RIGHT] and self.x < (self.path_width + (self.width - self.path_width)/2) - 52:
                self.x += 8  # Adjust player's position to ensure it doesn't go past the right edge

            # self.fsm.process(self.FULLY_LOADED)

    def turn_hike(self):
        print("Player is hiking")
        # Add your hike logic here

    def turn_rest(self):
        print("Player is resting")
        # Add your rest logic here

    def get_state(self):
        return self.fsm.current_state

    def turn_game_over(self):
        # Check if the game over condition is met
        if self.get_state() == "go":
            return True
        else:
            return False
    
