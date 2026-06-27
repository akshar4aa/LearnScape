import pygame
import random

from src.states.state import State
from src.ui.background import Background
from src.ui.progressbar import ProgressBar
from src.states.world_map_state import WorldMapState

class LoadingState(State):
    def __init__(self, game):
        super().__init__(game)
        width = self.game.screen.get_width()
        height = self.game.screen.get_height()
        self.background = Background(width, height)

        self.title_font = pygame.font.SysFont("arial", 60, bold=True)
        self.text_font = pygame.font.SysFont("arial", 28)
        self.small_font = pygame.font.SysFont("arial", 22)

        self.progress = 0.0
        self.timer = 0.0
        self.duration = 3.0  # 3 seconds loading

        # Educational/gaming loading tips
        self.tips = [
            "Tip: Earth contains Mathematics lessons like Fractions and Decimals.",
            "Tip: Jupiter contains Science lessons including Solar System and Animals.",
            "Tip: Saturn hosts Coding lessons covering Loops, Functions, and Lists.",
            "Tip: Streaks in Quiz Battle multiply the XP you receive!",
            "Tip: Re-complete quizzes to earn extra coins and lock achievements.",
            "Tip: You can customize your music volume in the Settings menu."
        ]
        self.selected_tip = random.choice(self.tips)

        # Initialize progress bar
        self.progress_bar = ProgressBar(290, 380, 700, 35)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
                return

    def update(self, dt):
        self.background.update(dt)
        self.timer += dt

        # Calculate progress fraction
        self.progress = min(1.0, self.timer / self.duration)
        self.progress_bar.set_progress(self.progress)

        # Automatically transition
        if self.timer >= self.duration:
            # First, check if global stats are initialized. If they are not (e.g. first load), initialize them:
            if not hasattr(self.game, 'hero_name'):
                self.game.hero_name = "Explorer"
            if not hasattr(self.game, 'char_type'):
                self.game.char_type = "Scholar"
            if not hasattr(self.game, 'xp'):
                self.game.xp = 0
            if not hasattr(self.game, 'coins'):
                self.game.coins = 0
            if not hasattr(self.game, 'level'):
                self.game.level = 1
            if not hasattr(self.game, 'unlocked_planets'):
                self.game.unlocked_planets = ["Earth"]
            if not hasattr(self.game, 'completed_lessons'):
                self.game.completed_lessons = []
            if not hasattr(self.game, 'achievements'):
                self.game.achievements = []

            # Save initial game state if it doesn't exist
            from src.utils.save_system import SaveSystem
            save_data = {
                "hero_name": self.game.hero_name,
                "char_type": self.game.char_type,
                "xp": self.game.xp,
                "coins": self.game.coins,
                "level": self.game.level,
                "unlocked_planets": self.game.unlocked_planets,
                "completed_lessons": self.game.completed_lessons,
                "achievements": self.game.achievements
            }
            SaveSystem.save(save_data)

            self.game.change_state(WorldMapState(self.game))

    def draw(self, screen):
        self.background.draw(screen)

        # Title
        title = self.title_font.render("LearnScape", True, (255, 220, 80))
        screen.blit(title, title.get_rect(center=(640, 140)))

        # Subtitle
        loading = self.text_font.render("Preparing Your Adventure...", True, (230, 230, 230))
        screen.blit(loading, loading.get_rect(center=(640, 230)))

        # Progress Bar
        self.progress_bar.draw(screen)

        # Percentage Text
        percent = self.small_font.render(f"{int(self.progress * 100)}%", True, (255, 255, 255))
        screen.blit(percent, percent.get_rect(center=(640, 450)))

        # Tip
        tip_surf = self.small_font.render(self.selected_tip, True, (200, 200, 200))
        screen.blit(tip_surf, tip_surf.get_rect(center=(640, 600)))