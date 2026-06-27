import pygame
import sys
from src.engine.settings import VIRTUAL_WIDTH, VIRTUAL_HEIGHT, GAME_TITLE, TARGET_FPS
from src.engine.sound_manager import SoundManager
from src.engine.database import DatabaseManager
from src.utils.question_generator import generate_default_questions

class Game:
    def __init__(self):
        pygame.init()
        
        # Window setup
        self.virtual_width = VIRTUAL_WIDTH
        self.virtual_height = VIRTUAL_HEIGHT
        
        # Screen surface and scaling support
        self.fullscreen = False
        self.screen = pygame.display.set_mode((self.virtual_width, self.virtual_height), pygame.RESIZABLE)
        pygame.display.set_caption(GAME_TITLE)
        
        # The internal logical canvas where all drawing occurs
        self.virtual_canvas = pygame.Surface((self.virtual_width, self.virtual_height))
        
        # Core managers
        generate_default_questions()
        self.db = DatabaseManager()
        self.sounds = SoundManager()
        
        # Load user saved settings
        self.load_settings()
        
        # State machine settings
        self.states = {}
        self.state_stack = []
        self.active_state = None
        
        # Fade transition parameters
        self.fade_alpha = 255 # Start fully black
        self.fade_target_alpha = 0
        self.fade_speed = 400.0 # Alpha points per second
        self.transition_to = None # Name of next state
        self.transition_mode = "change" # "change", "push", "pop"
        
        # Running loop variable
        self.running = True
        self.clock = pygame.time.Clock()
        
        # Initialize state database/instances (deferred imports)
        self.init_states()
        
        # Start game in splash state
        self.change_state("splash")

    def load_settings(self):
        settings = self.db.load_settings()
        if settings:
            self.sounds.set_volumes(settings["music_volume"], settings["sfx_volume"])
            self.fullscreen = settings["fullscreen"]
            if self.fullscreen:
                self.screen = pygame.display.set_mode(
                    (self.virtual_width, self.virtual_height), 
                    pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE
                )
            else:
                self.screen = pygame.display.set_mode((self.virtual_width, self.virtual_height), pygame.RESIZABLE)

    def save_settings(self):
        self.db.save_settings({
            "music_volume": self.sounds.music_volume,
            "sfx_volume": self.sounds.sfx_volume,
            "fullscreen": self.fullscreen,
            "keybindings": None # Place for keybindings maps
        })

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            # Set to fullscreen matching logical aspect ratio bounds
            self.screen = pygame.display.set_mode(
                (0, 0), 
                pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE
            )
        else:
            self.screen = pygame.display.set_mode((self.virtual_width, self.virtual_height), pygame.RESIZABLE)
        self.save_settings()

    def init_states(self):
        # Deferred imports to avoid circular dependencies
        from src.states.splash import SplashState
        from src.states.loading import LoadingState
        from src.states.menu import MenuState
        from src.states.profile import ProfileState
        from src.states.world_map import WorldMapState
        from src.states.explore import ExploreState
        from src.states.battle import BattleState
        from src.states.boss_battle import BossBattleState
        from src.states.shop import ShopState
        from src.states.achievements_menu import AchievementsState
        from src.states.settings_menu import SettingsState
        from src.states.pause import PauseState
        from src.states.victory import VictoryState
        from src.states.game_over import GameOverState

        self.states = {
            "splash": SplashState(self),
            "loading": LoadingState(self),
            "menu": MenuState(self),
            "profile": ProfileState(self),
            "world_map": WorldMapState(self),
            "explore": ExploreState(self),
            "battle": BattleState(self),
            "boss_battle": BossBattleState(self),
            "shop": ShopState(self),
            "achievements": AchievementsState(self),
            "settings": SettingsState(self),
            "pause": PauseState(self),
            "victory": VictoryState(self),
            "game_over": GameOverState(self),
        }

    # State Machine operations
    def set_state(self, state_name):
        if self.active_state:
            self.active_state.exit()
        self.active_state = self.states[state_name]
        self.state_stack = [self.active_state]
        self.active_state.enter()

    def change_state(self, state_name):
        self.transition_to = state_name
        self.transition_mode = "change"
        self.fade_target_alpha = 255

    def push_state(self, state_name):
        self.transition_to = state_name
        self.transition_mode = "push"
        self.fade_target_alpha = 255

    def pop_state(self):
        self.transition_to = "POP"
        self.transition_mode = "pop"
        self.fade_target_alpha = 255

    def get_scaled_rect(self):
        """Calculates scaling rect for letterboxing/pillarboxing."""
        screen_w, screen_h = self.screen.get_size()
        aspect_ratio = self.virtual_width / self.virtual_height
        
        if screen_w / screen_h > aspect_ratio:
            new_h = screen_h
            new_w = int(new_h * aspect_ratio)
            x = (screen_w - new_w) // 2
            y = 0
        else:
            new_w = screen_w
            new_h = int(new_w / aspect_ratio)
            x = 0
            y = (screen_h - new_h) // 2
        return pygame.Rect(x, y, new_w, new_h)

    def get_logical_mouse_pos(self):
        """Maps physical screen cursor position to logical canvas coordinates."""
        mx, my = pygame.mouse.get_pos()
        scaled_rect = self.get_scaled_rect()
        
        if scaled_rect.collidepoint(mx, my):
            rx = mx - scaled_rect.x
            ry = my - scaled_rect.y
            logical_x = int(rx * (self.virtual_width / scaled_rect.width))
            logical_y = int(ry * (self.virtual_height / scaled_rect.height))
            return (logical_x, logical_y)
        return (-999, -999)

    def run(self):
        while self.running:
            dt = self.clock.tick(TARGET_FPS) / 1000.0 # Delta time in seconds
            
            # 1. Event Polling
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f and (pygame.key.get_mods() & pygame.KMOD_ALT):
                        self.toggle_fullscreen()
                
                # Direct events to current active state (except during transitions)
                if not self.transition_to and self.active_state:
                    self.active_state.handle_event(event)

            # 2. Logic Update
            self.update_transition(dt)
            if self.active_state:
                self.active_state.update(dt)

            # 3. Canvas & Screen Drawing
            self.virtual_canvas.fill((0, 0, 0))
            if self.active_state:
                self.active_state.draw(self.virtual_canvas)
                
            # Draw Transition Fade Overlay
            if self.fade_alpha > 0:
                fade_surface = pygame.Surface((self.virtual_width, self.virtual_height))
                fade_surface.fill((0, 0, 0))
                fade_surface.set_alpha(int(self.fade_alpha))
                self.virtual_canvas.blit(fade_surface, (0, 0))
                
            # Blit Logical Canvas to Pygame Screen
            self.screen.fill((0, 0, 0))
            scaled_rect = self.get_scaled_rect()
            scaled_canvas = pygame.transform.smoothscale(self.virtual_canvas, scaled_rect.size)
            self.screen.blit(scaled_canvas, scaled_rect.topleft)
            pygame.display.flip()

        # Clean shutdown
        self.db.close()
        pygame.quit()
        sys.exit()

    def update_transition(self, dt):
        """Smoothly handles alpha levels during active swaps, pushes or pops."""
        if self.transition_to:
            # Fading Out to Black
            self.fade_alpha = min(255.0, self.fade_alpha + self.fade_speed * dt)
            if self.fade_alpha >= 255.0:
                self.fade_alpha = 255.0
                
                # Perform the state change
                if self.transition_mode == "change":
                    self.set_state(self.transition_to)
                elif self.transition_mode == "push":
                    if self.active_state:
                        self.active_state.exit()
                    self.active_state = self.states[self.transition_to]
                    self.state_stack.append(self.active_state)
                    self.active_state.enter()
                elif self.transition_mode == "pop":
                    if len(self.state_stack) > 1:
                        self.active_state.exit()
                        self.state_stack.pop()
                        self.active_state = self.state_stack[-1]
                        self.active_state.enter()
                        
                self.transition_to = None
        else:
            # Fading In from Black
            if self.fade_alpha > 0.0:
                self.fade_alpha = max(0.0, self.fade_alpha - self.fade_speed * dt)
