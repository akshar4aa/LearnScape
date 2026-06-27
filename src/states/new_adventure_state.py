import pygame

from src.states.state import State
from src.ui.background import Background


class NewAdventureState(State):

    def __init__(self, game):
        super().__init__(game)

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
            30,
            bold=True
        )

        self.text_font = pygame.font.SysFont(
            "arial",
            26
        )

        self.hero_name = "Akshara"
        self.name_active = True
        self.max_name_length = 12

        self.difficulties = [
            "Explorer",
            "Scholar",
            "Legend"
        ]

        self.selected = 0
        self.hero_name = ""
        self.name_active = True
        self.max_name_length = 12

        self.difficulties = [
    "Explorer",
    "Scholar",
    "Legend"
]

        self.selected = 0

    def update(self, dt):

        self.background.update(dt)

    def draw(self, screen):

        self.background.draw(screen)

        # -------------------------------
        # Title
        # -------------------------------

        title = self.title_font.render(
            "New Adventure",
            True,
            (255,220,80)
        )

        screen.blit(
            title,
            title.get_rect(
                center=(640,90)
            )
        )

        # -------------------------------
        # Description
        # -------------------------------

        desc = self.text_font.render(
            "Prepare your hero before starting the journey.",
            True,
            (225,225,225)
        )

        screen.blit(
            desc,
            desc.get_rect(
                center=(640,150)
            )
        )

        # -------------------------------
        # Hero Name
        # -------------------------------

        label = self.heading_font.render(
            "Hero Name",
            True,
            (255,220,80)
        )

        screen.blit(label,(390,220))

        pygame.draw.rect(
            screen,
            (35,40,60),
            (390,260,500,55),
            border_radius=10
        )

        pygame.draw.rect(
            screen,
            (255,220,80),
            (390,260,500,55),
            2,
            border_radius=10
        )

        display_name = self.hero_name

        if self.name_active:
         if int(pygame.time.get_ticks()/500) % 2 == 0:
             display_name += "|"

        name = self.text_font.render(
    display_name,
    True,
    (255,255,255)
)

        screen.blit(name,(410,275))

        # -------------------------------
        # Difficulty
        # -------------------------------

        difficulty = self.heading_font.render(
            "Difficulty",
            True,
            (255,220,80)
        )

        screen.blit(difficulty,(390,360))

        start_y = 410

        for i, item in enumerate(self.difficulties):

            selected = i == self.selected

            box = pygame.Rect(
                390,
                start_y + i*75,
                500,
                55
            )

            if selected:

                pygame.draw.rect(
                    screen,
                    (255,220,80),
                    box,
                    border_radius=10
                )

                color = (20,20,20)

            else:

                pygame.draw.rect(
                    screen,
                    (35,40,60),
                    box,
                    border_radius=10
                )

                pygame.draw.rect(
                    screen,
                    (255,220,80),
                    box,
                    2,
                    border_radius=10
                )

                color = (255,255,255)

            text = self.text_font.render(
                item,
                True,
                color
            )

            screen.blit(
                text,
                text.get_rect(
                    center=box.center
                )
            )

        # -------------------------------
        # Begin Button
        # -------------------------------

        button = pygame.Rect(
            470,
            660,
            340,
            60
        )

        pygame.draw.rect(
            screen,
            (255,220,80),
            button,
            border_radius=12
        )

        text = self.heading_font.render(
            "BEGIN JOURNEY",
            True,
            (20,20,20)
        )

        screen.blit(
            text,
            text.get_rect(
                center=button.center
            )
        )

        # -------------------------------
        # Bottom Hint
        # -------------------------------

        hint = self.text_font.render(
            "↑ ↓ Change Difficulty    ENTER Continue    ESC Back",
            True,
            (170,170,170)
        )

        screen.blit(
            hint,
            hint.get_rect(
                center=(640,760)
            )
        )