import pygame
from src.states.state import State


class SplashState(State):
    def __init__(self, game):
        super().__init__(game)

        self.timer = 0

        self.title_font = pygame.font.SysFont("arial", 72, bold=True)
        self.subtitle_font = pygame.font.SysFont("arial", 26)

    def handle_events(self, events):
        pass

    def update(self, dt):
        self.timer += dt

    def draw(self, screen):

        screen.fill((18, 22, 35))

        title = self.title_font.render("LearnScape", True, (255, 215, 0))

        subtitle = self.subtitle_font.render(
            "A Journey Through Knowledge",
            True,
            (220, 220, 220),
        )

        title_rect = title.get_rect(center=(640, 300))
        subtitle_rect = subtitle.get_rect(center=(640, 380))

        screen.blit(title, title_rect)
        screen.blit(subtitle, subtitle_rect)