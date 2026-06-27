import pygame
from src.engine.state import State
from src.ui.ui_elements import Button, Slider
from src.engine.settings import KEYS, KEY_NAMES
from src.utils.helpers import get_font, draw_rounded_panel, draw_gradient_rect

class SettingsState(State):
    def __init__(self, game):
        super().__init__(game)
        
        self.slider_music = None
        self.slider_sfx = None
        self.buttons = []
        
        # Keybinding remapping state
        self.remap_action = None # e.g. "up", "down", None
        
        self.font_title = get_font(28, is_bold=True)
        self.font_header = get_font(20, is_bold=True)
        self.font_label = get_font(14, is_bold=True)
        self.font_mapping = get_font(12, is_bold=True)
        
        self.init_settings_controls()

    def init_settings_controls(self):
        self.buttons = []
        
        # Audio Sliders
        # Music Volume Slider
        self.slider_music = Slider(180, 220, 300, 30, self.game.sounds.music_volume, self.set_music_volume)
        # SFX Volume Slider
        self.slider_sfx = Slider(180, 320, 300, 30, self.game.sounds.sfx_volume, self.set_sfx_volume)
        
        # Fullscreen Toggle Button
        cx = self.game.virtual_width // 2
        
        self.btn_fullscreen = Button(self.game, 180, 420, 300, 42, "Toggle Fullscreen", self.toggle_fullscreen, color=(40, 120, 100))
        self.buttons.append(self.btn_fullscreen)
        
        # Add remapping buttons dynamically
        # Actions: up, down, left, right, interact, inventory, run
        actions = ["up", "down", "left", "right", "interact", "inventory"]
        grid_x = 780
        grid_y = 180
        spacing_y = 52
        
        for idx, act in enumerate(actions):
            by = grid_y + idx * spacing_y
            
            # Remap callback triggers remapping state
            callback = lambda action=act: self.start_remap(action)
            btn = Button(self.game, grid_x, by, 180, 36, self.get_key_name(KEYS[act]), callback, font_size=12, color=(50, 45, 55))
            self.buttons.append(btn)

        # Back Button
        self.buttons.append(Button(self.game, cx - 110, 620, 220, 45, "Save & Return", self.go_back, color=(120, 50, 50)))

    def get_key_name(self, key_val):
        return KEY_NAMES.get(key_val, pygame.key.name(key_val).upper())

    def start_remap(self, action):
        self.remap_action = action
        # Play click
        self.game.sounds.play_sfx("click")

    def toggle_fullscreen(self):
        self.game.toggle_fullscreen()
        # Re-set buttons text if needed
        self.init_settings_controls()

    def set_music_volume(self, value):
        self.game.sounds.set_volumes(value, self.game.sounds.sfx_volume)

    def set_sfx_volume(self, value):
        self.game.sounds.set_volumes(self.game.sounds.music_volume, value)

    def go_back(self):
        # Save volumes back to database settings
        self.game.save_settings()
        self.game.change_state("menu")

    def enter(self):
        self.remap_action = None
        self.init_settings_controls()
        self.game.sounds.play_music("menu")

    def exit(self):
        pass

    def handle_event(self, event):
        mouse_pos = self.game.get_logical_mouse_pos()
        
        # If in key remapping mode, intercept next KEYDOWN
        if self.remap_action:
            if event.type == pygame.KEYDOWN:
                # Rebind action
                KEYS[self.remap_action] = event.key
                self.remap_action = None
                self.game.sounds.play_sfx("correct")
                # Rebuild buttons to refresh labels
                self.init_settings_controls()
            return

        # Slide controls
        self.slider_music.handle_event(event, mouse_pos)
        self.slider_sfx.handle_event(event, mouse_pos)
        
        # Buttons list
        for btn in self.buttons:
            if btn.handle_event(event, mouse_pos):
                break

    def update(self, dt):
        mouse_pos = self.game.get_logical_mouse_pos()
        
        # If waiting keypress, skip normal button checks
        if not self.remap_action:
            for btn in self.buttons:
                btn.update(dt, mouse_pos)
                
            # If waiting keypress, update slider highlights but no dragging
            # Check remapping button labels update
            # Refresh bindings highlight if hovered
            pass

    def draw(self, surface):
        # Backdrop
        draw_gradient_rect(surface, (20, 16, 28), (10, 20, 35), (0, 0, self.game.virtual_width, self.game.virtual_height))
        
        # Title
        title_surf = self.font_title.render("SYSTEM PREFERENCES", True, (255, 235, 120))
        surface.blit(title_surf, ((self.game.virtual_width - title_surf.get_width())//2, 35))
        
        # Panels
        # Left Panel (Audio & Screen)
        draw_rounded_panel(surface, (80, 110, 480, 480), (25, 25, 30), (165, 120, 25), border_width=2)
        # Right Panel (Controls Mapper)
        draw_rounded_panel(surface, (700, 110, 480, 480), (20, 20, 24), (165, 120, 25), border_width=2)

        # Draw left panel info
        audio_head = self.font_header.render("AUDIO & GRAPHICS", True, (230, 185, 55))
        surface.blit(audio_head, (80 + (480 - audio_head.get_width())//2, 130))
        
        # Volume sliders info labels
        music_lbl = self.font_label.render(f"Music Volume: {int(self.game.sounds.music_volume * 100)}%", True, (200, 200, 210))
        surface.blit(music_lbl, (120, 195))
        self.slider_music.draw(surface)
        
        sfx_lbl = self.font_label.render(f"Sound FX Volume: {int(self.game.sounds.sfx_volume * 100)}%", True, (200, 200, 210))
        surface.blit(sfx_lbl, (120, 295))
        self.slider_sfx.draw(surface)
        
        screen_lbl = self.font_label.render("Display Mode Options:", True, (200, 200, 210))
        surface.blit(screen_lbl, (120, 395))
        
        # Display resolution details below
        res_info = f"Current Window: {self.game.screen.get_width()}x{self.game.screen.get_height()}"
        if self.game.fullscreen:
            res_info += " (Fullscreen)"
        res_surf = get_font(12).render(res_info, True, (130, 130, 140))
        surface.blit(res_surf, (120, 475))

        # Draw right panel info (Keybindings remapping)
        ctrl_head = self.font_header.render("CONTROLS REMAPPING", True, (230, 185, 55))
        surface.blit(ctrl_head, (700 + (480 - ctrl_head.get_width())//2, 130))
        
        # Render command labels
        actions_list = [
            ("Walk Up / Climb:", "up"),
            ("Walk Down / Decend:", "down"),
            ("Walk Left Step:", "left"),
            ("Walk Right Step:", "right"),
            ("Interact / Talk / Open:", "interact"),
            ("Inventory View:", "inventory")
        ]
        
        for idx, (label, act) in enumerate(actions_list):
            ay = 180 + idx * 52
            
            lbl_surf = self.font_label.render(label, True, (200, 200, 210))
            surface.blit(lbl_surf, (730, ay + 8))
            
            # If currently mapping this key, show indicator inside the button area
            if self.remap_action == act:
                btn_rect = pygame.Rect(780, ay, 180, 36)
                pygame.draw.rect(surface, (230, 185, 55), btn_rect, border_radius=4)
                
                txt_wait = self.font_mapping.render("<Press Any Key>", True, (25, 25, 30))
                surface.blit(txt_wait, (btn_rect.x + (180 - txt_wait.get_width())//2, btn_rect.y + 10))

        # Draw standard buttons list (excluding buttons over-written by remap indicator)
        for btn in self.buttons:
            # Match action buttons
            btn_act = next((act for act in ["up", "down", "left", "right", "interact", "inventory"] if KEYS[act] == [k for k, v in KEYS.items() if self.get_key_name(v) == btn.text][0] if [k for k, v in KEYS.items() if self.get_key_name(v) == btn.text]), None)
            
            # Draw standard if not currently actively remapping it
            if btn_act and self.remap_action == btn_act:
                continue
                
            btn.draw(surface)
