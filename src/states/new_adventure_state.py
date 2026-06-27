import pygame

from src.states.state import State
from src.ui.background import Background


class NewAdventureState(State):

    def __init__(self, game):
        super().__init__(game)

        width = self.game.screen.get_width()
        height = self.game.screen.get_height()

        self.background = Background(width, height)

        # -----------------------------
        # Fonts
        # -----------------------------

        self.title_font = pygame.font.SysFont(
            "arial",
            60,
            bold=True
        )

        self.heading_font = pygame.font.SysFont(
            "arial",
            30,
            bold=True
        )

        self.text_font = pygame.font.SysFont(
            "arial",
            26
        )

        self.small_font = pygame.font.SysFont(
            "arial",
            22
        )

        # -----------------------------
        # Hero
        # -----------------------------

        self.hero_name = ""
        self.max_name_length = 12

        # True = typing name
        # False = selecting difficulty
        self.name_active = True

        # -----------------------------
        # Difficulty
        # -----------------------------

        self.difficulties = [
            "Explorer",
            "Scholar",
            "Legend"
        ]

        self.selected = 0

        # -----------------------------
        # Begin Button
        # -----------------------------

        self.button_rect = pygame.Rect(
            470,
            655,
            340,
            60
        )

        self.hover_button = False

    # =====================================
    # Events
    # =====================================

    def handle_events(self, events):

        mouse = pygame.mouse.get_pos()

        self.hover_button = self.button_rect.collidepoint(mouse)

        for event in events:

            # --------------------------
            # Quit
            # --------------------------

            if event.type == pygame.QUIT:

                self.game.running = False

            # --------------------------
            # Mouse
            # --------------------------

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if self.hover_button:

                    print("Hero:", self.hero_name)
                    print(
                        "Difficulty:",
                        self.difficulties[self.selected]
                    )

            # --------------------------
            # Keyboard
            # --------------------------

            elif event.type == pygame.KEYDOWN:

                # ESC

                if event.key == pygame.K_ESCAPE:

                    from src.states.menu_state import MenuState

                    self.game.change_state(
                        MenuState(self.game)
                    )

                    return

                # ----------------------
                # Typing Hero Name
                # ----------------------

                if self.name_active:

                    if event.key == pygame.K_BACKSPACE:

                        self.hero_name = self.hero_name[:-1]

                    elif event.key == pygame.K_RETURN:

                        self.name_active = False

                    else:

                        if (
                            event.unicode.isprintable()
                            and len(self.hero_name)
                            < self.max_name_length
                        ):

                            self.hero_name += event.unicode

                # ----------------------
                # Difficulty Mode
                # ----------------------

                else:

                    if event.key == pygame.K_UP:

                        self.selected -= 1

                        if self.selected < 0:
                            self.selected = len(self.difficulties) - 1

                    elif event.key == pygame.K_DOWN:

                        self.selected += 1

                        if self.selected >= len(self.difficulties):
                            self.selected = 0

                    elif event.key == pygame.K_TAB:

                        self.name_active = True

                    elif event.key == pygame.K_RETURN:

                        print("Hero:", self.hero_name)
                        print(
                            "Difficulty:",
                            self.difficulties[self.selected]
                        )

    # =====================================
    # Update
    # =====================================

    def update(self, dt):

        self.background.update(dt)
            # =====================================
    # Draw
    # =====================================

    def draw(self, screen):

        self.background.draw(screen)

        # ----------------------------
        # Title
        # ----------------------------

        title = self.title_font.render(
            "New Adventure",
            True,
            (255, 220, 80)
        )

        screen.blit(
            title,
            title.get_rect(center=(640, 80))
        )

        subtitle = self.text_font.render(
            "Prepare your hero before beginning the journey.",
            True,
            (225, 225, 225)
        )

        screen.blit(
            subtitle,
            subtitle.get_rect(center=(640, 140))
        )

        # ==================================
        # Main Panel
        # ==================================

        panel = pygame.Rect(
            280,
            180,
            720,
            500
        )

        pygame.draw.rect(
            screen,
            (22, 28, 45),
            panel,
            border_radius=18
        )

        pygame.draw.rect(
            screen,
            (255, 220, 80),
            panel,
            2,
            border_radius=18
        )

        # ==================================
        # Hero Name
        # ==================================

        heading = self.heading_font.render(
            "Hero Name",
            True,
            (255, 220, 80)
        )

        screen.blit(heading, (330, 220))

        input_box = pygame.Rect(
            330,
            265,
            620,
            55
        )

        pygame.draw.rect(
            screen,
            (35, 40, 60),
            input_box,
            border_radius=10
        )

        border = (
            (255, 220, 80)
            if self.name_active
            else
            (160, 160, 160)
        )

        pygame.draw.rect(
            screen,
            border,
            input_box,
            2,
            border_radius=10
        )

        display = self.hero_name

        if self.name_active:
            if (pygame.time.get_ticks() // 450) % 2 == 0:
                display += "|"

        if display == "":
            display = "Enter your name..."

        name_surface = self.text_font.render(
            display,
            True,
            (255, 255, 255)
        )

        screen.blit(
            name_surface,
            (350, 280)
        )

        # ==================================
        # Difficulty
        # ==================================

        diff_heading = self.heading_font.render(
            "Difficulty",
            True,
            (255, 220, 80)
        )

        screen.blit(diff_heading, (330, 360))

        start_y = 410

        for i, difficulty in enumerate(self.difficulties):

            rect = pygame.Rect(
                330,
                start_y + i * 70,
                620,
                55
            )

            selected = (
                i == self.selected
                and not self.name_active
            )

            if selected:

                pygame.draw.rect(
                    screen,
                    (255, 220, 80),
                    rect,
                    border_radius=10
                )

                text_color = (20, 20, 20)

            else:

                pygame.draw.rect(
                    screen,
                    (35, 40, 60),
                    rect,
                    border_radius=10
                )

                pygame.draw.rect(
                    screen,
                    (255, 220, 80),
                    rect,
                    2,
                    border_radius=10
                )

                text_color = (255, 255, 255)

            txt = self.text_font.render(
                difficulty,
                True,
                text_color
            )

            screen.blit(
                txt,
                txt.get_rect(center=rect.center)
            )

        # ==================================
        # Begin Journey Button
        # ==================================

        button_color = (
            (255, 235, 120)
            if self.hover_button
            else
            (255, 220, 80)
        )

        pygame.draw.rect(
            screen,
            button_color,
            self.button_rect,
            border_radius=12
        )

        button_text = self.heading_font.render(
            "BEGIN JOURNEY",
            True,
            (20, 20, 20)
        )

        screen.blit(
            button_text,
            button_text.get_rect(
                center=self.button_rect.center
            )
        )

        # ==================================
        # Controls
        # ==================================

        if self.name_active:

            help_text = (
                "Type your name • ENTER = Continue"
            )

        else:

            help_text = (
                "↑ ↓ Change Difficulty • TAB = Edit Name • ENTER = Begin"
            )

        controls = self.small_font.render(
            help_text,
            True,
            (180, 180, 180)
        )

        screen.blit(
            controls,
            controls.get_rect(
                center=(640, 730)
            )
        )