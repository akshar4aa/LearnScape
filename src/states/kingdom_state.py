import pygame

from src.states.state import State
from src.ui.background import Background


class KingdomState(State):

    def __init__(self, game, kingdom):

        super().__init__(game)

        self.game = game
        self.kingdom = kingdom

        width = self.game.screen.get_width()
        height = self.game.screen.get_height()

        self.background = Background(width, height)

        self.title_font = pygame.font.SysFont(
            "arial",
            60,
            bold=True
        )

        self.heading_font = pygame.font.SysFont(
            "arial",
            34,
            bold=True
        )

        self.text_font = pygame.font.SysFont(
            "arial",
            26
        )

        if kingdom == "Earth":

            self.subject = "Mathematics"

            self.chapters = [
                "Numbers",
                "Fractions",
                "Algebra",
                "Geometry"
            ]

            self.emoji = "🌍"

        elif kingdom == "Jupiter":

            self.subject = "Science"

            self.chapters = [
                "Physics",
                "Chemistry",
                "Biology",
                "Space"
            ]

            self.emoji = "🪐"

        else:

            self.subject = "Programming"

            self.chapters = [
                "Python",
                "Loops",
                "Functions",
                "Projects"
            ]

            self.emoji = "🪐"
                # =====================================
    # EVENTS
    # =====================================

    def handle_events(self, events):

        for event in events:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    from src.states.world_map_state import WorldMapState

                    self.game.change_state(
                        WorldMapState(self.game)
                    )

                elif event.key == pygame.K_RETURN:

                    from src.states.level_select_state import LevelSelectState

                    self.game.change_state(
                        LevelSelectState(
                        self.game,
                        self.kingdom
                    )
                )
                    # Next we'll open the Level Select page

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

        # Title
        title = self.title_font.render(
            self.kingdom,
            True,
            (255, 220, 80)
        )

        screen.blit(
            title,
            title.get_rect(center=(640, 80))
        )

        # Emoji
        emoji = self.title_font.render(
            self.emoji,
            True,
            (255, 255, 255)
        )

        screen.blit(
            emoji,
            emoji.get_rect(center=(640, 165))
        )

        # Subject Panel
        panel = pygame.Rect(
            290,
            230,
            700,
            360
        )

        pygame.draw.rect(
            screen,
            (30, 35, 55),
            panel,
            border_radius=20
        )

        pygame.draw.rect(
            screen,
            (255, 220, 80),
            panel,
            2,
            border_radius=20
        )

        subject = self.heading_font.render(
            f"Subject : {self.subject}",
            True,
            (255, 220, 80)
        )

        screen.blit(
            subject,
            (340, 270)
        )

        y = 340

        for chapter in self.chapters:

            text = self.text_font.render(
                "⭐ " + chapter,
                True,
                (230, 230, 230)
            )

            screen.blit(
                text,
                (360, y)
            )

            y += 55

        # Continue Button
        button = pygame.Rect(
            470,
            640,
            340,
            60
        )

        pygame.draw.rect(
            screen,
            (255, 220, 80),
            button,
            border_radius=12
        )

        text = self.heading_font.render(
            "START LEARNING",
            True,
            (20, 20, 20)
        )

        screen.blit(
            text,
            text.get_rect(center=button.center)
        )

        hint = self.text_font.render(
            "ENTER = Continue      ESC = World Map",
            True,
            (200, 200, 200)
        )

        screen.blit(
            hint,
            hint.get_rect(center=(640, 740))
        )