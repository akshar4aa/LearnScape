import pygame

class ProgressBar:
    def __init__(self, x, y, width, height, bg_color=(35, 40, 60), fill_color=(255, 220, 80), border_color=(255, 220, 80), border_radius=10):
        self.rect = pygame.Rect(x, y, width, height)
        self.bg_color = bg_color
        self.fill_color = fill_color
        self.border_color = border_color
        self.border_radius = border_radius
        self.progress = 0.0 # 0.0 to 1.0

    def set_progress(self, value):
        self.progress = max(0.0, min(1.0, value))

    def draw(self, screen):
        # Background
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=self.border_radius)
        
        # Fill
        if self.progress > 0:
            fill_width = int(self.rect.width * self.progress)
            fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
            pygame.draw.rect(screen, self.fill_color, fill_rect, border_radius=self.border_radius)

        # Border
        pygame.draw.rect(screen, self.border_color, self.rect, 2, border_radius=self.border_radius)
