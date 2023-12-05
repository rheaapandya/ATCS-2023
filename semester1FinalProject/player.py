# player.py
import pygame
import time

class Player:
    def __init__(self, x, y, width, height, path_width):
        self.x = x
        self.y = y
        self.state = "rest"
        self.food = 3
        self.last_food_update_time = time.time()
        self.width = width
        self.height = height
        self.path_width = path_width

    def update(self, keys):
        # Update food every 2 seconds
        current_time = time.time()
        if current_time - self.last_food_update_time >= 2:
            if self.state == "rest":
                self.food = min(self.food + 1, 4)  # Recharge by 1 every 2 seconds while resting, up to 4
            elif self.state == "hike":
                self.food -= 1


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
            if keys[pygame.K_LEFT] and self.x > 0:
                self.x = max(self.x - 8, 0)  # Adjust player's position to ensure it doesn't go past the left edge
            elif keys[pygame.K_RIGHT] and self.x < self.width - self.path_width:
                self.x = min(self.x + 8, self.width - self.path_width)  # Adjust player's position to ensure it doesn't go past the right edge

            self.state = "hike"

    def hike(self):
        print("Player is hiking")
        # Add your hike logic here

    def rest(self):
        print("Player is resting")
        # Add your rest logic here
