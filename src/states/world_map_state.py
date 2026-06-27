import pygame

from src.states.state import State
from src.ui.background import Background


class WorldMapState(State):

    def __init__(self, game):
        super().__init__(game)

        width = self.game.screen.get_width()
        height = self.game.screen.get_height()

        self.background = Background(width, height)

        self.title_font = pygame.font.SysFont(
            "arial",
            58,
            bold=True
        )

        self.text_font = pygame.font.SysFont(
            "arial",
            24
        )

        self.kingdoms = [

            {
                "name": "Math Kingdom",
                "x": 240,
                "y": 260
            },

            {
                "name": "Science Lab",
                "x": 640,
                "y": 180
            },

            {
                "name": "Coding Castle",
                "x": 980,
                "y": 360
            }

        ]

        self.selected = 0
            # =====================================
    # EVENTS
    # =====================================

    def handle_events(self, events):

        for event in events:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:

                    self.selected = (
                        self.selected - 1
                    ) % len(self.kingdoms)

                elif event.key == pygame.K_RIGHT:

                    self.selected = (
                        self.selected + 1
                    ) % len(self.kingdoms)

                elif event.key == pygame.K_RETURN:

                    print(
                        "Entering",
                        self.kingdoms[self.selected]["name"]
                    )

                elif event.key == pygame.K_ESCAPE:

                    from src.states.menu_state import MenuState

                    self.game.change_state(
                        MenuState(self.game)
                    )

    # =====================================
    # UPDATE
    # =====================================

    def update(self, dt):

        self.background.update(dt)

    # =====================================
    # DRAW
    # =====================================

    def draw(self, screen):

        self.background.draw(screen)

        title = self.title_font.render(
            "World Map",
            True,
            (255,220,80)
        )

        screen.blit(
            title,
            title.get_rect(center=(640,70))
        )

        for i, kingdom in enumerate(self.kingdoms):

            color = (
                (255,220,80)
                if i == self.selected
                else
                (120,180,255)
            )

            pygame.draw.circle(
                screen,
                color,
                (
                    kingdom["x"],
                    kingdom["y"]
                ),
                35
            )

            text = self.text_font.render(
                kingdom["name"],
                True,
                (255,255,255)
            )

            screen.blit(
                text,
                text.get_rect(
                    center=(
                        kingdom["x"],
                        kingdom["y"]+60
                    )
                )
            )

        hint = self.text_font.render(
            "← → Select Kingdom    ENTER Explore",
            True,
            (220,220,220)
        )

        screen.blit(
            hint,
            hint.get_rect(center=(640,740))
        )