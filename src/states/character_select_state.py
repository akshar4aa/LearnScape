import pygame

from src.states.state import State
from src.ui.background import Background
from src.states.loading_state import LoadingState


class CharacterSelectState(State):

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

        self.text_font = pygame.font.SysFont(
            "arial",
            24
        )

        self.card_font = pygame.font.SysFont(
            "arial",
            30,
            bold=True
        )

        self.characters = [

            {
                "name": "Scholar",
                "emoji": "📚",
                "desc": "Extra XP"
            },

            {
                "name": "Explorer",
                "emoji": "🗺️",
                "desc": "Balanced"
            },

            {
                "name": "Inventor",
                "emoji": "🧪",
                "desc": "Extra Hints"
            },

            {
                "name": "Speedster",
                "emoji": "⚡",
                "desc": "Fast Learner"
            }

        ]

        self.selected = 0
            # =========================================
    # Handle Events
    # =========================================

    def handle_events(self, events):

        for event in events:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    from src.states.new_adventure_state import NewAdventureState

                    self.game.change_state(
                        NewAdventureState(self.game)
                    )

                elif event.key == pygame.K_LEFT:

                    self.selected -= 1

                    if self.selected < 0:
                        self.selected = len(self.characters) - 1

                elif event.key == pygame.K_RIGHT:

                    self.selected += 1

                    if self.selected >= len(self.characters):
                        self.selected = 0

                elif event.key == pygame.K_RETURN:

                    self.game.change_state(
                    LoadingState(self.game)
                    )

    # =========================================
    # Update
    # =========================================

    def update(self, dt):

        self.background.update(dt)

    # =========================================
    # Draw
    # =========================================

    def draw(self, screen):

        self.background.draw(screen)

        # ------------------------
        # Title
        # ------------------------

        title = self.title_font.render(
            "Choose Your Hero",
            True,
            (255, 220, 80)
        )

        screen.blit(
            title,
            title.get_rect(center=(640, 80))
        )

        subtitle = self.text_font.render(
            "Select the hero for your adventure",
            True,
            (220, 220, 220)
        )

        screen.blit(
            subtitle,
            subtitle.get_rect(center=(640, 130))
        )

        # ------------------------
        # Character Cards
        # ------------------------

        start_x = 120
        spacing = 250

        for i, character in enumerate(self.characters):

            x = start_x + i * spacing
            y = 240

            card = pygame.Rect(
                x,
                y,
                180,
                300
            )

            if i == self.selected:

                pygame.draw.rect(
                    screen,
                    (255, 220, 80),
                    card,
                    border_radius=15
                )

                text_color = (20, 20, 20)

            else:

                pygame.draw.rect(
                    screen,
                    (35, 40, 60),
                    card,
                    border_radius=15
                )

                pygame.draw.rect(
                    screen,
                    (255, 220, 80),
                    card,
                    2,
                    border_radius=15
                )

                text_color = (255, 255, 255)

            # Emoji

            emoji = self.card_font.render(
                character["emoji"],
                True,
                text_color
            )

            screen.blit(
                emoji,
                emoji.get_rect(
                    center=(x + 90, y + 60)
                )
            )

            # Name

            name = self.card_font.render(
                character["name"],
                True,
                text_color
            )

            screen.blit(
                name,
                name.get_rect(
                    center=(x + 90, y + 130)
                )
            )

            # Description

            desc = self.text_font.render(
                character["desc"],
                True,
                text_color
            )

            screen.blit(
                desc,
                desc.get_rect(
                    center=(x + 90, y + 190)
                )
            )

        # ------------------------
        # Continue Button
        # ------------------------

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

        text = self.card_font.render(
            "CONTINUE",
            True,
            (20, 20, 20)
        )

        screen.blit(
            text,
            text.get_rect(
                center=button.center
            )
        )

        # ------------------------
        # Bottom Help
        # ------------------------

        help_text = self.text_font.render(
            "← → Select Character    ENTER Continue    ESC Back",
            True,
            (180, 180, 180)
        )

        screen.blit(
            help_text,
            help_text.get_rect(center=(640, 760))
        )