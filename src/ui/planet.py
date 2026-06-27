import pygame
import math

# Planet size
PLANET_SIZE = 300


class Planet:

    def __init__(self, x, y, image_path, name):

        self.x = x
        self.y = y
        self.name = name

        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.smoothscale(
            self.image,
            (PLANET_SIZE, PLANET_SIZE)
        )

        self.time = 0

        self.font = pygame.font.SysFont(
            "arial",
            28,
            bold=True
        )

    def update(self, dt):

        self.time += dt

    def draw(self, screen, selected=False):

        # Floating animation
        offset = math.sin(self.time * 2) * 5

        # ------------------------
        # Soft Glow
        # ------------------------

        # ------------------------
# Soft Glow
# ------------------------

        if selected:

            glow = pygame.Surface(
                (600, 600),
                pygame.SRCALPHA
                )

        # Bright center
            pygame.draw.circle(
                glow,
                (255, 245, 180, 140),
                (300, 300),
                140
                )

    # Strong glow
            pygame.draw.circle(
                glow,
                (255, 220, 80, 90),
                (300, 300),
                190
                )

    # Medium glow
            pygame.draw.circle(
                glow,
                (255, 220, 80, 50),
                (300, 300),
                240
                )

    # Outer halo
            pygame.draw.circle(
                glow,
                (255, 220, 80, 20),
                (300, 300),
                290
                )

            screen.blit(
                glow,
                (
                    self.x - 300,
                    self.y - 300 + offset
                )
            )

        # ------------------------
        # Planet Image
        # ------------------------

        screen.blit(
            self.image,
            (
                self.x - PLANET_SIZE // 2,
                self.y - PLANET_SIZE // 2 + offset
            )
        )

        # ------------------------
        # Planet Name
        # ------------------------

        text = self.font.render(
            self.name,
            True,
            (255, 255, 255)
        )

        screen.blit(
            text,
            text.get_rect(
                center=(
                    self.x,
                    self.y + PLANET_SIZE // 2 + 30 + offset
                )
            )
        )

        # ------------------------
        # Selection Arrow
        # ------------------------

        # if selected:

        #     pygame.draw.polygon(
        #         screen,
        #         (255, 220, 80),
        #         [
        #             (
        #                 self.x,
        #                 self.y - PLANET_SIZE // 2 - 15 + offset
        #             ),
        #             (
        #                 self.x - 15,
        #                 self.y - PLANET_SIZE // 2 - 40 + offset
        #             ),
        #             (
        #                 self.x + 15,
        #                 self.y - PLANET_SIZE // 2 - 40 + offset
        #             )
        #         ]
        #     )