import pygame

from src.states.state import State
from src.ui.background import Background


class LoadingState(State):

    def __init__(self, game):
        super().__init__(game)

        width = self.game.screen.get_width()
        height = self.game.screen.get_height()

        self.background = Background(width, height)

        self.title_font = pygame.font.SysFont(
            "arial",
            60,
            bold=True
        )

        self.text_font = pygame.font.SysFont(
            "arial",
            28
        )

        self.small_font = pygame.font.SysFont(
            "arial",
            22
        )

        self.progress = 0
        self.timer = 0
            # ==========================================
    # EVENTS
    # ==========================================

    def handle_events(self, events):

        for event in events:

            if event.type == pygame.QUIT:
                self.game.running = False

    # ==========================================
    # UPDATE
    # ==========================================

    def update(self, dt):

        self.background.update(dt)

        self.timer += dt

        # Fill progress bar over 3 seconds
        if self.progress < 100:
            self.progress += dt * 35

        # Automatically move to World Map
        if self.timer >= 3:
            print("Going to World Map")

            # We'll create this page next
            from src.states.world_map_state import WorldMapState

            self.game.change_state(
                WorldMapState(self.game)
            )

    # ==========================================
    # DRAW
    # ==========================================

    def draw(self, screen):

        self.background.draw(screen)

        # ---------------------------
        # Title
        # ---------------------------

        title = self.title_font.render(
            "LearnScape",
            True,
            (255, 220, 80)
        )

        screen.blit(
            title,
            title.get_rect(center=(640, 140))
        )

        # ---------------------------
        # Loading Text
        # ---------------------------

        loading = self.text_font.render(
            "Preparing Your Adventure...",
            True,
            (230, 230, 230)
        )

        screen.blit(
            loading,
            loading.get_rect(center=(640, 230))
        )

        # ---------------------------
        # Progress Bar Background
        # ---------------------------

        pygame.draw.rect(
            screen,
            (45, 45, 65),
            (290, 380, 700, 35),
            border_radius=10
        )

        # Progress

        pygame.draw.rect(
            screen,
            (255, 220, 80),
            (
                290,
                380,
                int(700 * (self.progress / 100)),
                35
            ),
            border_radius=10
        )

        # Percentage

        percent = self.small_font.render(
            f"{int(self.progress)}%",
            True,
            (255, 255, 255)
        )

        screen.blit(
            percent,
            percent.get_rect(center=(640, 450))
        )

        # ---------------------------
        # Tip
        # ---------------------------

        tip = self.small_font.render(
            "Tip: Practice every day to become a Master!",
            True,
            (200, 200, 200)
        )

        screen.blit(
            tip,
            tip.get_rect(center=(640, 650))
        )