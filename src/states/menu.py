import pygame
import sys
from src.engine.state import State
from src.ui.ui_elements import Button
from src.utils.helpers import get_font, draw_rounded_panel, draw_gradient_rect
from src.ui.particle import ParticleSystem, Particle
import random

class MenuState(State):
    def __init__(self, game):
        super().__init__(game)
        
        self.particles = ParticleSystem()
        self.buttons = []
        
        # Overlay panels toggle
        self.show_credits = False
        self.font_logo = get_font(48, is_bold=True)
        self.font_credits = get_font(16)
        
        self.init_menu_buttons()

    def init_menu_buttons(self):
        self.buttons = []
        
        # Center coordinates
        cx = self.game.virtual_width // 2 - 110 # Button width is 220
        start_y = 200
        spacing = 56
        
        # Play (starts new profile customization)
        self.buttons.append(Button(self.game, cx, start_y, 220, 42, "New Game", self.start_new_game))
        
        # Continue (enabled only if save is found)
        btn_continue = Button(self.game, cx, start_y + spacing, 220, 42, "Continue", self.load_saved_game)
        btn_continue.set_enabled(self.game.db.has_save())
        self.buttons.append(btn_continue)
        
        # Profile Customizer
        self.buttons.append(Button(self.game, cx, start_y + spacing * 2, 220, 42, "Character Profile", self.open_profile))
        
        # Achievements
        self.buttons.append(Button(self.game, cx, start_y + spacing * 3, 220, 42, "Achievements", self.open_achievements))
        
        # Settings
        self.buttons.append(Button(self.game, cx, start_y + spacing * 4, 220, 42, "Settings", self.open_settings))
        
        # Credits
        self.buttons.append(Button(self.game, cx, start_y + spacing * 5, 220, 42, "Credits", self.toggle_credits))
        
        # Exit
        self.buttons.append(Button(self.game, cx, start_y + spacing * 6, 220, 42, "Exit Game", self.exit_game))

    def enter(self):
        # Refresh "Continue" button status
        self.init_menu_buttons()
        self.show_credits = False
        self.game.sounds.play_music("menu")

    def exit(self):
        pass

    def start_new_game(self):
        # Reset DB and open Profile customizer
        self.game.db.reset_save()
        self.game.change_state("profile")

    def load_saved_game(self):
        # Reload player profile and launch explore state
        # Initial exploration coordinates are handled inside explore
        self.game.change_state("explore")

    def open_profile(self):
        self.game.change_state("profile")

    def open_achievements(self):
        self.game.change_state("achievements")

    def open_settings(self):
        self.game.change_state("settings")

    def toggle_credits(self):
        self.show_credits = not self.show_credits

    def exit_game(self):
        self.game.running = False

    def handle_event(self, event):
        mouse_pos = self.game.get_logical_mouse_pos()
        
        if self.show_credits:
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                self.show_credits = False
                self.game.sounds.play_sfx("click")
            return
            
        for btn in self.buttons:
            if btn.handle_event(event, mouse_pos):
                break

    def update(self, dt):
        mouse_pos = self.game.get_logical_mouse_pos()
        
        # Floating background magical sparks
        if random.random() < 0.1:
            self.particles.particles.append(Particle(
                random.randint(0, self.game.virtual_width),
                self.game.virtual_height + 10,
                random.uniform(-15, 15),
                random.uniform(-50, -20),
                (140, 180, 255),
                random.uniform(1.5, 3.5),
                random.uniform(2.0, 4.0)
            ))
            
        self.particles.update(dt)
        
        if not self.show_credits:
            for btn in self.buttons:
                btn.update(dt, mouse_pos)

    def draw(self, surface):
        # Rich gradient backdrop: Dark Purple to deep blue
        draw_gradient_rect(surface, (15, 10, 30), (10, 20, 45), (0, 0, self.game.virtual_width, self.game.virtual_height))
        
        # Draw sparks
        self.particles.draw(surface)
        
        # Draw game logo title on menu
        logo_text = "LearnScape"
        logo_font = get_font(56, is_bold=True)
        logo_surf = logo_font.render(logo_text, True, (255, 255, 255))
        lx = (self.game.virtual_width - logo_surf.get_width()) // 2
        ly = 50
        
        # Logo glow background shadow
        from src.utils.helpers import draw_glowing_text
        draw_glowing_text(surface, logo_text, logo_font, (255, 255, 255), (lx, ly), (230, 180, 40, 120), 2)
        
        # Draw version index
        v_surf = get_font(12).render("v1.0.0", True, (80, 75, 95))
        surface.blit(v_surf, (15, self.game.virtual_height - 30))
        
        # Draw standard buttons list
        if not self.show_credits:
            # Draw panel background to group buttons
            px = self.game.virtual_width // 2 - 140
            draw_rounded_panel(surface, (px, 150, 280, 440), (20, 20, 25), (165, 120, 25), border_width=2, border_radius=10, bg_alpha=180)
            for btn in self.buttons:
                btn.draw(surface)
        else:
            # Renders credits overlay dialogue
            cx = (self.game.virtual_width - 450) // 2
            cy = (self.game.virtual_height - 320) // 2
            draw_rounded_panel(surface, (cx, cy, 450, 320), (24, 20, 25), (230, 180, 40), border_width=3, border_radius=12, bg_alpha=240)
            
            # Title
            title_surf = get_font(24, is_bold=True).render("CREDITS", True, (230, 180, 40))
            surface.blit(title_surf, (cx + (450 - title_surf.get_width())//2, cy + 20))
            
            # Credits roll text
            from src.utils.helpers import draw_text_wrapped
            credits_text = (
                "Developed by: DeepMind Agent Pair Programmer\n\n"
                "Sound & Music Synthesizers: Pygame Synth Chiptunes\n"
                "Visual Art Sprites: Dynamic Procedural Drawer\n"
                "Educational Questions: JSON Question Bank\n"
                "Progress Persistency: SQLite Database Manager\n\n"
                "Special thanks to the Google team for advanced agency!\n\n"
                "Click anywhere to return..."
            )
            draw_text_wrapped(surface, credits_text, self.font_credits, (235, 230, 245), (cx + 25, cy + 60, 400, 240))
