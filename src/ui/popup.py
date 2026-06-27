import pygame
import math

class Popup:
    def __init__(self):
        self.active = False
        self.title = ""
        self.message = ""
        self.color = (255, 220, 80)
        self.timer = 0.0
        self.max_timer = 1.5
        
        self.title_font = pygame.font.SysFont("arial", 46, bold=True)
        self.text_font = pygame.font.SysFont("arial", 24)

    def show(self, title, color=(255, 220, 80), message=""):
        self.title = title
        self.color = color
        self.message = message
        self.timer = self.max_timer
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

        # Semi-transparent overlay
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        # Fade out towards the end of the timer
        alpha = int(180 * (min(self.timer, 0.4) / 0.4))
        overlay.fill((10, 12, 22, alpha))
        screen.blit(overlay, (0, 0))

        # Box dimensions
        box_width = 540
        box_height = 200 if self.message else 140
        box = pygame.Rect(0, 0, box_width, box_height)
        box.center = (screen.get_width() // 2, screen.get_height() // 2)

        # Scale animation (zoom in)
        elapsed = self.max_timer - self.timer
        scale = 1.0
        if elapsed < 0.2:
            # Zoom in from 0.4 to 1.0
            scale = 0.4 + 0.6 * (elapsed / 0.2)
            # Bounce effect
            scale = min(scale, 1.05)

        scaled_width = int(box_width * scale)
        scaled_height = int(box_height * scale)
        draw_rect = pygame.Rect(0, 0, scaled_width, scaled_height)
        draw_rect.center = box.center

        # Create panel surface for scaling
        panel_surf = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
        
        # Border glow
        border_radius = int(18 * scale)
        pygame.draw.rect(panel_surf, (25, 30, 48, alpha), (0, 0, scaled_width, scaled_height), border_radius=border_radius)
        pygame.draw.rect(panel_surf, (*self.color, alpha), (0, 0, scaled_width, scaled_height), int(4 * scale), border_radius=border_radius)

        screen.blit(panel_surf, draw_rect.topleft)

        # Draw text inside box (with scale offset)
        title_font_size = int(46 * scale)
        title_font = pygame.font.SysFont("arial", title_font_size, bold=True)
        title_surf = title_font.render(self.title, True, self.color)
        
        if self.message:
            title_rect = title_surf.get_rect(center=(box.centerx, box.centery - 25))
            screen.blit(title_surf, title_rect)
            
            text_font_size = int(24 * scale)
            text_font = pygame.font.SysFont("arial", text_font_size)
            text_surf = text_font.render(self.message, True, (255, 255, 255))
            text_rect = text_surf.get_rect(center=(box.centerx, box.centery + 30))
            screen.blit(text_surf, text_rect)
        else:
            title_rect = title_surf.get_rect(center=box.center)
            screen.blit(title_surf, title_rect)