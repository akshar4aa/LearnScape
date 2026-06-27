import pygame
from src.engine.state import State
from src.ui.ui_elements import Button
from src.utils.helpers import get_font, draw_rounded_panel, draw_gradient_rect

class GameOverState(State):
    def __init__(self, game):
        super().__init__(game)
        
        self.font_title = get_font(36, is_bold=True)
        self.font_desc = get_font(14)
        
        # Action Buttons
        cx = self.game.virtual_width // 2
        self.buttons = [
            Button(self.game, cx - 220, 480, 200, 45, "Respawn & Retry", self.retry, color=(50, 120, 80)),
            Button(self.game, cx + 20, 480, 200, 45, "Quit to Menu", self.quit_to_menu, color=(120, 50, 50))
        ]

    def retry(self):
        # Revive player with full health and reset map explore state
        player = self.game.player
        player.hp = player.max_hp
        player.mana = player.max_mana
        player.save_to_db()
        
        # Reload current kingdom explore state
        self.game.change_state("explore")

    def quit_to_menu(self):
        self.game.change_state("menu")

    def enter(self):
        # Play wrong SFX as game over highlight
        self.game.sounds.play_sfx("wrong")

    def exit(self):
        pass

    def handle_event(self, event):
        mouse_pos = self.game.get_logical_mouse_pos()
        for btn in self.buttons:
            btn.handle_event(event, mouse_pos)

    def update(self, dt):
        mouse_pos = self.game.get_logical_mouse_pos()
        for btn in self.buttons:
            btn.update(dt, mouse_pos)

    def draw(self, surface):
        # Grey/Dark red gradient backdrop
        draw_gradient_rect(surface, (30, 10, 10), (15, 15, 20), (0, 0, self.game.virtual_width, self.game.virtual_height))
        
        # Game over text
        from src.utils.helpers import draw_glowing_text
        tx = self.game.virtual_width // 2
        title_surf = self.font_title.render("YOU HAVE FALLEN!", True, (240, 70, 70))
        
        draw_glowing_text(
            surface, "YOU HAVE FALLEN!", self.font_title, 
            (245, 80, 80), (tx - title_surf.get_width()//2, 160), 
            (0, 0, 0, 120), 2
        )
        
        # Details box
        px = self.game.virtual_width // 2 - 200
        py = 240
        draw_rounded_panel(surface, (px, py, 400, 180), (22, 20, 20), (120, 50, 50), border_radius=8)
        
        # Review hint tips
        tip_text = (
            "Do not lose heart, scholar!\n\n"
            "Learning is a journey of trial and error.\n"
            "1. Visit the equipment merchant to purchase better weapons.\n"
            "2. Stock up on Health Potions and Knowledge Scrolls.\n"
            "3. Study the NPC teacher dialogs for concept hints!"
        )
        from src.utils.helpers import draw_text_wrapped
        draw_text_wrapped(surface, tip_text, self.font_desc, (200, 190, 190), (px + 20, py + 20, 360, 140))

        # Render retry actions buttons
        for btn in self.buttons:
            btn.draw(surface)
