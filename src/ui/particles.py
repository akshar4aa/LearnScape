import pygame
import random
import math


class Particle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.reset()

    def reset(self):
        self.x = random.uniform(0, self.width)
        self.y = random.uniform(self.height, self.height + 200)

        self.size = random.uniform(2, 5)

        self.speed = random.uniform(20, 60)

        self.alpha = random.randint(80, 220)

        self.life = random.uniform(2, 6)

        self.time = random.uniform(0, 6)

        self.color = random.choice([
            (255, 220, 120),
            (255, 255, 200),
            (180, 220, 255),
            (255, 180, 80)
        ])

    def update(self, dt):

        self.time += dt

        self.life -= dt

        self.y -= self.speed * dt

        self.x += math.sin(self.time * 2) * 15 * dt

        if self.life <= 0 or self.y < -20:
            self.reset()

    def draw(self, screen):

        glow = pygame.Surface(
            (40, 40),
            pygame.SRCALPHA
        )

        for r in range(18, 0, -2):

            alpha = int(self.alpha * (r / 18) * 0.25)

            pygame.draw.circle(
                glow,
                (*self.color, alpha),
                (20, 20),
                r
            )

        screen.blit(
            glow,
            (
                self.x - 20,
                self.y - 20
            )
        )

        pygame.draw.circle(
            screen,
            self.color,
            (
                int(self.x),
                int(self.y)
            ),
            int(self.size)
        )


class ParticleSystem:

    def __init__(self, width, height, amount=150):

        self.particles = [
            Particle(width, height)
            for _ in range(amount)
        ]

    def update(self, dt):

        for particle in self.particles:
            particle.update(dt)

    def draw(self, screen):

        for particle in self.particles:
            particle.draw(screen)