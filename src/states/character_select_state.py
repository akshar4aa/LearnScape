import pygame
from src.states.state import State
from src.ui.background import Background
from src.ui.character_card import CharacterCard
from src.states.loading_state import LoadingState

class CharacterSelectState(State):
    def __init__(self, game):
        super().__init__(game)
        width = self.game.screen.get_width()
        height = self.game.screen.get_height()
        self.background = Background(width, height)

        self.title_font = pygame.font.SysFont("arial", 56, bold=True)
        self.text_font = pygame.font.SysFont("arial", 24)

        self.characters = [
            {"name": "Scholar", "emoji": "📚", "desc": "Extra XP - Double bonus on streaks"},
            {"name": "Explorer", "emoji": "🗺️", "desc": "Balanced - Standard progression stats"},
            {"name": "Inventor", "emoji": "🧪", "desc": "Extra Hints - Safe answer options"},
            {"name": "Speedster", "emoji": "⚡", "desc": "Fast Learner - Quick level unlock scaling"}
        ]
        self.selected = 0

        # Card metrics
        self.cards = []
        start_x = 130
        spacing = 280
        for i, char in enumerate(self.characters):
            card = CharacterCard(start_x + i * spacing, 170, 200, 310, char)
            self.cards.append(card)

        self.cards[self.selected].selected = True

        # Continue Button
        self.continue_button = pygame.Rect(470, 530, 340, 55)

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
                return

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check cards click
                for i, card in enumerate(self.cards):
                    if card.handle_event(event, mouse_pos):
                        self.cards[self.selected].selected = False
                        self.selected = i
                        self.cards[self.selected].selected = True
                        if hasattr(self.game, 'audio'):
                            self.game.audio.play_sfx("assets/audio/click.wav")

                # Check button click
                if self.continue_button.collidepoint(mouse_pos):
                    self.confirm_hero()
                    return

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from src.states.new_adventure_state import NewAdventureState
                    self.game.change_state(NewAdventureState(self.game))
                    return

                elif event.key == pygame.K_LEFT:
                    self.cards[self.selected].selected = False
                    self.selected = (self.selected - 1) % len(self.characters)
                    self.cards[self.selected].selected = True
                    if hasattr(self.game, 'audio'):
                        self.game.audio.play_sfx("assets/audio/click.wav")

                elif event.key == pygame.K_RIGHT:
                    self.cards[self.selected].selected = False
                    self.selected = (self.selected + 1) % len(self.characters)
                    self.cards[self.selected].selected = True
                    if hasattr(self.game, 'audio'):
                        self.game.audio.play_sfx("assets/audio/click.wav")

                elif event.key == pygame.K_RETURN:
                    self.confirm_hero()
                    return

    def confirm_hero(self):
        # Save choice
        self.game.char_type = self.characters[self.selected]["name"]
        
        # Audio
        if hasattr(self.game, 'audio'):
            self.game.audio.play_sfx("assets/audio/click.wav")
            
        self.game.change_state(LoadingState(self.game))

    def update(self, dt):
        self.background.update(dt)
        mouse_pos = pygame.mouse.get_pos()
        for card in self.cards:
            card.update(dt)
            card.hovered = card.rect.collidepoint(mouse_pos)

    def draw(self, screen):
        self.background.draw(screen)

        # Title
        title_surf = self.title_font.render("Choose Your Hero", True, (255, 220, 80))
        screen.blit(title_surf, title_surf.get_rect(center=(640, 65)))

        subtitle_surf = self.text_font.render("Select the class that matches your style of study.", True, (220, 220, 220))
        screen.blit(subtitle_surf, subtitle_surf.get_rect(center=(640, 115)))

        # Draw Cards
        for card in self.cards:
            card.draw(screen)

        # Draw Continue Button
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.continue_button.collidepoint(mouse_pos)
        btn_bg = (255, 235, 120) if hovered else (255, 220, 80)
        
        if hovered:
            btn_glow = pygame.Surface((self.continue_button.width + 20, self.continue_button.height + 20), pygame.SRCALPHA)
            pygame.draw.rect(btn_glow, (255, 220, 80, 50), btn_glow.get_rect(), border_radius=12)
            screen.blit(btn_glow, (self.continue_button.x - 10, self.continue_button.y - 10))

        pygame.draw.rect(screen, btn_bg, self.continue_button, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), self.continue_button, 2, border_radius=12)

        cont_surf = self.title_font.render("CONTINUE", True, (20, 24, 35))
        # Keep title font size appropriate or recalculate SysFont size
        cont_font = pygame.font.SysFont("arial", 28, bold=True)
        cont_surf = cont_font.render("CONTINUE", True, (20, 24, 35))
        screen.blit(cont_surf, cont_surf.get_rect(center=self.continue_button.center))

        # Help
        help_surf = self.text_font.render("← → Select Character    ENTER/Click Continue    ESC Back", True, (130, 130, 150))
        screen.blit(help_surf, help_surf.get_rect(center=(640, 660)))