import pygame

class XPBar:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.target_pct = 0.0
        self.current_pct = 0.0
        self.font = pygame.font.SysFont("arial", 18, bold=True)

    def set_progress(self, xp, level):
        next_level_xp = level * 100
        self.target_pct = max(0.0, min(1.0, xp / next_level_xp))
        self.xp = xp
        self.next_level_xp = next_level_xp
        self.level = level

    def update(self, dt):
        # Smooth slide animation
        speed = 5.0
        self.current_pct += (self.target_pct - self.current_pct) * speed * dt

    def draw(self, screen):
        # Draw background
        bar_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, (35, 40, 60), bar_rect, border_radius=self.height // 2)

        # Draw filled progress (blue/purple gradient color or nice gold glow)
        fill_width = int(self.width * self.current_pct)
        if fill_width > 0:
            fill_rect = pygame.Rect(self.x, self.y, fill_width, self.height)
            pygame.draw.rect(screen, (100, 180, 255), fill_rect, border_radius=self.height // 2)

        # Draw border
        pygame.draw.rect(screen, (255, 220, 80), bar_rect, 2, border_radius=self.height // 2)

        # Draw text
        text_str = f"LVL {self.level} | {self.xp}/{self.next_level_xp} XP"
        text_surf = self.font.render(text_str, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=bar_rect.center)
        screen.blit(text_surf, text_rect)
