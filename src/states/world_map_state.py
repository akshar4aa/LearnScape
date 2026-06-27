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

        from src.ui.planet import Planet

        self.kingdoms = [

    Planet(
        220,
        450,
        "assets/planets/earth.png",
        "Earth"
    ),

    Planet(
        640,
        280,
        "assets/planets/jupiter.png",
        "Jupiter"
    ),

    Planet(
        1080,
        460,
        "assets/planets/saturn.png",
        "Saturn"
    )

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

                    from src.states.kingdom_state import KingdomState

                    self.game.change_state(
                        KingdomState(
                        self.game,
                        self.kingdoms[self.selected].name
                    )
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
        for planet in self.kingdoms:
            planet.update(dt)

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

        # Draw paths first
        pygame.draw.lines(
    screen,
    (120,120,170),
    False,
    [
        (220,450),
        (640,280),
        (1080,450)
    ],
    6
)

# Draw planets
        for i, planet in enumerate(self.kingdoms):

            planet.draw(
        screen,
        i == self.selected
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