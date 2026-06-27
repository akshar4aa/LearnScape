import pygame

from src.states.state import State
from src.ui.background import Background
from src.states.character_select_state import CharacterSelectState

class NewAdventureState(State):

    def __init__(self, game):
        super().__init__(game)

        self.game = game

        width = self.game.screen.get_width()
        height = self.game.screen.get_height()

        self.background = Background(width, height)

        # Fonts
        self.title_font = pygame.font.SysFont(
            "arial",
            60,
            bold=True
        )

        self.heading_font = pygame.font.SysFont(
            "arial",
            28,
            bold=True
        )

        self.text_font = pygame.font.SysFont(
            "arial",
            24
        )

        # Hero Name
        self.hero_name = ""
        self.name_active = True
        self.max_length = 12

        # Difficulty
        self.difficulties = [
            "Explorer",
            "Scholar",
            "Legend"
        ]

        self.selected = 0

        # UI Rectangles
        self.name_box = pygame.Rect(
            340,
            250,
            600,
            55
        )

        self.button_rect = pygame.Rect(
            470,
            650,
            340,
            60
        )

    # ====================================
    # EVENTS
    # ====================================

    def handle_events(self, events):

        for event in events:

            if event.type == pygame.QUIT:
                self.game.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if self.name_box.collidepoint(event.pos):
                    self.name_active = True

                elif self.button_rect.collidepoint(event.pos):

                    self.game.change_state(
        CharacterSelectState(self.game)
    )

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    from src.states.menu_state import MenuState

                    self.game.change_state(
                        MenuState(self.game)
                    )

                    return

                # -------------------
                # Typing Name
                # -------------------

                if self.name_active:

                    if event.key == pygame.K_BACKSPACE:

                        self.hero_name = self.hero_name[:-1]

                    elif event.key == pygame.K_RETURN:

                        self.name_active = False

                    else:

                        if (
                            event.unicode.isprintable()
                            and len(self.hero_name) < self.max_length
                        ):

                            self.hero_name += event.unicode

                # -------------------
                # Difficulty
                # -------------------

                else:

                    if event.key == pygame.K_UP:

                        self.selected -= 1

                        if self.selected < 0:
                            self.selected = 2

                    elif event.key == pygame.K_DOWN:

                        self.selected += 1

                        if self.selected > 2:
                            self.selected = 0

                    elif event.key == pygame.K_TAB:

                        self.name_active = True

                    elif event.key == pygame.K_RETURN:

                        self.game.change_state(
        CharacterSelectState(self.game)
    )

    # ====================================
    # UPDATE
    # ====================================

    def update(self, dt):

        self.background.update(dt)
            # ====================================
    # DRAW
    # ====================================

    def draw(self, screen):

        self.background.draw(screen)

        # ---------------------------
        # Title
        # ---------------------------

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
            "Create your hero and begin your journey.",
            True,
            (220, 220, 220)
        )

        screen.blit(
            subtitle,
            subtitle.get_rect(center=(640, 130))
        )

        # ---------------------------
        # Main Panel
        # ---------------------------

        panel = pygame.Rect(
            280,
            170,
            720,
            560
        )

        pygame.draw.rect(
            screen,
            (25, 30, 48),
            panel,
            border_radius=15
        )

        pygame.draw.rect(
            screen,
            (255, 220, 80),
            panel,
            2,
            border_radius=15
        )

        # ---------------------------
        # Hero Name
        # ---------------------------

        heading = self.heading_font.render(
            "Hero Name",
            True,
            (255, 220, 80)
        )

        screen.blit(
            heading,
            (340, 210)
        )

        border = (
            (255, 220, 80)
            if self.name_active
            else
            (150, 150, 150)
        )

        pygame.draw.rect(
            screen,
            (40, 45, 65),
            self.name_box,
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            border,
            self.name_box,
            2,
            border_radius=10
        )

        display = self.hero_name

        if display == "":
            display = "Enter Hero Name"

        if self.name_active:

            if (pygame.time.get_ticks() // 500) % 2 == 0:
                display += "|"

        name = self.text_font.render(
            display,
            True,
            (255, 255, 255)
        )

        screen.blit(
            name,
            (360, 267)
        )

        # ---------------------------
        # Difficulty
        # ---------------------------

        heading = self.heading_font.render(
            "Difficulty",
            True,
            (255, 220, 80)
        )

        screen.blit(
            heading,
            (340, 340)
        )

        start_y = 390

        for i, difficulty in enumerate(self.difficulties):

            rect = pygame.Rect(
                340,
                start_y + i * 70,
                600,
                55
            )

            if i == self.selected:

                pygame.draw.rect(
                    screen,
                    (255, 220, 80),
                    rect,
                    border_radius=10
                )

                color = (20, 20, 20)

            else:

                pygame.draw.rect(
                    screen,
                    (40, 45, 65),
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

                color = (255, 255, 255)

            text = self.text_font.render(
                difficulty,
                True,
                color
            )

            screen.blit(
                text,
                text.get_rect(center=rect.center)
            )

        # ---------------------------
        # Begin Button
        # ---------------------------

        mouse = pygame.mouse.get_pos()

        if self.button_rect.collidepoint(mouse):
            button_color = (255, 235, 120)
        else:
            button_color = (255, 220, 80)

        pygame.draw.rect(
            screen,
            button_color,
            self.button_rect,
            border_radius=12
        )

        button = self.heading_font.render(
            "BEGIN JOURNEY",
            True,
            (20, 20, 20)
        )

        screen.blit(
            button,
            button.get_rect(
                center=self.button_rect.center
            )
        )

        # ---------------------------
        # Help Text
        # ---------------------------

        if self.name_active:

            help_text = "Type Name • ENTER = Save Name"

        else:

            help_text = "↑ ↓ Change Difficulty • TAB = Edit Name"

        help_surface = self.text_font.render(
            help_text,
            True,
            (180, 180, 180)
        )

        screen.blit(
            help_surface,
            help_surface.get_rect(
                center=(640, 760)
            )
        )