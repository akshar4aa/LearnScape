import pygame
import math

class CharacterCard:
    def __init__(self, x, y, width, height, character_data):
        self.rect = pygame.Rect(x, y, width, height)
        self.char = character_data
        self.selected = False
        self.hovered = False
        self.time = 0.0
        
        self.emoji_font = pygame.font.SysFont("arial", 48)
        self.title_font = pygame.font.SysFont("arial", 28, bold=True)
        self.desc_font = pygame.font.SysFont("arial", 20)

    def handle_event(self, event, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered:
                return True
        return False

    def update(self, dt):
        self.time += dt

    def draw(self, screen):
        is_active = self.selected or self.hovered
        scale = 1.04 + math.sin(self.time * 5) * 0.02 if is_active else 1.0

        scaled_width = int(self.rect.width * scale)
        scaled_height = int(self.rect.height * scale)
        draw_rect = pygame.Rect(0, 0, scaled_width, scaled_height)
        draw_rect.center = self.rect.center

        # Card colors
        if is_active:
            bg_color = (75, 45, 115)       # Cosmic Purple
            border_color = (255, 220, 80)   # Gold border
            text_color = (255, 255, 255)
        else:
            bg_color = (25, 30, 48)         # Dark Blue Panel
            border_color = (130, 130, 150)  # Muted Gray border
            text_color = (200, 200, 200)

        # Draw card glow if selected
        if self.selected:
            glow = pygame.Surface((scaled_width + 40, scaled_height + 40), pygame.SRCALPHA)
            for r in range(16, 0, -2):
                alpha = int(50 * (r / 16))
                pygame.draw.rect(
                    glow,
                    (255, 220, 80, alpha),
                    (20 - r, 20 - r, scaled_width + 2*r, scaled_height + 2*r),
                    border_radius=15 + r
                )
            screen.blit(glow, (draw_rect.x - 20, draw_rect.y - 20))

        # Draw card container
        pygame.draw.rect(screen, bg_color, draw_rect, border_radius=15)
        pygame.draw.rect(screen, border_color, draw_rect, 3 if self.selected else 2, border_radius=15)

        # Draw Emoji
        emoji_surf = self.emoji_font.render(self.char["emoji"], True, text_color)
        emoji_rect = emoji_surf.get_rect(center=(draw_rect.centerx, draw_rect.y + 60))
        screen.blit(emoji_surf, emoji_rect)

        # Draw Name
        name_surf = self.title_font.render(self.char["name"], True, (255, 220, 80) if is_active else (255, 255, 255))
        name_rect = name_surf.get_rect(center=(draw_rect.centerx, draw_rect.y + 130))
        screen.blit(name_surf, name_rect)

        # Draw Description
        # Split description into lines if it is too long
        words = self.char["desc"].split(" ")
        lines = []
        curr_line = ""
        for word in words:
            if len(curr_line + word) < 16:
                curr_line += word + " "
            else:
                lines.append(curr_line.strip())
                curr_line = word + " "
        if curr_line:
            lines.append(curr_line.strip())

        y_offset = 180
        for line in lines:
            line_surf = self.desc_font.render(line, True, text_color)
            line_rect = line_surf.get_rect(center=(draw_rect.centerx, draw_rect.y + y_offset))
            screen.blit(line_surf, line_rect)
            y_offset += 26
