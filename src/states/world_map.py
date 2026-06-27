import pygame
import math
from src.engine.state import State
from src.ui.ui_elements import Button
from src.utils.helpers import get_font, draw_rounded_panel, draw_glowing_text, draw_gradient_rect

class WorldMapState(State):
    def __init__(self, game):
        super().__init__(game)
        
        self.font_title = get_font(28, is_bold=True)
        self.font_badge = get_font(14, is_bold=True)
        self.font_desc = get_font(12)
        
        # Kingdoms configs
        self.kingdoms = {
            "mathematics": {
                "pos": (180, 500),
                "title": "Math Kingdom",
                "subject": "Mathematics",
                "desc": "Conquer fractions, algebra & arithmetic.",
                "color": (50, 100, 240)
            },
            "biology": {
                "pos": (320, 440),
                "title": "Biology Forest",
                "subject": "Biology",
                "desc": "Examine plants, ecosystems & human cells.",
                "color": (40, 180, 60)
            },
            "chemistry": {
                "pos": (450, 220),
                "title": "Chemistry Volcano",
                "subject": "Chemistry",
                "desc": "Solve elements, atomic bonds & states of matter.",
                "color": (230, 90, 20)
            },
            "physics": {
                "pos": (580, 340),
                "title": "Physics Laboratory",
                "subject": "Physics",
                "desc": "Determine energy, forces, gravity & motion.",
                "color": (150, 50, 220)
            },
            "science": {
                "pos": (680, 520),
                "title": "Science Kingdom",
                "subject": "General Science",
                "desc": "Explore weather, planetary orbits & space.",
                "color": (20, 160, 180)
            },
            "english": {
                "pos": (840, 400),
                "title": "English Castle",
                "subject": "English Language",
                "desc": "Master verbs, adjectives, spellings & essays.",
                "color": (210, 160, 40)
            },
            "history": {
                "pos": (880, 200),
                "title": "History Museum",
                "subject": "World History",
                "desc": "Explore medieval empires, artifacts & legends.",
                "color": (160, 100, 50)
            },
            "geography": {
                "pos": (1020, 460),
                "title": "Geography Island",
                "subject": "Geography",
                "desc": "Identify oceans, flags, capitals & rivers.",
                "color": (40, 200, 220)
            },
            "computer_science": {
                "pos": (1080, 250),
                "title": "CS Cyber-City",
                "subject": "Computer Science",
                "desc": "Decode coding, binary numbers & algorithm loops.",
                "color": (30, 210, 100)
            }
        }
        
        self.progression_order = [
            "mathematics", "biology", "chemistry", "physics", 
            "science", "english", "history", "geography", "computer_science"
        ]
        
        # State values
        self.progress = {}
        self.hovered_k = None
        self.pulse_timer = 0.0
        
        # Back button
        self.btn_back = Button(self.game, 30, 30, 110, 38, "Main Menu", self.go_back, color=(80, 80, 90))

    def go_back(self):
        self.game.change_state("menu")

    def enter(self):
        # Load progress from SQLite
        self.progress = self.game.db.load_progress()
        
        # If progress is empty (first boot/new game), set up default progress dict
        if not self.progress:
            # Mathematics is initially unlocked, others locked
            for idx, k_id in enumerate(self.progression_order):
                self.progress[k_id] = {
                    "unlocked": (idx == 0),
                    "completed": False,
                    "boss_defeated": False,
                    "quests_done": []
                }
            self.game.db.save_progress(self.progress)
        else:
            # Recheck progression locks based on completions
            for idx, k_id in enumerate(self.progression_order):
                if idx == 0:
                    self.progress[k_id]["unlocked"] = True
                else:
                    prev_k = self.progression_order[idx - 1]
                    # Unlock current if previous is completed/boss defeated
                    if self.progress[prev_k]["completed"] or self.progress[prev_k]["boss_defeated"]:
                        self.progress[k_id]["unlocked"] = True
            self.game.db.save_progress(self.progress)
            
        self.game.sounds.play_music("menu")

    def exit(self):
        pass

    def handle_event(self, event):
        mouse_pos = self.game.get_logical_mouse_pos()
        
        # Button
        if self.btn_back.handle_event(event, mouse_pos):
            return
            
        # Click on kingdoms
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = mouse_pos
            for k_id, k_data in self.kingdoms.items():
                kx, ky = k_data["pos"]
                # Circle hit area check
                dist = math.sqrt((mx - kx)**2 + (my - ky)**2)
                if dist <= 24: # Radius of map dots is 18-20
                    if self.progress[k_id]["unlocked"]:
                        # Setup selected kingdom and transition to explore
                        self.game.sounds.play_sfx("portal")
                        
                        # Store selected world settings in explore state
                        self.game.states["explore"].set_active_kingdom(k_id)
                        self.game.change_state("explore")
                    else:
                        self.game.sounds.play_sfx("wrong") # Play wrong lock buzz
                    break

    def update(self, dt):
        mouse_pos = self.game.get_logical_mouse_pos()
        self.pulse_timer += dt * 4.0
        
        self.btn_back.update(dt, mouse_pos)
        
        # Check hoverings
        mx, my = mouse_pos
        self.hovered_k = None
        for k_id, k_data in self.kingdoms.items():
            kx, ky = k_data["pos"]
            dist = math.sqrt((mx - kx)**2 + (my - ky)**2)
            if dist <= 24:
                self.hovered_k = k_id
                break

    def draw(self, surface):
        # Draw sky/grass green landscape gradient backdrop
        draw_gradient_rect(surface, (25, 45, 65), (55, 95, 75), (0, 0, surface.get_width(), surface.get_height()))
        
        # Title Header
        title_surf = self.font_title.render("LEARNSCAPE WORLD MAP", True, (255, 235, 120))
        surface.blit(title_surf, ((self.game.virtual_width - title_surf.get_width())//2, 35))
        
        # --- DRAW PROGRESSION PATHS / LINES ---
        for idx in range(len(self.progression_order) - 1):
            k1_id = self.progression_order[idx]
            k2_id = self.progression_order[idx + 1]
            
            p1 = self.kingdoms[k1_id]["pos"]
            p2 = self.kingdoms[k2_id]["pos"]
            
            # Check if both are unlocked
            if self.progress[k2_id]["unlocked"]:
                # Glowing solid path line
                pygame.draw.line(surface, (255, 220, 100), p1, p2, 4)
            else:
                # Grey dashed path line
                # Draw small steps
                steps = 15
                for s in range(steps):
                    t = s / steps
                    nt = (s + 0.5) / steps
                    start_pos = (int(p1[0] + (p2[0]-p1[0])*t), int(p1[1] + (p2[1]-p1[1])*t))
                    end_pos = (int(p1[0] + (p2[0]-p1[0])*nt), int(p1[1] + (p2[1]-p1[1])*nt))
                    pygame.draw.line(surface, (80, 85, 95), start_pos, end_pos, 2)

        # --- DRAW KINGDOM DOTS ---
        for k_id, k_data in self.kingdoms.items():
            kx, ky = k_data["pos"]
            unlocked = self.progress[k_id]["unlocked"]
            
            # Pulse size for unlocked/hovered
            pulse = int(3 * math.sin(self.pulse_timer)) if (self.hovered_k == k_id and unlocked) else 0
            radius = 18 + pulse
            
            if unlocked:
                # Solid colored core with golden border
                pygame.draw.circle(surface, k_data["color"], (kx, ky), radius)
                pygame.draw.circle(surface, (255, 235, 120), (kx, ky), radius, 2)
                # Outer pulse rings
                pygame.draw.circle(surface, (*k_data["color"], 80), (kx, ky), radius + 6, 2)
                
                # Draw checkmark or mini crown if completed
                if self.progress[k_id]["completed"]:
                    # Draw a mini crown/star
                    star_font = get_font(12, is_bold=True)
                    star_surf = star_font.render("*", True, (255, 215, 0))
                    surface.blit(star_surf, (kx - star_surf.get_width()//2, ky - star_surf.get_height()//2 - 1))
            else:
                # Locked stone dot
                pygame.draw.circle(surface, (60, 60, 65), (kx, ky), 16)
                pygame.draw.circle(surface, (30, 30, 32), (kx, ky), 16, 2)
                
                # Lock symbol "L" or icon
                lock_font = get_font(10, is_bold=True)
                lock_surf = lock_font.render("X", True, (130, 130, 140))
                surface.blit(lock_surf, (kx - lock_surf.get_width()//2, ky - lock_surf.get_height()//2 - 1))

        # --- DRAW HOVERING INFO CARD BADGE ---
        if self.hovered_k:
            k_data = self.kingdoms[self.hovered_k]
            unlocked = self.progress[self.hovered_k]["unlocked"]
            kx, ky = k_data["pos"]
            
            # Position above hovered kingdom
            bx = kx - 120
            by = ky - 95
            
            # Bound inside screen
            bx = max(20, min(self.game.virtual_width - 260, bx))
            by = max(90, by)
            
            draw_rounded_panel(surface, (bx, by, 240, 75), (20, 20, 25), (230, 185, 55) if unlocked else (80, 80, 85), border_width=2)
            
            # Title
            title = k_data["title"] if unlocked else "Locked Realm"
            title_surf = self.font_badge.render(title, True, (255, 235, 120) if unlocked else (150, 150, 160))
            surface.blit(title_surf, (bx + 12, by + 10))
            
            # Subject & Desc
            sub = f"Subject: {k_data['subject']}" if unlocked else "Requirements: Beat previous kingdom"
            sub_surf = self.font_desc.render(sub, True, (200, 200, 210) if unlocked else (230, 100, 100))
            surface.blit(sub_surf, (bx + 12, by + 28))
            
            if unlocked:
                desc_surf = self.font_desc.render(k_data["desc"], True, (150, 150, 160))
                surface.blit(desc_surf, (bx + 12, by + 46))
                
        # Draw back button
        self.btn_back.draw(surface)
