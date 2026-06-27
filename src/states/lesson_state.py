import pygame

from src.states.state import State
from src.ui.background import Background


class LessonState(State):

    def __init__(self, game, kingdom, lesson):

        super().__init__(game)

        self.game = game
        self.kingdom = kingdom
        self.lesson = lesson

        width = self.game.screen.get_width()
        height = self.game.screen.get_height()

        self.background = Background(width, height)

        self.title_font = pygame.font.SysFont(
            "arial",
            52,
            bold=True
        )

        self.text_font = pygame.font.SysFont(
            "arial",
            28
        )

        self.dialogue = [

            "🧙 Welcome, Hero!",

            f"Today you will learn {lesson}.",

            "Complete this lesson to earn XP.",

            "Press ENTER to continue."
        ]

        self.current = 0
            # =====================================
    # EVENTS
    # =====================================

    def handle_events(self, events):

        for event in events:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    from src.states.level_select_state import LevelSelectState

                    self.game.change_state(
                        LevelSelectState(
                            self.game,
                            self.kingdom
                        )
                    )

                elif event.key == pygame.K_RETURN:

                    self.current += 1

                    if self.current >= len(self.dialogue):

                        from src.states.quiz_state import QuizState

                        self.game.change_state(
                            QuizState(self.game)
                        )

                        # Next page will be QuizState

    # =====================================
    # UPDATE
    # =====================================

    def update(self, dt):

        self.background.update(dt)

    # =====================================
    # DRAW
    # =====================================

    def draw(self, screen):

        self.background.draw(screen)

        # ---------------------------
        # Title
        # ---------------------------

        title = self.title_font.render(
            self.lesson,
            True,
            (255, 220, 80)
        )

        screen.blit(
            title,
            title.get_rect(center=(640, 80))
        )

        # ---------------------------
        # Wizard
        # ---------------------------

        wizard = self.title_font.render(
            "🧙",
            True,
            (255,255,255)
        )

        screen.blit(
            wizard,
            wizard.get_rect(center=(170,250))
        )

        # ---------------------------
        # Dialogue Box
        # ---------------------------

        box = pygame.Rect(
            220,
            170,
            850,
            280
        )

        pygame.draw.rect(
            screen,
            (35,40,60),
            box,
            border_radius=20
        )

        pygame.draw.rect(
            screen,
            (255,220,80),
            box,
            2,
            border_radius=20
        )

        message = self.text_font.render(
            self.dialogue[self.current],
            True,
            (255,255,255)
        )

        screen.blit(
            message,
            (260,250)
        )

        # ---------------------------
        # Progress
        # ---------------------------

        progress = self.text_font.render(
            f"Step {self.current+1}/{len(self.dialogue)}",
            True,
            (220,220,220)
        )

        screen.blit(
            progress,
            (520,500)
        )

        # ---------------------------
        # Continue Button
        # ---------------------------

        button = pygame.Rect(
            470,
            640,
            340,
            60
        )

        pygame.draw.rect(
            screen,
            (255,220,80),
            button,
            border_radius=12
        )

        button_text = self.text_font.render(
            "CONTINUE",
            True,
            (20,20,20)
        )

        screen.blit(
            button_text,
            button_text.get_rect(center=button.center)
        )

        # ---------------------------
        # Help
        # ---------------------------

        hint = self.text_font.render(
            "ENTER = Next Dialogue    ESC = Back",
            True,
            (180,180,180)
        )

        screen.blit(
            hint,
            hint.get_rect(center=(640,760))
        )