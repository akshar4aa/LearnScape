import pygame
from src.engine.state import State
from src.ui.ui_elements import Button
from src.utils.helpers import get_font, draw_rounded_panel

class PauseState(State):
    def __init__(self, game):
        super().__init__(game)
        
        self.buttons = []
        self.font_title = get_font(24, is_bold=True)
        
        self.init_pause_menu()

    def init_pause_menu(self):
        self.buttons = []
        
        # Centered coordinates
        cx = self.game.virtual_width // 2 - 110 # Button width is 220
        start_y = 260
        spacing = 54
        
        # Resume
        self.buttons.append(Button(self.game, cx, start_y, 220, 42, "Resume Game", self.resume_game, color=(40, 120, 70)))
        
        # Settings
        self.buttons.append(Button(self.game, cx, start_y + spacing, 220, 42, "Settings Preferences", self.open_settings))
        
        # Save & Return
        self.buttons.append(Button(self.game, cx, start_y + spacing * 2, 220, 42, "Save & Quit", self.save_and_quit, color=(140, 40, 40)))

    def resume_game(self):
        # Pop pause state to return to explore state
        self.game.pop_state()

    def open_settings(self):
        # Change state to settings menu directly
        self.game.change_state("settings")

    def save_and_quit(self):
        # Save player progression and inventory
        self.game.player.save_to_db()
        self.game.change_state("menu")

    def enter(self):
        self.init_pause_menu()

    def exit(self):
        pass

    def handle_event(self, event):
        mouse_pos = self.game.get_logical_mouse_pos()
        
        # Press ESC to pop/resume
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.resume_game()
            return
            
        for btn in self.buttons:
            if btn.handle_event(event, mouse_pos):
                break

    def update(self, dt):
        mouse_pos = self.game.get_logical_mouse_pos()
        for btn in self.buttons:
            btn.update(dt, mouse_pos)

    def draw(self, surface):
        # Dim backdrop: semi-transparent black rectangle
        # Drawing this on the logical surface dims whatever state was underneath
        dim_surf = pygame.Surface((self.game.virtual_width, self.game.virtual_height), pygame.SRCALPHA)
        dim_surf.fill((0, 0, 0, 150))
        surface.blit(dim_surf, (0, 0))
        
        # Centered container panel
        px = self.game.virtual_width // 2 - 140
        py = 180
        draw_rounded_panel(surface, (px, py, 280, 320), (20, 20, 24), (165, 120, 25), border_width=2, border_radius=10)
        
        # Pause Title
        title_surf = self.font_title.render("GAME PAUSED", True, (230, 185, 55))
        surface.blit(title_surf, (px + (280 - title_surf.get_width())//2, py + 25))
        
        # Render action buttons
        for btn in self.buttons:
            btn.draw(surface)
