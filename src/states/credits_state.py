import pygame
from src.states.state import State
from src.ui.background import Background
from src.ui.button import Button

class CreditsState(State):
    def __init__(self, game):
        super().__init__(game)
        width = self.game.screen.get_width()
        height = self.game.screen.get_height()
        self.background = Background(width, height)

        self.title_font = pygame.font.SysFont("arial", 56, bold=True)
        self.heading_font = pygame.font.SysFont("arial", 28, bold=True)
        self.text_font = pygame.font.SysFont("arial", 22)

        self.credits = [
            ("Game Development", "Akshara Kalivemula"),
            ("Design Aesthetic", "Modern Cute Space Fantasy Theme"),
            ("Framework Engine", "Pygame Community Edition (Pygame-CE)"),
            ("Assets Source", "Procedural fallbacks & custom planetary PNGs"),
            ("Education Core", "Mathematics, Science, & Python Programming")
        ]

        self.back_button = Button(width // 2 - 150, 520, 300, 55, "Back to Menu", font_size=24)
        self.back_button.selected = True

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
                return

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.back_button.handle_event(event, mouse_pos):
                    self.exit_credits()
                    return

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE):
                    self.exit_credits()
                    return

    def exit_credits(self):
        if hasattr(self.game, 'audio'):
            self.game.audio.play_sfx("assets/audio/click.wav")
        from src.states.menu_state import MenuState
        self.game.change_state(MenuState(self.game))

    def update(self, dt):
        self.background.update(dt)
        self.back_button.update(dt)

    def draw(self, screen):
        self.background.draw(screen)

        # Title
        title_surf = self.title_font.render("Credits", True, (255, 220, 80))
        screen.blit(title_surf, title_surf.get_rect(center=(640, 70)))

        # Panel Backing
        panel = pygame.Rect(240, 140, 800, 470)
        pygame.draw.rect(screen, (25, 30, 48), panel, border_radius=15)
        pygame.draw.rect(screen, (255, 220, 80), panel, 2, border_radius=15)

        # Credits details
        y_offset = 180
        for title, value in self.credits:
            title_surf = self.heading_font.render(title, True, (255, 220, 80))
            screen.blit(title_surf, title_surf.get_rect(center=(640, y_offset)))
            
            value_surf = self.text_font.render(value, True, (255, 255, 255))
            screen.blit(value_surf, value_surf.get_rect(center=(640, y_offset + 30)))
            
            y_offset += 65

        # Back Button
        self.back_button.draw(screen)

        # Help
        help_surf = self.text_font.render("Press ESC/ENTER or Click to return", True, (130, 130, 150))
        screen.blit(help_surf, help_surf.get_rect(center=(640, 675)))
