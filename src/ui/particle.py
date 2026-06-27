import pygame
import random
import math
from src.utils.helpers import get_font

class Particle:
    def __init__(self, x, y, vx, vy, color, size, max_life):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.life = max_life
        self.max_life = max_life

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        # Add friction or gravity
        self.vy += 20 * dt # light gravity
        self.life -= dt
        return self.life > 0

    def draw(self, surface):
        alpha = int(255 * (self.life / self.max_life))
        color_with_alpha = (*self.color[:3], alpha)
        
        # Draw soft circle
        temp_surf = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
        pygame.draw.circle(temp_surf, color_with_alpha, (int(self.size), int(self.size)), int(self.size))
        surface.blit(temp_surf, (int(self.x - self.size), int(self.y - self.size)))


class FloatingText:
    def __init__(self, text, x, y, color, size=24, life=1.0):
        self.text = text
        self.x = float(x)
        self.y = float(y)
        self.color = color
        self.font = get_font(size, is_bold=True)
        self.life = life
        self.max_life = life
        self.vx = random.uniform(-20, 20)
        self.vy = -60.0 # rising

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 10.0 * dt # slow down rise
        self.life -= dt
        return self.life > 0

    def draw(self, surface):
        alpha = int(255 * (self.life / self.max_life))
        text_surf = self.font.render(self.text, True, self.color)
        text_surf.set_alpha(alpha)
        
        # Black backdrop shadow
        shadow_surf = self.font.render(self.text, True, (0, 0, 0))
        shadow_surf.set_alpha(alpha)
        surface.blit(shadow_surf, (int(self.x) + 2, int(self.y) + 2))
        surface.blit(text_surf, (int(self.x), int(self.y)))


class ParticleSystem:
    def __init__(self):
        self.particles = []
        self.floating_texts = []

    def clear(self):
        self.particles.clear()
        self.floating_texts.clear()

    def add_hit_burst(self, x, y, color, count=15):
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 180)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed - 30
            size = random.uniform(3, 7)
            life = random.uniform(0.3, 0.6)
            self.particles.append(Particle(x, y, vx, vy, color, size, life))

    def add_heal_burst(self, x, y, count=12):
        for _ in range(count):
            vx = random.uniform(-20, 20)
            vy = random.uniform(-40, -10)
            size = random.uniform(4, 8)
            life = random.uniform(0.5, 1.0)
            color = (50, 230, 80) # Sparkling green
            self.particles.append(Particle(x, y, vx, vy, color, size, life))

    def add_magic_spell(self, x, y, color, count=20):
        # Swirling spiral spark emitter
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            vx = math.cos(angle) * 80.0
            vy = math.sin(angle) * 80.0 - 20
            size = random.uniform(3, 6)
            life = random.uniform(0.6, 1.2)
            self.particles.append(Particle(x, y, vx, vy, color, size, life))

    def add_floating_text(self, text, x, y, color, size=24):
        self.floating_texts.append(FloatingText(text, x, y, color, size))

    def update(self, dt):
        self.particles = [p for p in self.particles if p.update(dt)]
        self.floating_texts = [ft for ft in self.floating_texts if ft.update(dt)]

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)
        for ft in self.floating_texts:
            ft.draw(surface)


class WeatherOverlay:
    def __init__(self, mode="none"):
        self.mode = mode # "none", "rain", "snow", "fog"
        self.particles = []
        self.screen_w = 1280
        self.screen_h = 720
        
        # Pre-cache soft fog cloud surface to optimize performance
        self.fog_surf = pygame.Surface((180, 180), pygame.SRCALPHA)
        pygame.draw.circle(self.fog_surf, (240, 240, 250, 18), (90, 90), 90)
        
        self.init_weather()

    def set_mode(self, mode):
        if self.mode != mode:
            self.mode = mode
            self.particles.clear()
            self.init_weather()

    def init_weather(self):
        if self.mode == "rain":
            # Populate initial drop points
            for _ in range(80):
                self.particles.append({
                    "x": random.randint(0, self.screen_w + 200),
                    "y": random.randint(-self.screen_h, 0),
                    "length": random.randint(12, 22),
                    "speed": random.randint(400, 600)
                })
        elif self.mode == "snow":
            # Populate initial snowflakes
            for _ in range(70):
                self.particles.append({
                    "x": random.randint(-50, self.screen_w),
                    "y": random.randint(-self.screen_h, 0),
                    "size": random.uniform(2, 5),
                    "speed": random.randint(50, 100),
                    "wobble": random.uniform(0, 10)
                })
        elif self.mode == "fog":
            # Populate scrolling fog clusters
            for _ in range(12):
                self.particles.append({
                    "x": random.randint(-180, self.screen_w),
                    "y": random.randint(0, self.screen_h - 100),
                    "speed": random.randint(15, 35)
                })

    def update(self, dt):
        if self.mode == "none":
            return
            
        if self.mode == "rain":
            for drop in self.particles:
                # Diagonal fall
                drop["y"] += drop["speed"] * dt
                drop["x"] -= (drop["speed"] * 0.15) * dt
                
                # Recycle if off-screen
                if drop["y"] > self.screen_h:
                    drop["y"] = random.randint(-50, -10)
                    drop["x"] = random.randint(0, self.screen_w + 200)

        elif self.mode == "snow":
            for flake in self.particles:
                flake["wobble"] += dt * 2.0
                # Float down with wobble sway
                flake["y"] += flake["speed"] * dt
                flake["x"] += math.sin(flake["wobble"]) * 15 * dt
                
                # Recycle
                if flake["y"] > self.screen_h:
                    flake["y"] = random.randint(-30, -5)
                    flake["x"] = random.randint(-20, self.screen_w)

        elif self.mode == "fog":
            for cloud in self.particles:
                cloud["x"] += cloud["speed"] * dt
                
                # Recycle cloud on left side
                if cloud["x"] > self.screen_w:
                    cloud["x"] = -180
                    cloud["y"] = random.randint(0, self.screen_h - 100)

    def draw(self, surface):
        if self.mode == "none":
            return
            
        if self.mode == "rain":
            for drop in self.particles:
                # Diagonal blue lines
                x, y, l = drop["x"], drop["y"], drop["length"]
                pygame.draw.line(surface, (140, 170, 250, 100), (int(x), int(y)), (int(x - l*0.15), int(y + l)), 2)
                
        elif self.mode == "snow":
            for flake in self.particles:
                x, y, s = flake["x"], flake["y"], flake["size"]
                pygame.draw.circle(surface, (245, 245, 250, 160), (int(x), int(y)), int(s))
                
        elif self.mode == "fog":
            for cloud in self.particles:
                # Blit pre-cached transparent fog cloud surface
                surface.blit(self.fog_surf, (int(cloud["x"]), int(cloud["y"])))
