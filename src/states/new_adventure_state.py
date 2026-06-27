import pygame
from src.states.state import State
from src.ui.background import Background
from src.states.character_select_state import CharacterSelectState

class NewAdventureState(State):
    def __init__(self, game):
        super().__init__(game)
        width = self.game.screen.get_width()
        height = self.game.screen.get_height()
        self.background = Background(width, height)

        # Fonts
        self.title_font = pygame.font.SysFont("arial", 56, bold=True)
        self.heading_font = pygame.font.SysFont("arial", 28, bold=True)
        self.text_font = pygame.font.SysFont("arial", 24)

        # Hero Name
        self.hero_name = ""
        self.name_active = True
        self.max_length = 12

        # Difficulty
        self.difficulties = ["Explorer", "Scholar", "Legend"]
        self.selected_difficulty = 0 # 0=Explorer, 1=Scholar, 2=Legend
        
        # Grid Coordinates (fitting within 720 height)
        self.panel_rect = pygame.Rect(280, 150, 720, 480)
        self.name_box = pygame.Rect(340, 220, 600, 50)
        self.begin_button = pygame.Rect(470, 545, 340, 55)
        
        self.difficulty_rects = []
        diff_start_y = 330
        for i in range(3):
            self.difficulty_rects.append(pygame.Rect(340, diff_start_y + i * 60, 600, 48))

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
                return

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Name box focus
                if self.name_box.collidepoint(mouse_pos):
                    self.name_active = True
                else:
                    self.name_active = False

                # Difficulty click selection
                for i, rect in enumerate(self.difficulty_rects):
                    if rect.collidepoint(mouse_pos):
                        self.selected_difficulty = i
                        if hasattr(self.game, 'audio'):
                            self.game.audio.play_sfx("assets/audio/click.wav")

                # Begin button click
                if self.begin_button.collidepoint(mouse_pos):
                    self.begin_journey()
                    return

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from src.states.menu_state import MenuState
                    self.game.change_state(MenuState(self.game))
                    return

                if self.name_active:
                    if event.key == pygame.K_BACKSPACE:
                        self.hero_name = self.hero_name[:-1]
                    elif event.key == pygame.K_RETURN:
                        self.name_active = False
                    elif event.key == pygame.K_TAB:
                        self.name_active = False
                    else:
                        if event.unicode.isprintable() and len(self.hero_name) < self.max_length:
                            self.hero_name += event.unicode
                else:
                    # Key inputs when name is not active
                    if event.key == pygame.K_UP:
                        self.selected_difficulty = (self.selected_difficulty - 1) % 3
                    elif event.key == pygame.K_DOWN:
                        self.selected_difficulty = (self.selected_difficulty + 1) % 3
                    elif event.key == pygame.K_TAB:
                        self.name_active = True
                    elif event.key == pygame.K_RETURN:
                        self.begin_journey()
                        return

    def begin_journey(self):
        # Default name if left empty
        name = self.hero_name.strip()
        if not name:
            name = "Hero"
        
        # Save temp info in the game class
        self.game.hero_name = name
        self.game.difficulty = self.difficulties[self.selected_difficulty]
        
        # Audio
        if hasattr(self.game, 'audio'):
            self.game.audio.play_sfx("assets/audio/click.wav")
            
        self.game.change_state(CharacterSelectState(self.game))

    def update(self, dt):
        self.background.update(dt)

    def draw(self, screen):
        self.background.draw(screen)

        # Title
        title_surf = self.title_font.render("New Adventure", True, (255, 220, 80))
        screen.blit(title_surf, title_surf.get_rect(center=(640, 65)))

        subtitle_surf = self.text_font.render("Configure your explorer metrics.", True, (220, 220, 220))
        screen.blit(subtitle_surf, subtitle_surf.get_rect(center=(640, 115)))

        # Main Panel
        pygame.draw.rect(screen, (25, 30, 48), self.panel_rect, border_radius=15)
        pygame.draw.rect(screen, (255, 220, 80), self.panel_rect, 2, border_radius=15)

        # Name Title
        name_title = self.heading_font.render("Enter Hero Name", True, (255, 220, 80))
        screen.blit(name_title, (340, 180))

        # Name Box
        box_border = (255, 220, 80) if self.name_active else (130, 130, 150)
        pygame.draw.rect(screen, (40, 45, 65), self.name_box, border_radius=10)
        pygame.draw.rect(screen, box_border, self.name_box, 2, border_radius=10)

        # Render Name Text inside Box
        display_name = self.hero_name
        if not display_name and not self.name_active:
            display_name = "Enter Hero Name..."
            color = (130, 130, 150)
        else:
            color = (255, 255, 255)
            if self.name_active and (pygame.time.get_ticks() // 500) % 2 == 0:
                display_name += "|"

        name_surf = self.text_font.render(display_name, True, color)
        screen.blit(name_surf, (360, 230))

        # Difficulty Title
        diff_title = self.heading_font.render("Select Difficulty", True, (255, 220, 80))
        screen.blit(diff_title, (340, 290))

        # Difficulty Buttons
        for i, rect in enumerate(self.difficulty_rects):
            is_selected = (i == self.selected_difficulty)
            bg = (255, 220, 80) if is_selected else (40, 45, 65)
            border = (255, 255, 200) if is_selected else (255, 220, 80)
            txt_color = (20, 24, 35) if is_selected else (255, 255, 255)

            # Extra glow for selected
            if is_selected:
                glow = pygame.Surface((rect.width + 16, rect.height + 16), pygame.SRCALPHA)
                pygame.draw.rect(glow, (255, 220, 80, 40), glow.get_rect(), border_radius=10)
                screen.blit(glow, (rect.x - 8, rect.y - 8))

            pygame.draw.rect(screen, bg, rect, border_radius=10)
            pygame.draw.rect(screen, border, rect, 2, border_radius=10)

            diff_surf = self.text_font.render(self.difficulties[i], True, txt_color)
            screen.blit(diff_surf, diff_surf.get_rect(center=rect.center))

        # Begin Button
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.begin_button.collidepoint(mouse_pos)
        btn_bg = (255, 235, 120) if hovered else (255, 220, 80)
        
        if hovered:
            btn_glow = pygame.Surface((self.begin_button.width + 20, self.begin_button.height + 20), pygame.SRCALPHA)
            pygame.draw.rect(btn_glow, (255, 220, 80, 50), btn_glow.get_rect(), border_radius=12)
            screen.blit(btn_glow, (self.begin_button.x - 10, self.begin_button.y - 10))

        pygame.draw.rect(screen, btn_bg, self.begin_button, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), self.begin_button, 2, border_radius=12)

        begin_surf = self.heading_font.render("BEGIN JOURNEY", True, (20, 24, 35))
        screen.blit(begin_surf, begin_surf.get_rect(center=self.begin_button.center))

        # Help bar text
        if self.name_active:
            help_str = "Type Name • Press ENTER to confirm name"
        else:
            help_str = "↑ ↓ Change Difficulty • TAB to edit Name • ENTER to Begin"
            
        help_surf = self.text_font.render(help_str, True, (130, 130, 150))
        screen.blit(help_surf, help_surf.get_rect(center=(640, 675)))