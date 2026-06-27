import pygame
import math
import random

class Monster:
    def __init__(self, game, m_type, subject, x, y, level=1, is_boss=False):
        self.game = game
        self.m_type = m_type
        self.subject = subject
        self.x = float(x)
        self.y = float(y)
        self.start_x = x
        self.start_y = y
        self.level = level
        self.is_boss = is_boss
        
        # Scale stats with level and check if it is a boss
        if is_boss:
            self.max_hp = 100 + level * 50
            self.hp = self.max_hp
            self.attack = 15 + level * 5
            self.defense = 5 + level * 2
            self.name = f"{subject.capitalize()} Arch-Boss"
        else:
            self.max_hp = 25 + level * 15
            self.hp = self.max_hp
            self.attack = 8 + level * 2
            self.defense = 1 + level
            self.name = f"Wild {m_type.capitalize()} (Lvl {level})"
            
        # Animation & Patrol parameters
        self.patrol_radius = 60.0
        self.patrol_speed = 30.0
        self.angle = random.uniform(0, 2 * math.pi)
        self.anim_tick = random.uniform(0, 100)
        self.width = 64
        self.height = 64

    def get_rect(self):
        """Hitbox used for combat trigger check (explore collisions)."""
        return pygame.Rect(int(self.x + 12), int(self.y + 12), 40, 40)

    def update(self, dt):
        self.anim_tick += dt * 5.0
        
        # Roaming Patrol AI (only for non-bosses, bosses stay still)
        if not self.is_boss:
            self.angle += random.uniform(-0.5, 0.5) * dt
            dx = math.cos(self.angle) * self.patrol_speed * dt
            dy = math.sin(self.angle) * self.patrol_speed * dt
            
            # Check if moving outside patrol range
            new_x = self.x + dx
            new_y = self.y + dy
            dist = math.sqrt((new_x - self.start_x)**2 + (new_y - self.start_y)**2)
            
            if dist < self.patrol_radius:
                self.x = new_x
                self.y = new_y
            else:
                # Steer back to center
                self.angle = math.atan2(self.start_y - self.y, self.start_x - self.x)
                
    def draw(self, surface):
        loader = self.game.states["loading"].loader
        # Draw monster frame
        sprite = loader.get_image(
            f"monster_{self.m_type}", 
            loader.create_monster_sprite, 
            self.m_type, int(self.anim_tick)
        )
        surface.blit(sprite, (int(self.x), int(self.y)))


class KingdomBoss(Monster):
    def __init__(self, game, subject, x, y, level=5):
        # Choose a heavy monster type for the boss
        m_type = "dragon" if subject == "science" else "golem"
        super().__init__(game, m_type, subject, x, y, level, is_boss=True)
        
        # Boss Battle phase tracking (3 phases)
        self.max_phases = 3
        self.current_phase = 1
        self.shield_hp = 0
        self.shield_max = 50
        
    def take_damage(self, amount):
        """Damages boss. Handles phased checkpoints."""
        if self.shield_hp > 0:
            # Absorb with shield first
            self.shield_hp -= amount
            if self.shield_hp < 0:
                leftover = abs(self.shield_hp)
                self.shield_hp = 0
                self.hp = max(0, self.hp - leftover)
        else:
            self.hp = max(0, self.hp - amount)

        # Update phases based on HP thresholds
        # Phase 2 triggers at < 70% health
        # Phase 3 triggers at < 35% health
        health_pct = self.hp / self.max_hp
        
        if health_pct < 0.35 and self.current_phase < 3:
            self.current_phase = 3
            self.game.sounds.play_sfx("portal") # Play roar sweep sound
            print("Boss entering Phase 3! (Harder questions)")
        elif health_pct < 0.70 and self.current_phase < 2:
            self.current_phase = 2
            self.shield_hp = self.shield_max
            self.game.sounds.play_sfx("portal") # Play shield up sound
            print("Boss entering Phase 2! (Summoned Shield)")

    def get_phase_description(self):
        if self.current_phase == 1:
            return "Phase 1: Basic Combat"
        elif self.current_phase == 2:
            return f"Phase 2: Arcane Shield Active ({self.shield_hp} SHD)"
        else:
            return "Phase 3: Berserker Mode (Time limit questions!)"
