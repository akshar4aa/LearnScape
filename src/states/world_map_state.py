import pygame
import math

from src.states.state import State
from src.ui.background import Background
from src.ui.planet import Planet
from src.ui.particles import ParticleSystem
from src.states.lesson_state import LessonState

class WorldMapState(State):
    def __init__(self, game):
        super().__init__(game)
        width = self.game.screen.get_width()
        height = self.game.screen.get_height()

        self.background = Background(width, height)
        self.particles = ParticleSystem(width, height, amount=40)

        self.title_font = pygame.font.SysFont("arial", 48, bold=True)
        self.text_font = pygame.font.SysFont("arial", 22)
        self.hud_font = pygame.font.SysFont("arial", 20, bold=True)

        # 3 Planets with themes
        self.planets = [
            Planet(220, 360, "assets/planets/earth.png", "Earth", 
                   color_theme=((100, 180, 255), (30, 80, 180))),
            Planet(640, 280, "assets/planets/jupiter.png", "Jupiter", 
                   color_theme=((240, 160, 100), (160, 80, 30))),
            Planet(1060, 360, "assets/planets/saturn.png", "Saturn", 
                   color_theme=((230, 200, 150), (130, 100, 60)))
        ]
        self.selected = 0
        self.time = 0.0

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
                return

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.selected = (self.selected - 1) % len(self.planets)
                    if hasattr(self.game, 'audio'):
                        self.game.audio.play_sfx("assets/audio/planet_select.wav")
                elif event.key == pygame.K_RIGHT:
                    self.selected = (self.selected + 1) % len(self.planets)
                    if hasattr(self.game, 'audio'):
                        self.game.audio.play_sfx("assets/audio/planet_select.wav")
                elif event.key == pygame.K_RETURN:
                    # Verify planet is unlocked
                    planet_name = self.planets[self.selected].name
                    
                    # Unlock check: Earth is unlocked, Jupiter unlocked at lvl 2, Saturn at lvl 3
                    required_lvl = 1
                    if planet_name == "Jupiter":
                        required_lvl = 2
                    elif planet_name == "Saturn":
                        required_lvl = 3
                        
                    if self.game.level >= required_lvl:
                        if hasattr(self.game, 'audio'):
                            self.game.audio.play_sfx("assets/audio/click.wav")
                        self.game.change_state(LessonState(self.game, planet_name))
                    else:
                        # Played buzzer sound or failed lock notification
                        if hasattr(self.game, 'audio'):
                            self.game.audio.play_sfx("assets/audio/wrong.wav")
                            
                elif event.key == pygame.K_ESCAPE:
                    from src.states.menu_state import MenuState
                    self.game.change_state(MenuState(self.game))

    def update(self, dt):
        self.time += dt
        self.background.update(dt)
        self.particles.update(dt)
        for planet in self.planets:
            planet.update(dt)

    def draw_hud(self, screen):
        # Top HUD bar displaying Name, LVL, XP, and Coins
        hud_bg = pygame.Rect(20, 20, screen.get_width() - 40, 50)
        pygame.draw.rect(screen, (25, 30, 48), hud_bg, border_radius=12)
        pygame.draw.rect(screen, (255, 220, 80), hud_bg, 2, border_radius=12)

        # Player stats
        name_text = f"Hero: {self.game.hero_name} ({self.game.char_type})"
        lvl_text = f"Level: {self.game.level}"
        xp_text = f"XP: {self.game.xp}/{self.game.level * 100}"
        coins_text = f"Coins: 🪙 {self.game.coins}"

        name_surf = self.hud_font.render(name_text, True, (255, 255, 255))
        lvl_surf = self.hud_font.render(lvl_text, True, (255, 220, 80))
        xp_surf = self.hud_font.render(xp_text, True, (100, 180, 255))
        coins_surf = self.hud_font.render(coins_text, True, (255, 215, 0))

        screen.blit(name_surf, (40, 32))
        screen.blit(lvl_surf, (400, 32))
        screen.blit(xp_surf, (600, 32))
        screen.blit(coins_surf, (950, 32))

    def draw(self, screen):
        # Background Space Gradient
        self.background.draw(screen)
        self.particles.draw(screen)

        # Draw Title
        title = self.title_font.render("World Map", True, (255, 220, 80))
        screen.blit(title, title.get_rect(center=(screen.get_width() // 2, 110)))

        # Draw dotted path line between planets
        path_points = []
        for i in range(101):
            t = i / 100.0
            # Quadratic Bezier Curve from Earth to Saturn with Jupiter as high midpoint
            x = (1-t)**2 * 220 + 2*t*(1-t) * 640 + t**2 * 1060
            y = (1-t)**2 * 360 + 2*t*(1-t) * 160 + t**2 * 360 + math.sin(self.time * 2 + t * 5) * 5
            path_points.append((int(x), int(y)))
            
        # Draw path dots
        for idx in range(0, len(path_points), 3):
            pygame.draw.circle(screen, (100, 130, 200), path_points[idx], 3)

        # Draw Planets
        for i, planet in enumerate(self.planets):
            planet.draw(screen, i == self.selected)

            # Draw Lock Icon if locked
            required_lvl = 1 if planet.name == "Earth" else (2 if planet.name == "Jupiter" else 3)
            if self.game.level < required_lvl:
                # Draw lock visual
                lock_x = planet.x
                lock_y = planet.y - 30
                pygame.draw.rect(screen, (220, 80, 80), (lock_x - 20, lock_y - 15, 40, 30), border_radius=5)
                pygame.draw.circle(screen, (220, 80, 80), (lock_x, lock_y - 15), 12, 3)
                # Text required level
                req_text = self.text_font.render(f"LVL {required_lvl}", True, (255, 100, 100))
                screen.blit(req_text, req_text.get_rect(center=(planet.x, planet.y - 65)))

        # Draw HUD info
        self.draw_hud(screen)

        # Draw Help Footer
        hint = self.text_font.render("← → Select Planet    ENTER Open    ESC Main Menu", True, (200, 200, 220))
        screen.blit(hint, hint.get_rect(center=(screen.get_width() // 2, 675)))