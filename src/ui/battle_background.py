import pygame
import random
import math


class BattleBackground:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.time = 0

        # Stars
        self.stars = []

        for _ in range(80):

            self.stars.append([
                random.randint(0, width),
                random.randint(0, height),
                random.randint(1, 3),
                random.random() * 6
            ])

    def update(self, dt):

        self.time += dt

    def draw(self, screen):

        # Sky
        screen.fill((12, 16, 35))

        # Nebula
        for i in range(5):

            radius = 140 + i * 40

            glow = pygame.Surface(
                (radius * 2, radius * 2),
                pygame.SRCALPHA
            )

            pygame.draw.circle(
                glow,
                (80, 40, 180, 15),
                (radius, radius),
                radius
            )

            screen.blit(
                glow,
                (
                    180 + i * 170 - radius,
                    250 + math.sin(self.time + i) * 25 - radius
                )
            )

        # Stars
        for star in self.stars:

            alpha = int(
                170 +
                math.sin(self.time * 2 + star[3]) * 85
            )

            color = (
                alpha,
                alpha,
                alpha
            )

            pygame.draw.circle(
                screen,
                color,
                (star[0], star[1]),
                star[2]
            )

        # Ground
        pygame.draw.rect(
            screen,
            (28, 35, 45),
            (
                0,
                self.height - 120,
                self.width,
                120
            )
        )

        pygame.draw.line(
            screen,
            (70, 100, 120),
            (0, self.height - 120),
            (self.width, self.height - 120),
            3
        )