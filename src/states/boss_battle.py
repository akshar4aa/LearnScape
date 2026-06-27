import pygame
import math
import random
import os
import json
from src.states.battle import BattleState
from src.entities.monster import KingdomBoss
from src.ui.ui_elements import ProgressBar, Button
from src.ui.dialogue import BattleQuestionPanel
from src.utils.helpers import get_font, draw_rounded_panel, draw_glowing_text
from src.engine.settings import QUESTIONS_DIR

class BossBattleState(BattleState):
    def __init__(self, game):
        super().__init__(game)
        
        self.phase3_timer = 15.0
        self.max_timer = 15.0
        
        # Shield Progress bar
        self.pb_enemy_shield = None
        self.font_boss = get_font(18, is_bold=True)

    def init_boss_battle(self, subject, level):
        # Instantiate boss
        boss = KingdomBoss(self.game, subject, 880, 180, level)
        self.monster = boss
        
        self.particles.clear()
        self.player_offset_x = 0.0
        self.enemy_offset_x = 0.0
        self.shake_intensity = 0.0
        self.flash_red_timer = 0.0
        
        self.questions_asked = 0
        self.questions_correct = 0
        self.phase3_timer = self.max_timer
        
        # Setup question selector
        self.question_panel = BattleQuestionPanel(self.game, 40, 460, 920, 230, self.handle_answer)
        
        # HUD bars
        player = self.game.player
        self.pb_player_hp = ProgressBar(40, 100, 240, 22, player.hp, player.max_hp, (230, 50, 50), "HP:")
        self.pb_player_mana = ProgressBar(40, 130, 240, 22, player.mana, player.max_mana, (50, 140, 230), "MP:")
        self.pb_enemy_hp = ProgressBar(980, 100, 260, 22, boss.hp, boss.max_hp, (230, 50, 50), "HP:")
        self.pb_enemy_shield = ProgressBar(980, 130, 260, 22, boss.shield_hp, boss.shield_max, (40, 180, 240), "SHD:")
        
        self.refresh_item_buttons()
        self.fetch_new_question()

    def fetch_new_question(self):
        # Override to load harder questions in Phase 3
        super().fetch_new_question()
        
        # Reset rage countdown timer on new turn
        self.phase3_timer = self.max_timer

    def handle_answer(self, is_correct):
        player = self.game.player
        boss = self.monster
        
        self.questions_asked += 1
        
        if is_correct:
            # Player strikes boss
            self.questions_correct += 1
            self.player_offset_x = 80.0
            self.game.sounds.play_sfx("hit")
            
            atk_power = player.get_attack_power()
            damage = max(5, atk_power - boss.defense)
            
            # Apply phased damage reductions or core damage
            boss.take_damage(damage)
            
            # Draw particle indicators
            self.particles.add_hit_burst(900 + 32, 220 + 32, (255, 215, 0), count=25)
            self.particles.add_floating_text(str(damage), 900 + 10, 200, (255, 235, 100))
        else:
            # Boss counterstrikes
            self.enemy_offset_x = -80.0
            self.game.sounds.play_sfx("wrong")
            self.shake_intensity = 20.0
            self.flash_red_timer = 0.25
            
            damage = max(8, boss.attack - player.get_defense())
            # In phase 3, boss deals double counter damage!
            if boss.current_phase == 3:
                damage *= 2
                
            player.hp = max(0, player.hp - damage)
            self.particles.add_hit_burst(180 + 32, 280 + 32, (230, 50, 50), count=20)
            self.particles.add_floating_text(str(damage), 180 + 10, 240, (230, 50, 50))
            
        # Update HP display bounds
        self.pb_player_hp.set_values(player.hp, player.max_hp)
        self.pb_enemy_hp.set_values(boss.hp, boss.max_hp)
        self.pb_enemy_shield.set_values(boss.shield_hp, boss.shield_max)
        
        if boss.hp <= 0:
            self.end_boss_battle(won=True)
        elif player.hp <= 0:
            self.end_boss_battle(won=False)
        else:
            # Next turn
            self.fetch_new_question()

    def end_boss_battle(self, won):
        player = self.game.player
        boss = self.monster
        
        # Save metrics
        metrics = self.game.db.load_metrics()
        metrics["total_questions"] += self.questions_asked
        metrics["correct_questions"] += self.questions_correct
        
        if won:
            metrics["bosses_defeated"] += 1
            self.game.db.save_metrics(metrics)
            
            # Unlock next world progress on SQLite DB
            progress = self.game.db.load_progress()
            if boss.subject in progress:
                progress[boss.subject]["completed"] = True
                progress[boss.subject]["boss_defeated"] = True
                
                # Unlock next in list progression
                idx = self.progression_order.index(boss.subject)
                if idx + 1 < len(self.progression_order):
                    next_k = self.progression_order[idx + 1]
                    progress[next_k]["unlocked"] = True
                    
                self.game.db.save_progress(progress)
                
            # Deliver Boss loots rewards
            xp_loot = 250 + boss.level * 100
            coins_loot = 150 + boss.level * 50
            
            # High-tier epic gear rewards chance
            epic_loot = "gold_sword" if boss.subject in ["english", "physics"] else "dragon_shield" if boss.subject in ["chemistry", "biology"] else "obsidian_armor"
            
            self.game.states["victory"].set_rewards(xp_loot, coins_loot, epic_loot)
            self.game.change_state("victory")
        else:
            self.game.db.save_metrics(metrics)
            self.game.change_state("game_over")

    def enter(self):
        self.game.sounds.play_music("boss")

    def update(self, dt):
        super().update(dt)
        
        # Manage Phase 3 Countdown timers
        if self.monster.current_phase == 3 and not self.game.transition_to:
            self.phase3_timer = max(0.0, self.phase3_timer - dt)
            if self.phase3_timer <= 0.0:
                # Timeout is counted as wrong answer
                self.handle_answer(is_correct=False)
                
        self.pb_enemy_shield.update(dt)

    def draw(self, surface):
        # Rely on base BattleState rendering core layout
        super().draw(surface)
        
        # Draw Shield bar if active
        if self.monster.shield_hp > 0:
            self.pb_enemy_shield.draw(surface)
            
        # Draw Phase mode description text at top center
        phase_desc = self.monster.get_phase_description()
        desc_surf = self.font_boss.render(phase_desc, True, (255, 235, 100))
        surface.blit(desc_surf, ((self.game.virtual_width - desc_surf.get_width())//2, 20))
        
        # Draw Countdown Timer overlay if in Phase 3
        if self.monster.current_phase == 3:
            # Pulsing red timer circles in the top center
            tx = self.game.virtual_width // 2
            ty = 75
            
            # Blink color based on time left
            t_color = (255, 50, 50) if self.phase3_timer <= 5.0 else (240, 220, 50)
            
            pygame.draw.circle(surface, (20, 20, 25), (tx, ty), 25)
            pygame.draw.circle(surface, t_color, (tx, ty), 25, 2)
            
            timer_font = get_font(20, is_bold=True)
            timer_surf = timer_font.render(str(int(self.phase3_timer + 0.9)), True, t_color)
            surface.blit(timer_surf, (tx - timer_surf.get_width()//2, ty - timer_surf.get_height()//2 - 1))
            
            warning_font = get_font(12, is_bold=True)
            w_surf = warning_font.render("TIME LIMIT!", True, (255, 50, 50))
            surface.blit(w_surf, (tx - w_surf.get_width()//2, ty + 30))
