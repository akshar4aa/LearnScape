import pygame
from src.engine.state import State
from src.ui.ui_elements import Button
from src.utils.helpers import get_font, draw_rounded_panel, draw_gradient_rect

class AchievementsState(State):
    def __init__(self, game):
        super().__init__(game)
        
        self.metrics = {}
        self.progress = {}
        self.achievements_list = []
        
        self.font_title = get_font(28, is_bold=True)
        self.font_header = get_font(20, is_bold=True)
        self.font_stat_val = get_font(18, is_bold=True)
        self.font_desc = get_font(12)
        
        self.btn_back = Button(self.game, 40, 620, 180, 45, "Back to Menu", self.go_back, color=(120, 50, 50))

    def go_back(self):
        self.game.change_state("menu")

    def enter(self):
        # Load latest metrics and progress from SQLite
        self.metrics = self.game.db.load_metrics()
        self.progress = self.game.db.load_progress()
        
        # Safe default maps
        if not self.metrics:
            self.metrics = {
                "total_study_time": 0.0,
                "total_questions": 0,
                "correct_questions": 0,
                "monsters_defeated": 0,
                "bosses_defeated": 0
            }
            
        self.evaluate_achievements()
        self.game.sounds.play_music("menu")

    def exit(self):
        pass

    def evaluate_achievements(self):
        """Checks metric values to determine achievement unlocks dynamically."""
        self.achievements_list = []
        
        # 1. First Victory
        first_vic = self.metrics["monsters_defeated"] >= 1
        self.achievements_list.append({
            "title": "First Victory",
            "desc": "Defeat your first subject monster.",
            "unlocked": first_vic
        })
        
        # 2. 50 Correct answers
        seeker = self.metrics["correct_questions"] >= 25
        self.achievements_list.append({
            "title": "Knowledge Seeker",
            "desc": "Correctly answer 25 questions.",
            "unlocked": seeker
        })

        # 3. Math Master
        math_done = False
        if "mathematics" in self.progress:
            math_done = self.progress["mathematics"]["completed"]
        self.achievements_list.append({
            "title": "Math Scholar",
            "desc": "Complete the Mathematics Kingdom.",
            "unlocked": math_done
        })
        
        # 4. Science Master
        chem_done = self.progress.get("chemistry", {}).get("completed", False)
        phys_done = self.progress.get("physics", {}).get("completed", False)
        self.achievements_list.append({
            "title": "Science Genius",
            "desc": "Master Chemistry Volcano or Physics Lab.",
            "unlocked": chem_done or phys_done
        })

        # 5. CS Wizard
        cs_done = self.progress.get("computer_science", {}).get("completed", False)
        self.achievements_list.append({
            "title": "CS Wizard",
            "desc": "Conquer Computer Science City.",
            "unlocked": cs_done
        })

        # 6. Scholarly Legend
        legend = self.metrics["bosses_defeated"] >= 5
        self.achievements_list.append({
            "title": "Scholarly Legend",
            "desc": "Defeat 5 or more Arch-Bosses.",
            "unlocked": legend
        })

    def format_time(self, seconds):
        mins = int(seconds) // 60
        secs = int(seconds) % 60
        return f"{mins}m {secs}s"

    def handle_event(self, event):
        mouse_pos = self.game.get_logical_mouse_pos()
        self.btn_back.handle_event(event, mouse_pos)

    def update(self, dt):
        mouse_pos = self.game.get_logical_mouse_pos()
        self.btn_back.update(dt, mouse_pos)

    def draw(self, surface):
        # Background gradient
        draw_gradient_rect(surface, (18, 12, 28), (10, 20, 35), (0, 0, self.game.virtual_width, self.game.virtual_height))
        
        # Header
        title_surf = self.font_title.render("LEARNING METRICS & ACHIEVEMENTS", True, (255, 235, 120))
        surface.blit(title_surf, ((self.game.virtual_width - title_surf.get_width())//2, 35))
        
        # Left Panel (Statistics list)
        draw_rounded_panel(surface, (70, 110, 480, 480), (25, 25, 30), (165, 120, 25), border_width=2)
        
        # Right Panel (Achievements list)
        draw_rounded_panel(surface, (700, 110, 480, 480), (20, 20, 24), (165, 120, 25), border_width=2)

        # Draw Statistics
        stat_head = self.font_header.render("STUDY METRICS", True, (230, 185, 55))
        surface.blit(stat_head, (70 + (480 - stat_head.get_width())//2, 130))
        
        # Compute Accuracy
        total_q = self.metrics["total_questions"]
        correct_q = self.metrics["correct_questions"]
        accuracy = (correct_q / total_q) * 100.0 if total_q > 0 else 100.0
        
        stats_list = [
            ("Accuracy Percentage:", f"{accuracy:.1f}%", (80, 220, 140)),
            ("Total Questions Answered:", str(total_q), (255, 255, 255)),
            ("Correct Answers Solved:", str(correct_q), (255, 255, 255)),
            ("Monsters Defeated:", str(self.metrics["monsters_defeated"]), (255, 255, 255)),
            ("Arch-Bosses Slain:", str(self.metrics["bosses_defeated"]), (255, 255, 255)),
            ("Total Study Time:", self.format_time(self.metrics["total_study_time"]), (255, 215, 0))
        ]
        
        for idx, (label, val, val_color) in enumerate(stats_list):
            ly = 185 + idx * 56
            
            lbl_surf = get_font(16, is_bold=True).render(label, True, (200, 200, 210))
            val_surf = self.font_stat_val.render(val, True, val_color)
            
            # Draw line backdrop row
            pygame.draw.rect(surface, (35, 35, 42), (90, ly, 440, 46), border_radius=4)
            surface.blit(lbl_surf, (105, ly + 13))
            surface.blit(val_surf, (510 - val_surf.get_width(), ly + 13))

        # Draw Achievements List
        ach_head = self.font_header.render("UNLOCKED ACHIEVEMENTS", True, (230, 185, 55))
        surface.blit(ach_head, (700 + (480 - ach_head.get_width())//2, 130))
        
        for idx, ach in enumerate(self.achievements_list):
            ay = 180 + idx * 62
            
            bg_color = (40, 50, 40) if ach["unlocked"] else (30, 30, 32)
            border_glow = (50, 200, 80) if ach["unlocked"] else (80, 80, 85)
            
            draw_rounded_panel(surface, (720, ay, 440, 52), bg_color, border_glow, border_width=2, border_radius=6)
            
            # Title
            t_color = (255, 235, 100) if ach["unlocked"] else (130, 130, 135)
            t_surf = get_font(14, is_bold=True).render(ach["title"], True, t_color)
            surface.blit(t_surf, (735, ay + 8))
            
            # Description
            d_surf = self.font_desc.render(ach["desc"], True, (200, 200, 205) if ach["unlocked"] else (110, 110, 115))
            surface.blit(d_surf, (735, ay + 28))
            
            # Unlock badge checkmark
            badge_txt = "[UNLOCKED]" if ach["unlocked"] else "[LOCKED]"
            badge_color = (80, 220, 140) if ach["unlocked"] else (120, 120, 125)
            badge_surf = get_font(12, is_bold=True).render(badge_txt, True, badge_color)
            surface.blit(badge_surf, (1145 - badge_surf.get_width(), ay + 18))

        # Render back btn
        self.btn_back.draw(surface)
