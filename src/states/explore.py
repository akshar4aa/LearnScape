import pygame
import math
import random
from src.engine.state import State
from src.entities.npc import NPCTeacher
from src.entities.monster import Monster, KingdomBoss
from src.ui.particle import WeatherOverlay, ParticleSystem
from src.utils.helpers import get_font, draw_rounded_panel

class ExploreState(State):
    def __init__(self, game):
        super().__init__(game)
        
        self.active_kingdom = "mathematics"

        self.progression_order = [
                  "mathematics",
                  "science",
                  "biology",
                  "chemistry",
                  "physics",
                  "english",
                  "history",
                  "geography",
                  "computer_science"
]
        
        # Grid dimensions (40x30 grid of 32x32 tiles -> 1280x960 map)
        self.cols = 40
        self.rows = 30
        self.tile_size = 32
        self.map_w = self.cols * self.tile_size
        self.map_h = self.rows * self.tile_size
        
        # Layout arrays
        self.grid = []
        self.obstacles_rects = []
        self.trees = []
        self.chests = []
        
        # Roaming entities
        self.monsters = []
        self.teacher = None
        self.portal_rect = None
        
        # Camera bounds
        self.camera_x = 0
        self.camera_y = 0
        
        # Weather overlay & Dialogue overlay
        self.weather = WeatherOverlay("none")
        self.particles = ParticleSystem()
        
        # Active dialogue parameters
        self.active_dialogue_box = None
        self.dialogue_npc = None

    def set_active_kingdom(self, kingdom_id):
        self.active_kingdom = kingdom_id
        self.generate_map()
        
        # Choose weather overlay
        if kingdom_id == "biology":
            self.weather.set_mode("rain")
        elif kingdom_id == "chemistry":
            self.weather.set_mode("none") # volcanic heat
        elif kingdom_id == "geography":
            self.weather.set_mode("snow")
        elif kingdom_id == "computer_science":
            self.weather.set_mode("fog")
        else:
            self.weather.set_mode("none")
            
        # Select background music for the kingdom
        if kingdom_id in ["mathematics", "english", "history"]:
            self.game.sounds.play_music("menu")
        elif kingdom_id in ["physics", "science", "computer_science"]:
            self.game.sounds.play_music("explore")
        else: # biology, chemistry, geography
            self.game.sounds.play_music("explore")

    def enter(self):
        # Reset player to start area (clamped inside boundaries)
        if hasattr(self.game, "player"):
            self.game.player.x = 100.0
            self.game.player.y = 400.0
        else:
            from src.entities.player import Player
            self.game.player = Player(self.game)
            
        # Re-set music volume
        self.set_active_kingdom(self.active_kingdom)
        self.particles.clear()
        self.active_dialogue_box = None
        self.dialogue_npc = None

    def exit(self):
        if hasattr(self.game, "player"):
            self.game.player.save_to_db()

    def generate_map(self):
        """Generates a procedural tile layout depending on the kingdom theme."""
        self.grid = []
        self.obstacles_rects = []
        self.trees = []
        self.chests = []
        self.monsters = []
        self.portal_rect = pygame.Rect(self.map_w - 90, 400, 48, 64)
        
        # Determine tile keys based on kingdom
        # default: grass
        ground_tile = "grass"
        obstacle_tile = "wall"
        water_tile = "water"
        
        if self.active_kingdom == "chemistry":
            ground_tile = "dirt"
            obstacle_tile = "wall"
            water_tile = "lava"
        elif self.active_kingdom in ["physics", "computer_science"]:
            ground_tile = "floor_tech"
            obstacle_tile = "wall"
            water_tile = "water"
        elif self.active_kingdom == "geography":
            ground_tile = "ice"
            obstacle_tile = "wall"
            water_tile = "water"
        elif self.active_kingdom in ["history", "english"]:
            ground_tile = "dirt"
            obstacle_tile = "wall"
            water_tile = "water"

        # Populate basic ground grid (rows, cols)
        for r in range(self.rows):
            row_tiles = []
            for c in range(self.cols):
                # Put borders around edge
                if r == 0 or r == self.rows - 1 or c == 0 or c == self.cols - 1:
                    row_tiles.append("wall")
                    self.obstacles_rects.append(pygame.Rect(c*32, r*32, 32, 32))
                else:
                    row_tiles.append(ground_tile)
            self.grid.append(row_tiles)

        # Place vertical obstacle barrier/river dividing map at col 20
        bridge_row = 12
        for r in range(1, self.rows - 1):
            if r == bridge_row or r == bridge_row + 1:
                # Place wooden bridge
                self.grid[r][20] = "bridge"
            else:
                self.grid[r][20] = water_tile
                self.obstacles_rects.append(pygame.Rect(20*32, r*32, 32, 32))

        # Add scenery obstacles: Trees, rocks, ruins
        # Biology/Math maps spawn trees
        # Chemistry map spawns volcano columns
        # Physics map spawns computer systems
        scenery_count = 25
        for _ in range(scenery_count):
            # Left half scenery
            lx = random.randint(3, 17) * 32
            ly = random.randint(3, 27) * 32
            
            # Avoid bridge row and starting areas
            if ly in [bridge_row*32, (bridge_row+1)*32] or (lx < 200 and ly > 300 and ly < 500):
                continue
                
            self.trees.append({
                "type": "tree_pine" if self.active_kingdom in ["biology", "mathematics"] else "tree_oak" if self.active_kingdom == "english" else "castle" if self.active_kingdom in ["physics", "history"] else "mountain",
                "x": lx + 16,
                "y": ly + 24,
                "width": 32,
                "height": 48
            })
            # Add to physical collision obstacle bounds
            self.obstacles_rects.append(pygame.Rect(lx, ly, 32, 32))
            
            # Right half scenery
            rx = random.randint(23, 37) * 32
            ry = random.randint(3, 27) * 32
            
            # Avoid bridge row and portal zone
            if ry in [bridge_row*32, (bridge_row+1)*32] or rx > self.map_w - 150:
                continue
                
            self.trees.append({
                "type": "tree_pine" if self.active_kingdom in ["biology", "mathematics"] else "tree_oak" if self.active_kingdom == "english" else "castle" if self.active_kingdom in ["physics", "history"] else "mountain",
                "x": rx + 16,
                "y": ry + 24,
                "width": 32,
                "height": 48
            })
            self.obstacles_rects.append(pygame.Rect(rx, ry, 32, 32))

        # Spawn 3 chest boxes on map containing items
        chest_coords = [
            (random.randint(4, 15)*32 + 16, random.randint(4, 10)*32 + 24),
            (random.randint(4, 15)*32 + 16, random.randint(18, 25)*32 + 24),
            (random.randint(24, 35)*32 + 16, random.randint(4, 25)*32 + 24)
        ]
        
        # Populate loots per chest
        loot_tables = [
            {"coins": 50, "xp": 100, "item": "health_potion"},
            {"coins": 100, "xp": 150, "item": "hint_card"},
            {"coins": 200, "xp": 250, "item": "gold_sword" if self.active_kingdom == "computer_science" else "silver_sword"}
        ]
        
        for idx, (cx, cy) in enumerate(chest_coords):
            self.chests.append({
                "x": cx,
                "y": cy,
                "rect": pygame.Rect(cx - 16, cy - 24, 32, 32),
                "opened": False,
                "frame": 0,
                "loot": loot_tables[idx]
            })

        # Spawn NPC Teacher
        teacher_names = {
            "mathematics": ("Prof. Pytha", "Welcome to Mathematics Kingdom, student!\nWe must master equations to secure the gate!\nDefeat the Math Guardian portal at the end!"),
            "biology": ("Dr. Darwin", "Ah! Welcome to Biology Forest.\nStudy plant cells and organs carefully to progress!"),
            "chemistry": ("Dr. Curie", "Caution: Chemistry Volcano is active!\nBalance equations and elements to cool down the lava boss!"),
            "physics": ("Prof. Newton", "Forces and motion rule this Laboratory.\nCalculate vector masses to bypass the gatekeeper drone!"),
            "science": ("Dr. Galileo", "Science Kingdom holds secrets of space.\nAnswer solar riddles to cross to English Castle!"),
            "english": ("Prof. Bard", "A clean script is mightier than the sword!\nSlay vocabulary grammar errors in the Castle!"),
            "history": ("Dr. Herodotus", "Welcome to the History Museum.\nSolve historical dates to unlock the Desert Island!"),
            "geography": ("Dr. Magellan", "Study capitals and oceans on Geography Island.\nChart the course to CS City!"),
            "computer_science": ("Prof. Turing", "You reached CS City, the final frontier!\nMaster algorithms to complete your education saga!")
        }
        name, welcome_msg = teacher_names.get(self.active_kingdom, ("Professor", "Greetings traveler!"))
        
        self.teacher = NPCTeacher(
            self.game, name, self.active_kingdom, 
            350, 360, 
            [
                welcome_msg, 
                "Open treasure chests to buy better gear in the shop!", 
                "Settle combat answers correctly to inflict spell damages!"
            ]
        )
        
        # Spawn roaming monsters based on kingdom lvl difficulty
        k_lvl = self.progression_order.index(self.active_kingdom) + 1
        m_types = ["slime", "drone", "fire_elemental", "ent", "griffin", "mummy", "golem", "virus"]
        m_type = m_types[(k_lvl - 1) % len(m_types)]
        
        # Spawn 4 roaming monsters on map
        for _ in range(4):
            # Place in open area
            mx = random.randint(22, 36) * 32
            my = random.randint(3, 26) * 32
            
            # Avoid portal
            if mx > self.map_w - 120:
                continue
                
            self.monsters.append(Monster(self.game, m_type, self.active_kingdom, mx, my, level=k_lvl))

    def handle_event(self, event):
        mouse_pos = self.game.get_logical_mouse_pos()
        
        # 1. Dialogue overlay controls
        if self.active_dialogue_box:
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_e, pygame.K_RETURN, pygame.K_SPACE):
                if not self.active_dialogue_box.finished:
                    self.active_dialogue_box.skip()
                else:
                    # Advance text
                    next_text = self.dialogue_npc.interact()
                    if next_text:
                        from src.ui.dialogue import TypewriterDialogue
                        self.active_dialogue_box = TypewriterDialogue(
                            self.game, 180, 500, 920, 160, self.dialogue_npc.name, next_text
                        )
                    else:
                        # Clear dialogue box
                        self.active_dialogue_box = None
                        self.dialogue_npc = None
            return

        # 2. ESC key opens pause overlay
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.push_state("pause")
            return

        # 3. Handle key inputs for interactions on explore
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            player = self.game.player
            
            # Interact with teacher
            dist_to_teacher = math.sqrt((player.x - self.teacher.x)**2 + (player.y - self.teacher.y)**2)
            if dist_to_teacher < 90:
                self.dialogue_npc = self.teacher
                welcome_txt = self.teacher.interact()
                
                from src.ui.dialogue import TypewriterDialogue
                self.active_dialogue_box = TypewriterDialogue(
                    self.game, 180, 500, 920, 160, self.teacher.name, welcome_txt
                )
                return

            # Interact with chests
            for chest in self.chests:
                if not chest["opened"]:
                    dist_to_chest = math.sqrt((player.x - chest["x"])**2 + (player.y - chest["y"])**2)
                    if dist_to_chest < 60:
                        chest["opened"] = True
                        chest["frame"] = 2
                        self.game.sounds.play_sfx("chest")
                        
                        # Deliver loot
                        loot = chest["loot"]
                        player.coins += loot["coins"]
                        leveled_up = player.add_xp(loot["xp"])
                        
                        # Add item to inventory
                        item_id = loot["item"]
                        from src.items.item import get_item_details
                        item_details = get_item_details(item_id)
                        
                        # Check if item exists in inventory, else append
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
                            
                        # Floating notifications text
                        text_msg = f"+{loot['coins']} Coins  +{loot['xp']} XP"
                        if leveled_up:
                            text_msg += "  LEVEL UP!"
                        self.particles.add_floating_text(text_msg, player.x, player.y - 20, (255, 235, 100))
                        self.particles.add_floating_text(f"Received: {item_details['name']}", player.x, player.y - 45, (80, 220, 240))
                        break

    def update(self, dt):
        if self.active_dialogue_box:
            self.active_dialogue_box.update(dt)
            return

        keys = pygame.key.get_pressed()
        player = self.game.player
        
        # 1. Update entities
        player.update(dt, keys, self.obstacles_rects)
        
        for m in self.monsters:
            m.update(dt)
            
        self.weather.update(dt)
        self.particles.update(dt)
        
        # 2. Camera scroll calculation centering on player
        self.camera_x = player.x - self.game.virtual_width // 2
        self.camera_y = player.y - self.game.virtual_height // 2
        
        # Clamp camera to map dimensions
        self.camera_x = max(0, min(self.map_w - self.game.virtual_width, self.camera_x))
        self.camera_y = max(0, min(self.map_h - self.game.virtual_height, self.camera_y))

        # 3. Check monster collisions to trigger battles
        player_rect = player.get_rect()
        for m in self.monsters:
            if player_rect.colliderect(m.get_rect()):
                self.monsters.remove(m)
                
                # Pass monster to battle state
                self.game.states["battle"].init_battle(m)
                self.game.change_state("battle")
                return

        # 4. Check portal collision to trigger boss fight
        if player_rect.colliderect(self.portal_rect):
            # Check if teacher missions are ready or just challenge directly
            k_lvl = self.progression_order.index(self.active_kingdom) + 1
            self.game.states["boss_battle"].init_boss_battle(self.active_kingdom, k_lvl)
            self.game.change_state("boss_battle")
            return

    def draw(self, surface):
        # Draw background base tiles
        cam_x, cam_y = int(self.camera_x), int(self.camera_y)
        
        # Determine viewport bounds
        start_col = max(0, cam_x // self.tile_size)
        end_col = min(self.cols, (cam_x + self.game.virtual_width) // self.tile_size + 1)
        start_row = max(0, cam_y // self.tile_size)
        end_row = min(self.rows, (cam_y + self.game.virtual_height) // self.tile_size + 1)

        loader = self.game.states["loading"].loader
        tick = pygame.time.get_ticks() * 0.005 # Frame indices
        
        for r in range(start_row, end_row):
            for c in range(start_col, end_col):
                tile_type = self.grid[r][c]
                # Dynamic tile sprite retrieval
                tile_sprite = loader.get_image(
                    f"t_{tile_type}", 
                    loader.create_tile_sprite,
                    tile_type, int(tick)
                )
                surface.blit(tile_sprite, (c * self.tile_size - cam_x, r * self.tile_size - cam_y))

        # 2.5D Depth Sorted rendering queue
        # Queue holds tuples (y_depth, draw_callback)
        draw_queue = []

        # Add Chests
        for chest in self.chests:
            chest_y = chest["y"]
            draw_queue.append((chest_y + 8, lambda surf, ch=chest: loader.draw_scenery_object(surf, "chest", ch["x"] - cam_x, ch["y"] - cam_y, ch["frame"])))

        # Add Scenery Obstacles (Trees/Mountains/Castles)
        for tree in self.trees:
            draw_queue.append((tree["y"] + 24, lambda surf, tr=tree: loader.draw_scenery_object(surf, tr["type"], tr["x"] - cam_x, tr["y"] - cam_y)))

        # Add Portal at end
        draw_queue.append((self.portal_rect.bottom, lambda surf: loader.draw_scenery_object(surf, "portal", self.portal_rect.centerx - cam_x, self.portal_rect.bottom - cam_y, int(tick))))

        # Add Teacher
        draw_queue.append((self.teacher.y + 60, lambda surf: self.teacher.draw(surf, tick)))

        # Add Roaming Monsters
        for m in self.monsters:
            draw_queue.append((m.y + 60, lambda surf, monster=m: monster.draw(surf)))

        # Add Player
        player = self.game.player
        draw_queue.append((player.y + 60, lambda surf: player.draw(surf)))

        # Sort draw queue by y_depth coordinate (lowest y drawn first)
        draw_queue.sort(key=lambda item: item[0])
        
        # Execute draws
        for _, draw_func in draw_queue:
            draw_func(surface)

        # Draw particle systems (flying numbers, sparks on explore map coordinates)
        # Note: Particles coordinates are map-based, so subtract camera offsets
        # Temporarily shift surface drawing offsets
        map_overlay_surf = pygame.Surface((self.map_w, self.map_h), pygame.SRCALPHA)
        self.particles.draw(map_overlay_surf)
        surface.blit(map_overlay_surf, (-cam_x, -cam_y))

        # Draw weather overlays (fixed camera screen bounds)
        self.weather.draw(surface)

        # Draw interaction prompt widgets
        self.teacher.draw_prompt(surface, player)
        for chest in self.chests:
            if not chest["opened"]:
                dist = math.sqrt((player.x - chest["x"])**2 + (player.y - chest["y"])**2)
                if dist < 60:
                    bx, by = chest["x"] - cam_x, chest["y"] - 35 - cam_y
                    font = get_font(12, is_bold=True)
                    t_surf = font.render("[E] Open", True, (255, 235, 100))
                    
                    bg_rect = pygame.Rect(bx - t_surf.get_width()//2 - 6, by - 4, t_surf.get_width() + 12, t_surf.get_height() + 8)
                    pygame.draw.rect(surface, (20, 20, 25), bg_rect, border_radius=4)
                    pygame.draw.rect(surface, (230, 185, 55), bg_rect, 1, border_radius=4)
                    surface.blit(t_surf, (bx - t_surf.get_width()//2, by))

        # Draw HUD bar in upper-right corner
        hud_w = 260
        hud_h = 75
        draw_rounded_panel(surface, (self.game.virtual_width - hud_w - 20, 20, hud_w, hud_h), (25, 22, 22), (165, 120, 25), border_radius=8, bg_alpha=200)
        
        # HUD statistics labels
        hud_font = get_font(14, is_bold=True)
        gold_surf = hud_font.render(f"Coins: {player.coins}", True, (255, 235, 100))
        lvl_surf = hud_font.render(f"Level: {player.level} ({player.xp} XP)", True, (220, 130, 250))
        hp_surf = hud_font.render(f"HP: {player.hp}/{player.max_hp}", True, (255, 120, 120))
        
        surface.blit(gold_surf, (self.game.virtual_width - hud_w + 5, 30))
        surface.blit(lvl_surf, (self.game.virtual_width - hud_w + 5, 50))
        surface.blit(hp_surf, (self.game.virtual_width - hud_w + 5, 70))
        
        # Interactive shop shortcut button
        # Allow click E or shortcut shop? Let's add an explicit "Visit Shop" button in explore state HUD!
        shop_btn_font = get_font(12, is_bold=True)
        shop_btn_rect = pygame.Rect(self.game.virtual_width - 100, 30, 70, 24)
        
        # Check mouse collision on shop button
        mouse_pos = self.game.get_logical_mouse_pos()
        hover_shop = shop_btn_rect.collidepoint(mouse_pos)
        
        pygame.draw.rect(surface, (50, 150, 80) if hover_shop else (30, 120, 60), shop_btn_rect, border_radius=4)
        pygame.draw.rect(surface, (255, 215, 0) if hover_shop else (165, 120, 25), shop_btn_rect, 1, border_radius=4)
        
        shop_txt = shop_btn_font.render("Shop [S]", True, (255, 255, 255))
        surface.blit(shop_txt, (shop_btn_rect.x + (shop_btn_rect.width - shop_txt.get_width())//2, shop_btn_rect.y + (shop_btn_rect.height - shop_txt.get_height())//2))
        
        # Check S click to open shop
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s] and not self.active_dialogue_box:
            # Check shop shortcut toggle
            self.game.change_state("shop")
            return
            
        # Clicking shop button directly
        if pygame.mouse.get_pressed()[0] and hover_shop:
            self.game.sounds.play_sfx("click")
            self.game.change_state("shop")
            return

        # Draw active Typewriter dialogue box on top
        if self.active_dialogue_box:
            self.active_dialogue_box.draw(surface)
