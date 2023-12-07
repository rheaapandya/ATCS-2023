# player.py
from fsm import FSM
import pygame
import time

class Player:
    def __init__(self, x, y, width, height, path_width):
        self.x = x
        self.y = y
        self.fsm = FSM("rest")
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
        self.fsm.add_transition(self.TIMER_UP, self.RED, self.turn_green, self.GREEN)
        self.fsm.add_transition(self.TIMER_UP, self.GREEN, self.turn_yellow, self.YELLOW)
        self.fsm.add_transition(self.TIMER_UP, self.YELLOW, self.turn_red, self.RED)
        
    def update(self, keys):
        # Update food every 2 seconds
        current_time = time.time()
        if current_time - self.last_food_update_time >= 2:
            if self.state == "rest":
                self.food = min(self.food + 1, 4)  # Recharge by 1 every 2 seconds while resting, up to 4
            elif self.state == "hike":
                self.food -= 1

            # Check if food is at 0 and update the zero food timer
            if self.food == 0:
                self.zero_food_timer += 2  # Increase timer by 2 seconds every update
            else:
                self.zero_food_timer = 0  # Reset the timer if food is not at 0

            self.last_food_update_time = current_time

        if self.food < 0:
            self.food = 0  # Ensure food doesn't go below 0

        if keys[pygame.K_SPACE]:
            self.state = "rest"
            # Change state to "hike" if food reaches above 3
            if self.food >= 3:
                self.state = "hike"
        else:
            # Arrow key movement with bounds checking
            if keys[pygame.K_LEFT] and self.x > ((self.width - self.path_width)/2):
                self.x -= 8  # Adjust player's position to ensure it doesn't go past the left edge
            elif keys[pygame.K_RIGHT] and self.x < (self.path_width + (self.width - self.path_width)/2) - 52:
                self.x += 8  # Adjust player's position to ensure it doesn't go past the right edge

            self.state = "hike"

    def hike(self):
        print("Player is hiking")
        # Add your hike logic here

    def rest(self):
        print("Player is resting")
        # Add your rest logic here

    def check_game_over(self):
        # Check if the game over condition is met
        if self.zero_food_timer >= 2:
            return True
        return False
