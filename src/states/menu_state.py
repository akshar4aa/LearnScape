import pygame
import math

from src.states.state import State
from src.ui.background import Background


class MenuState(State):

    def __init__(self, game):
        super().__init__(game)

        width = self.game.screen.get_width()
        height = self.game.screen.get_height()

        self.background = Background(width, height)

        self.title_font = pygame.font.SysFont(
            "arial",
            72,
            bold=True
        )

        self.subtitle_font = pygame.font.SysFont(
            "arial",
            24
        )

        self.button_font = pygame.font.SysFont(
            "arial",
            30,
            bold=True
        )

        self.options = [
            "New Adventure",
            "Continue",
            "Settings",
            "Achievements",
            "Exit"
        ]

        self.selected = 0
        self.time = 0.0

    # ----------------------------------------
    # Events
    # ----------------------------------------

    def handle_events(self, events):

        for event in events:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    self.selected = (
                        self.selected - 1
                    ) % len(self.options)

                elif event.key == pygame.K_DOWN:
                    self.selected = (
                        self.selected + 1
                    ) % len(self.options)

                elif event.key == pygame.K_RETURN:

                    option = self.options[self.selected]

                    if option == "New Adventure":
                        from src.states.new_adventure_state import NewAdventureState
                        self.game.change_state(
                            NewAdventureState(self.game)
                        )
                    elif option == "Exit":
                        self.game.running = False

    # ----------------------------------------
    # Update
    # ----------------------------------------

    def update(self, dt):

        self.time += dt

        self.background.update(dt)

    # ----------------------------------------
    # Castle
    # ----------------------------------------

    def draw_castle(self, screen):

        width = screen.get_width()
        height = screen.get_height()

        ground = height - 20

        castle = (35, 40, 60)

        # Ground
        pygame.draw.rect(
            screen,
            castle,
            (0, ground, width, 90)
        )

        # Main Building
        pygame.draw.rect(
            screen,
            castle,
            (
                width // 2 - 120,
                ground - 90,
                240,
                90
            )
        )

        # Center Tower
        pygame.draw.rect(
            screen,
            castle,
            (
                width // 2 - 35,
                ground - 220,
                70,
                220
            )
        )

        # Left Tower
        pygame.draw.rect(
            screen,
            castle,
            (
                width // 2 - 145,
                ground - 170,
                55,
                170
            )
        )

        # Right Tower
        pygame.draw.rect(
            screen,
            castle,
            (
                width // 2 + 90,
                ground - 170,
                55,
                170
            )
        )

        # Center Roof
        pygame.draw.polygon(
            screen,
            castle,
            [
                (width//2-40, ground-220),
                (width//2, ground-275),
                (width//2+40, ground-220)
            ]
        )

        # Left Roof
        pygame.draw.polygon(
            screen,
            castle,
            [
                (width//2-150, ground-170),
                (width//2-118, ground-215),
                (width//2-86, ground-170)
            ]
        )

        # Right Roof
        pygame.draw.polygon(
            screen,
            castle,
            [
                (width//2+86, ground-170),
                (width//2+118, ground-215),
                (width//2+150, ground-170)
            ]
        )

        # Door
        pygame.draw.arc(
            screen,
            (50, 50, 65),
            (
                width//2-22,
                ground-42,
                44,
                42
            ),
            math.pi,
            math.pi * 2,
            4
        )

        # Flag Pole
        # pygame.draw.line(
            # screen,
            # (130,130,130),
            # (
            #     width//2,
            #     ground-275
            # ),
            # (
            #     width//2,
            #     ground-315
        #     ),
        #     2
        # )

        # # Flag
        # pygame.draw.polygon(
        #     screen,
        #     (255,200,70),
        #     [
        #         (width//2, ground-315),
        #         (width//2+24, ground-307),
        #         (width//2, ground-299)
        #     ]
        # )

    # ----------------------------------------
    # Draw
    # ----------------------------------------

    def draw(self, screen):

        self.background.draw(screen)

        self.draw_castle(screen)

        title_scale = (
            1 +
            math.sin(self.time * 2) * 0.02
        )

        title_font = pygame.font.SysFont(
            "arial",
            int(72 * title_scale),
            bold=True
        )

        title = title_font.render(
            "LearnScape",
            True,
            (255,220,80)
        )

        title_rect = title.get_rect(
            center=(
                screen.get_width()//2,
                90
            )
        )

        screen.blit(title, title_rect)
                # ----------------------------------------
        # Subtitle
        # ----------------------------------------

        subtitle = self.subtitle_font.render(
            "A Journey Through Knowledge",
            True,
            (225, 225, 235)
        )

        subtitle_rect = subtitle.get_rect(
            center=(
                screen.get_width() // 2,
                150
            )
        )

        screen.blit(
            subtitle,
            subtitle_rect
        )

        # ----------------------------------------
        # Menu Buttons
        # ----------------------------------------

        start_y = 240

        for index, option in enumerate(self.options):

            selected = index == self.selected

            scale = 1.0

            if selected:
                scale = (
                    1.05 +
                    math.sin(self.time * 6) * 0.03
                )

            font = pygame.font.SysFont(
                "arial",
                int(30 * scale),
                bold=True
            )

            if selected:
                text_color = (255, 220, 80)
            else:
                text_color = (225, 225, 225)

            text = font.render(
                option,
                True,
                text_color
            )

            rect = text.get_rect(
                center=(
                    screen.get_width() // 2,
                    start_y + index * 65
                )
            )

            if selected:

                glow = pygame.Surface(
                    (
                        rect.width + 80,
                        rect.height + 40
                    ),
                    pygame.SRCALPHA
                )

                pygame.draw.rect(
                    glow,
                    (255, 210, 80, 40),
                    glow.get_rect(),
                    border_radius=18
                )

                screen.blit(
                    glow,
                    (
                        rect.x - 40,
                        rect.y - 20
                    )
                )

                pygame.draw.polygon(
                    screen,
                    (255, 220, 80),
                    [
                        (rect.x - 35, rect.centery),
                        (rect.x - 18, rect.centery - 10),
                        (rect.x - 18, rect.centery + 10)
                    ]
                )

            screen.blit(
                text,
                rect
            )

        # ----------------------------------------
        # Decorative Line
        # ----------------------------------------

        pygame.draw.line(
            screen,
            (255, 210, 80),
            (
                screen.get_width() // 2 - 170,
                190
            ),
            (
                screen.get_width() // 2 + 170,
                190
            ),
            2
        )

        # ----------------------------------------
        # Version
        # ----------------------------------------

        version_font = pygame.font.SysFont(
            "arial",
            18
        )

        version = version_font.render(
            "LearnScape v1.0.0",
            True,
            (130, 130, 150)
        )

        screen.blit(
            version,
            (
                20,
                screen.get_height() - 35
            )
        )

        controls = version_font.render(
            "↑ ↓ Navigate   ENTER Select",
            True,
            (130, 130, 150)
        )

        controls_rect = controls.get_rect(
            bottomright=(
                screen.get_width() - 20,
                screen.get_height() - 15
            )
        )

        screen.blit(
            controls,
            controls_rect
        )