import pygame
import math
from src.engine.settings import COLOR_RED, COLOR_BLUE

class Player:
    def __init__(self, game):
        self.game = game
        
        # Profile fields
        self.name = "Hero"
        self.avatar = "adventurer"
        self.level = 1
        self.xp = 0
        self.coins = 100
        
        # Stats
        self.hp = 100
        self.max_hp = 100
        self.mana = 50
        self.max_mana = 50
        self.unlocked_abilities = ["Strike"]
        
        # Customization colors
        self.hair_color = (200, 50, 50)
        self.outfit_color = (50, 80, 200)
        
        # Position and physics
        self.x = 200.0
        self.y = 200.0
        self.width = 64
        self.height = 64
        
        # Speed params
        self.walk_speed = 180.0
        self.run_speed = 300.0
        
        # Collisions bounds (small rect at player feet for 2.5D feel)
        self.rect_width = 32
        self.rect_height = 18
        self.rect_offset_x = 16 # (64 - 32) / 2
        self.rect_offset_y = 44 # near bottom of sprite
        
        # Animation parameters
        self.moving = False
        self.running = False
        self.anim_tick = 0.0
        self.direction = "down" # "up", "down", "left", "right"
        
        # Inventory list of items
        self.inventory = []
        
        # Initial loads
        self.load_from_db()

    def get_rect(self):
        """Returns the physical collision hitbox at the feet."""
        return pygame.Rect(
            int(self.x + self.rect_offset_x), 
            int(self.y + self.rect_offset_y), 
            self.rect_width, 
            self.rect_height
        )

    def load_from_db(self):
        """Loads progression and custom colors from SQLite db."""
        p_data = self.game.db.load_profile()
        if p_data:
            self.name = p_data["name"]
            self.avatar = p_data["avatar"]
            self.level = p_data["level"]
            self.xp = p_data["xp"]
            self.coins = p_data["coins"]
            self.hp = p_data["hp"]
            self.max_hp = p_data["max_hp"]
            self.mana = p_data["mana"]
            self.max_mana = p_data["max_mana"]
            self.hair_color = p_data["hair_color"]
            self.outfit_color = p_data["outfit_color"]
            
        # Load unlocked abilities based on level
        self.update_abilities()
        
        # Load inventory
        inv_data = self.game.db.load_inventory()
        self.inventory = inv_data if inv_data else [
            {"id": "silver_sword", "type": "weapon", "quantity": 1, "equipped": True},
            {"id": "iron_shield", "type": "shield", "quantity": 1, "equipped": True},
            {"id": "health_potion", "type": "potion", "quantity": 3, "equipped": False},
            {"id": "hint_card", "type": "card", "quantity": 2, "equipped": False}
        ]

    def save_to_db(self):
        """Saves current state back to SQLite db."""
        self.game.db.save_profile({
            "name": self.name,
            "avatar": self.avatar,
            "level": self.level,
            "xp": self.xp,
            "coins": self.coins,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "mana": self.mana,
            "max_mana": self.max_mana,
            "hair_color": self.hair_color,
            "outfit_color": self.outfit_color
        })
        self.game.db.save_inventory(self.inventory)

    def add_xp(self, amount):
        self.xp += amount
        xp_needed = self.level * 150
        leveled_up = False
        while self.xp >= xp_needed:
            self.xp -= xp_needed
            self.level += 1
            self.max_hp += 15
            self.max_mana += 10
            self.hp = self.max_hp
            self.mana = self.max_mana
            xp_needed = self.level * 150
            leveled_up = True
            
        if leveled_up:
            self.update_abilities()
            self.game.sounds.play_sfx("level_up")
        return leveled_up

    def update_abilities(self):
        # Level thresholds unlock new spells
        self.unlocked_abilities = ["Strike"]
        if self.level >= 2:
            self.unlocked_abilities.append("Heal Spell (15 Mana)")
        if self.level >= 4:
            self.unlocked_abilities.append("Fireball (20 Mana)")
        if self.level >= 6:
            self.unlocked_abilities.append("Thunderbolt (30 Mana)")

    def get_attack_power(self):
        power = 10 + self.level * 2
        # Add weapon bonus
        equipped_weapon = next((i for i in self.inventory if i["type"] == "weapon" and i["equipped"]), None)
        if equipped_weapon:
            if "gold" in equipped_weapon["id"]: power += 15
            elif "silver" in equipped_weapon["id"]: power += 8
            else: power += 4
        return power

    def get_defense(self):
        def_val = 2 + self.level
        # Add shield/armor bonuses
        equipped_shield = next((i for i in self.inventory if i["type"] == "shield" and i["equipped"]), None)
        equipped_armor = next((i for i in self.inventory if i["type"] == "armor" and i["equipped"]), None)
        if equipped_shield:
            if "dragon" in equipped_shield["id"]: def_val += 10
            elif "iron" in equipped_shield["id"]: def_val += 4
        if equipped_armor:
            if "obsidian" in equipped_armor["id"]: def_val += 15
            elif "iron" in equipped_armor["id"]: def_val += 6
        return def_val

    def update(self, dt, keys, obstacles):
        # Determine directional movement inputs
        dx, dy = 0, 0
        self.running = keys[pygame.K_LSHIFT]
        speed = self.run_speed if self.running else self.walk_speed
        
        # Up-Down
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= 1
            self.direction = "up"
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += 1
            self.direction = "down"
            
        # Left-Right
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= 1
            self.direction = "left"
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += 1
            self.direction = "right"

        # Apply movements
        if dx != 0 or dy != 0:
            # Normalize diagonal velocity
            length = math.sqrt(dx*dx + dy*dy)
            dx = (dx / length) * speed * dt
            dy = (dy / length) * speed * dt
            
            self.moving = True
            # Speed up animation tick when running
            self.anim_tick += dt * (14.0 if self.running else 9.0)
        else:
            self.moving = False
            self.anim_tick += dt * 4.0 # Gentle bob for idle

        # Collision check along X axis
        if dx != 0:
            self.x += dx
            player_rect = self.get_rect()
            for obs in obstacles:
                if player_rect.colliderect(obs):
                    if dx > 0:
                        self.x = obs.left - self.rect_width - self.rect_offset_x
                    else:
                        self.x = obs.right - self.rect_offset_x
                    break
                    
        # Collision check along Y axis
        if dy != 0:
            self.y += dy
            player_rect = self.get_rect()
            for obs in obstacles:
                if player_rect.colliderect(obs):
                    if dy > 0:
                        self.y = obs.top - self.rect_height - self.rect_offset_y
                    else:
                        self.y = obs.bottom - self.rect_offset_y
                    break

    def draw(self, surface):
        # Choose frame name
        frame_type = "idle"
        if self.moving:
            cycle = int(self.anim_tick) % 4
            if cycle == 0:
                frame_type = "walk_1" if not self.running else "run_1"
            elif cycle == 1:
                frame_type = "idle"
            elif cycle == 2:
                frame_type = "walk_2" if not self.running else "run_2"
            else:
                frame_type = "idle"
        else:
            frame_type = "idle"
            
        # Draw dynamic procedural character
        frame_tick = int(self.anim_tick)
        sprite = self.game.states["loading"].loader.get_image(
            f"player_{frame_type}", 
            self.game.states["loading"].loader.create_character_frame,
            frame_type, self.hair_color, self.outfit_color, frame_tick
        )
        
        # Handle simple horizontal flip for left movement direction
        if self.direction == "left":
            sprite = pygame.transform.flip(sprite, True, False)
            
        surface.blit(sprite, (int(self.x), int(self.y)))
