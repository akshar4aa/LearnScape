import pygame
import math
import random


class Star:
    def __init__(self, width, height):
        self.x = random.randint(0, width)
        self.y = random.randint(0, height // 2)

        self.radius = random.randint(1, 3)

        self.offset = random.uniform(0, 6.28)

    def draw(self, screen, time):

        glow = (math.sin(time * 2 + self.offset) + 1) / 2

        radius = self.radius + glow

        pygame.draw.circle(
            screen,
            (255, 255, 230),
            (int(self.x), int(self.y)),
            int(radius),
        )


class Cloud:
    def __init__(self, width):

        self.width = width

        self.x = random.randint(-300, width)

        self.y = random.randint(40, 220)

        self.speed = random.uniform(8, 18)

    def update(self, dt):

        self.x += self.speed * dt

        if self.x > self.width + 250:
            self.x = -250

    def draw(self, screen):

        surf = pygame.Surface((220, 90), pygame.SRCALPHA)

        pygame.draw.ellipse(
            surf,
            (255, 255, 255, 20),
            (0, 20, 120, 55),
        )

        pygame.draw.ellipse(
            surf,
            (255, 255, 255, 25),
            (60, 0, 120, 70),
        )

        pygame.draw.ellipse(
            surf,
            (255, 255, 255, 20),
            (110, 20, 100, 50),
        )

        screen.blit(surf, (self.x, self.y))


class ShootingStar:
    def __init__(self, width):

        self.width = width

        self.reset()

    def reset(self):

        self.x = random.randint(-300, self.width)

        self.y = random.randint(0, 180)

        self.speed = random.randint(450, 650)

        self.length = random.randint(60, 120)

        self.timer = random.uniform(2, 8)

    def update(self, dt):

        self.timer -= dt

        if self.timer <= 0:

            self.x += self.speed * dt
            self.y += self.speed * dt * 0.35

            if self.x > self.width + 300:
                self.reset()

    def draw(self, screen):

        if self.timer > 0:
            return

        pygame.draw.line(
            screen,
            (255, 255, 220),
            (self.x, self.y),
            (
                self.x - self.length,
                self.y - self.length // 3,
            ),
            2,
        )


class Background:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.time = 0

        self.stars = [
            Star(width, height)
            for _ in range(120)
        ]

        self.clouds = [
            Cloud(width)
            for _ in range(5)
        ]

        self.shooting = [
            ShootingStar(width)
            for _ in range(2)
        ]

    def update(self, dt):

        self.time += dt

        for cloud in self.clouds:
            cloud.update(dt)

        for star in self.shooting:
            star.update(dt)

    def draw_gradient(self, screen):

        top = (10, 18, 55)
        bottom = (42, 22, 65)

        for y in range(self.height):

            t = y / self.height

            r = int(top[0] + (bottom[0] - top[0]) * t)
            g = int(top[1] + (bottom[1] - top[1]) * t)
            b = int(top[2] + (bottom[2] - top[2]) * t)

            pygame.draw.line(
                screen,
                (r, g, b),
                (0, y),
                (self.width, y),
            )

    def draw_moon(self, screen):

        moon_x = self.width - 170
        moon_y = 110

        glow = pygame.Surface(
            (220, 220),
            pygame.SRCALPHA,
        )

        for r in range(90, 0, -2):

            alpha = int((90 - r) * 1.8)

            pygame.draw.circle(
                glow,
                (255, 255, 180, alpha),
                (110, 110),
                r,
            )

        screen.blit(
            glow,
            (moon_x - 110, moon_y - 110),
        )

        pygame.draw.circle(
            screen,
            (248, 245, 215),
            (moon_x, moon_y),
            42,
        )

        pygame.draw.circle(
            screen,
            (255, 255, 235),
            (moon_x - 7, moon_y - 7),
            34,
        )

    def draw(self, screen):

        self.draw_gradient(screen)

        self.draw_moon(screen)

        for star in self.stars:
            star.draw(screen, self.time)

        for cloud in self.clouds:
            cloud.draw(screen)

        for shooting in self.shooting:
            shooting.draw(screen)