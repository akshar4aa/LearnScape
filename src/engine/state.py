import pygame

class State:
    """
    Abstract Base Class representing a game state/screen.
    """
    def __init__(self, game):
        self.game = game

    def enter(self):
        """Called once when entering the state."""
        pass

    def exit(self):
        """Called once when leaving the state."""
        pass

    def handle_event(self, event):
        """Handles Pygame events."""
        pass

    def update(self, dt):
        """Updates logic. dt is elapsed time in seconds."""
        pass

    def draw(self, surface):
        """Draws visual elements to the provided surface (logical resolution)."""
        pass
