import pygame
from src.engine.state import State
from src.ui.ui_elements import Button
from src.utils.helpers import get_font, draw_rounded_panel, draw_gradient_rect

class VictoryState(State):
    def __init__(self, game):
        super().__init__(game)
        
        self.xp_earned = 0
        self.coins_earned = 0
        self.loot_item_id = None
        self.leveled_up = False
        
        self.font_title = get_font(32, is_bold=True)
        self.font_header = get_font(20, is_bold=True)
        self.font_details = get_font(16, is_bold=True)
        self.font_ability = get_font(12, is_bold=True)
        
        # Navigation
        self.btn_continue = Button(self.game, self.game.virtual_width//2 - 100, 580, 200, 45, "Continue", self.go_next, color=(50, 140, 80))

    def set_rewards(self, xp, coins, item_id=None):
        self.xp_earned = xp
        self.coins_earned = coins
        self.loot_item_id = item_id
        
        # Process progression rewards on Player entity
        player = self.game.player
        player.coins += coins
        
        # Check if XP triggered a level-up
        self.leveled_up = player.add_xp(xp)
        
        # Deliver item if any
        if item_id:
            from src.items.item import get_item_details
            item_details = get_item_details(item_id)
            existing = next((i for i in player.inventory if i["id"] == item_id), None)
            if existing:
                existing["quantity"] += 1
            else:
                player.inventory.append({
                    "id": item_id,
                    "type": item_details["type"],
                    "quantity": 1,
                    "equipped": False
                })
                
        # Save modifications
        player.save_to_db()

    def go_next(self):
        # Return back to exploration mode
        # The explore state remains initialized, so progress resumes cleanly!
        self.game.change_state("explore")

    def enter(self):
        # Play victory fanfare sound
        self.game.sounds.play_sfx("level_up")

    def exit(self):
        pass

    def handle_event(self, event):
        mouse_pos = self.game.get_logical_mouse_pos()
        self.btn_continue.handle_event(event, mouse_pos)

    def update(self, dt):
        mouse_pos = self.game.get_logical_mouse_pos()
        self.btn_continue.update(dt, mouse_pos)

    def draw(self, surface):
        # Background gradient: Dark Green/Gold theme
        draw_gradient_rect(surface, (12, 28, 18), (10, 20, 25), (0, 0, self.game.virtual_width, self.game.virtual_height))
        
        # Victory Title
        title_surf = self.font_title.render("VICTORY ACHIEVED!", True, (100, 240, 140))
        surface.blit(title_surf, ((self.game.virtual_width - title_surf.get_width())//2, 80))
        
        # Centered summary container
        px = self.game.virtual_width // 2 - 220
        py = 160
        draw_rounded_panel(surface, (px, py, 440, 360), (22, 25, 22), (230, 185, 55), border_width=3, border_radius=12)
        
        # Summary Header
        sum_head = self.font_header.render("BATTLE REWARDS", True, (230, 185, 55))
        surface.blit(sum_head, (px + (440 - sum_head.get_width())//2, py + 20))
        
        # Rewards list
        r_list = [
            (f"+{self.xp_earned} Experience Points", (180, 80, 240)),
            (f"+{self.coins_earned} Shiny Coins", (255, 215, 0))
        ]
        
        # Draw rewards rows
        for idx, (txt, color) in enumerate(r_list):
            ry = py + 70 + idx * 56
            pygame.draw.rect(surface, (30, 35, 30), (px + 30, ry, 380, 42), border_radius=4)
            
            txt_surf = self.font_details.render(txt, True, color)
            surface.blit(txt_surf, (px + 45, ry + 11))

        # Renders Loot Item if any
        ly = py + 70 + len(r_list) * 56
        if self.loot_item_id:
            from src.items.item import get_item_details
            item_details = get_item_details(self.loot_item_id)
            
            pygame.draw.rect(surface, (30, 35, 30), (px + 30, ly, 380, 42), border_radius=4)
            
            # Show item icon & label
            loader = self.game.states["loading"].loader
            item_icon = loader.get_image(f"loot_ic_{self.loot_item_id}", loader.create_item_sprite, self.loot_item_id)
            item_icon_small = pygame.transform.scale(item_icon, (32, 32))
            
            surface.blit(item_icon_small, (px + 45, ly + 5))
            
            loot_txt = f"Found Loot: {item_details['name']}"
            txt_surf = self.font_details.render(loot_txt, True, (80, 200, 220))
            surface.blit(txt_surf, (px + 90, ly + 11))
        else:
            pygame.draw.rect(surface, (30, 35, 30), (px + 30, ly, 380, 42), border_radius=4)
            no_loot_surf = self.font_details.render("No extra item loot found.", True, (130, 130, 140))
            surface.blit(no_loot_surf, (px + 45, ly + 11))

        # Show LEVEL UP announcement overlay
        if self.leveled_up:
            player = self.game.player
            # Overlay panel over bottom half of card
            ly_p = py + 250
            pygame.draw.rect(surface, (45, 20, 60), (px + 20, ly_p, 400, 95), border_radius=6)
            pygame.draw.rect(surface, (200, 100, 255), (px + 20, ly_p, 400, 95), 1, border_radius=6)
            
            lvl_lbl = get_font(20, is_bold=True).render(f"LEVEL UP! REACHED LEVEL {player.level}", True, (220, 130, 250))
            surface.blit(lvl_lbl, (px + 20 + (400 - lvl_lbl.get_width())//2, ly_p + 10))
            
            stat_lbl = self.font_ability.render(f"Max HP: {player.max_hp} (+15)    Max Mana: {player.max_mana} (+10)", True, (230, 230, 235))
            surface.blit(stat_lbl, (px + 20 + (400 - stat_lbl.get_width())//2, ly_p + 42))
            
            ab_txt = f"Unlocked Action: {player.unlocked_abilities[-1]}"
            ab_surf = self.font_ability.render(ab_txt, True, (255, 235, 100))
            surface.blit(ab_surf, (px + 20 + (400 - ab_surf.get_width())//2, ly_p + 68))

        # Continue button
        self.btn_continue.draw(surface)
