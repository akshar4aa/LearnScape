import pygame
import math
import random
import json
import os
from src.engine.state import State
from src.ui.dialogue import BattleQuestionPanel
from src.ui.ui_elements import ProgressBar, Button
from src.ui.particle import ParticleSystem, Particle
from src.utils.helpers import get_font, draw_rounded_panel, draw_gradient_rect
from src.engine.settings import QUESTIONS_DIR

class BattleState(State):
    def __init__(self, game):
        super().__init__(game)
        
        self.monster = None
        self.particles = ParticleSystem()
        
        # Attack animations offsets (lunge slides)
        self.player_offset_x = 0.0
        self.enemy_offset_x = 0.0
        
        # Screen shake parameters
        self.shake_intensity = 0.0
        self.shake_decay = 10.0 # decay speed per second
        self.flash_red_timer = 0.0
        
        # HUD bars
        self.pb_player_hp = None
        self.pb_player_mana = None
        self.pb_enemy_hp = None
        
        # Interactive question panel
        self.question_panel = None
        self.active_question = None
        
        # Battle menus buttons (inventory slots)
        self.btn_potion_hp = None
        self.btn_potion_mp = None
        self.btn_hint = None
        
        self.font_stats = get_font(14, is_bold=True)
        self.font_combat_log = get_font(16)
        
        # Study metrics tracking per battle
        self.questions_asked = 0
        self.questions_correct = 0

    def init_battle(self, monster):
        self.monster = monster
        self.particles.clear()
        
        self.player_offset_x = 0.0
        self.enemy_offset_x = 0.0
        self.shake_intensity = 0.0
        self.flash_red_timer = 0.0
        self.questions_asked = 0
        self.questions_correct = 0
        
        # Setup question callback
        self.question_panel = BattleQuestionPanel(self.game, 40, 460, 920, 230, self.handle_answer)
        
        # HUD Progress bars
        player = self.game.player
        self.pb_player_hp = ProgressBar(40, 100, 240, 22, player.hp, player.max_hp, (230, 50, 50), "HP:")
        self.pb_player_mana = ProgressBar(40, 130, 240, 22, player.mana, player.max_mana, (50, 140, 230), "MP:")
        self.pb_enemy_hp = ProgressBar(980, 100, 260, 22, monster.hp, monster.max_hp, (230, 50, 50), "HP:")
        
        # Battle actionable items buttons
        self.refresh_item_buttons()
        self.fetch_new_question()

    def refresh_item_buttons(self):
        player = self.game.player
        
        # Get item quantities from inventory list
        count_hp = next((i["quantity"] for i in player.inventory if i["id"] == "health_potion"), 0)
        count_mp = next((i["quantity"] for i in player.inventory if i["id"] == "mana_potion"), 0)
        count_hint = next((i["quantity"] for i in player.inventory if i["id"] == "hint_card"), 0)
        
        # Instantiate buttons
        bx = 980
        by = 460
        spacing = 54
        
        self.btn_potion_hp = Button(self.game, bx, by, 260, 42, f"Heal Potion ({count_hp})", self.use_health_potion, color=(140, 40, 40))
        self.btn_potion_mp = Button(self.game, bx, by + spacing, 260, 42, f"Mana Potion ({count_mp})", self.use_mana_potion, color=(30, 80, 140))
        self.btn_hint = Button(self.game, bx, by + spacing * 2, 260, 42, f"Use Hint Card ({count_hint})", self.use_hint_card, color=(120, 100, 30))
        
        # Disable buttons if counts are zero
        self.btn_potion_hp.set_enabled(count_hp > 0)
        self.btn_potion_mp.set_enabled(count_mp > 0)
        self.btn_hint.set_enabled(count_hint > 0)

    def fetch_new_question(self):
        """Loads a random question from subject JSON files."""
        subject = self.monster.subject
        file_path = os.path.join(QUESTIONS_DIR, f"{subject}.json")
        
        # Fallback question if file is not found
        default_q = {
            "question": "What is the value of 12 * 9?",
            "choices": ["108", "96", "112", "118"],
            "answer": "108"
        }
        
        if os.path.exists(file_path):
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)
                    if data:
                        # Grab random item
                        default_q = random.choice(data)
            except Exception as e:
                print(f"Error reading question JSON: {e}")
                
        # Shuffle choices order
        shuffled = list(default_q["choices"])
        random.shuffle(shuffled)
        
        self.active_question = {
            "question": default_q["question"],
            "choices": shuffled,
            "answer": default_q["answer"]
        }
        self.question_panel.load_question(self.active_question)

    # Item usages
    def use_health_potion(self):
        player = self.game.player
        item = next((i for i in player.inventory if i["id"] == "health_potion"), None)
        if item and item["quantity"] > 0:
            item["quantity"] -= 1
            player.hp = min(player.max_hp, player.hp + 50)
            self.game.sounds.play_sfx("correct")
            self.particles.add_heal_burst(180 + 32, 280 + 32)
            self.particles.add_floating_text("+50 HP", 180, 240, (50, 230, 80))
            self.refresh_item_buttons()

    def use_mana_potion(self):
        player = self.game.player
        item = next((i for i in player.inventory if i["id"] == "mana_potion"), None)
        if item and item["quantity"] > 0:
            item["quantity"] -= 1
            player.mana = min(player.max_mana, player.mana + 30)
            self.game.sounds.play_sfx("correct")
            self.particles.add_magic_spell(180 + 32, 280 + 32, (50, 180, 240), 10)
            self.particles.add_floating_text("+30 Mana", 180, 240, (50, 180, 240))
            self.refresh_item_buttons()

    def use_hint_card(self):
        player = self.game.player
        item = next((i for i in player.inventory if i["id"] == "hint_card"), None)
        if item and item["quantity"] > 0:
            if self.question_panel.apply_hint_card():
                item["quantity"] -= 1
                self.game.sounds.play_sfx("correct")
                self.refresh_item_buttons()

    # Answer Evaluation
    def handle_answer(self, is_correct):
        player = self.game.player
        monster = self.monster
        
        self.questions_asked += 1
        
        if is_correct:
            # 1. Correct Answer triggers Player Strike
            self.questions_correct += 1
            self.player_offset_x = 80.0 # Lunge forward
            self.game.sounds.play_sfx("hit")
            
            # Compute damage based on stats
            atk_power = player.get_attack_power()
            damage = max(5, atk_power - monster.defense)
            monster.hp = max(0, monster.hp - damage)
            
            # Particle effect on enemy
            self.particles.add_hit_burst(900 + 32, 220 + 32, (255, 215, 0), count=20)
            self.particles.add_floating_text(str(damage), 900 + 10, 200, (255, 235, 100))
        else:
            # 2. Incorrect Answer triggers Enemy Counter strike
            self.enemy_offset_x = -80.0 # Lunge left
            self.game.sounds.play_sfx("wrong")
            
            # Screen shake and red flash
            self.shake_intensity = 15.0
            self.flash_red_timer = 0.25
            
            # Damage player
            m_atk = monster.attack
            damage = max(5, m_atk - player.get_defense())
            player.hp = max(0, player.hp - damage)
            
            # Sparks effect on player
            self.particles.add_hit_burst(180 + 32, 280 + 32, (230, 50, 50), count=15)
            self.particles.add_floating_text(str(damage), 180 + 10, 240, (230, 50, 50))
            
        # Update HP display
        self.pb_player_hp.set_values(player.hp, player.max_hp)
        self.pb_enemy_hp.set_values(monster.hp, monster.max_hp)
        
        # Check battle outcomes
        if monster.hp <= 0:
            # Player Won!
            self.end_battle(won=True)
        elif player.hp <= 0:
            # Player Lost!
            self.end_battle(won=False)
        else:
            # Next turn: load new question
            self.fetch_new_question()

    def end_battle(self, won):
        player = self.game.player
        
        # Save study metrics back to SQL DB
        accuracy = (self.questions_correct / self.questions_asked) * 100.0 if self.questions_asked > 0 else 100.0
        
        # Load previous metrics
        metrics = self.game.db.load_metrics()
        if not metrics:
            metrics = {
                "total_study_time": 0.0,
                "total_questions": 0,
                "correct_questions": 0,
                "monsters_defeated": 0,
                "bosses_defeated": 0
            }
        
        metrics["total_questions"] += self.questions_asked
        metrics["correct_questions"] += self.questions_correct
        
        if won:
            metrics["monsters_defeated"] += 1
            self.game.db.save_metrics(metrics)
            
            # Load victory reward parameters and change state
            # Base rewards: level scale
            coins_loot = 25 + self.monster.level * 10
            xp_loot = 50 + self.monster.level * 20
            
            # Random loot chance
            loot_item = None
            if random.random() < 0.35:
                loot_item = random.choice(["health_potion", "mana_potion", "hint_card"])
                
            # Direct victory info parameters to Victory screen state
            self.game.states["victory"].set_rewards(xp_loot, coins_loot, loot_item)
            self.game.change_state("victory")
        else:
            self.game.db.save_metrics(metrics)
            # Transition to GameOver state
            self.game.change_state("game_over")

    def enter(self):
        self.game.sounds.play_music("battle")

    def exit(self):
        pass

    def handle_event(self, event):
        mouse_pos = self.game.get_logical_mouse_pos()
        
        # Question actions buttons
        self.question_panel.handle_event(event, mouse_pos)
        
        # Item slots buttons
        self.btn_potion_hp.handle_event(event, mouse_pos)
        self.btn_potion_mp.handle_event(event, mouse_pos)
        self.btn_hint.handle_event(event, mouse_pos)

    def update(self, dt):
        mouse_pos = self.game.get_logical_mouse_pos()
        
        # Smoothly decay attack offsets (sliding characters back)
        if self.player_offset_x > 0:
            self.player_offset_x = max(0.0, self.player_offset_x - 300 * dt)
        if self.enemy_offset_x < 0:
            self.enemy_offset_x = min(0.0, self.enemy_offset_x + 300 * dt)
            
        # Screen shake calculations
        if self.shake_intensity > 0:
            self.shake_intensity = max(0.0, self.shake_intensity - self.shake_decay * dt)
            
        if self.flash_red_timer > 0:
            self.flash_red_timer = max(0.0, self.flash_red_timer - dt)

        # Update HUD progress bars
        self.pb_player_hp.update(dt)
        self.pb_player_mana.update(dt)
        self.pb_enemy_hp.update(dt)
        
        # Update particles
        self.particles.update(dt)
        
        # Update widgets
        self.question_panel.update(dt, mouse_pos)
        self.btn_potion_hp.update(dt, mouse_pos)
        self.btn_potion_mp.update(dt, mouse_pos)
        self.btn_hint.update(dt, mouse_pos)

    def draw(self, surface):
        # Apply screen shake offsets
        offset_x = 0
        offset_y = 0
        if self.shake_intensity > 0:
            offset_x = random.randint(-int(self.shake_intensity), int(self.shake_intensity))
            offset_y = random.randint(-int(self.shake_intensity), int(self.shake_intensity))
            
        # Create temp canvas to render shakes safely
        shake_canvas = pygame.Surface((self.game.virtual_width, self.game.virtual_height))
        
        # Arena background split
        # Top half: deep dark blue cave sky
        draw_gradient_rect(shake_canvas, (10, 12, 22), (25, 20, 35), (0, 0, self.game.virtual_width, 280))
        # Bottom half: matching floor ground (e.g. green grid/dark stone)
        floor_color = (40, 80, 50) if self.monster.subject == "biology" else (60, 30, 20) if self.monster.subject == "chemistry" else (30, 40, 55)
        pygame.draw.rect(shake_canvas, floor_color, (0, 280, self.game.virtual_width, 440))
        pygame.draw.line(shake_canvas, (165, 120, 25), (0, 280), (self.game.virtual_width, 280), 3) # Divider

        # Renders User & Enemy Stats Panels
        draw_rounded_panel(shake_canvas, (30, 20, 320, 150), (20, 20, 25), (165, 120, 25), border_width=2, bg_alpha=200)
        draw_rounded_panel(shake_canvas, (930, 20, 320, 150), (20, 20, 25), (165, 120, 25), border_width=2, bg_alpha=200)

        # Draw Player stats labels
        player = self.game.player
        p_name = self.font_stats.render(f"HERO: {player.name} (Lvl {player.level})", True, (255, 235, 100))
        p_atk = self.font_stats.render(f"Attack: {player.get_attack_power()}", True, (200, 200, 210))
        p_def = self.font_stats.render(f"Defense: {player.get_defense()}", True, (200, 200, 210))
        
        shake_canvas.blit(p_name, (40, 35))
        shake_canvas.blit(p_atk, (40, 60))
        shake_canvas.blit(p_def, (180, 60))
        self.pb_player_hp.draw(shake_canvas)
        self.pb_player_mana.draw(shake_canvas)

        # Draw Enemy stats labels
        m_name = self.font_stats.render(self.monster.name, True, (255, 100, 100))
        m_atk_lbl = self.font_stats.render(f"Atk: {self.monster.attack}", True, (200, 200, 210))
        m_def_lbl = self.font_stats.render(f"Def: {self.monster.defense}", True, (200, 200, 210))
        
        shake_canvas.blit(m_name, (980, 35))
        shake_canvas.blit(m_atk_lbl, (980, 65))
        shake_canvas.blit(m_def_lbl, (1120, 65))
        self.pb_enemy_hp.draw(shake_canvas)

        # Renders Player & Monster sprites (with attack lunge offsets)
        loader = self.game.states["loading"].loader
        tick = pygame.time.get_ticks() * 0.005
        
        # Player (double scale)
        p_sprite = loader.get_image(
            "player_battle_idle", 
            loader.create_character_frame,
            "idle", player.hair_color, player.outfit_color, int(tick)
        )
        p_sprite_large = pygame.transform.scale(p_sprite, (128, 128))
        px = 180 + int(self.player_offset_x)
        py = 200
        # Draw shadow
        sh_surf = pygame.Surface((48, 16), pygame.SRCALPHA)
        pygame.draw.ellipse(sh_surf, (0, 0, 0, 90), (0, 0, 48, 16))
        shake_canvas.blit(sh_surf, (px + 40, py + 110))
        shake_canvas.blit(p_sprite_large, (px, py))

        # Monster (double scale)
        m_sprite = loader.get_image(
            f"monster_battle_{self.monster.m_type}", 
            loader.create_monster_sprite,
            self.monster.m_type, int(tick)
        )
        m_sprite_large = pygame.transform.scale(m_sprite, (128, 128))
        mx = 900 + int(self.enemy_offset_x)
        my = 200
        # Draw shadow
        shake_canvas.blit(sh_surf, (mx + 40, my + 110))
        
        # Flip monster horizontally so they look left at player
        m_sprite_flipped = pygame.transform.flip(m_sprite_large, True, False)
        shake_canvas.blit(m_sprite_flipped, (mx, my))

        # Render floating particles/damage numbers
        self.particles.draw(shake_canvas)

        # Draw Question and Choices Panels
        self.question_panel.draw(shake_canvas)
        
        # Draw Item buttons panel on right side
        draw_rounded_panel(shake_canvas, (970, 450, 280, 240), (20, 20, 25), (165, 120, 25), border_width=2, bg_alpha=200)
        self.btn_potion_hp.draw(shake_canvas)
        self.btn_potion_mp.draw(shake_canvas)
        self.btn_hint.draw(shake_canvas)

        # Blit canvas to screen applying shakes offsets
        surface.blit(shake_canvas, (offset_x, offset_y))
        
        # Draw red flash overlay if player took damage
        if self.flash_red_timer > 0:
            red_surf = pygame.Surface((self.game.virtual_width, self.game.virtual_height))
            red_surf.fill((255, 0, 0))
            red_surf.set_alpha(int(80 * (self.flash_red_timer / 0.25)))
            surface.blit(red_surf, (0, 0))
