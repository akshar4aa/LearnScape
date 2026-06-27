import pygame

from src.states.state import State

from src.ui.battle_background import BattleBackground
from src.ui.health_bar import HealthBar
from src.ui.battle_button import BattleButton
from src.ui.popup import Popup


class QuizState(State):

    def __init__(self, game):

        super().__init__(game)

        self.game = game

        width = self.game.screen.get_width()
        height = self.game.screen.get_height()

        # Background
        self.background = BattleBackground(width, height)

        # Fonts
        self.title_font = pygame.font.SysFont(
            "arial",
            52,
            bold=True
        )

        self.question_font = pygame.font.SysFont(
            "arial",
            30,
            bold=True
        )

        self.small_font = pygame.font.SysFont(
            "arial",
            22
        )

        # Popup
        self.popup = Popup()

        # HP Bars
        self.hero_hp = HealthBar(
            60,
            120,
            220,
            22,
            5
        )

        self.enemy_hp = HealthBar(
            1000,
            120,
            220,
            22,
            5
        )

        # Question
        self.question = "What is 8 × 7 ?"

        self.answers = [
            "54",
            "56",
            "64",
            "48"
        ]

        self.correct = 1

        # Buttons
        self.buttons = []

        start_y = 320

        for i in range(4):

            self.buttons.append(

                BattleButton(

                    330,

                    start_y + i * 85,

                    620,

                    60,

                    self.answers[i]

                )

            )

        self.selected = 0
        self.buttons[0].selected = True