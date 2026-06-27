import pygame
import random
import os
import math

from src.states.state import State
from src.ui.battle_background import BattleBackground
from src.ui.healthbar import HealthBar
from src.ui.battle_button import BattleButton
from src.ui.popup import Popup

class QuizState(State):
    def __init__(self, game, planet, lesson_name):
        super().__init__(game)
        self.planet = planet
        self.lesson_name = lesson_name

        width = self.game.screen.get_width()
        height = self.game.screen.get_height()

        self.background = BattleBackground(width, height)
        self.popup = Popup()

        # HP Bars (5 hit points each)
        self.hero_hp = HealthBar(60, 120, 220, 22, 5)
        self.enemy_hp = HealthBar(1000, 120, 220, 22, 5)

        # Fonts
        self.title_font = pygame.font.SysFont("arial", 48, bold=True)
        self.question_font = pygame.font.SysFont("arial", 26, bold=True)
        self.small_font = pygame.font.SysFont("arial", 20)
        self.damage_font = pygame.font.SysFont("arial", 36, bold=True)

        # Load Questions dynamically
        self.questions_bank = []
        try:
            if self.planet == "Earth":
                from src.data.earth_questions import EARTH_QUESTIONS
                self.questions_bank = EARTH_QUESTIONS[self.lesson_name]
            elif self.planet == "Jupiter":
                from src.data.jupiter_questions import JUPITER_QUESTIONS
                self.questions_bank = JUPITER_QUESTIONS[self.lesson_name]
            else: # Saturn
                from src.data.saturn_questions import SATURN_QUESTIONS
                self.questions_bank = SATURN_QUESTIONS[self.lesson_name]
        except Exception as e:
            print(f"Error loading questions for {self.planet} - {self.lesson_name}: {e}")
            # Fallback dummy question bank
            self.questions_bank = [
                {"question": f"Is this a fallback quiz for {self.lesson_name}?", "options": ["Yes", "No", "Maybe", "Incorrect"], "answer": 0}
            ]

        self.question_indices = list(range(len(self.questions_bank)))
        random.shuffle(self.question_indices)

        # Battle stats
        self.combo = 0
        self.xp_earned = 0
        self.coins_earned = 0
        
        self.battle_ended = False
        self.end_timer = 0.0

        # Sprite loaders with fallbacks
        self.hero_sprite = self.load_sprite("assets/hero.png", (160, 160))
        if not self.hero_sprite:
            self.hero_sprite = self.load_sprite("assets/characters/player/hero.png", (160, 160))
            
        self.enemy_sprite = self.load_sprite("assets/alien.png", (160, 160))
        if not self.enemy_sprite:
            self.enemy_sprite = self.load_sprite("assets/characters/enemies/alien.png", (160, 160))

        # Animations
        self.hero_attack = 0.0
        self.enemy_shake = 0.0
        self.flash = 0.0
        self.damage_text = ""
        self.damage_y = 0.0
        self.damage_x = 0.0
        self.damage_color = (255, 80, 80)

        # Set up first question
        self.next_question()

    def load_sprite(self, path, size):
        if os.path.exists(path):
            try:
                img = pygame.image.load(path).convert_alpha()
                return pygame.transform.smoothscale(img, size)
            except Exception as e:
                print(f"Warning: Failed to load sprite at {path}: {e}")
        return None

    def next_question(self):
        if not self.question_indices:
            # Refill and reshuffle
            self.question_indices = list(range(len(self.questions_bank)))
            random.shuffle(self.question_indices)

        self.current_q_idx = self.question_indices.pop()
        q_data = self.questions_bank[self.current_q_idx]

        self.question_text = q_data["question"]
        self.options = q_data["options"]
        self.correct_answer = q_data["answer"]

        # Re-initialize buttons
        self.buttons = []
        start_y = 280
        for i, opt in enumerate(self.options):
            # Safeguard if list is too long, wrap around or limit text
            btn = BattleButton(340, start_y + i * 78, 600, 56, opt[:45])
            self.buttons.append(btn)

        self.selected = 0
        self.buttons[self.selected].selected = True

    def handle_events(self, events):
        if self.popup.active or self.battle_ended:
            # Block inputs during animations and dialog popups
            return

        mouse_pos = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
                return

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check clicks
                for i, btn in enumerate(self.buttons):
                    if btn.rect.collidepoint(mouse_pos):
                        self.selected = i
                        self.submit_answer()
                        return

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Return to lesson list
                    from src.states.lesson_state import LessonState
                    self.game.change_state(LessonState(self.game, self.planet))
                    return

                elif event.key == pygame.K_UP:
                    self.buttons[self.selected].selected = False
                    self.selected = (self.selected - 1) % len(self.buttons)
                    self.buttons[self.selected].selected = True
                    if hasattr(self.game, 'audio'):
                        self.game.audio.play_sfx("assets/audio/planet_select.wav")
                elif event.key == pygame.K_DOWN:
                    self.buttons[self.selected].selected = False
                    self.selected = (self.selected + 1) % len(self.buttons)
                    self.buttons[self.selected].selected = True
                    if hasattr(self.game, 'audio'):
                        self.game.audio.play_sfx("assets/audio/planet_select.wav")
                elif event.key == pygame.K_RETURN:
                    self.submit_answer()
                    return

    def submit_answer(self):
        if self.selected == self.correct_answer:
            # Correct answer! Damage enemy
            self.enemy_hp.current = max(0, self.enemy_hp.current - 1)
            
            # Animate
            self.hero_attack = 1.0
            self.enemy_shake = 0.5
            self.flash = 0.3
            
            # Damage floating text
            self.damage_text = "-1 HP"
            self.damage_x = 1060
            self.damage_y = 220
            self.damage_color = (255, 220, 80) # Gold text for enemy damage

            self.combo += 1
            
            # XP Calculation based on hero class
            xp_gained = 20
            if self.game.char_type == "Scholar":
                # Scholar streak double bonus
                xp_gained += self.combo * 8
            else:
                xp_gained += self.combo * 4
            self.xp_earned += xp_gained
            
            # Coins
            self.coins_earned += 5
            
            # Audio
            if hasattr(self.game, 'audio'):
                self.game.audio.play_sfx("assets/audio/correct.wav")

            # Show Success Popup
            self.popup.show("CORRECT!", (80, 220, 100), f"+{xp_gained} XP | Streak: {self.combo}")
        else:
            # Wrong answer! Damage hero
            self.hero_hp.current = max(0, self.hero_hp.current - 1)
            
            # Animate
            self.enemy_shake = 0.0
            self.flash = 0.2
            
            # Damage text on hero
            self.damage_text = "-1 HP"
            self.damage_x = 120
            self.damage_y = 220
            self.damage_color = (220, 60, 60) # Red text

            self.combo = 0
            
            # Audio
            if hasattr(self.game, 'audio'):
                self.game.audio.play_sfx("assets/audio/wrong.wav")

            # Show Error Popup
            corr_ans_text = self.options[self.correct_answer]
            self.popup.show("WRONG!", (220, 80, 80), f"Correct answer: {corr_ans_text}")

        # Check for Battle End
        if self.enemy_hp.current <= 0:
            self.battle_ended = True
            self.battle_victory = True
            self.end_timer = 1.2
        elif self.hero_hp.current <= 0:
            self.battle_ended = True
            self.battle_victory = False
            self.end_timer = 1.2

    def update(self, dt):
        self.background.update(dt)
        self.popup.update(dt)
        self.hero_hp.update(dt)
        self.enemy_hp.update(dt)

        # Update animation timers
        if self.hero_attack > 0:
            self.hero_attack -= dt * 4.0
        if self.enemy_shake > 0:
            self.enemy_shake -= dt * 4.0
        if self.flash > 0:
            self.flash -= dt * 3.0
            
        # Float damage text up
        if self.damage_text:
            self.damage_y -= dt * 60
            if self.damage_y < 120:
                self.damage_text = ""

        # Post-popup logic or battle end transitions
        if not self.popup.active:
            if self.battle_ended:
                self.end_timer -= dt
                if self.end_timer <= 0:
                    if self.battle_victory:
                        from src.states.victory_state import VictoryState
                        self.game.change_state(VictoryState(self.game, self.planet, self.lesson_name, self.xp_earned, self.coins_earned))
                    else:
                        from src.states.game_over_state import GameOverState
                        self.game.change_state(GameOverState(self.game, self.planet, self.lesson_name))
            else:
                # Load next question if current is finished
                # Check if we need to load a new question (i.e. if the popup just deactivated)
                if not hasattr(self, 'last_popup_active') or self.last_popup_active:
                    self.next_question()

        self.last_popup_active = self.popup.active

    def draw_characters(self, screen):
        # 1. Draw Hero
        # Move hero slightly right during attack animation
        hero_offset_x = int(self.hero_attack * 40)
        hero_x = 100 + hero_offset_x
        hero_y = 230

        if self.hero_sprite:
            screen.blit(self.hero_sprite, (hero_x, hero_y))
        else:
            # Draw cute procedural Scholar block
            pygame.draw.rect(screen, (30, 80, 180), (hero_x, hero_y, 160, 160), border_radius=15)
            pygame.draw.rect(screen, (255, 220, 80), (hero_x, hero_y, 160, 160), 3, border_radius=15)
            # Draw face/eyes
            pygame.draw.circle(screen, (255, 255, 255), (hero_x + 100, hero_y + 60), 12)
            pygame.draw.circle(screen, (0, 0, 0), (hero_x + 104, hero_y + 60), 5)
            # Scholar Hat
            pygame.draw.polygon(screen, (75, 45, 115), [
                (hero_x - 10, hero_y + 10), (hero_x + 80, hero_y - 25), 
                (hero_x + 170, hero_y + 10), (hero_x + 80, hero_y + 25)
            ])
            pygame.draw.rect(screen, (255, 220, 80), (hero_x + 75, hero_y + 15, 10, 40))

        # 2. Draw Enemy (Alien)
        # Shake enemy horizontally if shake is active
        enemy_offset_x = 0
        if self.enemy_shake > 0:
            enemy_offset_x = int(math.sin(pygame.time.get_ticks() * 0.1) * 10)
        enemy_x = 1020 + enemy_offset_x
        enemy_y = 230

        if self.enemy_sprite:
            screen.blit(self.enemy_sprite, (enemy_x, enemy_y))
        else:
            # Draw cute procedural space alien block
            pygame.draw.rect(screen, (120, 50, 150), (enemy_x, enemy_y, 160, 160), border_radius=15)
            pygame.draw.rect(screen, (220, 80, 220), (enemy_x, enemy_y, 160, 160), 3, border_radius=15)
            # Draw 3 eyes
            pygame.draw.circle(screen, (80, 255, 100), (enemy_x + 40, enemy_y + 60), 15)
            pygame.draw.circle(screen, (0, 0, 0), (enemy_x + 40, enemy_y + 60), 6)
            pygame.draw.circle(screen, (80, 255, 100), (enemy_x + 120, enemy_y + 60), 15)
            pygame.draw.circle(screen, (0, 0, 0), (enemy_x + 120, enemy_y + 60), 6)
            pygame.draw.circle(screen, (80, 255, 100), (enemy_x + 80, enemy_y + 40), 18)
            pygame.draw.circle(screen, (0, 0, 0), (enemy_x + 80, enemy_y + 40), 8)
            # Floating tentacles
            for k in range(3):
                tx = enemy_x + 30 + k * 50
                ty = enemy_y + 160 + int(math.sin(self.background.time * 6 + k) * 8)
                pygame.draw.circle(screen, (120, 50, 150), (tx, ty), 10)

    def draw(self, screen):
        # Background Space/Nebula
        self.background.draw(screen)

        # Title
        title_surf = self.title_font.render("QUIZ BATTLE", True, (255, 220, 80))
        screen.blit(title_surf, title_surf.get_rect(center=(screen.get_width() // 2, 45)))

        # Draw Characters (Hero vs Alien)
        self.draw_characters(screen)

        # HP Bars and Labels
        self.hero_hp.draw(screen, (60, 220, 90))
        self.enemy_hp.draw(screen, (220, 60, 60))

        hero_lbl = self.small_font.render(f"{self.game.hero_name}", True, (255, 255, 255))
        enemy_lbl = self.small_font.render("Cosmic Alien", True, (255, 255, 255))
        screen.blit(hero_lbl, (60, 90))
        screen.blit(enemy_lbl, (1000, 90))

        # Show HP numerical values
        h_val = self.small_font.render(f"HP: {self.hero_hp.current}/5", True, (200, 255, 200))
        e_val = self.small_font.render(f"HP: {self.enemy_hp.current}/5", True, (255, 200, 200))
        screen.blit(h_val, (60, 148))
        screen.blit(e_val, (1000, 148))

        # Question Panel Backing
        card = pygame.Rect(280, 100, 720, 530)
        pygame.draw.rect(screen, (25, 30, 48), card, border_radius=18)
        pygame.draw.rect(screen, (255, 220, 80), card, 2, border_radius=18)

        # Question Text (handling double lines if needed)
        q_lines = []
        words = self.question_text.split(" ")
        curr = ""
        for word in words:
            # Check length or if newline
            if "\n" in word:
                sub_parts = word.split("\n")
                curr += sub_parts[0]
                q_lines.append(curr.strip())
                curr = sub_parts[1] + " "
            elif len(curr + word) < 45:
                curr += word + " "
            else:
                q_lines.append(curr.strip())
                curr = word + " "
        if curr:
            q_lines.append(curr.strip())

        q_y = 135
        for q_line in q_lines:
            q_surf = self.question_font.render(q_line, True, (255, 255, 255))
            screen.blit(q_surf, q_surf.get_rect(center=(640, q_y)))
            q_y += 32

        # Draw Option Buttons
        for btn in self.buttons:
            btn.draw(screen)

        # HUD Round Info
        streak_surf = self.small_font.render(f"Streak: {self.combo}x", True, (255, 215, 0))
        xp_surf = self.small_font.render(f"Round XP: {self.xp_earned}", True, (100, 180, 255))
        screen.blit(streak_surf, (295, 110))
        screen.blit(xp_surf, (840, 110))

        # Footer controls hint
        footer = self.small_font.render("↑ ↓ Nav Choices    ENTER Select    ESC Flee Battle", True, (180, 180, 200))
        screen.blit(footer, footer.get_rect(center=(screen.get_width() // 2, 655)))

        # Damage Floating numbers
        if self.damage_text:
            dmg_surf = self.damage_font.render(self.damage_text, True, self.damage_color)
            screen.blit(dmg_surf, (self.damage_x, int(self.damage_y)))

        # Damage Screen Flash Overlay
        if self.flash > 0:
            flash_surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            flash_surf.fill((255, 255, 255, int(150 * self.flash)))
            screen.blit(flash_surf, (0, 0))

        # Popup rendering
        self.popup.draw(screen)