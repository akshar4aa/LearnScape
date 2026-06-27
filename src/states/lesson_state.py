import pygame
from src.states.state import State
from src.ui.background import Background

# Lesson Database Content
LESSON_CONTENT = {
    "Earth": {
        "Numbers": {
            "title": "Understanding Numbers",
            "desc": "Learn about even and odd numbers, prime values, and number sequences.",
            "example": "Even: 2, 4, 6... Odd: 1, 3, 5...\nPrimes are divisible only by 1 and itself (2, 3, 5, 7).\nSequences: 2, 4, 6, 8 (adds 2 each step)."
        },
        "Addition": {
            "title": "Summation (Addition)",
            "desc": "Combine two numbers together to find the grand total. Carry values over when units sum exceeds 9.",
            "example": "25 + 9 = 34\nCalculation: Units (5 + 9 = 14, write 4, carry 1),\nTens (2 + carry 1 = 3) -> 34."
        },
        "Subtraction": {
            "title": "Subtraction (Deduction)",
            "desc": "Deduct one amount from another. Borrow values from the left column if the digit is too small.",
            "example": "25 - 9 = 16\nCalculation: Borrow from Tens to make Units 15.\n15 - 9 = 6. Tens digit decreases by 1 (2 -> 1) -> 16."
        },
        "Multiplication": {
            "title": "Multiplication (Repeated Addition)",
            "desc": "Repeated addition of a number a certain amount of times. Master tables for quick calculations.",
            "example": "8 × 7 = 56\nExplanation: Add 8 to itself 7 times:\n8 + 8 + 8 + 8 + 8 + 8 + 8 = 56."
        },
        "Division": {
            "title": "Division (Equal Sharing)",
            "desc": "Splitting an amount into equal groups. Division is the inverse operation of multiplication.",
            "example": "56 ÷ 7 = 8\nExplanation: How many times does 7 fit into 56?\nSince 7 × 8 = 56, the answer is 8."
        },
        "Fractions": {
            "title": "Fractions (Parts of a Whole)",
            "desc": "Fractions represent parts of a whole. Numerator (top) divided by Denominator (bottom).",
            "example": "1/2 represents half of an object.\nLike denominators: 1/4 + 2/4 = 3/4.\nHalves: 1/2 + 1/2 = 1 whole."
        },
        "Decimals": {
            "title": "Decimals (Base-10 Fractions)",
            "desc": "Decimals represent fractional parts using tenths, hundredths, etc. separated by a decimal point.",
            "example": "0.5 is equal to a half (1/2).\n0.25 is equal to one quarter (1/4).\n0.3 + 0.4 = 0.7."
        }
    },
    "Jupiter": {
        "Plants": {
            "title": "Plant Biology",
            "desc": "Discover how roots, stems, leaves, flowers, and chlorophyll power the plant life cycle.",
            "example": "Roots absorb water. Stem transports nutrients.\nLeaves perform photosynthesis using sunlight, water, and CO2\nto create oxygen and glucose."
        },
        "Animals": {
            "title": "Animal Kingdom",
            "desc": "Classify animals into mammals, birds, reptiles, amphibians, and fish by their traits and diets.",
            "example": "Mammals: Warm-blooded, fur, feed milk (e.g., Whales, Bats).\nHerbivores: Eat plants (Deer).\nCarnivores: Eat meat (Lions)."
        },
        "Solar System": {
            "title": "Astronomy & Solar System",
            "desc": "Explore the Sun, planets, orbits, and features of our cosmic neighborhood.",
            "example": "Planets order: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune.\nAsteroid Belt separates Mars (rocky) and Jupiter (gas giant)."
        },
        "Human Body": {
            "title": "Human Physiology",
            "desc": "Examine key body organs (heart, lungs, brain) and organ systems (skeletal, circulatory, respiratory).",
            "example": "Brain controls actions. Lungs breathe oxygen.\nHeart pumps blood. Human skeleton has 206 bones."
        },
        "Weather": {
            "title": "Meteorology & Weather",
            "desc": "Understand the water cycle (evaporation, condensation, precipitation) and storm clouds.",
            "example": "Evaporation: Water turns to gas (vapor) due to heat.\nCondensation: Vapor turns to liquid droplets (clouds).\nCumulonimbus: Dark storm clouds."
        }
    },
    "Saturn": {
        "Variables": {
            "title": "Coding: Variables",
            "desc": "Variables store data values in memory. They can hold strings, integers, floats, or booleans.",
            "example": "x = 5  # stores an integer\nmsg = 'hello'  # stores a string\nx = x + 2  # x becomes 7"
        },
        "Loops": {
            "title": "Coding: Loops",
            "desc": "Loops repeat a block of code. 'for' loops iterate over ranges; 'while' loops run while a condition is True.",
            "example": "for i in range(3): print(i)\n# Output: 0, 1, 2 (repeats 3 times)\nwhile x < 5: x += 1"
        },
        "Conditions": {
            "title": "Coding: Conditionals",
            "desc": "Use if, elif, and else statements to make decisions based on logical conditions.",
            "example": "if score >= 90:\n    print('A')\nelse:\n    print('B')  # prints B if score is below 90"
        },
        "Functions": {
            "title": "Coding: Functions",
            "desc": "Functions are reusable code blocks defined with 'def'. They accept parameters and return values.",
            "example": "def double(n):\n    return n * 2\nx = double(5)  # x becomes 10"
        },
        "Lists": {
            "title": "Coding: Lists",
            "desc": "Lists store ordered collections of items. Access elements using zero-based index numbers.",
            "example": "fruits = ['apple', 'banana']\nfruits[0] is 'apple'\nfruits.append('orange')  # adds to end"
        }
    }
}

class LessonState(State):
    def __init__(self, game, planet, lesson_name=None):
        super().__init__(game)
        self.planet = planet
        self.lesson_name = lesson_name # If None, show selection menu first

        width = self.game.screen.get_width()
        height = self.game.screen.get_height()
        self.background = Background(width, height)

        self.title_font = pygame.font.SysFont("arial", 48, bold=True)
        self.heading_font = pygame.font.SysFont("arial", 28, bold=True)
        self.text_font = pygame.font.SysFont("arial", 22)
        self.code_font = pygame.font.SysFont("courier", 20, bold=True)

        # Subject list for selection menu
        self.lessons = list(LESSON_CONTENT[planet].keys())
        self.selected_idx = 0

        # Continue / Begin Quiz Button
        self.button_rect = pygame.Rect(470, 560, 340, 55)

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
                return

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.lesson_name is not None:
                        # Go back to level select
                        self.lesson_name = None
                    else:
                        # Go back to world map
                        from src.states.world_map_state import WorldMapState
                        self.game.change_state(WorldMapState(self.game))
                    return

                if self.lesson_name is None:
                    # Level select navigation
                    if event.key == pygame.K_UP:
                        self.selected_idx = (self.selected_idx - 1) % len(self.lessons)
                        if hasattr(self.game, 'audio'):
                            self.game.audio.play_sfx("assets/audio/planet_select.wav")
                    elif event.key == pygame.K_DOWN:
                        self.selected_idx = (self.selected_idx + 1) % len(self.lessons)
                        if hasattr(self.game, 'audio'):
                            self.game.audio.play_sfx("assets/audio/planet_select.wav")
                    elif event.key == pygame.K_RETURN:
                        self.select_lesson(self.lessons[self.selected_idx])
                else:
                    # Lesson reading navigation
                    if event.key == pygame.K_RETURN:
                        self.start_quiz()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.lesson_name is None:
                    # Clicking lesson item
                    start_y = 180
                    for i in range(len(self.lessons)):
                        rect = pygame.Rect(340, start_y + i * 65, 600, 50)
                        if rect.collidepoint(mouse_pos):
                            self.selected_idx = i
                            self.select_lesson(self.lessons[i])
                            return
                else:
                    # Clicking Begin Quiz Button
                    if self.button_rect.collidepoint(mouse_pos):
                        self.start_quiz()
                        return

    def select_lesson(self, name):
        self.lesson_name = name
        if hasattr(self.game, 'audio'):
            self.game.audio.play_sfx("assets/audio/click.wav")

    def start_quiz(self):
        if hasattr(self.game, 'audio'):
            self.game.audio.play_sfx("assets/audio/click.wav")
        from src.states.quiz_state import QuizState
        self.game.change_state(QuizState(self.game, self.planet, self.lesson_name))

    def update(self, dt):
        self.background.update(dt)

    def draw_lesson_select(self, screen):
        # Draw Planet header
        planet_subject = "Mathematics" if self.planet == "Earth" else ("Science" if self.planet == "Jupiter" else "Programming")
        title_surf = self.title_font.render(f"{self.planet} Academy", True, (255, 220, 80))
        screen.blit(title_surf, title_surf.get_rect(center=(640, 65)))

        sub_surf = self.text_font.render(f"Subject Area: {planet_subject}", True, (200, 200, 220))
        screen.blit(sub_surf, sub_surf.get_rect(center=(640, 115)))

        # Panel Backing
        panel = pygame.Rect(280, 150, 720, 480)
        pygame.draw.rect(screen, (25, 30, 48), panel, border_radius=15)
        pygame.draw.rect(screen, (255, 220, 80), panel, 2, border_radius=15)

        # Subject list items
        start_y = 180
        for i, lesson in enumerate(self.lessons):
            rect = pygame.Rect(340, start_y + i * 65, 600, 50)
            is_sel = (i == self.selected_idx)
            bg = (255, 220, 80) if is_sel else (40, 45, 65)
            border = (255, 255, 200) if is_sel else (255, 220, 80)
            txt_color = (20, 24, 35) if is_sel else (255, 255, 255)

            if is_sel:
                glow = pygame.Surface((rect.width + 16, rect.height + 16), pygame.SRCALPHA)
                pygame.draw.rect(glow, (255, 220, 80, 40), glow.get_rect(), border_radius=10)
                screen.blit(glow, (rect.x - 8, rect.y - 8))

            pygame.draw.rect(screen, bg, rect, border_radius=10)
            pygame.draw.rect(screen, border, rect, 2, border_radius=10)

            # Check if this lesson has been completed in this save game
            completed_str = "🏆" if f"{self.planet}_{lesson}" in getattr(self.game, 'completed_lessons', []) else "⭐"
            txt_surf = self.heading_font.render(f"{completed_str}  {lesson}", True, txt_color)
            screen.blit(txt_surf, txt_surf.get_rect(center=rect.center))

        # Help
        help_surf = self.text_font.render("↑ ↓ Select Topic    ENTER/Click Open    ESC Back to Map", True, (130, 130, 150))
        screen.blit(help_surf, help_surf.get_rect(center=(640, 675)))

    def draw_lesson_details(self, screen):
        data = LESSON_CONTENT[self.planet][self.lesson_name]

        # Draw Planet header
        title_surf = self.title_font.render(data["title"], True, (255, 220, 80))
        screen.blit(title_surf, title_surf.get_rect(center=(640, 65)))

        sub_surf = self.text_font.render(f"Planet {self.planet} • Level Lesson", True, (200, 200, 220))
        screen.blit(sub_surf, sub_surf.get_rect(center=(640, 115)))

        # Lesson panel backing
        panel = pygame.Rect(200, 150, 880, 390)
        pygame.draw.rect(screen, (25, 30, 48), panel, border_radius=15)
        pygame.draw.rect(screen, (255, 220, 80), panel, 2, border_radius=15)

        # Tutor image fallback / Emoji
        tutor_emoji = "🧙" if self.planet == "Earth" else ("👽" if self.planet == "Jupiter" else "🤖")
        tutor_font = pygame.font.SysFont("arial", 64)
        tutor_surf = tutor_font.render(tutor_emoji, True, (255, 255, 255))
        screen.blit(tutor_surf, (230, 180))

        # Description text
        desc_title = self.heading_font.render("Lesson Explanation", True, (255, 220, 80))
        screen.blit(desc_title, (340, 180))

        # Break desc into lines
        words = data["desc"].split(" ")
        lines = []
        curr = ""
        for word in words:
            if len(curr + word) < 55:
                curr += word + " "
            else:
                lines.append(curr.strip())
                curr = word + " "
        if curr:
            lines.append(curr.strip())

        y = 220
        for line in lines:
            line_surf = self.text_font.render(line, True, (255, 255, 255))
            screen.blit(line_surf, (340, y))
            y += 28

        # Example Code/Math block
        ex_title = self.heading_font.render("Interactive Example", True, (255, 220, 80))
        screen.blit(ex_title, (340, 330))

        example_box = pygame.Rect(340, 370, 700, 140)
        pygame.draw.rect(screen, (15, 18, 30), example_box, border_radius=10)
        pygame.draw.rect(screen, (75, 45, 115), example_box, 1, border_radius=10)

        # Draw lines of examples (handling line breaks)
        ex_lines = data["example"].split("\n")
        ex_y = 385
        for ex_line in ex_lines:
            ex_surf = self.code_font.render(ex_line, True, (255, 255, 200))
            screen.blit(ex_surf, (360, ex_y))
            ex_y += 30

        # Draw Begin Quiz Button
        mouse_pos = pygame.mouse.get_pos()
        hovered = self.button_rect.collidepoint(mouse_pos)
        btn_bg = (255, 235, 120) if hovered else (255, 220, 80)

        if hovered:
            btn_glow = pygame.Surface((self.button_rect.width + 20, self.button_rect.height + 20), pygame.SRCALPHA)
            pygame.draw.rect(btn_glow, (255, 220, 80, 50), btn_glow.get_rect(), border_radius=12)
            screen.blit(btn_glow, (self.button_rect.x - 10, self.button_rect.y - 10))

        pygame.draw.rect(screen, btn_bg, self.button_rect, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), self.button_rect, 2, border_radius=12)

        begin_surf = self.heading_font.render("BEGIN QUIZ BATTLE", True, (20, 24, 35))
        screen.blit(begin_surf, begin_surf.get_rect(center=self.button_rect.center))

        # Help
        help_surf = self.text_font.render("ENTER/Click Begin Quiz Battle    ESC Back to Subject List", True, (130, 130, 150))
        screen.blit(help_surf, help_surf.get_rect(center=(640, 675)))

    def draw(self, screen):
        self.background.draw(screen)
        if self.lesson_name is None:
            self.draw_lesson_select(screen)
        else:
            self.draw_lesson_details(screen)