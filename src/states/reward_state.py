import pygame
import math
from src.states.state import State
from src.ui.background import Background
from src.utils.save_system import SaveSystem

class RewardState(State):
    def __init__(self, game, planet, lesson_name, xp_earned, coins_earned):
        super().__init__(game)
        self.planet = planet
        self.lesson_name = lesson_name
        self.xp_earned = xp_earned
        self.coins_earned = coins_earned

        width = self.game.screen.get_width()
        height = self.game.screen.get_height()
        self.background = Background(width, height)

        self.title_font = pygame.font.SysFont("arial", 56, bold=True)
        self.heading_font = pygame.font.SysFont("arial", 28, bold=True)
        self.text_font = pygame.font.SysFont("arial", 22)
        self.badge_font = pygame.font.SysFont("arial", 32)
        
        self.time = 0.0
        self.leveled_up = False
        self.new_planets = []
        self.new_achievements = []

        # Process progression
        self.process_progression()

        # Save data
        self.save_progress()

        # Continue Button
        self.button_rect = pygame.Rect(470, 540, 340, 55)

    def process_progression(self):
        # Add lesson to completed
        lesson_key = f"{self.planet}_{self.lesson_name}"
        if lesson_key not in self.game.completed_lessons:
            self.game.completed_lessons.append(lesson_key)

        # Cache old stats
        old_level = self.game.level
        
        # Add XP and Coins
        self.game.xp += self.xp_earned
        self.game.coins += self.coins_earned

        # Check Level Up (XP threshold = level * 100)
        while self.game.xp >= self.game.level * 100:
            self.game.xp -= self.game.level * 100
            self.game.level += 1
            self.leveled_up = True
            
        if self.leveled_up:
            if hasattr(self.game, 'audio'):
                self.game.audio.play_sfx("assets/audio/level_up.wav")

        # Planet Unlocks
        if self.game.level >= 2 and "Jupiter" not in self.game.unlocked_planets:
            self.game.unlocked_planets.append("Jupiter")
            self.new_planets.append("Jupiter")
        if self.game.level >= 3 and "Saturn" not in self.game.unlocked_planets:
            self.game.unlocked_planets.append("Saturn")
            self.new_planets.append("Saturn")

        # Achievement unlocks
        if len(self.game.completed_lessons) >= 1 and "First Steps" not in self.game.achievements:
            self.game.achievements.append("First Steps")
            self.new_achievements.append("First Steps")

        earth_lessons = ["Numbers", "Addition", "Subtraction", "Multiplication", "Division", "Fractions", "Decimals"]
        has_all_earth = all(f"Earth_{l}" in self.game.completed_lessons for l in earth_lessons)
        if has_all_earth and "Math Explorer" not in self.game.achievements:
            self.game.achievements.append("Math Explorer")
            self.new_achievements.append("Math Explorer")

        if self.game.coins >= 50 and "Wealthy" not in self.game.achievements:
            self.game.achievements.append("Wealthy")
            self.new_achievements.append("Wealthy")

    def save_progress(self):
        save_data = {
            "hero_name": self.game.hero_name,
            "char_type": self.game.char_type,
            "xp": self.game.xp,
            "coins": self.game.coins,
            "level": self.game.level,
            "unlocked_planets": self.game.unlocked_planets,
            "completed_lessons": self.game.completed_lessons,
            "achievements": self.game.achievements
        }
        SaveSystem.save(save_data)

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
                return

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.button_rect.collidepoint(mouse_pos):
                    self.continue_to_map()
                    return

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.continue_to_map()
                    return

    def continue_to_map(self):
        if hasattr(self.game, 'audio'):
            self.game.audio.play_sfx("assets/audio/click.wav")
        from src.states.world_map_state import WorldMapState
        self.game.change_state(WorldMapState(self.game))

    def update(self, dt):
        self.time += dt
        self.background.update(dt)

    def draw(self, screen):
        self.background.draw(screen)

        # Title
        title_surf = self.title_font.render("Rewards Summary", True, (255, 220, 80))
        screen.blit(title_surf, title_surf.get_rect(center=(640, 70)))

        # Panel Backing
        panel = pygame.Rect(280, 140, 720, 370)
        pygame.draw.rect(screen, (25, 30, 48), panel, border_radius=15)
        pygame.draw.rect(screen, (255, 220, 80), panel, 2, border_radius=15)

        # Reward details
        y_offset = 180
        
        # XP
        xp_txt = self.heading_font.render(f"XP Gained: +{self.xp_earned} XP", True, (100, 180, 255))
        screen.blit(xp_txt, xp_txt.get_rect(center=(640, y_offset)))
        y_offset += 45

        # Coins
        coins_txt = self.heading_font.render(f"Coins Collected: 🪙 +{self.coins_earned}", True, (255, 215, 0))
        screen.blit(coins_txt, coins_txt.get_rect(center=(640, y_offset)))
        y_offset += 55

        # Level up notifier
        if self.leveled_up:
            pulse = 1.0 + math.sin(self.time * 6) * 0.04
            lvl_font = pygame.font.SysFont("arial", int(34 * pulse), bold=True)
            lvl_txt = lvl_font.render(f"LEVEL UP! REACHED LEVEL {self.game.level}!", True, (100, 255, 100))
            screen.blit(lvl_txt, lvl_txt.get_rect(center=(640, y_offset)))
            y_offset += 55
        else:
            # XP Remaining indicator
            xp_needed = self.game.level * 100 - self.game.xp
            progress_txt = self.text_font.render(f"Progress to Level {self.game.level+1}: {self.game.xp}/{self.game.level*100} XP (Need {xp_needed} more)", True, (200, 200, 220))
            screen.blit(progress_txt, progress_txt.get_rect(center=(640, y_offset)))
            y_offset += 45

        # Planet unlocked indicator
        if self.new_planets:
            planets_str = ", ".join(self.new_planets)
            unlock_txt = self.heading_font.render(f"🪐 UNLOCKED NEW PLANETS: {planets_str}!", True, (255, 220, 80))
            screen.blit(unlock_txt, unlock_txt.get_rect(center=(640, y_offset)))
            y_offset += 45

        # Achievement indicator
        if self.new_achievements:
            ach_str = ", ".join(self.new_achievements)
            ach_txt = self.heading_font.render(f"🏆 NEW ACHIEVEMENTS: {ach_str}!", True, (100, 255, 255))
            screen.blit(ach_txt, ach_txt.get_rect(center=(640, y_offset)))
            
        # Draw some unlocked badges iconically if any exist
        if self.game.achievements:
            badge_y = 430
            badge_lbl = self.text_font.render("Your Achievements Badges:", True, (150, 150, 160))
            screen.blit(badge_lbl, badge_lbl.get_rect(center=(640, badge_y)))
            
            badge_start_x = 640 - (len(self.game.achievements) * 60) // 2
            for idx, badge in enumerate(self.game.achievements):
                bx = badge_start_x + idx * 60 + 30
                by = badge_y + 40
                # Draw badge circle
                pygame.draw.circle(screen, (75, 45, 115), (bx, by), 22)
                pygame.draw.circle(screen, (255, 215, 0), (bx, by), 22, 2)
                # Badge symbol emoji
                sym = "🧭" if badge == "First Steps" else ("🎓" if badge == "Math Explorer" else "💰")
                sym_surf = self.badge_font.render(sym, True, (255, 255, 255))
                screen.blit(sym_surf, sym_surf.get_rect(center=(bx, by)))

        # Continue Button
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.button_rect.collidepoint(mouse_pos)
        btn_bg = (255, 235, 120) if hovered else (255, 220, 80)

        if hovered:
            btn_glow = pygame.Surface((self.button_rect.width + 20, self.button_rect.height + 20), pygame.SRCALPHA)
            pygame.draw.rect(btn_glow, (255, 220, 80, 50), btn_glow.get_rect(), border_radius=12)
            screen.blit(btn_glow, (self.button_rect.x - 10, self.button_rect.y - 10))

        pygame.draw.rect(screen, btn_bg, self.button_rect, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), self.button_rect, 2, border_radius=12)

        cont_font = pygame.font.SysFont("arial", 28, bold=True)
        cont_surf = cont_font.render("CONTINUE TO MAP", True, (20, 24, 35))
        screen.blit(cont_surf, cont_surf.get_rect(center=self.button_rect.center))

        # Bottom hint
        help_surf = self.text_font.render("ENTER/Click to Continue", True, (130, 130, 150))
        screen.blit(help_surf, help_surf.get_rect(center=(640, 660)))
