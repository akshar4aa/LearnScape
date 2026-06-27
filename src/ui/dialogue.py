import pygame
from src.utils.helpers import get_font, draw_rounded_panel, draw_text_wrapped, draw_glowing_text
from src.ui.ui_elements import Button

class TypewriterDialogue:
    def __init__(self, game, x, y, w, h, speaker_name, full_text, callback=None):
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)
        self.speaker_name = speaker_name
        self.full_text = full_text
        self.callback = callback
        
        # Typewriter states
        self.visible_text = ""
        self.char_index = 0.0
        self.speed = 45.0 # Chars per second
        self.finished = False
        
        # Style
        self.font = get_font(18)
        self.speaker_font = get_font(16, is_bold=True)
        self.sound_cooldown = 0.0

    def update(self, dt):
        if self.finished:
            return
            
        # Update character indexing
        last_idx = int(self.char_index)
        self.char_index += self.speed * dt
        curr_idx = int(self.char_index)
        
        if curr_idx >= len(self.full_text):
            self.visible_text = self.full_text
            self.finished = True
            if self.callback:
                self.callback()
        else:
            self.visible_text = self.full_text[:curr_idx]
            
            # Play a tiny click sound for letter typing
            if curr_idx > last_idx:
                self.sound_cooldown -= dt
                if self.sound_cooldown <= 0:
                    # Brief click
                    self.game.sounds.play_sfx("click")
                    self.sound_cooldown = 0.08 # limit rate

    def skip(self):
        """Skip typewriter animation and display full text."""
        self.visible_text = self.full_text
        self.finished = True
        if self.callback:
            self.callback()

    def draw(self, surface):
        # Draw dialogue outer glass panel
        bg_color = (25, 22, 22)
        border_color = (210, 160, 40)
        draw_rounded_panel(surface, self.rect, bg_color, border_color, border_width=3, border_radius=12)
        
        # Speaker Name Badge Overlay
        if self.speaker_name:
            badge_surf = self.speaker_font.render(self.speaker_name, True, (255, 235, 120))
            bw, bh = badge_surf.get_size()
            badge_rect = pygame.Rect(self.rect.x + 20, self.rect.y - 12, bw + 16, bh + 6)
            
            pygame.draw.rect(surface, (20, 20, 25), badge_rect, border_radius=4)
            pygame.draw.rect(surface, (210, 160, 40), badge_rect, 1, border_radius=4)
            surface.blit(badge_surf, (badge_rect.x + 8, badge_rect.y + 3))

        # Render scrolling text body
        margin_x = 24
        margin_y = 20
        text_rect = (
            self.rect.x + margin_x, 
            self.rect.y + margin_y, 
            self.rect.width - margin_x*2, 
            self.rect.height - margin_y*2
        )
        draw_text_wrapped(surface, self.visible_text, self.font, (240, 240, 245), text_rect)
        
        # "Press E to continue" indicator
        if self.finished:
            ind_font = get_font(12, is_bold=True)
            ind_surf = ind_font.render("Press [E] to continue...", True, (230, 185, 55))
            # Blinking pulse
            alpha = int(128 + 127 * math.sin(pygame.time.get_ticks() * 0.01))
            ind_surf.set_alpha(alpha)
            surface.blit(ind_surf, (self.rect.right - ind_surf.get_width() - 20, self.rect.bottom - ind_surf.get_height() - 10))


class BattleQuestionPanel:
    def __init__(self, game, x, y, w, h, answer_callback):
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)
        self.answer_callback = answer_callback
        
        self.question = None
        self.choices = []
        self.correct_choice = ""
        self.disabled_indices = [] # Indices greyed out by hints
        
        # Grid buttons for choices (A, B, C, D)
        self.buttons = []
        self.font_q = get_font(18, is_bold=True)
        
    def load_question(self, question_data):
        self.question = question_data["question"]
        self.choices = question_data["choices"] # A list of 4 items
        self.correct_choice = question_data["answer"] # Text matching correct item
        self.disabled_indices = []
        
        # Construct the buttons dynamically
        # Arranged in a 2x2 grid below the question text
        self.buttons = []
        
        grid_x = self.rect.x + 20
        grid_y = self.rect.y + 60
        btn_w = (self.rect.width - 60) // 2
        btn_h = 45
        
        labels = ["A: ", "B: ", "C: ", "D: "]
        for idx, choice in enumerate(self.choices):
            bx = grid_x if (idx % 2 == 0) else (grid_x + btn_w + 20)
            by = grid_y if (idx < 2) else (grid_y + btn_h + 12)
            
            btn_text = f"{labels[idx]}{choice}"
            
            # Use callback that maps option text directly
            callback = lambda opt=choice: self.submit_answer(opt)
            btn = Button(self.game, bx, by, btn_w, btn_h, btn_text, callback, color=(28, 36, 48), hover_color=(40, 120, 230), font_size=14)
            self.buttons.append(btn)

    def submit_answer(self, option):
        is_correct = (option == self.correct_choice)
        self.answer_callback(is_correct)

    def apply_hint_card(self):
        """Grey out 2 incorrect choices."""
        if not self.choices or len(self.disabled_indices) >= 2:
            return False # Already used or no options
            
        incorrect_indices = [idx for idx, opt in enumerate(self.choices) if opt != self.correct_choice]
        # Randomly choose 2 to disable
        to_disable = random.sample(incorrect_indices, 2)
        self.disabled_indices.extend(to_disable)
        
        for idx in to_disable:
            self.buttons[idx].set_enabled(False)
        return True

    def handle_event(self, event, mouse_pos):
        for btn in self.buttons:
            if btn.handle_event(event, mouse_pos):
                break

    def update(self, dt, mouse_pos):
        for btn in self.buttons:
            btn.update(dt, mouse_pos)

    def draw(self, surface):
        # Draw Question Container Panel
        draw_rounded_panel(surface, self.rect, (24, 28, 36), (65, 80, 110), border_width=3, border_radius=12)
        
        # Display Question Text (Wrapped inside upper panel half)
        q_rect = (self.rect.x + 20, self.rect.y + 15, self.rect.width - 40, 45)
        draw_text_wrapped(surface, self.question, self.font_q, (255, 255, 255), q_rect)
        
        # Draw Choices Buttons
        for btn in self.buttons:
            btn.draw(surface)
