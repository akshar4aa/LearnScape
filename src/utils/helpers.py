import pygame
import math

def draw_text_wrapped(surface, text, font, color, rect, line_spacing=2):
    """
    Renders text word-by-word wrapping to fit a given rect bounding box.
    Returns the vertical position of the last line drawn.
    """
    x, y, max_w, max_h = rect
    words = text.split(' ')
    space_w, _ = font.size(' ')
    lines = []
    
    current_line = []
    current_w = 0
    
    for word in words:
        # Handle manual newlines
        if '\n' in word:
            parts = word.split('\n')
            for idx, part in enumerate(parts):
                part_w, _ = font.size(part)
                if current_w + part_w <= max_w:
                    current_line.append(part)
                    current_w += part_w + space_w
                else:
                    lines.append(" ".join(current_line))
                    current_line = [part]
                    current_w = part_w + space_w
                
                # If it's a newline separator, force end current line
                if idx < len(parts) - 1:
                    lines.append(" ".join(current_line))
                    current_line = []
                    current_w = 0
            continue
            
        word_w, _ = font.size(word)
        if current_w + word_w <= max_w:
            current_line.append(word)
            current_w += word_w + space_w
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_w = word_w + space_w
            
    if current_line:
        lines.append(" ".join(current_line))
        
    cursor_y = y
    for line in lines:
        if line.strip() == "":
            cursor_y += font.get_linesize() + line_spacing
            continue
        line_surface = font.render(line, True, color)
        line_w, line_h = line_surface.get_size()
        if cursor_y + line_h > y + max_h:
            break # Stop if exceeds boundary
        surface.blit(line_surface, (x, cursor_y))
        cursor_y += line_h + line_spacing
        
    return cursor_y

def draw_glowing_text(surface, text, font, color, pos, glow_color, glow_radius=2):
    """
    Draws text with a glowing/shadow outline by rendering copies offset slightly.
    """
    gx, gy = pos
    # Render glow offset layers
    for dx in range(-glow_radius, glow_radius + 1):
        for dy in range(-glow_radius, glow_radius + 1):
            if dx == 0 and dy == 0:
                continue
            glow_surface = font.render(text, True, glow_color)
            surface.blit(glow_surface, (gx + dx, gy + dy))
            
    # Render main text
    main_surface = font.render(text, True, color)
    surface.blit(main_surface, pos)

def draw_gradient_rect(surface, start_color, end_color, rect, horizontal=False):
    """
    Draws a vertical or horizontal color gradient within a bounding rect.
    """
    x, y, w, h = rect
    start_r, start_g, start_b = start_color
    end_r, end_g, end_b = end_color
    
    if horizontal:
        for dx in range(w):
            t = dx / max(1, w - 1)
            r = int(start_r + (end_r - start_r) * t)
            g = int(start_g + (end_g - start_g) * t)
            b = int(start_b + (end_b - start_b) * t)
            pygame.draw.line(surface, (r, g, b), (x + dx, y), (x + dx, y + h - 1))
    else:
        for dy in range(h):
            t = dy / max(1, h - 1)
            r = int(start_r + (end_r - start_r) * t)
            g = int(start_g + (end_g - start_g) * t)
            b = int(start_b + (end_b - start_b) * t)
            pygame.draw.line(surface, (r, g, b), (x, y + dy), (x + w - 1, y + dy))

def draw_rounded_panel(surface, rect, bg_color, border_color, border_width=2, border_radius=10, bg_alpha=200):
    """
    Draws a high-quality double-layered panel with glassmorphism/translucency.
    """
    x, y, w, h = rect
    
    # Draw transparent/translucent background panel
    temp_surf = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(temp_surf, (*bg_color, bg_alpha), (0, 0, w, h), border_radius=border_radius)
    surface.blit(temp_surf, (x, y))
    
    # Draw solid border
    if border_width > 0:
        pygame.draw.rect(surface, border_color, rect, border_width, border_radius=border_radius)

def get_font(size, is_bold=False):
    """
    Attempts to load a standard system font fallback if a specific custom font file is absent.
    """
    try:
        # Check standard Pygame fonts or fallbacks
        font_name = "georgia" if is_bold else "arial"
        return pygame.font.SysFont(font_name, size, bold=is_bold)
    except:
        return pygame.font.Font(None, size)
