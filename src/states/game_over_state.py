import pygame
import math
from src.states.state import State
from src.ui.background import Background

class GameOverState(State):
    def __init__(self, game, planet, lesson_name):
        super().__init__(game)
        self.planet = planet
        self.lesson_name = lesson_name

        width = self.game.screen.get_width()
        height = self.game.screen.get_height()
        self.background = Background(width, height)

        self.title_font = pygame.font.SysFont("arial", 60, bold=True)
        self.heading_font = pygame.font.SysFont("arial", 28, bold=True)
        self.text_font = pygame.font.SysFont("arial", 24)
        self.time = 0.0

        # Buttons
        self.retry_button = pygame.Rect(470, 440, 340, 55)
        self.map_button = pygame.Rect(470, 515, 340, 55)

        # Play sad tone or game over sound
        if hasattr(self.game, 'audio'):
            self.game.audio.play_sfx("assets/audio/wrong.wav")

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
                return

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.retry_button.collidepoint(mouse_pos):
                    self.retry_quiz()
                    return
                elif self.map_button.collidepoint(mouse_pos):
                    self.return_to_map()
                    return

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.retry_quiz()
                    return
                elif event.key == pygame.K_ESCAPE:
                    self.return_to_map()
                    return

    def retry_quiz(self):
        if hasattr(self.game, 'audio'):
            self.game.audio.play_sfx("assets/audio/click.wav")
        from src.states.quiz_state import QuizState
        self.game.change_state(QuizState(self.game, self.planet, self.lesson_name))

    def return_to_map(self):
        if hasattr(self.game, 'audio'):
            self.game.audio.play_sfx("assets/audio/click.wav")
        from src.states.world_map_state import WorldMapState
        self.game.change_state(WorldMapState(self.game))

    def update(self, dt):
        self.time += dt
        self.background.update(dt)

    def draw(self, screen):
        self.background.draw(screen)

        # Scale pulsing text
        pulse = 1.0 + math.sin(self.time * 3) * 0.02
        font_size = int(60 * pulse)
        scaled_font = pygame.font.SysFont("arial", font_size, bold=True)
        
        title_surf = scaled_font.render("BATTLE DEFEAT!", True, (220, 80, 80)) # Dark Red
        title_rect = title_surf.get_rect(center=(640, 140))
        screen.blit(title_surf, title_rect)

        # Stats panel
        panel = pygame.Rect(340, 220, 600, 180)
        pygame.draw.rect(screen, (25, 30, 48), panel, border_radius=15)
        pygame.draw.rect(screen, (220, 80, 80), panel, 2, border_radius=15)

        sub_lbl = self.heading_font.render(f"Lesson: {self.lesson_name}", True, (255, 255, 255))
        screen.blit(sub_lbl, sub_lbl.get_rect(center=(640, 260)))

        unlocked_lbl = self.text_font.render("Keep trying! Every defeat makes you stronger.", True, (200, 200, 220))
        screen.blit(unlocked_lbl, unlocked_lbl.get_rect(center=(640, 320)))

        # Draw Retry Button
        mouse_pos = pygame.mouse.get_pos()
        retry_hovered = self.retry_button.collidepoint(mouse_pos)
        retry_bg = (255, 235, 120) if retry_hovered else (255, 220, 80)
        
        if retry_hovered:
            btn_glow = pygame.Surface((self.retry_button.width + 20, self.retry_button.height + 20), pygame.SRCALPHA)
            pygame.draw.rect(btn_glow, (255, 220, 80, 50), btn_glow.get_rect(), border_radius=12)
            screen.blit(btn_glow, (self.retry_button.x - 10, self.retry_button.y - 10))

        pygame.draw.rect(screen, retry_bg, self.retry_button, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), self.retry_button, 2, border_radius=12)
        
        btn_font = pygame.font.SysFont("arial", 24, bold=True)
        retry_surf = btn_font.render("RETRY QUIZ BATTLE", True, (20, 24, 35))
        screen.blit(retry_surf, retry_surf.get_rect(center=self.retry_button.center))

        # Draw World Map Button
        map_hovered = self.map_button.collidepoint(mouse_pos)
        map_bg = (100, 150, 240) if map_hovered else (80, 120, 200)

        if map_hovered:
            btn_glow = pygame.Surface((self.map_button.width + 20, self.map_button.height + 20), pygame.SRCALPHA)
            pygame.draw.rect(btn_glow, (100, 150, 240, 50), btn_glow.get_rect(), border_radius=12)
            screen.blit(btn_glow, (self.map_button.x - 10, self.map_button.y - 10))

        pygame.draw.rect(screen, map_bg, self.map_button, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), self.map_button, 2, border_radius=12)

        map_surf = btn_font.render("RETURN TO WORLD MAP", True, (255, 255, 255))
        screen.blit(map_surf, map_surf.get_rect(center=self.map_button.center))

        # Bottom help
        help_surf = self.text_font.render("ENTER to Retry    ESC for World Map", True, (130, 130, 150))
        screen.blit(help_surf, help_surf.get_rect(center=(640, 660)))
