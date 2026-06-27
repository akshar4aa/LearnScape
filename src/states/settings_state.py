import pygame
from src.states.state import State
from src.ui.background import Background
from src.ui.button import Button

class SettingsState(State):
    def __init__(self, game):
        super().__init__(game)
        width = self.game.screen.get_width()
        height = self.game.screen.get_height()
        self.background = Background(width, height)

        self.title_font = pygame.font.SysFont("arial", 56, bold=True)
        self.heading_font = pygame.font.SysFont("arial", 28, bold=True)
        self.text_font = pygame.font.SysFont("arial", 24)

        # Selected control row: 0 = Music Volume, 1 = SFX Volume, 2 = Back Button
        self.selected_row = 0

        # Sliders layout
        self.music_slider = pygame.Rect(440, 260, 400, 16)
        self.sfx_slider = pygame.Rect(440, 380, 400, 16)

        # Back Button
        self.back_button = Button(width // 2 - 150, 480, 300, 55, "Save & Exit", font_size=24)

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        music_vol = self.game.audio.music_volume
        sfx_vol = self.game.audio.sfx_volume

        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
                return

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Handle slider clicks
                if self.music_slider.collidepoint(mouse_pos):
                    self.selected_row = 0
                    self.adjust_slider_mouse(mouse_pos[0], is_music=True)
                elif self.sfx_slider.collidepoint(mouse_pos):
                    self.selected_row = 1
                    self.adjust_slider_mouse(mouse_pos[0], is_music=False)
                elif self.back_button.handle_event(event, mouse_pos):
                    self.exit_settings()
                    return

            elif event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:
                # Dragging sliders
                if self.music_slider.collidepoint(mouse_pos) or self.selected_row == 0:
                    if self.music_slider.x <= mouse_pos[0] <= self.music_slider.right:
                        self.adjust_slider_mouse(mouse_pos[0], is_music=True)
                if self.sfx_slider.collidepoint(mouse_pos) or self.selected_row == 1:
                    if self.sfx_slider.x <= mouse_pos[0] <= self.sfx_slider.right:
                        self.adjust_slider_mouse(mouse_pos[0], is_music=False)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit_settings()
                    return

                # Keyboard navigation
                elif event.key == pygame.K_UP:
                    self.selected_row = (self.selected_row - 1) % 3
                    self.update_selection_highlight()
                elif event.key == pygame.K_DOWN:
                    self.selected_row = (self.selected_row + 1) % 3
                    self.update_selection_highlight()

                # Adjust slider value with arrow keys
                elif event.key == pygame.K_LEFT:
                    if self.selected_row == 0:
                        self.game.audio.set_music_volume(music_vol - 0.05)
                    elif self.selected_row == 1:
                        self.game.audio.set_sfx_volume(sfx_vol - 0.05)
                elif event.key == pygame.K_RIGHT:
                    if self.selected_row == 0:
                        self.game.audio.set_music_volume(music_vol + 0.05)
                    elif self.selected_row == 1:
                        self.game.audio.set_sfx_volume(sfx_vol + 0.05)
                        
                elif event.key == pygame.K_RETURN and self.selected_row == 2:
                    self.exit_settings()
                    return

    def adjust_slider_mouse(self, mouse_x, is_music):
        slider = self.music_slider if is_music else self.sfx_slider
        pct = (mouse_x - slider.x) / slider.width
        pct = max(0.0, min(1.0, pct))
        if is_music:
            self.game.audio.set_music_volume(pct)
        else:
            self.game.audio.set_sfx_volume(pct)

    def update_selection_highlight(self):
        self.back_button.selected = (self.selected_row == 2)
        if hasattr(self.game, 'audio'):
            self.game.audio.play_sfx("assets/audio/planet_select.wav")

    def exit_settings(self):
        if hasattr(self.game, 'audio'):
            self.game.audio.play_sfx("assets/audio/click.wav")
        from src.states.menu_state import MenuState
        self.game.change_state(MenuState(self.game))

    def update(self, dt):
        self.background.update(dt)
        self.back_button.update(dt)
        self.back_button.selected = (self.selected_row == 2)

    def draw_slider(self, screen, rect, value, is_selected):
        # Draw track
        pygame.draw.rect(screen, (35, 40, 60), rect, border_radius=8)
        # Draw fill progress
        fill_width = int(rect.width * value)
        if fill_width > 0:
            fill_rect = pygame.Rect(rect.x, rect.y, fill_width, rect.height)
            pygame.draw.rect(screen, (100, 180, 255) if is_selected else (60, 100, 180), fill_rect, border_radius=8)
            
        # Draw border
        border_color = (255, 220, 80) if is_selected else (130, 130, 150)
        pygame.draw.rect(screen, border_color, rect, 2, border_radius=8)
        
        # Draw knob
        knob_x = rect.x + fill_width
        knob_y = rect.centery
        pygame.draw.circle(screen, (255, 220, 80) if is_selected else (255, 255, 255), (knob_x, knob_y), 12)
        pygame.draw.circle(screen, (20, 24, 35), (knob_x, knob_y), 12, 2)

    def draw(self, screen):
        self.background.draw(screen)

        # Title
        title_surf = self.title_font.render("Settings", True, (255, 220, 80))
        screen.blit(title_surf, title_surf.get_rect(center=(640, 70)))

        # Panel Backing
        panel = pygame.Rect(280, 150, 720, 420)
        pygame.draw.rect(screen, (25, 30, 48), panel, border_radius=15)
        pygame.draw.rect(screen, (255, 220, 80), panel, 2, border_radius=15)

        # 1. Music Volume Control
        music_title_color = (255, 220, 80) if self.selected_row == 0 else (255, 255, 255)
        music_title = self.heading_font.render("Music Volume", True, music_title_color)
        screen.blit(music_title, (340, 210))
        
        self.draw_slider(screen, self.music_slider, self.game.audio.music_volume, self.selected_row == 0)
        
        music_pct = self.text_font.render(f"{int(self.game.audio.music_volume * 100)}%", True, (200, 200, 220))
        screen.blit(music_pct, (860, 253))

        # 2. SFX Volume Control
        sfx_title_color = (255, 220, 80) if self.selected_row == 1 else (255, 255, 255)
        sfx_title = self.heading_font.render("Sound Effects Volume", True, sfx_title_color)
        screen.blit(sfx_title, (340, 330))

        self.draw_slider(screen, self.sfx_slider, self.game.audio.sfx_volume, self.selected_row == 1)

        sfx_pct = self.text_font.render(f"{int(self.game.audio.sfx_volume * 100)}%", True, (200, 200, 220))
        screen.blit(sfx_pct, (860, 373))

        # 3. Save & Exit Button
        self.back_button.draw(screen)

        # Help footer
        help_str = "↑ ↓ Select Control    ← → Adjust Slider Value    ENTER Click button"
        help_surf = self.text_font.render(help_str, True, (130, 130, 150))
        screen.blit(help_surf, help_surf.get_rect(center=(640, 675)))
