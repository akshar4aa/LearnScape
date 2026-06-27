import pygame


class BattleButton:

    def __init__(self, x, y, width, height, text):

        self.rect = pygame.Rect(x, y, width, height)

        self.text = text

        self.selected = False

        self.font = pygame.font.SysFont(
            "arial",
            28,
            bold=True
        )

    def draw(self, screen):

        if self.selected:

            bg = (255, 220, 80)
            border = (255, 255, 180)
            text_color = (20, 20, 20)

        else:

            bg = (42, 48, 72)
            border = (90, 120, 255)
            text_color = (255, 255, 255)

        # Glow
        if self.selected:

            glow = pygame.Surface(
                (
                    self.rect.width + 30,
                    self.rect.height + 30
                ),
                pygame.SRCALPHA
            )

            pygame.draw.rect(
                glow,
                (255, 220, 80, 45),
                glow.get_rect(),
                border_radius=20
            )

            screen.blit(
                glow,
                (
                    self.rect.x - 15,
                    self.rect.y - 15
                )
            )

        # Button

        pygame.draw.rect(
            screen,
            bg,
            self.rect,
            border_radius=15
        )

        pygame.draw.rect(
            screen,
            border,
            self.rect,
            3,
            border_radius=15
        )

        text = self.font.render(
            self.text,
            True,
            text_color
        )

        screen.blit(
            text,
            text.get_rect(
                center=self.rect.center
            )
        )