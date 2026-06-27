import pygame
import sys
import math

from src.states.state import State
from src.ui.background import Background
from src.ui.button import Button
from src.utils.save_system import SaveSystem

class MenuState(State):
    def __init__(self, game):
        super().__init__(game)
        width = self.game.screen.get_width()
        height = self.game.screen.get_height()
        
        self.background = Background(width, height)
        self.title_font = pygame.font.SysFont("arial", 72, bold=True)
        self.subtitle_font = pygame.font.SysFont("arial", 24)
        self.version_font = pygame.font.SysFont("arial", 18)

        self.options = ["New Adventure", "Continue", "Settings", "Credits", "Exit"]
        self.selected = 0
        self.time = 0.0

        # Check if we have a save game
        self.has_save = SaveSystem.has_save()

        # Initialize buttons
        self.buttons = []
        start_y = 230
        for i, opt in enumerate(self.options):
            # If "Continue" is disabled (no save), we draw it differently but still render it
            btn = Button(width // 2 - 150, start_y + i * 80, 300, 55, opt, font_size=24)
            self.buttons.append(btn)

        # Highlight the first item
        self.buttons[self.selected].selected = True

    def handle_events(self, events):
        mouse_pos = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
                return

            # Mouse button clicks
            for i, btn in enumerate(self.buttons):
                # Disabled "Continue" if no save
                if btn.text == "Continue" and not self.has_save:
                    continue
                
                if btn.handle_event(event, mouse_pos):
                    self.execute_option(btn.text)
                    return

            # Keyboard navigation
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.buttons[self.selected].selected = False
                    self.selected = (self.selected - 1) % len(self.options)
                    self.buttons[self.selected].selected = True
                elif event.key == pygame.K_DOWN:
                    self.buttons[self.selected].selected = False
                    self.selected = (self.selected + 1) % len(self.options)
                    self.buttons[self.selected].selected = True
                elif event.key == pygame.K_RETURN:
                    opt_text = self.options[self.selected]
                    if opt_text == "Continue" and not self.has_save:
                        continue # can't click Continue if no save file
                    self.execute_option(opt_text)

    def execute_option(self, option):
        # Audio feedback play click
        # (Audio manager is hold in Game, e.g., self.game.audio.play_sfx("assets/audio/click.wav"))
        if hasattr(self.game, 'audio'):
            self.game.audio.play_sfx("assets/audio/click.wav")

        if option == "New Adventure":
            from src.states.new_adventure_state import NewAdventureState
            self.game.change_state(NewAdventureState(self.game))
        elif option == "Continue":
            # Load save and go directly to WorldMapState
            save_data = SaveSystem.load()
            # Set game player parameters from loaded save
            self.game.hero_name = save_data.get("hero_name", "Hero")
            self.game.char_type = save_data.get("char_type", "Scholar")
            self.game.xp = save_data.get("xp", 0)
            self.game.coins = save_data.get("coins", 0)
            self.game.level = save_data.get("level", 1)
            self.game.unlocked_planets = save_data.get("unlocked_planets", ["Earth"])
            self.game.completed_lessons = save_data.get("completed_lessons", [])
            self.game.achievements = save_data.get("achievements", [])
            
            from src.states.world_map_state import WorldMapState
            self.game.change_state(WorldMapState(self.game))
        elif option == "Settings":
            from src.states.settings_state import SettingsState
            self.game.change_state(SettingsState(self.game))
        elif option == "Credits":
            from src.states.credits_state import CreditsState
            self.game.change_state(CreditsState(self.game))
        elif option == "Exit":
            self.game.running = False

    def update(self, dt):
        self.time += dt
        self.background.update(dt)

        mouse_pos = pygame.mouse.get_pos()
        # Update hover states
        for i, btn in enumerate(self.buttons):
            btn.update(dt)
            # Update hovered attribute
            btn.hovered = btn.rect.collidepoint(mouse_pos)
            
            # Lock visual styling of Continue if disabled
            if btn.text == "Continue" and not self.has_save:
                btn.hovered = False

    def draw_castle(self, screen):
        width = screen.get_width()
        height = screen.get_height()
        ground = height - 20
        castle = (35, 40, 60)

        # Ground
        pygame.draw.rect(screen, castle, (0, ground, width, 90))
        # Main Building
        pygame.draw.rect(screen, castle, (width // 2 - 120, ground - 90, 240, 90))
        # Center Tower
        pygame.draw.rect(screen, castle, (width // 2 - 35, ground - 220, 70, 220))
        # Left Tower
        pygame.draw.rect(screen, castle, (width // 2 - 145, ground - 170, 55, 170))
        # Right Tower
        pygame.draw.rect(screen, castle, (width // 2 + 90, ground - 170, 55, 170))
        # Center Roof
        pygame.draw.polygon(screen, castle, [(width//2-40, ground-220), (width//2, ground-275), (width//2+40, ground-220)])
        # Left Roof
        pygame.draw.polygon(screen, castle, [(width//2-150, ground-170), (width//2-118, ground-215), (width//2-86, ground-170)])
        # Right Roof
        pygame.draw.polygon(screen, castle, [(width//2+86, ground-170), (width//2+118, ground-215), (width//2+150, ground-170)])
        # Door
        pygame.draw.arc(screen, (50, 50, 65), (width//2-22, ground-42, 44, 42), math.pi, math.pi * 2, 4)

    def draw(self, screen):
        self.background.draw(screen)
        self.draw_castle(screen)

        # Oscillating title scale
        title_scale = 1 + math.sin(self.time * 2) * 0.02
        scaled_title_font = pygame.font.SysFont("arial", int(72 * title_scale), bold=True)
        title = scaled_title_font.render("LearnScape", True, (255, 220, 80))
        title_rect = title.get_rect(center=(screen.get_width() // 2, 90))
        screen.blit(title, title_rect)

        # Subtitle
        subtitle = self.subtitle_font.render("A Journey Through Knowledge", True, (225, 225, 235))
        screen.blit(subtitle, subtitle.get_rect(center=(screen.get_width() // 2, 150)))

        # Decorative line
        pygame.draw.line(screen, (255, 210, 80), (screen.get_width() // 2 - 170, 190), (screen.get_width() // 2 + 170, 190), 2)

        # Draw buttons
        for btn in self.buttons:
            # If Continue is disabled, render with opacity
            if btn.text == "Continue" and not self.has_save:
                # Cache original drawing details
                disabled_btn = Button(btn.rect.x, btn.rect.y, btn.rect.width, btn.rect.height, "Continue (No Save)", font_size=20)
                disabled_btn.selected = False
                disabled_btn.hovered = False
                
                # Draw a grayed-out look
                pygame.draw.rect(screen, (25, 27, 35), btn.rect, border_radius=12)
                pygame.draw.rect(screen, (80, 80, 90), btn.rect, 2, border_radius=12)
                txt_surf = pygame.font.SysFont("arial", 20, bold=True).render("Continue (No Save)", True, (100, 100, 110))
                screen.blit(txt_surf, txt_surf.get_rect(center=btn.rect.center))
            else:
                btn.draw(screen)

        # Help footer
        version = self.version_font.render("LearnScape v1.0.0", True, (130, 130, 150))
        screen.blit(version, (20, screen.get_height() - 35))

        controls = self.version_font.render("↑ ↓ Navigate   ENTER/Mouse Select", True, (130, 130, 150))
        controls_rect = controls.get_rect(bottomright=(screen.get_width() - 20, screen.get_height() - 15))
        screen.blit(controls, controls_rect)