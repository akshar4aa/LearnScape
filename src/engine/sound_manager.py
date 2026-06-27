import pygame
import math
import struct
import random

class SoundManager:
    def __init__(self):
        # Default volume parameters
        self.music_volume = 0.5
        self.sfx_volume = 0.5
        
        # Audio parameters
        self.sample_rate = 22050
        
        # Initialize pygame mixer
        try:
            pygame.mixer.init(frequency=self.sample_rate, size=-16, channels=1, buffer=1024)
        except Exception as e:
            print(f"Mixer initialization failed: {e}")
        
        # Audio assets dictionaries
        self.music_tracks = {}
        self.sfx_sounds = {}
        
        # Current active music channel & track name
        self.music_channel = None
        self.current_music_name = None
        
        # Generate procedural sound effects and music tracks
        self.generate_assets()

    def set_volumes(self, music_vol, sfx_vol):
        self.music_volume = max(0.0, min(1.0, music_vol))
        self.sfx_volume = max(0.0, min(1.0, sfx_vol))
        
        # Update active music channel volume
        if self.music_channel:
            self.music_channel.set_volume(self.music_volume)

    # --- Synth Helpers ---
    def generate_sine_wave(self, freq, duration, amplitude=16000):
        num_samples = int(self.sample_rate * duration)
        samples = []
        for i in range(num_samples):
            t = i / self.sample_rate
            val = amplitude * math.sin(2 * math.pi * freq * t)
            samples.append(int(val))
        return samples

    def generate_square_wave(self, freq, duration, amplitude=8000):
        num_samples = int(self.sample_rate * duration)
        samples = []
        period = self.sample_rate / freq
        for i in range(num_samples):
            val = amplitude if (i % period) < (period / 2) else -amplitude
            samples.append(int(val))
        return samples

    def generate_triangle_wave(self, freq, duration, amplitude=12000):
        num_samples = int(self.sample_rate * duration)
        samples = []
        period = self.sample_rate / freq
        for i in range(num_samples):
            phase = (i % period) / period
            val = amplitude * (4 * abs(phase - 0.5) - 1)
            samples.append(int(val))
        return samples

    def generate_noise_wave(self, duration, amplitude=8000):
        num_samples = int(self.sample_rate * duration)
        samples = []
        for _ in range(num_samples):
            val = random.uniform(-amplitude, amplitude)
            samples.append(int(val))
        return samples

    def samples_to_sound(self, samples):
        # Pack list of integers into a byte string (16-bit little-endian signed integer)
        byte_data = struct.pack(f"<{len(samples)}h", *samples)
        try:
            return pygame.mixer.Sound(buffer=byte_data)
        except Exception as e:
            print(f"Failed to create Sound from buffer: {e}")
            # Return a blank Sound
            return pygame.mixer.Sound(buffer=b'\x00' * 100)

    # --- Procedural Sound Effects ---
    def generate_assets(self):
        print("Synthesizing audio assets...")
        
        # 1. Click SFX: short sweeping-down sine wave
        click_samples = []
        duration = 0.08
        num_samples = int(self.sample_rate * duration)
        for i in range(num_samples):
            t = i / self.sample_rate
            freq = 600 - 400 * (t / duration)
            val = 14000 * math.sin(2 * math.pi * freq * t) * (1.0 - t/duration)
            click_samples.append(int(val))
        self.sfx_sounds["click"] = self.samples_to_sound(click_samples)

        # 2. Hit SFX: decaying white noise combined with low triangle buzz
        hit_samples = []
        duration = 0.25
        num_samples = int(self.sample_rate * duration)
        for i in range(num_samples):
            t = i / self.sample_rate
            env = (1.0 - t / duration) ** 2
            noise = random.uniform(-10000, 10000) * env
            buzz = 5000 * (1 if math.sin(2 * math.pi * 90 * t) > 0 else -1) * env
            hit_samples.append(int(noise + buzz))
        self.sfx_sounds["hit"] = self.samples_to_sound(hit_samples)

        # 3. Correct Answer SFX: chiptune arpeggio (C5 -> G5)
        correct_samples = []
        # C5 (523Hz) for 0.1s, then G5 (784Hz) for 0.2s
        correct_samples.extend(self.generate_triangle_wave(523.25, 0.1, amplitude=10000))
        correct_samples.extend(self.generate_triangle_wave(783.99, 0.2, amplitude=10000))
        self.sfx_sounds["correct"] = self.samples_to_sound(correct_samples)

        # 4. Wrong Answer SFX: buzzing low frequency sweep down
        wrong_samples = []
        duration = 0.4
        num_samples = int(self.sample_rate * duration)
        for i in range(num_samples):
            t = i / self.sample_rate
            freq = 150 - 80 * (t / duration)
            period = self.sample_rate / freq
            val = 10000 if (i % period) < (period / 2) else -10000
            val *= (1.0 - t / duration) # Decay
            wrong_samples.append(int(val))
        self.sfx_sounds["wrong"] = self.samples_to_sound(wrong_samples)

        # 5. Chest Open SFX: rapid positive arpeggio
        chest_samples = []
        pitches = [261.63, 329.63, 392.00, 523.25, 659.25, 783.99] # C4, E4, G4, C5, E5, G5
        for pitch in pitches:
            chest_samples.extend(self.generate_sine_wave(pitch, 0.05, amplitude=6000))
        self.sfx_sounds["chest"] = self.samples_to_sound(chest_samples)

        # 6. Level Up SFX: victory theme arpeggio
        lvl_samples = []
        notes = [523.25, 659.25, 783.99, 1046.50] # C5, E5, G5, C6
        for note in notes[:-1]:
            lvl_samples.extend(self.generate_triangle_wave(note, 0.1, amplitude=9000))
        lvl_samples.extend(self.generate_triangle_wave(notes[-1], 0.3, amplitude=9000))
        self.sfx_sounds["level_up"] = self.samples_to_sound(lvl_samples)

        # 7. Portal SFX: sliding laser swoop
        portal_samples = []
        duration = 0.5
        num_samples = int(self.sample_rate * duration)
        for i in range(num_samples):
            t = i / self.sample_rate
            freq = 100 + 1200 * math.sin(math.pi * t / duration)
            val = 8000 * math.sin(2 * math.pi * freq * t) * (1.0 - t/duration)
            portal_samples.append(int(val))
        self.sfx_sounds["portal"] = self.samples_to_sound(portal_samples)

        # --- Music Loop Synth (Melody + Bass chiptunes) ---
        # We will create 4 simple background music tracks: menu, explore, battle, boss
        self.music_tracks["menu"] = self.samples_to_sound(self.synth_music_loop("menu"))
        self.music_tracks["explore"] = self.samples_to_sound(self.synth_music_loop("explore"))
        self.music_tracks["battle"] = self.samples_to_sound(self.synth_music_loop("battle"))
        self.music_tracks["boss"] = self.samples_to_sound(self.synth_music_loop("boss"))
        print("Audio assets synthesized successfully!")

    def synth_music_loop(self, style):
        """Generates a looping chiptune track based on a notes sequence."""
        # 4 seconds loop
        tempo = 120 # BPM
        beat_len = 60.0 / tempo # 0.5 seconds per beat
        
        # Note pitches dictionary (Key to Freq)
        # C4=261.63, D4=293.66, E4=329.63, F4=349.23, G4=392.00, A4=440.00, B4=493.88
        # C5=523.25, D5=587.33, E5=659.25, F5=698.46, G5=783.99, A5=880.00, B5=987.77
        notes = {
            'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23, 'G4': 392.00, 'A4': 440.00, 'B4': 493.88,
            'C5': 523.25, 'D5': 587.33, 'E5': 659.25, 'F5': 698.46, 'G5': 783.99, 'A5': 880.00, 'B5': 987.77,
            'REST': 0
        }
        
        melody = []
        bass = []
        
        if style == "menu":
            # Magical, slow arpeggio (C Major / A minor vibe)
            # Duration = 8 beats * 0.5s = 4.0s
            melody_seq = [('A4', 1), ('C5', 1), ('E5', 1), ('G5', 1), ('F5', 1), ('E5', 1), ('D5', 1), ('C5', 1)]
            bass_seq = [('A3', 2), ('C3', 2), ('F3', 2), ('G3', 2)] # We pitch bass down
        elif style == "explore":
            # Upbeat, heroic major progression (C major)
            # 8 beats
            melody_seq = [('C5', 1), ('E5', 0.5), ('G5', 0.5), ('A5', 1), ('G5', 1), ('F5', 1), ('E5', 1), ('D5', 2)]
            bass_seq = [('C3', 2), ('F3', 2), ('G3', 2), ('C3', 2)]
        elif style == "battle":
            # Tense, minor key melody (D minor)
            # 8 beats
            melody_seq = [('D5', 0.5), ('REST', 0.5), ('F5', 0.5), ('A5', 0.5), ('G5', 1), ('F5', 1), ('E5', 1), ('A5', 1), ('D5', 2)]
            bass_seq = [('D3', 1), ('D3', 1), ('F3', 1), ('G3', 1), ('A3', 2), ('D3', 2)]
        else: # boss
            # Tense and scary minor chords/jumps (G minor / C# diminished)
            # 8 beats
            melody_seq = [('G4', 1), ('A#4', 1), ('C#5', 2), ('C5', 1), ('A#4', 1), ('G4', 2)]
            bass_seq = [('G2', 2), ('C#2', 2), ('C2', 2), ('G2', 2)]

        # Lower octaves for bass
        bass_freqs = []
        for note_name, duration in bass_seq:
            base_name = note_name[:-1]
            octave = int(note_name[-1])
            freq = notes.get(f"{base_name}{octave+1}", 0) / 2.0 # shift down an octave
            bass_freqs.append((freq, duration))
            
        melody_freqs = []
        for note_name, duration in melody_seq:
            freq = notes.get(note_name, 0)
            melody_freqs.append((freq, duration))

        # Render melody
        melody_samples = []
        for freq, duration in melody_freqs:
            len_sec = duration * beat_len
            if freq == 0:
                melody_samples.extend([0] * int(self.sample_rate * len_sec))
            else:
                # Square wave for retro lead
                melody_samples.extend(self.generate_square_wave(freq, len_sec, amplitude=4000))
                
        # Render bass
        bass_samples = []
        for freq, duration in bass_freqs:
            len_sec = duration * beat_len
            if freq == 0:
                bass_samples.extend([0] * int(self.sample_rate * len_sec))
            else:
                # Triangle wave for smooth bass
                bass_samples.extend(self.generate_triangle_wave(freq, len_sec, amplitude=6000))

        # Pad to equal size
        max_len = max(len(melody_samples), len(bass_samples))
        melody_samples.extend([0] * (max_len - len(melody_samples)))
        bass_samples.extend([0] * (max_len - len(bass_samples)))

        # Blend
        combined = []
        for i in range(max_len):
            val = melody_samples[i] + bass_samples[i]
            # Ensure it fits in 16-bit
            val = max(-32768, min(32767, val))
            combined.append(val)
            
        return combined

    def play_sfx(self, name):
        if name in self.sfx_sounds:
            sound = self.sfx_sounds[name]
            sound.set_volume(self.sfx_volume)
            sound.play()

    def play_music(self, name):
        if name == self.current_music_name:
            return # Already playing
            
        if name in self.music_tracks:
            # Stop existing music
            self.stop_music()
            
            sound = self.music_tracks[name]
            self.current_music_name = name
            
            # Play on loop
            try:
                self.music_channel = sound.play(loops=-1)
                if self.music_channel:
                    self.music_channel.set_volume(self.music_volume)
            except Exception as e:
                print(f"Failed to play music: {e}")

    def stop_music(self):
        if self.music_channel:
            try:
                self.music_channel.stop()
            except:
                pass
            self.music_channel = None
        self.current_music_name = None
