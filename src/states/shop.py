import pygame
from src.engine.state import State
from src.ui.ui_elements import Button
from src.items.item import ITEMS_DATABASE, get_item_details
from src.utils.helpers import get_font, draw_rounded_panel, draw_gradient_rect

class ShopState(State):
    def __init__(self, game):
        super().__init__(game)
        
        self.selected_item_id = "health_potion"
        self.buttons = []
        self.item_buttons = []
        
        self.font_title = get_font(28, is_bold=True)
        self.font_header = get_font(20, is_bold=True)
        self.font_stats = get_font(14, is_bold=True)
        self.font_desc = get_font(12)
        
        self.init_shop_controls()

    def init_shop_controls(self):
        self.buttons = []
        
        # Navigation
        self.buttons.append(Button(self.game, 40, 620, 180, 45, "Back to Explore", self.go_back, color=(120, 50, 50)))
        
        # Action Buttons (Buy / Equip)
        # Positioned in the right detailed panel
        self.btn_buy = Button(self.game, 820, 490, 220, 45, "BUY ITEM", self.buy_selected, color=(50, 150, 80))
        self.btn_equip = Button(self.game, 820, 550, 220, 45, "EQUIP ITEM", self.equip_selected, color=(220, 150, 30))
        
        self.buttons.append(self.btn_buy)
        self.buttons.append(self.btn_equip)

    def init_item_list(self):
        # Generate item choice buttons dynamically on the left panel
        self.item_buttons = []
        
        item_keys = [
            "health_potion", "mana_potion", "hint_card",
            "silver_sword", "iron_shield", "iron_armor",
            "gold_sword", "dragon_shield", "obsidian_armor"
        ]
        
        grid_x = 90
        grid_y = 150
        btn_w = 200
        btn_h = 42
        
        for idx, key in enumerate(item_keys):
            item_details = get_item_details(key)
            name = item_details["name"]
            
            bx = grid_x if (idx % 2 == 0) else (grid_x + btn_w + 20)
            by = grid_y + (idx // 2) * 52
            
            callback = lambda choice=key: self.select_item(choice)
            btn = Button(self.game, bx, by, btn_w, btn_h, name, callback, color=(40, 45, 55))
            self.item_buttons.append(btn)

    def select_item(self, item_id):
        self.selected_item_id = item_id

    def buy_selected(self):
        player = self.game.player
        item_details = get_item_details(self.selected_item_id)
        cost = item_details["cost"]
        
        if player.coins >= cost:
            player.coins -= cost
            self.game.sounds.play_sfx("chest") # Play cash pickup SFX
            
            # Find item in inventory
            inv_item = next((i for i in player.inventory if i["id"] == self.selected_item_id), None)
            if inv_item:
                inv_item["quantity"] += 1
            else:
                player.inventory.append({
                    "id": self.selected_item_id,
                    "type": item_details["type"],
                    "quantity": 1,
                    "equipped": False
                })
            player.save_to_db()
        else:
            self.game.sounds.play_sfx("wrong") # Buzz

    def equip_selected(self):
        player = self.game.player
        item_details = get_item_details(self.selected_item_id)
        
        # Check if item is in inventory
        inv_item = next((i for i in player.inventory if i["id"] == self.selected_item_id), None)
        if inv_item:
            # Toggle equipped state
            # If it's a weapon/shield/armor, un-equip any active item of that type first
            item_type = item_details["type"]
            if item_type in ["weapon", "shield", "armor"]:
                for i in player.inventory:
                    if i["type"] == item_type:
                        i["equipped"] = False
                        
                inv_item["equipped"] = True
                self.game.sounds.play_sfx("correct") # Ding
                player.save_to_db()

    def go_back(self):
        self.game.change_state("explore")

    def enter(self):
        self.init_item_list()
        self.game.sounds.play_music("menu")

    def exit(self):
        self.game.player.save_to_db()

    def handle_event(self, event):
        mouse_pos = self.game.get_logical_mouse_pos()
        
        for btn in self.buttons:
            btn.handle_event(event, mouse_pos)
            
        for btn in self.item_buttons:
            btn.handle_event(event, mouse_pos)

    def update(self, dt):
        mouse_pos = self.game.get_logical_mouse_pos()
        player = self.game.player
        item_details = get_item_details(self.selected_item_id)
        
        # Update buttons
        for btn in self.buttons:
            btn.update(dt, mouse_pos)
        for btn in self.item_buttons:
            btn.update(dt, mouse_pos)
            
        # Determine button enable states dynamically
        # Buy: enabled if player has coins
        self.btn_buy.set_enabled(player.coins >= item_details["cost"])
        
        # Equip: enabled if they own the item and it's an equippable type (weapon, shield, armor)
        inv_item = next((i for i in player.inventory if i["id"] == self.selected_item_id), None)
        is_equippable = item_details["type"] in ["weapon", "shield", "armor"]
        
        # Enable equip button if they own it and it is not already equipped
        self.btn_equip.set_enabled(inv_item is not None and is_equippable and not inv_item["equipped"])

    def draw(self, surface):
        # Backdrop
        draw_gradient_rect(surface, (18, 14, 25), (10, 20, 35), (0, 0, self.game.virtual_width, self.game.virtual_height))
        
        player = self.game.player
        item_details = get_item_details(self.selected_item_id)
        
        # Renders header
        title_surf = self.font_title.render("KINGDOM EQUIPMENT MERCHANT", True, (255, 235, 100))
        surface.blit(title_surf, ((self.game.virtual_width - title_surf.get_width())//2, 35))
        
        # Display coins bag balance
        coins_surf = self.font_header.render(f"YOUR GOLD: {player.coins} Coins", True, (255, 215, 0))
        surface.blit(coins_surf, (self.game.virtual_width - coins_surf.get_width() - 50, 42))

        # Panels
        # Left Panel (Items selection grid list)
        draw_rounded_panel(surface, (70, 110, 480, 480), (25, 25, 30), (165, 120, 25), border_width=2)
        
        # Right Panel (Item details inspection)
        draw_rounded_panel(surface, (700, 110, 480, 480), (20, 20, 24), (165, 120, 25), border_width=2)

        # Draw left list buttons
        for btn in self.item_buttons:
            # Highlight selected choice outline green
            btn_key = next((k for k, v in ITEMS_DATABASE.items() if v["name"] == btn.text), "")
            if btn_key == self.selected_item_id:
                pygame.draw.rect(surface, (230, 185, 55), btn.rect, 2, border_radius=8)
            btn.draw(surface)

        # Draw right details inspection panel text
        head_det = self.font_header.render("ITEM DETAILS", True, (230, 185, 55))
        surface.blit(head_det, (700 + (480 - head_det.get_width())//2, 130))
        
        # Renders the large procedural equipment icon
        loader = self.game.states["loading"].loader
        item_sprite = loader.get_image(
            f"shop_preview_{self.selected_item_id}", 
            loader.create_item_sprite, 
            self.selected_item_id
        )
        # Double size icon for inspection
        item_sprite_large = pygame.transform.scale(item_sprite, (96, 96))
        surface.blit(item_sprite_large, (700 + (480 - 96)//2, 180))

        # Item info lines
        name_surf = get_font(20, is_bold=True).render(item_details["name"], True, (255, 255, 255))
        surface.blit(name_surf, (700 + (480 - name_surf.get_width())//2, 290))
        
        type_txt = f"Type: {item_details['type'].capitalize()}"
        type_surf = self.font_stats.render(type_txt, True, (150, 150, 160))
        surface.blit(type_surf, (730, 335))
        
        cost_txt = f"Price: {item_details['cost']} Coins"
        cost_surf = self.font_stats.render(cost_txt, True, (255, 215, 0))
        surface.blit(cost_surf, (730, 360))
        
        # Show stats bonus if applicable
        stat_bonus = ""
        if "power" in item_details:
            stat_bonus = f"Weapon Power: +{item_details['power']} Attack"
        elif "defense" in item_details:
            stat_bonus = f"Armor Defense: +{item_details['defense']} Defense"
        if "hp_boost" in item_details:
            stat_bonus += f", +{item_details['hp_boost']} Max HP"
        if "mana_boost" in item_details:
            stat_bonus = f"Tome Intellect: +{item_details['mana_boost']} Max Mana"
            
        if stat_bonus:
            bonus_surf = self.font_stats.render(stat_bonus, True, (80, 220, 140))
            surface.blit(bonus_surf, (730, 385))

        # Ownership state
        inv_item = next((i for i in player.inventory if i["id"] == self.selected_item_id), None)
        own_qty = inv_item["quantity"] if inv_item else 0
        eq_status = "Equipped" if (inv_item and inv_item["equipped"]) else "Unequipped" if (inv_item and is_equippable) else "Consumable"
        
        own_txt = f"You Own: {own_qty}   ({eq_status})"
        own_surf = self.font_stats.render(own_txt, True, (120, 210, 255) if own_qty > 0 else (120, 120, 125))
        surface.blit(own_surf, (730, 415))

        # Description text wrap
        desc_rect = (730, 442, 420, 45)
        from src.utils.helpers import draw_text_wrapped
        draw_text_wrapped(surface, item_details["desc"], self.font_desc, (180, 180, 190), desc_rect)

        # Draw Buy/Equip controls
        self.btn_buy.draw(surface)
        self.btn_equip.draw(surface)
        
        # Navigation back
        for btn in self.buttons:
            btn.draw(surface)
