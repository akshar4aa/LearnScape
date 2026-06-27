import pygame

from src.engine.settings import *
from src.states.splash_state import SplashState

class Game:

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)

        self.clock = pygame.time.Clock()

        self.running = True

        self.state = SplashState(self)

    def run(self):

        while self.running:

            dt = self.clock.tick(FPS) / 1000

            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.state.handle_events(events)
            self.state.update(dt)

            self.screen.fill(BACKGROUND_COLOR)

            self.state.draw(self.screen)

            pygame.display.flip()

        pygame.quit()