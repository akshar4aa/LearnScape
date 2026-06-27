import pygame
import math
import random
from src.engine.settings import VIRTUAL_WIDTH, VIRTUAL_HEIGHT

class AssetLoader:
    def __init__(self):
        # Image cache: stores generated surfaces
        self.images = {}

    def get_image(self, key, creator_func, *args):
        """Checks cache, and generates asset if missing."""
        cache_key = f"{key}_{'_'.join(str(a) for a in args)}" if args else key
        if cache_key not in self.images:
            self.images[cache_key] = creator_func(*args)
        return self.images[cache_key]

    # --- PROCEDURAL PIXEL ART GENERATORS ---

    def create_character_frame(self, frame_type, hair_color, outfit_color, pose_tick=0):
        """
        Generates a 32x32 pixel character sprite frame.
        frame_type: 'idle', 'walk_1', 'walk_2', 'run_1', 'run_2', 'interact'
        """
        surf = pygame.Surface((32, 32), pygame.SRCALPHA)
        
        # Color palettes
        skin_color = (250, 210, 180)
        boot_color = (60, 45, 30)
        belt_color = (50, 40, 30)
        eye_color = (40, 40, 50)
        
        # Shadow (translucent ellipse under character)
        shadow_surf = pygame.Surface((24, 8), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (0, 0, 0, 90), (0, 0, 24, 8))
        surf.blit(shadow_surf, (4, 24))
        
        # Vertical offsets based on animations (bobbing)
        y_off = 0
        leg_offset = 0
        arm_offset = 0
        
        if frame_type in ['walk_1', 'run_1']:
            y_off = -1
            leg_offset = 2
            arm_offset = 3
        elif frame_type in ['walk_2', 'run_2']:
            y_off = 0
            leg_offset = -2
            arm_offset = -3
        elif frame_type == 'idle':
            # Subtly bob up and down based on pose_tick
            y_off = 1 if pose_tick % 2 == 0 else 0

        # --- DRAW LEGS/BOOTS ---
        # Left Leg
        pygame.draw.rect(surf, boot_color, (10, 23 + leg_offset, 4, 5))
        # Right Leg
        pygame.draw.rect(surf, boot_color, (18, 23 - leg_offset, 4, 5))

        # --- DRAW BODY / OUTFIT ---
        # Torso
        pygame.draw.rect(surf, outfit_color, (9, 13 + y_off, 14, 10), border_radius=2)
        # Belt
        pygame.draw.rect(surf, belt_color, (9, 21 + y_off, 14, 2))
        
        # --- DRAW ARMS ---
        if frame_type == 'interact':
            # Right arm extended forward
            pygame.draw.rect(surf, skin_color, (23, 14 + y_off, 6, 4))
            pygame.draw.rect(surf, outfit_color, (18, 13 + y_off, 6, 5))
            # Left arm down
            pygame.draw.rect(surf, outfit_color, (6, 13 + y_off, 3, 7))
        else:
            # Left arm swings with arm_offset
            pygame.draw.rect(surf, outfit_color, (6, 13 + y_off + arm_offset, 3, 7), border_radius=1)
            pygame.draw.rect(surf, skin_color, (6, 20 + y_off + arm_offset, 3, 2))
            
            # Right arm swings opposite
            pygame.draw.rect(surf, outfit_color, (23, 13 + y_off - arm_offset, 3, 7), border_radius=1)
            pygame.draw.rect(surf, skin_color, (23, 20 + y_off - arm_offset, 3, 2))

        # --- DRAW HEAD & HAIR ---
        # Head (Skin)
        pygame.draw.circle(surf, skin_color, (16, 8 + y_off), 5)
        # Hair
        pygame.draw.rect(surf, hair_color, (10, 2 + y_off, 12, 6), border_radius=2) # Main hair
        pygame.draw.rect(surf, hair_color, (9, 4 + y_off, 3, 5)) # Side burn left
        pygame.draw.rect(surf, hair_color, (20, 4 + y_off, 3, 5)) # Side burn right
        
        # Eyes
        pygame.draw.rect(surf, eye_color, (13, 7 + y_off, 2, 2))
        pygame.draw.rect(surf, eye_color, (17, 7 + y_off, 2, 2))
        
        # Return scaled sprite (e.g. 64x64 for visual clarity)
        return pygame.transform.scale(surf, (64, 64))

    def create_monster_sprite(self, m_type, frame_idx=0):
        """Generates a 64x64 pixel sprite for subject monsters."""
        surf = pygame.Surface((64, 64), pygame.SRCALPHA)
        
        # Shadow
        shadow_surf = pygame.Surface((36, 12), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (0, 0, 0, 90), (0, 0, 36, 12))
        surf.blit(shadow_surf, (14, 48))
        
        bob = int(3 * math.sin(frame_idx * 0.5))
        
        if m_type == "slime":  # Math / Biology
            # Jell-O bouncing slime
            slime_color = (60, 160, 240) # Bright Blue
            core_color = (30, 100, 200)
            
            # Draw body
            pygame.draw.ellipse(surf, slime_color, (12, 20 + bob, 40, 30))
            pygame.draw.ellipse(surf, core_color, (16, 25 + bob, 32, 22))
            
            # Eyes
            pygame.draw.circle(surf, (255, 255, 255), (25, 32 + bob), 4)
            pygame.draw.circle(surf, (255, 255, 255), (39, 32 + bob), 4)
            pygame.draw.circle(surf, (0, 0, 0), (26, 32 + bob), 2)
            pygame.draw.circle(surf, (0, 0, 0), (38, 32 + bob), 2)
            
        elif m_type == "drone":  # Physics
            # Neon hovering drone
            metal_color = (130, 140, 150)
            glow_color = (255, 80, 255)
            
            # Base shape
            pygame.draw.circle(surf, metal_color, (32, 28 + bob), 16)
            pygame.draw.rect(surf, (60, 60, 65), (20, 28 + bob, 24, 6))
            
            # Neon core
            pygame.draw.circle(surf, glow_color, (32, 28 + bob), 6)
            
            # Rotor blades
            pygame.draw.line(surf, metal_color, (16, 12 + bob), (48, 12 + bob), 3)
            pygame.draw.line(surf, (30, 30, 30), (32, 12 + bob), (32, 20 + bob), 4)
            
        elif m_type == "fire_elemental":  # Chemistry
            # Fire particles body
            color_flame = (240, 90, 20)
            color_core = (255, 210, 50)
            
            # Flicker effect
            flicker = random.randint(-2, 2)
            pygame.draw.circle(surf, color_flame, (32, 28 + bob), 18 + flicker)
            pygame.draw.circle(surf, color_core, (32, 28 + bob), 10 + flicker)
            
            # Fiery tails
            for _ in range(8):
                fx = 32 + random.randint(-15, 15)
                fy = 28 + bob - random.randint(5, 22)
                pygame.draw.circle(surf, color_flame, (fx, fy), random.randint(3, 7))
                
            # Angry eyes
            pygame.draw.polygon(surf, (255, 255, 255), [(23, 26 + bob), (28, 29 + bob), (23, 31 + bob)])
            pygame.draw.polygon(surf, (255, 255, 255), [(41, 26 + bob), (36, 29 + bob), (41, 31 + bob)])
            
        elif m_type == "ent":  # Biology Forest
            # Bark green walking tree stump
            brown_bark = (100, 65, 35)
            leaf_green = (35, 150, 60)
            
            # Trunk
            pygame.draw.rect(surf, brown_bark, (22, 20 + bob, 20, 28), border_radius=4)
            # Foliage crown
            pygame.draw.circle(surf, leaf_green, (32, 16 + bob), 14)
            pygame.draw.circle(surf, leaf_green, (22, 14 + bob), 10)
            pygame.draw.circle(surf, leaf_green, (42, 14 + bob), 10)
            
            # Eyes (glowing yellow dots)
            pygame.draw.circle(surf, (240, 240, 50), (28, 28 + bob), 3)
            pygame.draw.circle(surf, (240, 240, 50), (36, 28 + bob), 3)
            
        elif m_type == "griffin":  # English Castle
            # Golden winged eagle/lion
            gold = (210, 160, 40)
            white = (245, 240, 230)
            
            # Lion body
            pygame.draw.rect(surf, gold, (18, 28 + bob, 28, 18), border_radius=5)
            # Legs
            pygame.draw.rect(surf, gold, (22, 44 + bob, 5, 8))
            pygame.draw.rect(surf, gold, (37, 44 + bob, 5, 8))
            # Head (white feathers)
            pygame.draw.circle(surf, white, (22, 22 + bob), 10)
            # Beak (yellow)
            pygame.draw.polygon(surf, (250, 200, 30), [(14, 20 + bob), (10, 23 + bob), (14, 26 + bob)])
            # Wings
            pygame.draw.ellipse(surf, white, (32, 16 + bob, 18, 24))
            
        elif m_type == "mummy":  # History Museum
            # Sandy wrapped skeleton
            wrap_color = (220, 210, 180)
            eye_red = (230, 40, 40)
            
            # Body
            pygame.draw.rect(surf, wrap_color, (20, 18 + bob, 24, 30), border_radius=3)
            # Black strips for gaps
            pygame.draw.line(surf, (20, 20, 20), (20, 24 + bob), (44, 24 + bob), 2)
            pygame.draw.line(surf, (20, 20, 20), (20, 34 + bob), (44, 34 + bob), 2)
            # Head
            pygame.draw.circle(surf, wrap_color, (32, 12 + bob), 8)
            # Red eyes
            pygame.draw.circle(surf, eye_red, (29, 11 + bob), 2)
            pygame.draw.circle(surf, eye_red, (35, 11 + bob), 2)

        elif m_type == "golem":  # Geography Island
            # Rock monster
            rock_color = (110, 110, 115)
            moss_green = (70, 130, 50)
            
            # Giant shoulders
            pygame.draw.rect(surf, rock_color, (12, 16 + bob, 40, 20), border_radius=6)
            # Head (small and nested)
            pygame.draw.rect(surf, rock_color, (26, 8 + bob, 12, 10), border_radius=2)
            # Moss highlights
            pygame.draw.circle(surf, moss_green, (32, 18 + bob), 6)
            # Big fist arms
            pygame.draw.rect(surf, rock_color, (6, 26 + bob, 10, 18), border_radius=3)
            pygame.draw.rect(surf, rock_color, (48, 26 + bob, 10, 18), border_radius=3)
            # Legs
            pygame.draw.rect(surf, rock_color, (18, 36 + bob, 10, 14))
            pygame.draw.rect(surf, rock_color, (36, 36 + bob, 10, 14))

        elif m_type == "virus":  # Computer Science
            # Hologram/glitch cyber block
            glow = (0, 255, 100)
            
            # Inner square
            pygame.draw.rect(surf, (20, 40, 30), (16, 16 + bob, 32, 32), border_radius=4)
            # Glitching borders
            pygame.draw.rect(surf, glow, (16, 16 + bob, 32, 32), 2, border_radius=4)
            
            # Tech matrix codes inside
            pygame.draw.line(surf, glow, (24, 22 + bob), (24, 30 + bob), 2)
            pygame.draw.line(surf, glow, (28, 34 + bob), (40, 34 + bob), 2)
            pygame.draw.circle(surf, glow, (38, 24 + bob), 3)

        elif m_type == "dragon":  # Final Boss
            # Large winged epic dragon
            red = (180, 20, 20)
            dark_red = (120, 10, 10)
            gold = (230, 180, 40)
            
            # Enlarged canvas for dragon (96x96 bounds scaled in 64x64 surf)
            drag_surf = pygame.Surface((128, 128), pygame.SRCALPHA)
            
            # Tail
            pygame.draw.rect(drag_surf, red, (15, 75 + bob, 40, 12), border_radius=4)
            pygame.draw.circle(drag_surf, dark_red, (15, 75 + bob), 8) # Spike
            
            # Body
            pygame.draw.ellipse(drag_surf, red, (35, 45 + bob, 65, 45))
            pygame.draw.ellipse(drag_surf, gold, (50, 65 + bob, 40, 20)) # Gold underbelly
            
            # Neck & Head
            pygame.draw.line(drag_surf, red, (85, 65 + bob), (105, 35 + bob), 12)
            pygame.draw.circle(drag_surf, red, (105, 30 + bob), 16)
            pygame.draw.polygon(drag_surf, (30, 30, 30), [(105, 25 + bob), (115, 28 + bob), (105, 32 + bob)]) # Horn
            
            # Wings (Left & Right flapping)
            wing_flap = int(10 * math.sin(frame_idx * 0.8))
            pygame.draw.polygon(drag_surf, dark_red, [
                (55, 45 + bob), 
                (35 - wing_flap, 10 + bob), 
                (75 - wing_flap, 25 + bob)
            ])
            pygame.draw.polygon(drag_surf, dark_red, [
                (70, 45 + bob), 
                (95 + wing_flap, 10 + bob), 
                (80 + wing_flap, 25 + bob)
            ])
            
            # Render downscaled onto 64x64
            surf.blit(pygame.transform.scale(drag_surf, (64, 64)), (0, 0))

        return surf

    def create_tile_sprite(self, tile_type, animation_frame=0):
        """Generates a 32x32 terrain tile sprite."""
        surf = pygame.Surface((32, 32))
        
        if tile_type == "grass":
            surf.fill((65, 145, 60))
            # Blade details
            pygame.draw.line(surf, (55, 125, 50), (4, 8), (4, 12), 2)
            pygame.draw.line(surf, (55, 125, 50), (22, 18), (24, 22), 2)
            pygame.draw.line(surf, (75, 160, 70), (14, 26), (16, 28), 2)
            
        elif tile_type == "water":
            # Animated ripples
            surf.fill((40, 110, 200))
            offset = int(4 * math.sin(animation_frame * 0.5))
            pygame.draw.line(surf, (80, 150, 240), (4 + offset, 8), (14 + offset, 8), 2)
            pygame.draw.line(surf, (80, 150, 240), (16 - offset, 24), (26 - offset, 24), 2)
            
        elif tile_type == "lava":
            # Red/Orange bubbling
            surf.fill((190, 40, 10))
            offset = int(3 * math.cos(animation_frame * 0.5))
            pygame.draw.line(surf, (240, 120, 20), (2 + offset, 12), (16 + offset, 12), 2)
            pygame.draw.line(surf, (240, 120, 20), (12 - offset, 26), (28 - offset, 26), 2)
            pygame.draw.circle(surf, (255, 200, 30), (24 + offset, 8), 2)
            
        elif tile_type == "dirt":
            surf.fill((110, 80, 50))
            # Rocks in dirt
            pygame.draw.rect(surf, (90, 65, 40), (6, 8, 4, 3))
            pygame.draw.rect(surf, (95, 70, 42), (20, 22, 3, 3))
            
        elif tile_type == "bridge":
            # Wooden planks
            surf.fill((139, 90, 43))
            pygame.draw.line(surf, (90, 55, 25), (0, 6), (32, 6), 2)
            pygame.draw.line(surf, (90, 55, 25), (0, 16), (32, 16), 2)
            pygame.draw.line(surf, (90, 55, 25), (0, 26), (32, 26), 2)
            # Vertical plank dividers
            pygame.draw.line(surf, (60, 40, 20), (8, 0), (8, 32), 1)
            pygame.draw.line(surf, (60, 40, 20), (24, 0), (24, 32), 1)
            
        elif tile_type == "wall":
            # Stone wall
            surf.fill((80, 80, 85))
            # Brick cracks/grid
            pygame.draw.rect(surf, (55, 55, 60), (0, 0, 32, 32), 1)
            pygame.draw.line(surf, (55, 55, 60), (0, 16), (32, 16), 2)
            pygame.draw.line(surf, (55, 55, 60), (16, 0), (16, 16), 2)
            pygame.draw.line(surf, (55, 55, 60), (8, 16), (8, 32), 2)
            pygame.draw.line(surf, (55, 55, 60), (24, 16), (24, 32), 2)
            
        elif tile_type == "ice":
            surf.fill((180, 230, 245))
            # Shimmer lines
            pygame.draw.line(surf, (255, 255, 255), (4, 4), (16, 4), 1)
            pygame.draw.line(surf, (220, 250, 255), (14, 18), (28, 18), 1)
            
        elif tile_type == "floor_tech":
            # Computer science city tiles
            surf.fill((20, 30, 35))
            pygame.draw.rect(surf, (0, 180, 100), (0, 0, 32, 32), 1)
            # Circuit line
            pygame.draw.line(surf, (0, 255, 140), (16, 0), (16, 16), 1)
            pygame.draw.line(surf, (0, 255, 140), (16, 16), (28, 16), 1)
            pygame.draw.circle(surf, (0, 255, 140), (28, 16), 2)
            
        return surf

    def create_item_sprite(self, item_name):
        """Generates a 48x48 icon for shop/inventory items."""
        surf = pygame.Surface((48, 48), pygame.SRCALPHA)
        
        # Golden grid slot border
        pygame.draw.rect(surf, (50, 45, 40), (0, 0, 48, 48), border_radius=4)
        pygame.draw.rect(surf, (165, 120, 25), (0, 0, 48, 48), 2, border_radius=4)
        
        # Center core icon
        if "sword" in item_name:
            # Blade colors
            blade_color = (200, 200, 210) if "silver" in item_name else (235, 190, 50)
            hilt_color = (130, 80, 30)
            guard_color = (180, 140, 40)
            
            # Hilt (slanted bottom-left to top-right)
            pygame.draw.line(surf, hilt_color, (12, 36), (18, 30), 4)
            # Guard
            pygame.draw.line(surf, guard_color, (14, 28), (22, 36), 3)
            # Blade
            pygame.draw.line(surf, blade_color, (18, 30), (36, 12), 4)
            # Tip highlight
            pygame.draw.circle(surf, (255, 255, 255), (36, 12), 2)
            
        elif "shield" in item_name:
            # Shield shape
            shield_color = (110, 110, 120) if "iron" in item_name else (200, 60, 60)
            rim_color = (190, 150, 40)
            
            # Rim outer
            pygame.draw.polygon(surf, rim_color, [(24, 8), (40, 14), (34, 34), (24, 42), (14, 34), (8, 14)])
            # Shield inner
            pygame.draw.polygon(surf, shield_color, [(24, 12), (36, 17), (31, 32), (24, 38), (17, 32), (12, 17)])
            
            if "dragon" in item_name:
                # Add gold dragon symbol inside
                pygame.draw.circle(surf, (220, 170, 30), (24, 22), 4)
                
        elif "armor" in item_name:
            plate_color = (150, 150, 160) if "iron" in item_name else (40, 40, 45)
            trim_color = (190, 150, 40)
            
            # Chestplate outline
            pygame.draw.rect(surf, plate_color, (12, 14, 24, 24), border_radius=4)
            # Shoulder cuts
            pygame.draw.rect(surf, (0, 0, 0, 0), (12, 14, 6, 8))
            pygame.draw.rect(surf, (0, 0, 0, 0), (30, 14, 6, 8))
            # Gold trim
            pygame.draw.rect(surf, trim_color, (12, 14, 24, 24), 2, border_radius=4)
            
        elif "potion" in item_name:
            # Flask body
            liquid_color = (220, 40, 40) if "health" in item_name else (40, 130, 240)
            
            # Cork
            pygame.draw.rect(surf, (139, 90, 43), (22, 8, 4, 5))
            # Neck
            pygame.draw.rect(surf, (200, 200, 220), (20, 13, 8, 6))
            # Bottle rounded base
            pygame.draw.circle(surf, (200, 200, 220), (24, 28), 11)
            pygame.draw.circle(surf, liquid_color, (24, 29), 8)
            # Reflection dot
            pygame.draw.circle(surf, (255, 255, 255), (20, 25), 2)
            
        elif "book" in item_name:
            cover_color = (30, 60, 150) if "magic" in item_name else (140, 30, 180)
            
            # Book cover angled
            pygame.draw.rect(surf, cover_color, (12, 10, 24, 28), border_radius=2)
            # Pages side
            pygame.draw.rect(surf, (240, 235, 220), (32, 12, 4, 24))
            # Emblem on cover (gold star)
            pygame.draw.circle(surf, (230, 180, 40), (22, 24), 4)
            
        elif "scroll" in item_name:
            # Rolled parchment
            pygame.draw.rect(surf, (230, 210, 170), (10, 14, 28, 20), border_radius=2)
            # Wooden rollers
            pygame.draw.rect(surf, (110, 70, 30), (7, 12, 3, 24))
            pygame.draw.rect(surf, (110, 70, 30), (38, 12, 3, 24))
            # Red ribbon tying scroll
            pygame.draw.rect(surf, (200, 40, 40), (22, 14, 4, 20))
            
        elif "card" in item_name:
            # Card shape
            pygame.draw.rect(surf, (240, 240, 245), (12, 8, 24, 32), border_radius=2)
            pygame.draw.rect(surf, (40, 120, 220), (12, 8, 24, 32), 2, border_radius=2)
            # Question mark inside card
            font = pygame.font.SysFont("arial", 18, bold=True)
            text_surf = font.render("?", True, (40, 120, 220))
            surf.blit(text_surf, (20, 14))
            
        else: # Generic gem / coin reward icon
            # Diamond shape
            pygame.draw.polygon(surf, (40, 220, 240), [(24, 10), (36, 20), (24, 38), (12, 20)])
            # Glimmer
            pygame.draw.line(surf, (255, 255, 255), (24, 14), (24, 30), 1)

        return surf

    def draw_scenery_object(self, surface, obj_type, x, y, frame_tick=0):
        """Draws complex map assets (trees, rocks, castles, bridges, portals) onto maps."""
        
        if obj_type == "tree_pine":
            # Pine tree (layers of green triangles)
            trunk_w, trunk_h = 8, 12
            pygame.draw.rect(surface, (100, 65, 30), (x - trunk_w//2, y - trunk_h, trunk_w, trunk_h)) # Trunk
            
            # Layers of foliage
            pygame.draw.polygon(surface, (30, 95, 45), [(x, y - trunk_h - 26), (x - 22, y - trunk_h), (x + 22, y - trunk_h)])
            pygame.draw.polygon(surface, (35, 110, 50), [(x, y - trunk_h - 36), (x - 18, y - trunk_h - 10), (x + 18, y - trunk_h - 10)])
            pygame.draw.polygon(surface, (40, 125, 55), [(x, y - trunk_h - 44), (x - 14, y - trunk_h - 20), (x + 14, y - trunk_h - 20)])
            
        elif obj_type == "tree_oak":
            # Oak tree (round foliage)
            trunk_w, trunk_h = 10, 16
            pygame.draw.rect(surface, (90, 55, 25), (x - trunk_w//2, y - trunk_h, trunk_w, trunk_h)) # Trunk
            # Foliage spheres
            pygame.draw.circle(surface, (40, 130, 50), (x, y - trunk_h - 16), 18)
            pygame.draw.circle(surface, (45, 145, 55), (x - 12, y - trunk_h - 12), 14)
            pygame.draw.circle(surface, (45, 145, 55), (x + 12, y - trunk_h - 12), 14)
            pygame.draw.circle(surface, (55, 160, 65), (x, y - trunk_h - 24), 12)
            
        elif obj_type == "chest":
            # Animated chest box. Width = 32, Height = 32
            # frame_tick = 0 (closed), 1 (opening), 2 (open)
            box_color = (139, 90, 43)
            iron_trim = (100, 100, 105)
            gold_lock = (220, 180, 40)
            
            cx, cy = x - 16, y - 24
            
            # Base bottom (same for all)
            pygame.draw.rect(surface, box_color, (cx + 2, cy + 12, 28, 12), border_radius=1)
            pygame.draw.rect(surface, iron_trim, (cx + 2, cy + 12, 28, 12), 2, border_radius=1)
            
            if frame_tick == 0:  # Closed
                # Top lid closed
                pygame.draw.rect(surface, box_color, (cx + 2, cy + 4, 28, 8), border_radius=2)
                pygame.draw.rect(surface, iron_trim, (cx + 2, cy + 4, 28, 8), 2, border_radius=2)
                # Golden lock
                pygame.draw.rect(surface, gold_lock, (cx + 14, cy + 10, 4, 4))
            elif frame_tick == 1: # Opening
                # Lid tilted open
                pygame.draw.polygon(surface, box_color, [(cx+2, cy+4), (cx+10, cy-2), (cx+22, cy-2), (cx+30, cy+4)])
                pygame.draw.polygon(surface, iron_trim, [(cx+2, cy+4), (cx+10, cy-2), (cx+22, cy-2), (cx+30, cy+4)], 1)
                # Interior glow
                pygame.draw.rect(surface, (255, 220, 100), (cx + 6, cy + 8, 20, 4))
            else: # Open
                # Lid fully back
                pygame.draw.rect(surface, box_color, (cx + 4, cy - 4, 24, 8), border_radius=2)
                # Glowing treasure gold inside
                pygame.draw.ellipse(surface, (255, 215, 0), (cx + 4, cy + 6, 24, 8))
                
        elif obj_type == "portal":
            # Magical glowing teleportation portal
            # Animated rotating rings
            cx, cy = x, y - 32
            radius_x = int(24 + 4 * math.sin(frame_tick * 0.4))
            radius_y = 48
            
            # Layered ellipses for swirling effect
            portal_colors = [(130, 50, 240, 80), (80, 120, 255, 140), (255, 255, 255, 220)]
            for idx, color in enumerate(portal_colors):
                temp_surf = pygame.Surface((radius_x*2, radius_y*2), pygame.SRCALPHA)
                rx = radius_x - idx * 6
                ry = radius_y - idx * 10
                if rx > 0 and ry > 0:
                    pygame.draw.ellipse(temp_surf, color, (radius_x - rx, radius_y - ry, rx * 2, ry * 2), 4)
                    surface.blit(temp_surf, (cx - radius_x, cy - radius_y))
                    
            # Glowing base circle
            pygame.draw.ellipse(surface, (100, 60, 220, 150), (cx - 16, cy + 32, 32, 10))

        elif obj_type == "mountain":
            # Snowy triangular mountain peek
            pygame.draw.polygon(surface, (80, 85, 95), [(x, y - 60), (x - 50, y), (x + 50, y)])
            # Snow peak
            pygame.draw.polygon(surface, (245, 245, 250), [(x, y - 60), (x - 18, y - 38), (x + 18, y - 38)])
            pygame.draw.polygon(surface, (220, 220, 230), [(x, y - 60), (x - 10, y - 38), (x - 5, y - 30), (x + 5, y - 35), (x + 10, y - 38)])
            
        elif obj_type == "castle":
            # Ancient fantasy castle structures
            cx, cy = x - 40, y - 80
            # Base stone wall
            pygame.draw.rect(surface, (100, 100, 105), (cx + 10, cy + 30, 60, 50), border_radius=2)
            # Crenellations (top bricks)
            for bx in range(cx + 10, cx + 70, 12):
                pygame.draw.rect(surface, (80, 80, 85), (bx, cy + 24, 8, 6))
            # Wooden door
            pygame.draw.rect(surface, (90, 50, 20), (cx + 30, cy + 50, 20, 30), border_radius=6)
            # Left tower spire
            pygame.draw.rect(surface, (90, 90, 95), (cx, cy + 10, 16, 70), border_radius=1)
            pygame.draw.polygon(surface, (180, 40, 40), [(cx + 8, cy - 10), (cx - 2, cy + 10), (cx + 18, cy + 10)]) # Cone roof
            # Right tower spire
            pygame.draw.rect(surface, (90, 90, 95), (cx + 64, cy + 10, 16, 70), border_radius=1)
            pygame.draw.polygon(surface, (180, 40, 40), [(cx + 72, cy - 10), (cx + 62, cy + 10), (cx + 82, cy + 10)])
            
        elif obj_type == "village_house":
            # Small wooden RPG village house
            cx, cy = x - 30, y - 45
            # Walls
            pygame.draw.rect(surface, (139, 115, 85), (cx + 5, cy + 15, 50, 30), border_radius=2)
            # Door
            pygame.draw.rect(surface, (80, 50, 20), (cx + 24, cy + 25, 12, 20))
            # Window
            pygame.draw.rect(surface, (255, 230, 120), (cx + 10, cy + 20, 8, 8))
            pygame.draw.rect(surface, (80, 50, 20), (cx + 10, cy + 20, 8, 8), 1)
            # Roof (triangular)
            pygame.draw.polygon(surface, (160, 50, 40), [(cx + 30, cy - 2), (cx - 2, cy + 16), (cx + 62, cy + 16)])
