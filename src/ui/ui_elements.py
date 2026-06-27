import pygame
from src.utils.helpers import get_font, draw_rounded_panel, draw_gradient_rect, draw_glowing_text

class Button:
    def __init__(self, game, x, y, w, h, text, callback=None, color=(40, 100, 200), hover_color=(230, 175, 45), font_size=20):
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.callback = callback
        
        # Style parameters
        self.base_color = color
        self.hover_color = hover_color
        self.font = get_font(font_size, is_bold=True)
        self.font_size = font_size
        
        # State tracking
        self.is_hovered = False
        self.clicked = False
        self.enabled = True
        
        # Hover animations
        self.glow_time = 0.0
        self.scale_factor = 1.0

    def set_enabled(self, val):
        self.enabled = bool(val)

    def handle_event(self, event, logical_mouse_pos):
        if not self.enabled or not self.callback:
            return False
            
        mx, my = logical_mouse_pos
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(mx, my):
                self.game.sounds.play_sfx("click")
                self.callback()
                return True
        return False

    def update(self, dt, logical_mouse_pos):
        if not self.enabled:
            self.is_hovered = False
            return
            
        mx, my = logical_mouse_pos
        was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mx, my)
        
        # Play subtle click hover sound only once on transition
        if self.is_hovered and not was_hovered:
            self.game.sounds.play_sfx("click")
            
        if self.is_hovered:
            # Pulsing hover size glow
            self.glow_time += dt * 5.0
            self.scale_factor = 1.0 + 0.03 * abs(pygame.math.sin(self.glow_time))
        else:
            self.glow_time = 0
            self.scale_factor = 1.0

    def draw(self, surface):
        x, y, w, h = self.rect
        
        # Scale button surface slightly if hovered
        if self.is_hovered:
            sw = int(w * self.scale_factor)
            sh = int(h * self.scale_factor)
            sx = x - (sw - w) // 2
            sy = y - (sh - h) // 2
            draw_rect = pygame.Rect(sx, sy, sw, sh)
            draw_color = self.hover_color
            border_glow = (255, 235, 120)
        else:
            draw_rect = self.rect
            draw_color = self.base_color
            border_glow = (60, 50, 40)
            
        if not self.enabled:
            draw_color = (60, 60, 65)
            border_glow = (40, 40, 45)
            
        # Draw button panel
        draw_rounded_panel(surface, draw_rect, draw_color, border_glow, border_width=2, border_radius=8, bg_alpha=255)
        
        # Render text
        t_color = (255, 255, 255) if self.enabled else (120, 120, 125)
        text_surf = self.font.render(self.text, True, t_color)
        tw, th = text_surf.get_size()
        
        # Draw glowing outline for text if hovered
        tx = draw_rect.x + (draw_rect.width - tw) // 2
        ty = draw_rect.y + (draw_rect.height - th) // 2
        
        if self.is_hovered:
            draw_glowing_text(surface, self.text, self.font, t_color, (tx, ty), (255, 215, 0, 120), 1)
        else:
            surface.blit(text_surf, (tx, ty))


class ProgressBar:
    def __init__(self, x, y, w, h, val, max_val, color, text_prefix=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.val = val
        self.max_val = max(1, max_val)
        self.color = color
        self.text_prefix = text_prefix
        
        # Smooth lerp variables
        self.displayed_val = float(val)
        self.font = get_font(12, is_bold=True)

    def set_values(self, val, max_val):
        self.val = val
        self.max_val = max(1, max_val)

    def update(self, dt):
        # Smoothly slide towards target values
        diff = self.val - self.displayed_val
        if abs(diff) > 0.05:
            self.displayed_val += diff * 12.0 * dt
        else:
            self.displayed_val = float(self.val)

    def draw(self, surface):
        x, y, w, h = self.rect
        
        # 1. Draw Background Slot
        pygame.draw.rect(surface, (30, 25, 25), self.rect, border_radius=4)
        
        # 2. Draw Filled portion (scaled by current lerp value)
        pct = max(0.0, min(1.0, self.displayed_val / self.max_val))
        fill_w = int(w * pct)
        if fill_w > 0:
            fill_rect = pygame.Rect(x, y, fill_w, h)
            pygame.draw.rect(surface, self.color, fill_rect, border_radius=4)
            # Add reflection/sheen gradient line on top half of the bar
            pygame.draw.rect(surface, (255, 255, 255, 60), (x, y, fill_w, h//2), border_radius=2)
            
        # Draw Border
        pygame.draw.rect(surface, (100, 85, 60), self.rect, 2, border_radius=4)
        
        # 3. Draw text (e.g. "HP: 50 / 100")
        label = f"{self.text_prefix} {int(self.displayed_val)} / {self.max_val}" if self.text_prefix else f"{int(self.displayed_val)}/{self.max_val}"
        text_surf = self.font.render(label, True, (255, 255, 255))
        tw, th = text_surf.get_size()
        surface.blit(text_surf, (x + (w - tw)//2, y + (h - th)//2))


class Slider:
    def __init__(self, x, y, w, h, initial_val=0.5, callback=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.value = initial_val # 0.0 to 1.0
        self.callback = callback
        
        self.handle_width = 16
        self.is_dragging = False

    def handle_event(self, event, logical_mouse_pos):
        mx, my = logical_mouse_pos
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if clicked inside slider bounds
            if self.rect.inflate(10, 10).collidepoint(mx, my):
                self.is_dragging = True
                self.update_value_from_mouse(mx)
                return True
                
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_dragging = False
            
        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            self.update_value_from_mouse(mx)
            return True
            
        return False

    def update_value_from_mouse(self, mx):
        x, _, w, _ = self.rect
        rel_x = mx - x
        self.value = max(0.0, min(1.0, rel_x / w))
        if self.callback:
            self.callback(self.value)

    def draw(self, surface):
        x, y, w, h = self.rect
        
        # Draw Slider line bar
        pygame.draw.rect(surface, (40, 35, 30), (x, y + h//2 - 3, w, 6), border_radius=3)
        pygame.draw.rect(surface, (230, 185, 55), (x, y + h//2 - 3, int(w * self.value), 6), border_radius=3)
        
        # Draw Handle selector
        hx = x + int(w * self.value) - self.handle_width//2
        hy = y + h//2 - 10
        handle_rect = pygame.Rect(hx, hy, self.handle_width, 20)
        
        pygame.draw.rect(surface, (220, 170, 30), handle_rect, border_radius=4)
        pygame.draw.rect(surface, (255, 235, 150), handle_rect, 1, border_radius=4)


class TextBox:
    def __init__(self, x, y, w, h, default_text="Hero", max_chars=12):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = default_text
        self.max_chars = max_chars
        self.active = False
        self.font = get_font(22, is_bold=True)
        self.blink_timer = 0.0

    def handle_event(self, event, logical_mouse_pos):
        mx, my = logical_mouse_pos
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(mx, my)
            return self.active
            
        if self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                self.active = False
            else:
                # Add text char if within bounds
                if len(self.text) < self.max_chars and event.unicode.isalnum() or event.unicode == ' ':
                    self.text += event.unicode
            return True
            
        return False

    def update(self, dt):
        if self.active:
            self.blink_timer += dt
        else:
            self.blink_timer = 0.0

    def draw(self, surface):
        x, y, w, h = self.rect
        
        # Outer glow color if active
        border_color = (230, 185, 55) if self.active else (100, 90, 80)
        bg_color = (25, 25, 30)
        
        draw_rounded_panel(surface, self.rect, bg_color, border_color, border_width=2, border_radius=6, bg_alpha=255)
        
        # Display Text
        disp_text = self.text
        if self.active and int(self.blink_timer * 2) % 2 == 0:
            disp_text += "|" # blinking cursor
            
        text_surf = self.font.render(disp_text, True, (255, 255, 255))
        tw, th = text_surf.get_size()
        surface.blit(text_surf, (x + 10, y + (h - th)//2))
