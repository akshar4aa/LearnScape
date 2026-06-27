import math
import pygame

from src.states.state import State


class SplashState(State):
    def __init__(self, game):
        super().__init__(game)

        self.timer = 0.0
        self.logo_time = 0.0

        self.base_title_size = 72

        self.subtitle_font = pygame.font.SysFont(
            "arial",
            26
        )

    def handle_events(self, events):

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print("Go to Main Menu")

    def update(self, dt):

        self.timer += dt
        self.logo_time += dt

    def draw(self, screen):

        screen.fill((18, 22, 35))

        # ---------------------------------------
        # Animated Logo
        # ---------------------------------------

        scale = 1 + math.sin(self.logo_time * 2) * 0.03

        font_size = int(self.base_title_size * scale)

        title_font = pygame.font.SysFont(
            "arial",
            font_size,
            bold=True
        )

        title = title_font.render(
            "LearnScape",
            True,
            (255, 215, 0)
        )

        title_rect = title.get_rect(
            center=(
                self.game.screen.get_width() // 2,
                280,
            )
        )

        screen.blit(title, title_rect)

        # ---------------------------------------
        # Subtitle
        # ---------------------------------------

        subtitle = self.subtitle_font.render(
            "A Journey Through Knowledge",
            True,
            (220, 220, 220),
        )

        subtitle_rect = subtitle.get_rect(
            center=(
                self.game.screen.get_width() // 2,
                360,
            )
        )

        screen.blit(subtitle, subtitle_rect)

        # ---------------------------------------
        # Press Enter
        # ---------------------------------------

        alpha = (math.sin(self.logo_time * 4) + 1) / 2

        color = (
            int(180 + alpha * 75),
            int(180 + alpha * 75),
            int(180 + alpha * 75),
        )

        press_font = pygame.font.SysFont(
            "arial",
            22,
            bold=True
        )

        press = press_font.render(
            "Press ENTER",
            True,
            color,
        )

        press_rect = press.get_rect(
            center=(
                self.game.screen.get_width() // 2,
                520,
            )
        )

        screen.blit(press, press_rect)