# path.py

class Path:
    def __init__(self, width, height):
        self.width = width // 1.5  # Make the path in width
        self.height = height * 2  # Make the path in height
        self.y = height  # Start the path at the bottom of the screen

    def scroll(self, player_state):
        if player_state == "h":
            self.y -= 10
        if self.y < 0:
            self.y = self.height  # Reset the path when it reaches the top
