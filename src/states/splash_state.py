import math
import pygame

from src.states.state import State
from src.ui.background import Background

class SplashState(State):
    def __init__(self, game):
        super().__init__(game)
        self.timer = 0.0
        self.logo_time = 0.0
        self.duration = 2.0  # 2 seconds total

        width = self.game.screen.get_width()
        height = self.game.screen.get_height()
        self.background = Background(width, height)

        self.title_size = 72
        self.title_font = pygame.font.SysFont("arial", self.title_size, bold=True)
        self.subtitle_font = pygame.font.SysFont("arial", 26)
        self.press_font = pygame.font.SysFont("arial", 22, bold=True)
        self.version_font = pygame.font.SysFont("arial", 18)

        # Star positions
        self.stars = [
            (120, 90), (230, 60), (420, 110), (560, 80), (720, 150),
            (880, 70), (1020, 120), (1140, 90), (950, 180), (350, 170)
        ]

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                    self.skip_to_menu()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.skip_to_menu()

    def skip_to_menu(self):
        from src.states.menu_state import MenuState
        self.game.change_state(MenuState(self.game))

    def update(self, dt):
        self.timer += dt
        self.logo_time += dt
        self.background.update(dt)

        # Auto transition after duration
        if self.timer >= self.duration:
            self.skip_to_menu()

    def draw(self, screen):
        # 1. Background
        self.background.draw(screen)

        # 2. Twinkling Stars
        for index, (x, y) in enumerate(self.stars):
            glow = (math.sin(self.logo_time * 3 + index) + 1) / 2
            radius = 2 + glow * 2
            pygame.draw.circle(screen, (255, 255, 220), (x, y), int(radius))

        # 3. Logo Glow
        glow_surf = pygame.Surface((520, 260), pygame.SRCALPHA)
        for r in range(140, 0, -2):
            alpha = int(70 * (r / 140))
            pygame.draw.circle(glow_surf, (255, 215, 80, alpha), (260, 130), r)
        screen.blit(glow_surf, (screen.get_width() // 2 - 260, 140))

        # 4. Floating Title
        scale = 1 + math.sin(self.logo_time * 2) * 0.03
        logo_y = 280 + math.sin(self.logo_time * 1.5) * 8
        scaled_font = pygame.font.SysFont("arial", int(self.title_size * scale), bold=True)
        title = scaled_font.render("LearnScape", True, (255, 220, 80))
        title_rect = title.get_rect(center=(screen.get_width() // 2, logo_y))
        screen.blit(title, title_rect)

        # 5. Subtitle
        subtitle = self.subtitle_font.render("A Journey Through Knowledge", True, (225, 225, 235))
        subtitle_rect = subtitle.get_rect(center=(screen.get_width() // 2, 365))
        screen.blit(subtitle, subtitle_rect)

        # 6. Floating Magic Book icon
        book_y = 470 + math.sin(self.logo_time * 2) * 5
        book_rect = pygame.Rect(screen.get_width() // 2 - 35, int(book_y), 70, 45)

        # Book Glow
        book_glow = pygame.Surface((160, 120), pygame.SRCALPHA)
        for r in range(55, 0, -2):
            alpha = int(70 * (r / 55))
            pygame.draw.circle(book_glow, (255, 215, 100, alpha), (80, 60), r)
        screen.blit(book_glow, (book_rect.centerx - 80, book_rect.centery - 60))

        # Draw book vector shape
        pygame.draw.rect(screen, (110, 55, 20), book_rect, border_radius=6)
        pygame.draw.rect(screen, (245, 240, 220), (book_rect.x + 6, book_rect.y + 5, 58, 35), border_radius=4)
        pygame.draw.line(screen, (180, 180, 180), (book_rect.centerx, book_rect.y + 5), (book_rect.centerx, book_rect.bottom - 5), 2)

        # Sparkles around book
        for i in range(8):
            angle = self.logo_time * 2.5 + i
            px = book_rect.centerx + math.cos(angle) * 45
            py = book_rect.centery + math.sin(angle) * 20
            pygame.draw.circle(screen, (255, 235, 120), (int(px), int(py)), 2)

        # 7. Press Enter message
        pulse = (math.sin(self.logo_time * 4) + 1) / 2
        color = (int(170 + pulse * 85), int(170 + pulse * 85), int(170 + pulse * 85))
        press = self.press_font.render("Press ENTER to skip", True, color)
        press_rect = press.get_rect(center=(screen.get_width() // 2, 590))
        screen.blit(press, press_rect)

        # 8. Version
        version = self.version_font.render("LearnScape v1.0.0", True, (130, 130, 150))
        screen.blit(version, (20, screen.get_height() - 35))

        # 9. Screen Fade-In/Fade-Out overlay based on timer
        fade_alpha = 0
        if self.timer < 0.5:
            # Fade in from black
            fade_alpha = int(255 * (1.0 - (self.timer / 0.5)))
        elif self.timer > (self.duration - 0.5):
            # Fade out to black
            fade_alpha = int(255 * ((self.timer - (self.duration - 0.5)) / 0.5))
        
        if fade_alpha > 0:
            fade_surf = pygame.Surface(screen.get_size())
            fade_surf.fill((12, 16, 35))
            fade_surf.set_alpha(fade_alpha)
            screen.blit(fade_surf, (0, 0))