import pygame
import math

class Button:
    def __init__(self, x, y, width, height, text, font_size=24, border_radius=12):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font_size = font_size
        self.border_radius = border_radius
        self.selected = False
        self.hovered = False
        self.font = pygame.font.SysFont("arial", font_size, bold=True)
        self.time = 0.0

    def handle_event(self, event, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered:
                return True
        return False

    def update(self, dt):
        self.time += dt

    def draw(self, screen):
        # Determine scale and colors
        is_active = self.selected or self.hovered
        scale = 1.05 + math.sin(self.time * 6) * 0.02 if is_active else 1.0

        scaled_width = int(self.rect.width * scale)
        scaled_height = int(self.rect.height * scale)
        draw_rect = pygame.Rect(0, 0, scaled_width, scaled_height)
        draw_rect.center = self.rect.center

        # Colors based on state
        if is_active:
            bg_color = (255, 220, 80)      # Gold
            border_color = (255, 255, 200) # Bright yellow
            text_color = (20, 24, 35)       # Dark cosmic blue
        else:
            bg_color = (35, 40, 60)         # Gray blue
            border_color = (255, 220, 80)   # Gold border
            text_color = (255, 255, 255)    # White

        # Draw Glow if active
        if is_active:
            glow = pygame.Surface((scaled_width + 30, scaled_height + 30), pygame.SRCALPHA)
            for r in range(15, 0, -2):
                alpha = int(60 * (r / 15))
                pygame.draw.rect(
                    glow,
                    (255, 220, 80, alpha),
                    (15 - r, 15 - r, scaled_width + 2*r, scaled_height + 2*r),
                    border_radius=self.border_radius + r
                )
            screen.blit(glow, (draw_rect.x - 15, draw_rect.y - 15))

        # Draw main button body
        pygame.draw.rect(screen, bg_color, draw_rect, border_radius=self.border_radius)
        # Draw border
        pygame.draw.rect(screen, border_color, draw_rect, 2, border_radius=self.border_radius)

        # Draw text
        text_surf = self.font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=draw_rect.center)
        screen.blit(text_surf, text_rect)
