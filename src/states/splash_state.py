import math
import pygame

from src.states.state import State
from src.ui.background import Background


class SplashState(State):

    def __init__(self, game):
        super().__init__(game)

        self.timer = 0.0
        self.logo_time = 0.0

        width = self.game.screen.get_width()
        height = self.game.screen.get_height()

        self.background = Background(width, height)

    

        self.title_size = 72

        self.title_font = pygame.font.SysFont(
            "arial",
            self.title_size,
            bold=True
        )

        self.subtitle_font = pygame.font.SysFont(
            "arial",
            26
        )

        self.press_font = pygame.font.SysFont(
            "arial",
            22,
            bold=True
        )

        self.stars = [
            (120, 90),
            (230, 60),
            (420, 110),
            (560, 80),
            (720, 150),
            (880, 70),
            (1020, 120),
            (1140, 90),
            (950, 180),
            (350, 170)
        ]

    def handle_events(self, events):

        for event in events:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:

                    from src.states.menu_state import MenuState

                    self.game.change_state(
                        MenuState(self.game)
                    )

    def update(self, dt):

        self.timer += dt
        self.logo_time += dt

        self.background.update(dt)
        

    def draw(self, screen):

        # ===================================
        # Background
        # ===================================

        self.background.draw(screen)

        # self.particles.draw(screen)

        # ===================================
        # Extra Twinkling Stars
        # ===================================

        for index, (x, y) in enumerate(self.stars):

            glow = (
                math.sin(
                    self.logo_time * 2 + index
                ) + 1
            ) / 2

            radius = 2 + glow * 2

            pygame.draw.circle(
                screen,
                (255, 255, 220),
                (x, y),
                int(radius)
            )

        # ===================================
        # Golden Glow
        # ===================================

        glow = pygame.Surface(
            (520, 260),
            pygame.SRCALPHA
        )

        for r in range(140, 0, -2):

            alpha = int(
                70 * (r / 140)
            )

            pygame.draw.circle(
                glow,
                (
                    255,
                    215,
                    80,
                    alpha
                ),
                (260, 130),
                r
            )

        screen.blit(
            glow,
            (
                screen.get_width() // 2 - 260,
                140
            )
        )

        # ===================================
        # Floating Logo
        # ===================================

        scale = (
            1 +
            math.sin(
                self.logo_time * 2
            ) * 0.03
        )

        font = pygame.font.SysFont(
            "arial",
            int(self.title_size * scale),
            bold=True
        )

        logo_y = (
            280 +
            math.sin(
                self.logo_time * 1.5
            ) * 8
        )

        title = font.render(
            "LearnScape",
            True,
            (
                255,
                220,
                80
            )
        )

        title_rect = title.get_rect(
            center=(
                screen.get_width() // 2,
                logo_y
            )
        )

        screen.blit(
            title,
            title_rect
        )
                # ===================================
        # Subtitle
        # ===================================

        subtitle = self.subtitle_font.render(
            "A Journey Through Knowledge",
            True,
            (225, 225, 235)
        )

        subtitle_rect = subtitle.get_rect(
            center=(
                screen.get_width() // 2,
                365
            )
        )

        screen.blit(
            subtitle,
            subtitle_rect
        )

        # ===================================
        # Floating Magic Book
        # ===================================

        book_y = 470 + math.sin(
            self.logo_time * 2
        ) * 5

        book_rect = pygame.Rect(
            screen.get_width() // 2 - 35,
            int(book_y),
            70,
            45
        )

        # Book glow
        glow = pygame.Surface(
            (160, 120),
            pygame.SRCALPHA
        )

        for r in range(55, 0, -2):

            alpha = int(70 * (r / 55))

            pygame.draw.circle(
                glow,
                (255, 215, 100, alpha),
                (80, 60),
                r
            )

        screen.blit(
            glow,
            (
                book_rect.centerx - 80,
                book_rect.centery - 60
            )
        )

        # Book cover
        pygame.draw.rect(
            screen,
            (110, 55, 20),
            book_rect,
            border_radius=6
        )

        # Book pages
        pygame.draw.rect(
            screen,
            (245, 240, 220),
            (
                book_rect.x + 6,
                book_rect.y + 5,
                58,
                35
            ),
            border_radius=4
        )

        # Book center line
        pygame.draw.line(
            screen,
            (180, 180, 180),
            (
                book_rect.centerx,
                book_rect.y + 5
            ),
            (
                book_rect.centerx,
                book_rect.bottom - 5
            ),
            2
        )

        # ===================================
        # Magic Sparkles
        # ===================================

        for i in range(8):

            angle = self.logo_time * 2 + i

            px = (
                book_rect.centerx +
                math.cos(angle) * 45
            )

            py = (
                book_rect.centery +
                math.sin(angle) * 20
            )

            pygame.draw.circle(
                screen,
                (255, 235, 120),
                (
                    int(px),
                    int(py)
                ),
                2
            )

        # ===================================
        # Press ENTER
        # ===================================

        pulse = (
            math.sin(
                self.logo_time * 4
            ) + 1
        ) / 2

        color = (
            int(170 + pulse * 85),
            int(170 + pulse * 85),
            int(170 + pulse * 85)
        )

        press = self.press_font.render(
            "Press ENTER",
            True,
            color
        )

        press_rect = press.get_rect(
            center=(
                screen.get_width() // 2,
                590
            )
        )

        screen.blit(
            press,
            press_rect
        )

        # ===================================
        # Version
        # ===================================

        version_font = pygame.font.SysFont(
            "arial",
            18
        )

        version = version_font.render(
            "LearnScape v1.0",
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