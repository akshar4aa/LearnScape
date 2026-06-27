import pygame
import math
from src.engine.state import State
from src.utils.helpers import get_font, draw_glowing_text
from src.ui.particle import ParticleSystem

class SplashState(State):
    def __init__(self, game):
        super().__init__(game)
        self.timer = 0.0
        self.duration = 4.0 # Splash duration
        self.particles = ParticleSystem()
        
        self.logo_scale = 1.0
        self.logo_glow = 0.0
        
        self.font_title = get_font(52, is_bold=True)
        self.font_subtitle = get_font(22)

    def enter(self):
        self.timer = 0.0
        self.particles.clear()
        self.game.sounds.play_music("menu")

    def exit(self):
        pass

    def handle_event(self, event):
        # Click or space bar skips splash
        if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            self.game.change_state("loading")

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.duration:
            self.game.change_state("loading")
            return

        # Logo pulsing animations
        self.logo_glow += dt * 3.0
        self.logo_scale = 1.0 + 0.04 * math.sin(self.logo_glow)
        
        # Spawn glowing rising golden sparks
        if random.random() < 0.15:
            sx = self.game.virtual_width // 2 + random.randint(-150, 150)
            sy = self.game.virtual_height // 2 + 50
            vx = random.uniform(-10, 10)
            vy = random.uniform(-40, -10)
            color = (255, 215, 0) # Gold
            size = random.uniform(2, 4)
            life = random.uniform(1.0, 1.8)
            # Access particle class directly
            from src.ui.particle import Particle
            self.particles.particles.append(Particle(sx, sy, vx, vy, color, size, life))
            
        self.particles.update(dt)

    def draw(self, surface):
        surface.fill((15, 12, 20)) # Dark night violet bg
        
        # Draw background stars/particles
        self.particles.draw(surface)
        
        # Calculate pulse scale rect
        logo_text = "LearnScape"
        scaled_font_size = int(52 * self.logo_scale)
        font = get_font(scaled_font_size, is_bold=True)
        
        # Main logo rendering centered
        lt_surf = font.render(logo_text, True, (255, 255, 255))
        lx = (self.game.virtual_width - lt_surf.get_width()) // 2
        ly = (self.game.virtual_height - lt_surf.get_height()) // 2 - 30
        
        # Draw glowing gold backing
        glow_color = (230, 175, 45, 140)
        draw_glowing_text(surface, logo_text, font, (255, 255, 255), (lx, ly), glow_color, 3)
        
        # Draw Subtitle "An Educational RPG Adventure"
        sub_text = "An Educational RPG Adventure"
        sub_surf = self.font.subtitle.render(sub_text, True, (160, 150, 180))
        sx = (self.game.virtual_width - sub_surf.get_width()) // 2
        sy = ly + lt_surf.get_height() + 15
        surface.blit(sub_surf, (sx, sy))
        
        # Bottom Prompt
        prompt_text = "Press SPACE to Skip"
        prompt_font = get_font(12, is_bold=True)
        prompt_surf = prompt_font.render(prompt_text, True, (80, 75, 95))
        px = (self.game.virtual_width - prompt_surf.get_width()) // 2
        py = self.game.virtual_height - 50
        # Gentle blink
        if int(self.timer * 2) % 2 == 0:
            surface.blit(prompt_surf, (px, py))

# Add missing import for random
import random
