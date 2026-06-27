import pygame
import math
from src.utils.helpers import get_font

class NPCTeacher:
    def __init__(self, game, name, subject, x, y, dialogues):
        self.game = game
        self.name = name
        self.subject = subject
        self.x = x
        self.y = y
        self.width = 64
        self.height = 64
        
        # Dialogue queue
        self.dialogues = dialogues
        self.dialogue_index = 0
        self.quest_delivered = False
        
        # Distinct customization colors for teachers based on subjects
        self.hair_color = (220, 220, 220) # Grey hair professors
        if subject == "biology":
            self.outfit_color = (40, 130, 60) # Green robes
        elif subject == "chemistry":
            self.outfit_color = (200, 80, 20) # Orange robes
        elif subject == "physics":
            self.outfit_color = (130, 40, 180) # Purple robes
        elif subject == "mathematics":
            self.outfit_color = (30, 80, 180) # Blue robes
        elif subject == "computer_science":
            self.outfit_color = (30, 170, 90) # Cyber Green robes
        else:
            self.outfit_color = (130, 90, 40) # Brown scholarly robes

    def get_rect(self):
        """Returns the interaction/collision rect of the teacher."""
        return pygame.Rect(self.x + 16, self.y + 16, 32, 48)

    def draw(self, surface, animation_tick=0):
        # Retrieve professor sprite frame
        loader = self.game.states["loading"].loader
        prof_sprite = loader.get_image(
            f"teacher_{self.subject}", 
            loader.create_character_frame,
            "idle", self.hair_color, self.outfit_color, int(animation_tick)
        )
        
        # Draw shadow
        shadow_surf = pygame.Surface((24, 8), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surf, (0, 0, 0, 90), (0, 0, 24, 8))
        surface.blit(shadow_surf, (self.x + 4, self.y + 24))
        
        # Draw teacher
        surface.blit(prof_sprite, (self.x, self.y))

    def draw_prompt(self, surface, player):
        """Draws an interaction indicator above their head if player is close."""
        dist = math.sqrt((player.x - self.x)**2 + (player.y - self.y)**2)
        if dist < 90:
            # Floating yellow indicator bubble
            bx = int(self.x + 16)
            by = int(self.y - 20 + 3 * math.sin(pygame.time.get_ticks() * 0.005))
            
            font = get_font(12, is_bold=True)
            text_surf = font.render("[E] Talk", True, (255, 235, 100))
            
            # Rounded background bubble
            bg_rect = pygame.Rect(bx - text_surf.get_width()//2 - 6, by - 4, text_surf.get_width() + 12, text_surf.get_height() + 8)
            pygame.draw.rect(surface, (20, 20, 25), bg_rect, border_radius=4)
            pygame.draw.rect(surface, (230, 185, 55), bg_rect, 1, border_radius=4)
            
            surface.blit(text_surf, (bx - text_surf.get_width()//2, by))

    def interact(self):
        """Advances dialogue. Returns the text to display, or None if done."""
        if self.dialogue_index < len(self.dialogues):
            text = self.dialogues[self.dialogue_index]
            self.dialogue_index += 1
            return text
        else:
            self.dialogue_index = 0 # Reset dialogue loop
            return None
