import pygame

class Panel:
    def __init__(self, x, y, width, height, bg_color=(25, 30, 48), border_color=(255, 220, 80), border_width=2, border_radius=15, glow=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius
        self.glow = glow

    def draw(self, screen):
        # Draw Glow if enabled
        if self.glow:
            glow_surf = pygame.Surface((self.rect.width + 40, self.rect.height + 40), pygame.SRCALPHA)
            for r in range(20, 0, -2):
                alpha = int(40 * (r / 20))
                pygame.draw.rect(
                    glow_surf,
                    (*self.border_color, alpha),
                    (20 - r, 20 - r, self.rect.width + 2*r, self.rect.height + 2*r),
                    border_radius=self.border_radius + r
                )
            screen.blit(glow_surf, (self.rect.x - 20, self.rect.y - 20))

        # Main Panel BG
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=self.border_radius)
        # Panel Border
        if self.border_width > 0:
            pygame.draw.rect(screen, self.border_color, self.rect, self.border_width, border_radius=self.border_radius)
