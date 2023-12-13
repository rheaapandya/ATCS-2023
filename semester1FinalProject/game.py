# game.py
import pygame
from player import Player
from path import Path
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 50

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Initialize display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Scrolling Game")

# Create objects
player = Player(WIDTH // 2 - PLAYER_SIZE // 2, HEIGHT - 2 * PLAYER_SIZE, WIDTH, HEIGHT, WIDTH // 1.5)
path = Path(WIDTH, HEIGHT)  # Pass WIDTH and HEIGHT to the Path constructor

# Font setup
font = pygame.font.Font(None, 36)

# Game loop
clock = pygame.time.Clock()

game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update player and path
    keys = pygame.key.get_pressed()
    player.update(keys)

    # if player.state == "hike":
    #     player.hike()
    # elif player.state == "rest":
    #     player.rest()
    
    path.scroll(player.get_state())  # Pass player's state to the scroll method

    # Check game over condition
    game_over = player.turn_game_over()

    # Draw everything
    screen.fill(WHITE)
    pygame.draw.rect(screen, RED, (WIDTH // 2 - path.width // 2, path.y, path.width, path.height))  # Draw scrolling path
    pygame.draw.rect(screen, BLACK, (player.x, player.y, PLAYER_SIZE, PLAYER_SIZE))  # Draw player in black

    # Display food value at the top left of the screen
    food_text = font.render(f"Food: {player.food}", True, RED)
    water_text = font.render(f"Water: {player.water}", True, RED)
    screen.blit(food_text, (10, 10))
    screen.blit(water_text, (10, 50))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

# Game over screen
screen.fill(WHITE)
game_over_text = font.render("Game Over", True, BLACK)
screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
pygame.display.flip()

# Wait for a few seconds before quitting (optional)
pygame.time.delay(3000)

pygame.quit()
sys.exit()
