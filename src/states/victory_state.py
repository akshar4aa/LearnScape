import pygame
import math
from src.states.state import State
from src.ui.background import Background
from src.states.reward_state import RewardState

class VictoryState(State):
    def __init__(self, game, planet, lesson_name, xp_earned, coins_earned):
        super().__init__(game)
        self.planet = planet
        self.lesson_name = lesson_name
        self.xp_earned = xp_earned
        self.coins_earned = coins_earned

        width = self.game.screen.get_width()
        height = self.game.screen.get_height()
        self.background = Background(width, height)

        self.title_font = pygame.font.SysFont("arial", 60, bold=True)
        self.heading_font = pygame.font.SysFont("arial", 28, bold=True)
        self.text_font = pygame.font.SysFont("arial", 24)
        self.time = 0.0

        # Continue Button
        self.button_rect = pygame.Rect(470, 540, 340, 55)

        # Play victory music
        if hasattr(self.game, 'audio'):
            self.game.audio.play_sfx("assets/audio/victory.wav")

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
                return

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.button_rect.collidepoint(mouse_pos):
                    self.claim_rewards()
                    return

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.claim_rewards()
                    return

    def claim_rewards(self):
        if hasattr(self.game, 'audio'):
            self.game.audio.play_sfx("assets/audio/click.wav")
        self.game.change_state(RewardState(self.game, self.planet, self.lesson_name, self.xp_earned, self.coins_earned))

    def update(self, dt):
        self.time += dt
        self.background.update(dt)

    def draw(self, screen):
        self.background.draw(screen)

        # Scale pulsing text
        pulse = 1.0 + math.sin(self.time * 4) * 0.03
        font_size = int(64 * pulse)
        scaled_font = pygame.font.SysFont("arial", font_size, bold=True)
        
        title_surf = scaled_font.render("VICTORY!", True, (255, 215, 0)) # Shiny Gold
        title_rect = title_surf.get_rect(center=(640, 140))
        screen.blit(title_surf, title_rect)

        # Star Particles procedural burst
        for i in range(12):
            angle = self.time * 2 + i * (math.pi / 6)
            dist = 160 + math.sin(self.time * 4 + i) * 15
            px = 640 + math.cos(angle) * dist
            py = 140 + math.sin(angle) * dist
            pygame.draw.circle(screen, (255, 220, 80), (int(px), int(py)), 3)

        # Stats panel
        panel = pygame.Rect(340, 220, 600, 280)
        pygame.draw.rect(screen, (25, 30, 48), panel, border_radius=15)
        pygame.draw.rect(screen, (255, 215, 0), panel, 2, border_radius=15)

        sub_lbl = self.heading_font.render(f"Lesson: {self.lesson_name} Complete", True, (255, 255, 255))
        screen.blit(sub_lbl, sub_lbl.get_rect(center=(640, 260)))

        # Earned readouts
        xp_lbl = self.text_font.render(f"Experience Gained:  +{self.xp_earned} XP", True, (100, 180, 255))
        coins_lbl = self.text_font.render(f"Space Coins Earned: 🪙 +{self.coins_earned}", True, (255, 215, 0))
        screen.blit(xp_lbl, xp_lbl.get_rect(center=(640, 320)))
        screen.blit(coins_lbl, coins_lbl.get_rect(center=(640, 370)))

        unlocked_lbl = self.text_font.render("Claim your rewards and level up your character!", True, (200, 200, 220))
        screen.blit(unlocked_lbl, unlocked_lbl.get_rect(center=(640, 440)))

        # Continue Button
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.button_rect.collidepoint(mouse_pos)
        btn_bg = (255, 235, 120) if hovered else (255, 220, 80)
        
        if hovered:
            btn_glow = pygame.Surface((self.button_rect.width + 20, self.button_rect.height + 20), pygame.SRCALPHA)
            pygame.draw.rect(btn_glow, (255, 220, 80, 50), btn_glow.get_rect(), border_radius=12)
            screen.blit(btn_glow, (self.button_rect.x - 10, self.button_rect.y - 10))

        pygame.draw.rect(screen, btn_bg, self.button_rect, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), self.button_rect, 2, border_radius=12)

        cont_font = pygame.font.SysFont("arial", 28, bold=True)
        cont_surf = cont_font.render("CLAIM REWARDS", True, (20, 24, 35))
        screen.blit(cont_surf, cont_surf.get_rect(center=self.button_rect.center))

        # Bottom help
        help_surf = self.text_font.render("ENTER/Click to Continue", True, (130, 130, 150))
        screen.blit(help_surf, help_surf.get_rect(center=(640, 660)))
