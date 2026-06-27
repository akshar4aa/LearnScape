import pygame

from src.states.state import State
from src.ui.background import Background


class LevelSelectState(State):

    def __init__(self, game, kingdom):

        super().__init__(game)

        self.game = game
        self.kingdom = kingdom

        width = self.game.screen.get_width()
        height = self.game.screen.get_height()

        self.background = Background(width, height)

        self.title_font = pygame.font.SysFont(
            "arial",
            56,
            bold=True
        )

        self.level_font = pygame.font.SysFont(
            "arial",
            28,
            bold=True
        )

        self.text_font = pygame.font.SysFont(
            "arial",
            24
        )

        if kingdom == "Earth":

            self.levels = [
                "Numbers",
                "Fractions",
                "Algebra",
                "Geometry",
                "Boss Battle"
            ]

        elif kingdom == "Jupiter":

            self.levels = [
                "Physics",
                "Chemistry",
                "Biology",
                "Astronomy",
                "Boss Battle"
            ]

        else:

            self.levels = [
                "Python",
                "Loops",
                "Functions",
                "Projects",
                "Boss Battle"
            ]

        self.selected = 0
            # =====================================
    # EVENTS
    # =====================================

    def handle_events(self, events):

        for event in events:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    from src.states.kingdom_state import KingdomState

                    self.game.change_state(
                        KingdomState(
                            self.game,
                            self.kingdom
                        )
                    )

                elif event.key == pygame.K_UP:

                    self.selected = (
                        self.selected - 1
                    ) % len(self.levels)

                elif event.key == pygame.K_DOWN:

                    self.selected = (
                        self.selected + 1
                    ) % len(self.levels)

                elif event.key == pygame.K_RETURN:

                    print(
                        "Starting:",
                        self.levels[self.selected]
                    )

                    # Next page will be LessonState

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

        title = self.title_font.render(
            f"{self.kingdom} Levels",
            True,
            (255,220,80)
        )

        screen.blit(
            title,
            title.get_rect(center=(640,80))
        )

        xp = self.text_font.render(
            "⭐ XP : 1250",
            True,
            (255,255,255)
        )

        coins = self.text_font.render(
            "🪙 Coins : 350",
            True,
            (255,255,255)
        )

        screen.blit(xp,(70,140))
        screen.blit(coins,(980,140))

        start_y = 220

        for i, level in enumerate(self.levels):

            rect = pygame.Rect(
                260,
                start_y + i * 90,
                760,
                65
            )

            if i == self.selected:

                pygame.draw.rect(
                    screen,
                    (255,220,80),
                    rect,
                    border_radius=15
                )

                color = (20,20,20)

            else:

                pygame.draw.rect(
                    screen,
                    (40,45,65),
                    rect,
                    border_radius=15
                )

                pygame.draw.rect(
                    screen,
                    (255,220,80),
                    rect,
                    2,
                    border_radius=15
                )

                color = (255,255,255)

            stars = "⭐" * (i + 1)

            text = self.level_font.render(
                f"{stars}   {level}",
                True,
                color
            )

            screen.blit(
                text,
                text.get_rect(center=rect.center)
            )

        hint = self.text_font.render(
            "↑ ↓ Select Level    ENTER Start    ESC Back",
            True,
            (190,190,190)
        )

        screen.blit(
            hint,
            hint.get_rect(center=(640,760))
        )