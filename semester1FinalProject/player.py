# player.py
from fsm import FSM
import pygame
import time

class Player:
     # STATES
    HIKE = "h"
    FOOD_REST = "fr"
    WATER_REST = "wr"
    GAMEOVER = "go"

    # INPUTS
    FOOD_UP = "fu"
    WATER_UP = "wu"
    FOOD_FULLY_LOADED = "ffl"
    FOOD_ZERO = "fz"
    WATER_ZERO = "wz"
    WATER_FULLY_LOADED = "wfl"
    FOOD_REST_OVER = "fro"
    WATER_REST_OVER = "wro"

    def __init__(self, x, y, width, height, path_width):
        self.x = x
        self.y = y
        self.fsm = FSM(self.FOOD_REST)
        self.init_fsm()
        self.food = 3
        self.water = 3
        self.last_food_update_time = time.time()
        self.last_water_update_time = time.time()
        self.zero_food_timer = 0  # Timer for tracking how long the food value has been at 0
        self.zero_water_timer = 0
        self.width = width
        self.height = height
        self.path_width = path_width

       

    def init_fsm(self):
        """
        Adds all states to the FSM
        """
        self.fsm.add_transition(self.FOOD_UP, self.FOOD_REST, self.turn_hike, self.HIKE)
        self.fsm.add_transition(self.FOOD_UP, self.HIKE, self.turn_rest, self.FOOD_REST)
        self.fsm.add_transition(self.FOOD_FULLY_LOADED, self.FOOD_REST, self.turn_hike, self.HIKE)
        self.fsm.add_transition(self.FOOD_FULLY_LOADED, self.HIKE, self.turn_hike, self.HIKE)
        self.fsm.add_transition(self.FOOD_ZERO, self.HIKE, self.turn_game_over, self.GAMEOVER)
        self.fsm.add_transition(self.FOOD_ZERO, self.FOOD_REST, self.turn_game_over, self.GAMEOVER)
        self.fsm.add_transition(self.FOOD_ZERO, self.GAMEOVER, self.turn_game_over, self.GAMEOVER)
        self.fsm.add_transition(self.FOOD_FULLY_LOADED, self.GAMEOVER, self.turn_game_over, self.GAMEOVER)
        self.fsm.add_transition(self.FOOD_UP, self.GAMEOVER, self.turn_game_over, self.GAMEOVER)
        self.fsm.add_transition(self.FOOD_REST_OVER, self.FOOD_REST, self.turn_hike, self.HIKE)
        self.fsm.add_transition(self.FOOD_REST_OVER, self.HIKE, self.turn_hike, self.HIKE)

        self.fsm.add_transition(self.WATER_REST_OVER, self.WATER_REST, self.turn_hike, self.HIKE)
        self.fsm.add_transition(self.WATER_REST_OVER, self.HIKE, self.turn_hike, self.HIKE)
        self.fsm.add_transition(self.WATER_UP, self.WATER_REST, self.turn_hike, self.HIKE)
        self.fsm.add_transition(self.WATER_UP, self.HIKE, self.turn_rest, self.WATER_REST)
        self.fsm.add_transition(self.WATER_ZERO, self.HIKE, self.turn_game_over, self.GAMEOVER)
        self.fsm.add_transition(self.WATER_ZERO, self.WATER_REST, self.turn_game_over, self.GAMEOVER)
        self.fsm.add_transition(self.WATER_ZERO, self.GAMEOVER, self.turn_game_over, self.GAMEOVER)

        self.fsm.add_transition(self.WATER_FULLY_LOADED, self.WATER_REST, self.turn_hike, self.HIKE)
        self.fsm.add_transition(self.WATER_FULLY_LOADED, self.HIKE, self.turn_hike, self.HIKE)
        self.fsm.add_transition(self.WATER_FULLY_LOADED, self.GAMEOVER, self.turn_game_over, self.GAMEOVER)
        
    def update(self, keys):
        # Update food every 2 seconds
        
        current_time = time.time()
        if current_time - self.last_food_update_time >= 3:
            if self.get_state() == "fr":
                self.food = min(self.food + 1, 4)  # Recharge by 1 every 2 seconds while resting, up to 4
            elif self.get_state() == "h":
                self.food -= 1
        
        if current_time - self.last_water_update_time >= 4:
            if self.get_state() == "wr":
                self.water = min(self.water + 1, 4)  # Recharge by 1 every 2 seconds while resting, up to 4
            elif self.get_state() == "h":
                self.water -= 1

            # Check if food is at 0 and update the zero food timer
            if self.food == 0:
                self.zero_food_timer += 2  # Increase timer by 2 seconds every update
            else:
                self.zero_food_timer = 0  # Reset the timer if food is not at 0

            if self.water == 0:
                self.zero_water_timer += 2  # Increase timer by 2 seconds every update
            else:
                self.zero_water_timer = 0 

            self.last_food_update_time = current_time
            self.last_water_update_time = current_time

        if self.zero_food_timer >= 2:
            self.fsm.process(self.FOOD_ZERO)

        if self.zero_water_timer >= 2:
            self.fsm.process(self.WATER_ZERO)

        if self.food < 0:
            self.food = 0  # Ensure food doesn't go below 0
        
        if self.water < 0:
            self.water = 0
        

        if keys[pygame.K_SPACE]:
            if self.get_state() == self.HIKE:
                # If the space bar is held, transition to "rest"
                self.fsm.process(self.FOOD_UP)
            if self.food > 3:
                self.fsm.process(self.FOOD_REST_OVER)

        elif keys[pygame.K_w]:
            if self.get_state() == self.HIKE:
                # If the space bar is held, transition to "rest"
                self.fsm.process(self.WATER_UP)
            if self.water > 3:
                self.fsm.process(self.WATER_REST_OVER)

        else:
            # If the space bar is not held, transition to "hike"
            self.fsm.process(self.FOOD_FULLY_LOADED)
            # Arrow key movement with bounds checking
            if keys[pygame.K_LEFT] and self.x > ((self.width - self.path_width)/2):
                self.x -= 8  # Adjust player's position to ensure it doesn't go past the left edge
            elif keys[pygame.K_RIGHT] and self.x < (self.path_width + (self.width - self.path_width)/2) - 52:
                self.x += 8  # Adjust player's position to ensure it doesn't go past the right edge

            # self.fsm.process(self.FULLY_LOADED)

       
        # else:
        #     # If the space bar is not held, transition to "hike"
        #     self.fsm.process(self.WATER_FULLY_LOADED)
        #     # Arrow key movement with bounds checking
        #     if keys[pygame.K_LEFT] and self.x > ((self.width - self.path_width)/2):
        #         self.x -= 8  # Adjust player's position to ensure it doesn't go past the left edge
        #     elif keys[pygame.K_RIGHT] and self.x < (self.path_width + (self.width - self.path_width)/2) - 52:
        #         self.x += 8  # Adjust player's position to ensure it doesn't go past the right edge

        #     # self.fsm.process(self.FULLY_LOADED)



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
    





# # player.py
# from fsm import FSM
# import pygame
# import time

# class Player:
#     # STATES
#     HIKE = "h"
#     REST = "r"
#     GAMEOVER = "go"

#     # INPUTS
#     FOOD_UP = "fu"
#     FULLY_LOADED = "fl"
#     FOOD_ZERO = "fz"
#     REST_OVER = "ro"
    
#     WATER_UP = "wu"
#     WATER_ZERO = "wz"

#     def __init__(self, x, y, width, height, path_width):
#         self.x = x
#         self.y = y
#         self.fsm = FSM(self.REST)
#         self.init_fsm()
#         self.food = 3
#         self.water = 3
#         self.last_food_update_time = time.time()
#         self.last_water_update_time = time.time()
#         self.zero_food_timer = 0
#         self.zero_water_timer = 0
#         self.width = width
#         self.height = height
#         self.path_width = path_width

#     def init_fsm(self):
#         # Add transitions for food
#         self.fsm.add_transition(self.FOOD_UP, self.REST, self.turn_hike, self.HIKE)
#         self.fsm.add_transition(self.FOOD_UP, self.HIKE, self.turn_rest, self.REST)
#         self.fsm.add_transition(self.FULLY_LOADED, self.REST, self.turn_hike, self.HIKE)
#         self.fsm.add_transition(self.FULLY_LOADED, self.HIKE, self.turn_hike, self.HIKE)
#         self.fsm.add_transition(self.FOOD_ZERO, self.HIKE, self.turn_game_over, self.GAMEOVER)
#         self.fsm.add_transition(self.FOOD_ZERO, self.REST, self.turn_game_over, self.GAMEOVER)
#         self.fsm.add_transition(self.FOOD_ZERO, self.GAMEOVER, self.turn_game_over, self.GAMEOVER)
#         self.fsm.add_transition(self.FULLY_LOADED, self.GAMEOVER, self.turn_game_over, self.GAMEOVER)
#         self.fsm.add_transition(self.FOOD_UP, self.GAMEOVER, self.turn_game_over, self.GAMEOVER)
#         self.fsm.add_transition(self.REST_OVER, self.REST, self.turn_hike, self.HIKE)
#         self.fsm.add_transition(self.REST_OVER, self.HIKE, self.turn_hike, self.HIKE)

#         # Add transitions for water
#         self.fsm.add_transition(self.WATER_UP, self.REST, self.turn_hike, self.HIKE)
#         self.fsm.add_transition(self.WATER_UP, self.HIKE, self.turn_rest, self.REST)
#         self.fsm.add_transition(self.WATER_ZERO, self.HIKE, self.turn_game_over, self.GAMEOVER)
#         self.fsm.add_transition(self.WATER_ZERO, self.REST, self.turn_game_over, self.GAMEOVER)
#         self.fsm.add_transition(self.WATER_ZERO, self.GAMEOVER, self.turn_game_over, self.GAMEOVER)

#     def update(self, keys):
#         # Update food every 2 seconds
#         current_time = time.time()
#         if current_time - self.last_food_update_time >= 2:
#             if self.get_state() == self.REST:
#                 self.food = min(self.food + 1, 2)
#             elif self.get_state() == self.HIKE:
#                 self.food -= 1

#             if self.food == 0:
#                 self.zero_food_timer += 2
#             else:
#                 self.zero_food_timer = 0

#             self.last_food_update_time = current_time

#         # Update water every 4 seconds
#         if current_time - self.last_water_update_time >= 4:
#             if self.get_state() == self.REST:
#                 self.water = min(self.water + 1, 2)
#             elif self.get_state() == self.HIKE:
#                 self.water -= 1

#             if self.water == 0:
#                 self.zero_water_timer += 4
#             else:
#                 self.zero_water_timer = 0

#             self.last_water_update_time = current_time

#         if self.zero_food_timer >= 2:
#             self.fsm.process(self.FOOD_ZERO)

#         if self.zero_water_timer >= 4:
#             self.fsm.process(self.WATER_ZERO)

#         if self.food < 0:
#             self.food = 0

#         if self.water < 0:
#             self.water = 0

#         if keys[pygame.K_w]:  # Pressing "W" reloads water
#             if self.get_state() == self.HIKE:
#                 self.fsm.process(self.WATER_UP)
#             if self.water > 3:
#                 self.fsm.process(self.REST_OVER)
#         else:
#             self.fsm.process(self.FULLY_LOADED)
#             # Arrow key movement with bounds checking
#             if keys[pygame.K_LEFT] and self.x > ((self.width - self.path_width)/2):
#                 self.x -= 8
#             elif keys[pygame.K_RIGHT] and self.x < (self.path_width + (self.width - self.path_width)/2) - 52:
#                 self.x += 8

#         if keys[pygame.K_SPACE]:
#             if self.get_state() == self.HIKE:
#                 # If the space bar is held, transition to "rest"
#                 self.fsm.process(self.FOOD_UP)
#             if self.food > 3:
#                 self.fsm.process(self.REST_OVER)
#         else:
#             # If the space bar is not held, transition to "hike"
#             self.fsm.process(self.FULLY_LOADED)
#             # Arrow key movement with bounds checking
#             if keys[pygame.K_LEFT] and self.x > ((self.width - self.path_width)/2):
#                 self.x -= 8  # Adjust player's position to ensure it doesn't go past the left edge
#             elif keys[pygame.K_RIGHT] and self.x < (self.path_width + (self.width - self.path_width)/2) - 52:
#                 self.x += 8  # Adjust player's position to ensure it doesn't go past the right edge

#             # self.fsm.process(self.FULLY_LOADED)

#     def turn_hike(self):
#         print("Player is hiking")
#         # Add your hike logic here

#     def turn_rest(self):
#         print("Player is resting")
#         # Add your rest logic here

#     def get_state(self):
#         return self.fsm.current_state

#     def turn_game_over(self):
#         # Check if the game over condition is met
#         if self.get_state() == "go":
#             return True
#         else:
#             return False
    
