import pygame


class HealthBar:

    def __init__(self, x, y, width, height, maximum):

        self.x = x
        self.y = y

        self.width = width
        self.height = height

        self.maximum = maximum
        self.current = maximum
        self.display = maximum

    def update(self, dt):

        speed = 6

        self.display += (
            self.current - self.display
        ) * speed * dt

    def draw(self, screen, color):

        pygame.draw.rect(
            screen,
            (45,45,55),
            (
                self.x,
                self.y,
                self.width,
                self.height
            ),
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            color,
            (
                self.x,
                self.y,
                int(
                    self.width *
                    (
                        self.display /
                        self.maximum
                    )
                ),
                self.height
            ),
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            (255,255,255),
            (
                self.x,
                self.y,
                self.width,
                self.height
            ),
            2,
            border_radius=10
        )