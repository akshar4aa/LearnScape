import pygame
import os

class AudioManager:
    def __init__(self):
        self.mixer_initialized = False
        try:
            pygame.mixer.init()
            self.mixer_initialized = True
        except Exception as e:
            print(f"Warning: Audio mixer failed to initialize: {e}")

        self.music_volume = 0.5
        self.sfx_volume = 0.5
        self.sounds = {}
        self.current_music = None

    def play_music(self, path, loops=-1):
        if not self.mixer_initialized:
            return
        
        # Check if file exists
        if not os.path.exists(path):
            print(f"Audio Warning: Music file not found at {path}")
            return

        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(loops)
            self.current_music = path
        except Exception as e:
            print(f"Audio Error: Failed to play music {path}: {e}")

    def stop_music(self):
        if not self.mixer_initialized:
            return
        pygame.mixer.music.stop()
        self.current_music = None

    def play_sfx(self, path):
        if not self.mixer_initialized:
            return

        if path not in self.sounds:
            if not os.path.exists(path):
                print(f"Audio Warning: SFX file not found at {path}")
                return
            try:
                self.sounds[path] = pygame.mixer.Sound(path)
            except Exception as e:
                print(f"Audio Error: Failed to load SFX {path}: {e}")
                return

        try:
            sound = self.sounds[path]
            sound.set_volume(self.sfx_volume)
            sound.play()
        except Exception as e:
            print(f"Audio Error: Failed to play SFX {path}: {e}")

    def set_music_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, volume))
        if self.mixer_initialized:
            pygame.mixer.music.set_volume(self.music_volume)

    def set_sfx_volume(self, volume):
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)
