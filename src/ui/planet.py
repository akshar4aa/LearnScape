import pygame
import math
import os

PLANET_SIZE = 160 # Reduced size to fit layout comfortably on screen

class Planet:
    def __init__(self, x, y, image_path, name, color_theme=((100, 150, 255), (50, 100, 200))):
        self.x = x
        self.y = y
        self.name = name
        self.color_theme = color_theme
        self.time = 0.0
        self.font = pygame.font.SysFont("arial", 24, bold=True)
        
        self.image = None
        if os.path.exists(image_path):
            try:
                self.image = pygame.image.load(image_path).convert_alpha()
                self.image = pygame.transform.smoothscale(self.image, (PLANET_SIZE, PLANET_SIZE))
            except Exception as e:
                print(f"Warning: Failed to load planet image {image_path}: {e}")
                self.image = None
        else:
            print(f"Warning: Planet image not found at {image_path}. Using fallback procedural rendering.")

    def update(self, dt):
        self.time += dt

    def draw(self, screen, selected=False):
        # Floating height animation
        offset = math.sin(self.time * 2.2) * 8

        # 1. Soft Glow behind Planet
        glow_size = PLANET_SIZE + 80
        glow = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
        glow_color = (255, 220, 80) if selected else (120, 150, 255)
        max_alpha = 100 if selected else 40
        
        for r in range(glow_size // 2, PLANET_SIZE // 2 - 10, -3):
            pct = 1.0 - (r - PLANET_SIZE // 2) / (glow_size // 2 - PLANET_SIZE // 2 + 1)
            alpha = int(max_alpha * pct)
            pygame.draw.circle(glow, (*glow_color, alpha), (glow_size // 2, glow_size // 2), r)
        
        screen.blit(glow, (self.x - glow_size // 2, self.y - glow_size // 2 + offset))

        # 2. Draw Planet Image or Procedural Fallback
        if self.image:
            screen.blit(self.image, (self.x - PLANET_SIZE // 2, self.y - PLANET_SIZE // 2 + offset))
        else:
            # Procedurally render a beautiful sphere
            radius = PLANET_SIZE // 2
            # Base sphere
            pygame.draw.circle(screen, self.color_theme[1], (self.x, int(self.y + offset)), radius)
            
            # Draw details (Earth continents, Jupiter stripes, Saturn rings)
            if self.name == "Earth":
                # Draw continent shapes
                pygame.draw.circle(screen, (80, 200, 100), (self.x - 20, int(self.y - 10 + offset)), 25)
                pygame.draw.circle(screen, (80, 200, 100), (self.x + 15, int(self.y + 15 + offset)), 30)
                pygame.draw.circle(screen, (60, 180, 80), (self.x + 30, int(self.y - 15 + offset)), 15)
            elif self.name == "Jupiter":
                # Draw gaseous bands
                pygame.draw.rect(screen, (220, 120, 80), (self.x - radius + 5, int(self.y - 20 + offset), radius * 2 - 10, 8), border_radius=4)
                pygame.draw.rect(screen, (240, 200, 160), (self.x - radius + 2, int(self.y - 5 + offset), radius * 2 - 4, 12), border_radius=6)
                pygame.draw.rect(screen, (200, 90, 60), (self.x - radius + 6, int(self.y + 15 + offset), radius * 2 - 12, 10), border_radius=5)
                # Great Red Spot
                pygame.draw.ellipse(screen, (180, 40, 40), (self.x + 10, int(self.y + offset), 22, 14))
            elif self.name == "Saturn":
                # Draw Saturn rings
                # Draw back ring
                ring_surf_back = pygame.Surface((PLANET_SIZE * 2, 60), pygame.SRCALPHA)
                pygame.draw.ellipse(ring_surf_back, (230, 200, 160, 120), (0, 0, PLANET_SIZE * 2, 60), 12)
                # We need to draw rings tilted: let's draw a rotated ellipse
                # For pygame, simpler to draw a flat stretched ellipse and rotate or draw flat and let it overlay
                pygame.draw.ellipse(screen, (210, 180, 140), (self.x - radius * 1.8, int(self.y - 15 + offset), radius * 3.6, 30), 8)
                # Draw sphere details
                pygame.draw.rect(screen, (225, 200, 150), (self.x - radius + 4, int(self.y - 10 + offset), radius * 2 - 8, 10))
                pygame.draw.rect(screen, (190, 160, 120), (self.x - radius + 2, int(self.y + 10 + offset), radius * 2 - 4, 8))

            # Draw shading overlay (shadow/depth effect)
            shading = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(shading, (0, 0, 0, 80), (radius, radius), radius)
            # Create a spherical highlight
            pygame.draw.circle(shading, (255, 255, 255, 40), (radius - 20, radius - 20), radius // 2)
            screen.blit(shading, (self.x - radius, self.y - radius + offset))

        # 3. Planet Name
        text_color = (255, 220, 80) if selected else (255, 255, 255)
        text = self.font.render(self.name, True, text_color)
        text_rect = text.get_rect(center=(self.x, self.y + PLANET_SIZE // 2 + 25 + offset))
        screen.blit(text, text_rect)