import pygame
from src.engine.state import State
from src.ui.ui_elements import Button, TextBox
from src.utils.helpers import get_font, draw_rounded_panel, draw_gradient_rect

class ProfileState(State):
    def __init__(self, game):
        super().__init__(game)
        
        # Temp customize values (loaded from database first if present)
        self.char_name = "Hero"
        self.avatar_type = "adventurer"
        self.hair_color = (200, 50, 50)
        self.outfit_color = (50, 80, 200)
        
        # Color palettes options
        self.hair_palettes = [
            ("Red", (200, 50, 50)),
            ("Blue", (50, 100, 210)),
            ("Green", (50, 150, 80)),
            ("Yellow", (220, 175, 45)),
            ("Black", (30, 30, 35)),
            ("White", (230, 230, 235)),
            ("Purple", (140, 50, 180)),
            ("Brown", (110, 70, 40))
        ]
        
        self.outfit_palettes = [
            ("Blue", (50, 80, 200)),
            ("Red", (200, 50, 50)),
            ("Teal", (0, 150, 160)),
            ("Green", (40, 140, 70)),
            ("Orange", (220, 90, 20)),
            ("Purple", (130, 30, 180)),
            ("Golden", (210, 160, 40)),
            ("Black", (40, 40, 45))
        ]
        
        # Animation
        self.anim_tick = 0.0
        self.font_header = get_font(24, is_bold=True)
        self.font_label = get_font(16, is_bold=True)
        
        # Buttons and controls
        self.txt_name = None
        self.buttons = []
        self.init_controls()

    def init_controls(self):
        self.buttons = []
        
        # TextBox for player name
        self.txt_name = TextBox(120, 200, 240, 45, self.char_name, max_chars=12)
        
        # Avatar selectors
        avatars = ["adventurer", "scholar", "wizard", "rogue"]
        for idx, av in enumerate(avatars):
            btn_x = 120 + (idx % 2) * 125
            btn_y = 310 + (idx // 2) * 50
            
            # Select avatar callback
            callback = lambda choice=av: self.set_avatar(choice)
            self.buttons.append(Button(self.game, btn_x, btn_y, 115, 38, av.capitalize(), callback, font_size=12))

        # Color Swatches for hair and outfit
        # Hair colors (Column on right: x=860)
        for idx, (name, color) in enumerate(self.hair_palettes):
            bx = 840 + (idx % 2) * 110
            by = 200 + (idx // 2) * 50
            cb = lambda c=color: self.set_hair_color(c)
            self.buttons.append(Button(self.game, bx, by, 100, 38, name, cb, color=color, font_size=12))
            
        # Outfit colors
        for idx, (name, color) in enumerate(self.outfit_palettes):
            bx = 840 + (idx % 2) * 110
            by = 420 + (idx // 2) * 50
            cb = lambda c=color: self.set_outfit_color(c)
            self.buttons.append(Button(self.game, bx, by, 100, 38, name, cb, color=color, font_size=12))

        # Bottom navigation
        cx = self.game.virtual_width // 2
        self.buttons.append(Button(self.game, cx - 220, 620, 180, 45, "Back", self.go_back, color=(120, 50, 50)))
        self.buttons.append(Button(self.game, cx + 40, 620, 180, 45, "Save & Play", self.save_profile, color=(50, 150, 80)))

    def enter(self):
        # Retrieve active player settings if they exist in DB
        p_data = self.game.db.load_profile()
        if p_data:
            self.char_name = p_data["name"]
            self.avatar_type = p_data["avatar"]
            self.hair_color = p_data["hair_color"]
            self.outfit_color = p_data["outfit_color"]
            
        # Re-initialize text box
        self.txt_name.text = self.char_name
        self.game.sounds.play_music("menu")

    def exit(self):
        pass

    def set_avatar(self, name):
        self.avatar_type = name

    def set_hair_color(self, color):
        self.hair_color = color

    def set_outfit_color(self, color):
        self.outfit_color = color

    def go_back(self):
        self.game.change_state("menu")

    def save_profile(self):
        # Update name
        name_val = self.txt_name.text.strip()
        if name_val == "":
            name_val = "Hero"
            
        # Write to SQLite
        self.game.db.save_profile({
            "name": name_val,
            "avatar": self.avatar_type,
            "level": 1,
            "xp": 0,
            "coins": 100,
            "hp": 100,
            "max_hp": 100,
            "mana": 50,
            "max_mana": 50,
            "hair_color": self.hair_color,
            "outfit_color": self.outfit_color
        })
        
        # Instantiate character updates in explore
        # Load profile details to player entity
        from src.entities.player import Player
        self.game.player = Player(self.game)
        
        # Advance to explore maps state
        self.game.change_state("explore")

    def handle_event(self, event):
        mouse_pos = self.game.get_logical_mouse_pos()
        
        # TextBox event
        self.txt_name.handle_event(event, mouse_pos)
        
        for btn in self.buttons:
            if btn.handle_event(event, mouse_pos):
                break

    def update(self, dt):
        mouse_pos = self.game.get_logical_mouse_pos()
        
        self.anim_tick += dt * 8.0 # Walking cycle animation
        self.txt_name.update(dt)
        
        for btn in self.buttons:
            btn.update(dt, mouse_pos)

    def draw(self, surface):
        # Background gradient
        draw_gradient_rect(surface, (20, 15, 35), (10, 20, 45), (0, 0, self.game.virtual_width, self.game.virtual_height))
        
        # Renders layout panels
        # Left Panel (Name & Class)
        draw_rounded_panel(surface, (80, 100, 320, 480), (25, 25, 30), (165, 120, 25), border_width=2)
        
        # Center Panel (Preview)
        draw_rounded_panel(surface, (440, 100, 320, 480), (15, 15, 20), (165, 120, 25), border_width=2)
        
        # Right Panel (Colors customization)
        draw_rounded_panel(surface, (800, 100, 320, 480), (25, 25, 30), (165, 120, 25), border_width=2)

        # Draw left panel texts
        head_name = self.font_header.render("CHARACTER SETUP", True, (230, 185, 55))
        surface.blit(head_name, (80 + (320 - head_name.get_width())//2, 120))
        
        name_lbl = self.font_label.render("Enter Name:", True, (200, 200, 210))
        surface.blit(name_lbl, (100, 175))
        self.txt_name.draw(surface)
        
        avatar_lbl = self.font_label.render("Choose Avatar Class:", True, (200, 200, 210))
        surface.blit(avatar_lbl, (100, 275))

        # Draw center panel: Preview Animation (128x128 Double sized)
        preview_lbl = self.font_label.render(f"PREVIEW: {self.avatar_type.upper()}", True, (230, 185, 55))
        surface.blit(preview_lbl, (440 + (320 - preview_lbl.get_width())//2, 120))
        
        # Get customized frame
        loader = self.game.states["loading"].loader
        cycle = int(self.anim_tick) % 4
        frame_type = "idle"
        if cycle == 0: frame_type = "walk_1"
        elif cycle == 2: frame_type = "walk_2"
        
        sprite = loader.get_image(
            f"preview_{frame_type}", 
            loader.create_character_frame,
            frame_type, self.hair_color, self.outfit_color, int(self.anim_tick)
        )
        # Double the size for preview (64x64 scaled to 128x128)
        sprite_large = pygame.transform.scale(sprite, (128, 128))
        
        px = 440 + (320 - 128)//2
        py = 240
        surface.blit(sprite_large, (px, py))

        # Draw right panel color labels
        colors_lbl = self.font_header.render("STYLES & COLORS", True, (230, 185, 55))
        surface.blit(colors_lbl, (800 + (320 - colors_lbl.get_width())//2, 120))
        
        hair_lbl = self.font_label.render("Hair Color:", True, (200, 200, 210))
        surface.blit(hair_lbl, (820, 175))
        
        outfit_lbl = self.font_label.render("Outfit Color:", True, (200, 200, 210))
        surface.blit(outfit_lbl, (820, 395))

        # Render all buttons
        for btn in self.buttons:
            btn.draw(surface)
        
        # Highlight active avatar choice button outline in panel
        for btn in self.buttons:
            if btn.text.lower() == self.avatar_type:
                pygame.draw.rect(surface, (255, 235, 120), btn.rect, 2, border_radius=8)
