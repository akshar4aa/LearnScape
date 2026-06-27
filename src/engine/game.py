import pygame
import os

from src.engine.settings import *
from src.engine.audio_manager import AudioManager
from src.states.splash_state import SplashState

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        
        # Setup Window
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        # Core Systems
        self.audio = AudioManager()

        # Session Stats (default values, overwritten when loading save or creating new game)
        self.hero_name = "New Hero"
        self.char_type = "Scholar"
        self.xp = 0
        self.coins = 0
        self.level = 1
        self.unlocked_planets = ["Earth"]
        self.completed_lessons = []
        self.achievements = []

        # Initial State
        self.current_state = SplashState(self)

        # Attempt to play background music (will fail silently if file is missing)
        self.audio.play_music("assets/audio/music.mp3")

    def change_state(self, new_state):
        self.current_state.exit()
        self.current_state = new_state
        self.current_state.enter()

    def run(self):
        while self.running:
            # Maintain 60 FPS
            dt = self.clock.tick(FPS) / 1000.0

            # Gather events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            # State Loop
            self.current_state.handle_events(events)
            self.current_state.update(dt)

            # Draw Screen
            self.screen.fill(BACKGROUND_COLOR)
            self.current_state.draw(self.screen)
            pygame.display.flip()

        pygame.quit()