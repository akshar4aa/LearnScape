import pygame


class Popup:

    def __init__(self):

        self.active = False
        self.success = True

        self.title = ""
        self.message = ""

        self.timer = 0

        self.title_font = pygame.font.SysFont(
            "arial",
            42,
            bold=True
        )

        self.text_font = pygame.font.SysFont(
            "arial",
            28
        )

    def show(self, success, title, message):

        self.success = success
        self.title = title
        self.message = message

        self.timer = 1.5
        self.active = True

    def update(self, dt):

        if not self.active:
            return

        self.timer -= dt

        if self.timer <= 0:
            self.active = False

    def draw(self, screen):

        if not self.active:
            return

        overlay = pygame.Surface(
            screen.get_size(),
            pygame.SRCALPHA
        )

        overlay.fill((0, 0, 0, 150))

        screen.blit(overlay, (0, 0))

        box = pygame.Rect(
            320,
            220,
            640,
            260
        )

        if self.success:
            color = (50, 200, 90)
        else:
            color = (220, 70, 70)

        pygame.draw.rect(
            screen,
            (35, 35, 55),
            box,
            border_radius=18
        )

        pygame.draw.rect(
            screen,
            color,
            box,
            4,
            border_radius=18
        )

        title = self.title_font.render(
            self.title,
            True,
            color
        )

        screen.blit(
            title,
            title.get_rect(center=(640, 285))
        )

        text = self.text_font.render(
            self.message,
            True,
            (255, 255, 255)
        )

        screen.blit(
            text,
            text.get_rect(center=(640, 360))
        )