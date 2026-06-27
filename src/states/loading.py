import pygame
from src.engine.state import State
from src.utils.asset_loader import AssetLoader
from src.utils.helpers import get_font

class LoadingState(State):
    def __init__(self, game):
        super().__init__(game)
        self.loader = AssetLoader()
        
        # Loading states
        self.progress = 0.0
        self.target_progress = 0.0
        self.font = get_font(24, is_bold=True)
        self.font_sub = get_font(14)
        
        # List of assets to pre-generate sequentially in update loop
        self.generation_queue = [
            ("player_idle", "player", "idle"),
            ("player_walk_1", "player", "walk_1"),
            ("player_walk_2", "player", "walk_2"),
            ("player_run_1", "player", "run_1"),
            ("player_run_2", "player", "run_2"),
            ("player_interact", "player", "interact"),
            ("monster_slime", "monster", "slime"),
            ("monster_drone", "monster", "drone"),
            ("monster_fire_elemental", "monster", "fire_elemental"),
            ("monster_ent", "monster", "ent"),
            ("monster_griffin", "monster", "griffin"),
            ("monster_mummy", "monster", "mummy"),
            ("monster_golem", "monster", "golem"),
            ("monster_virus", "monster", "virus"),
            ("monster_dragon", "monster", "dragon"),
            ("tile_grass", "tile", "grass"),
            ("tile_water", "tile", "water"),
            ("tile_lava", "tile", "lava"),
            ("tile_dirt", "tile", "dirt"),
            ("tile_bridge", "tile", "bridge"),
            ("tile_wall", "tile", "wall"),
            ("tile_ice", "tile", "ice"),
            ("tile_floor_tech", "tile", "floor_tech"),
            ("item_silver_sword", "item", "silver_sword"),
            ("item_gold_sword", "item", "gold_sword"),
            ("item_iron_shield", "item", "iron_shield"),
            ("item_dragon_shield", "item", "dragon_shield"),
            ("item_iron_armor", "item", "iron_armor"),
            ("item_obsidian_armor", "item", "obsidian_armor"),
            ("item_health_potion", "item", "health_potion"),
            ("item_mana_potion", "item", "mana_potion"),
            ("item_hint_card", "item", "hint_card"),
            ("item_spellbook_intellect", "item", "spellbook_intellect")
        ]
        self.total_assets = len(self.generation_queue)
        self.current_index = 0

    def enter(self):
        self.progress = 0.0
        self.target_progress = 0.0
        self.current_index = 0

    def update(self, dt):
        # Smooth progress lerp
        self.progress += (self.target_progress - self.progress) * 8.0 * dt
        
        # Load one asset per tick to keep frame rates alive and render progress
        if self.current_index < self.total_assets:
            key, asset_type, extra = self.generation_queue[self.current_index]
            
            # Generate and cache via the AssetLoader
            if asset_type == "player":
                # Generate default colors (hair red, outfit blue)
                self.loader.get_image(key, self.loader.create_character_frame, extra, (200, 50, 50), (50, 80, 200), 0)
            elif asset_type == "monster":
                self.loader.get_image(key, self.loader.create_monster_sprite, extra, 0)
            elif asset_type == "tile":
                self.loader.get_image(key, self.loader.create_tile_sprite, extra, 0)
            elif asset_type == "item":
                self.loader.get_image(key, self.loader.create_item_sprite, extra)
                
            self.current_index += 1
            self.target_progress = (self.current_index / self.total_assets) * 100.0
        else:
            self.progress = 100.0
            if self.progress >= 99.5:
                # Transition to menu once done
                self.game.change_state("menu")

    def draw(self, surface):
        surface.fill((20, 20, 25))
        
        # Draw Loading Text
        txt_surf = self.font.render("Pre-generating RPG World...", True, (255, 255, 255))
        tx = (self.game.virtual_width - txt_surf.get_width()) // 2
        ty = self.game.virtual_height // 2 - 40
        surface.blit(txt_surf, (tx, ty))
        
        # Draw Progress Bar
        bar_w = 400
        bar_h = 24
        bx = (self.game.virtual_width - bar_w) // 2
        by = ty + 50
        
        # Background slot
        pygame.draw.rect(surface, (40, 35, 35), (bx, by, bar_w, bar_h), border_radius=4)
        
        # Fill bar
        fill_w = int(bar_w * (self.progress / 100.0))
        if fill_w > 0:
            pygame.draw.rect(surface, (230, 185, 55), (bx, by, fill_w, bar_h), border_radius=4)
            
        # Draw gold border
        pygame.draw.rect(surface, (165, 120, 25), (bx, by, bar_w, bar_h), 2, border_radius=4)
        
        # Draw Percentage
        pct_surf = self.font_sub.render(f"{int(self.progress)}%", True, (255, 255, 255))
        surface.blit(pct_surf, (bx + (bar_w - pct_surf.get_width())//2, by + (bar_h - pct_surf.get_height())//2))
