import pygame

print("1")

from src.engine.settings import *

print("2")

from src.states.splash_state import SplashState

print("3")


class Game:
    def __init__(self):

        print("4")

        pygame.init()

        print("5")

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)

        self.clock = pygame.time.Clock()
        self.running = True

        self.current_state = SplashState(self)

    def change_state(self, new_state):
        self.current_state = new_state

    def run(self):

        while self.running:

            dt = self.clock.tick(FPS) / 1000

            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.current_state.handle_events(events)
            self.current_state.update(dt)

            self.screen.fill(BACKGROUND_COLOR)
            self.current_state.draw(self.screen)

            pygame.display.flip()

        pygame.quit()