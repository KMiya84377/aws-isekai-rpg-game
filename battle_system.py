#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math
from game_assets import WHITE, BLACK, RED, GREEN
from enemy_data import get_enemy_by_type

# 画面サイズ定数
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class BattleSystem:
    def __init__(self, player, party, assets):
        self.player = player
        self.party = party
        self.assets = assets
        self.enemy = None
        self.state = "start"  # start, player_turn, enemy_turn, victory, defeat
        self.message = ""
        self.selected_action = None
        self.selected_skill = None
        self.selected_target = None
        self.animation_frame = 0
        self.battle_log = []
        self.party_skill_mode = False
        self.selected_party_member = None
        
    def start_battle(self, enemy_type="normal"):
        """バトルを開始する"""
        # 敵データを取得
        self.enemy = get_enemy_by_type(enemy_type)
        
        # プレイヤーの初期位置に基づいて敵の強さを調整
        # 中央付近（初期位置）では敵を弱くする
        if self.player["tile_x"] >= 20 and self.player["tile_x"] <= 30 and \
           self.player["tile_y"] >= 20 and self.player["tile_y"] <= 30:
            # 敵のステータスを弱体化（約30%減）
            self.enemy["hp"] = int(self.enemy["hp"] * 0.7)
            self.enemy["max_hp"] = int(self.enemy["max_hp"] * 0.7)
            self.enemy["attack"] = int(self.enemy["attack"] * 0.7)
            self.enemy["defense"] = int(self.enemy["defense"] * 0.7)
            
        self.state = "player_turn"
        self.message = f"A {self.enemy['name']} appeared!"
        self.add_to_log(self.message)
        self.animation_frame = 0
        self.party_skill_mode = False
        self.selected_party_member = None
        
    def add_to_log(self, message):
        """バトルログにメッセージを追加"""
        self.battle_log.append(message)
        if len(self.battle_log) > 5:
            self.battle_log.pop(0)
            
    def player_attack(self):
        """プレイヤーの通常攻撃"""
        damage = max(1, self.player["attack"] - self.enemy["defense"] // 2)
        
        # クリティカルヒット（10%の確率）
        if random.random() < 0.1:
            damage = int(damage * 1.5)
            self.message = f"Critical hit! You dealt {damage} damage to {self.enemy['name']}!"
        else:
            self.message = f"You attacked {self.enemy['name']} for {damage} damage!"
            
        self.add_to_log(self.message)
        self.enemy["hp"] = max(0, self.enemy["hp"] - damage)
        
        # 敵のダメージアニメーション
        self.state = "enemy_damage"
        self.animation_frame = 12
        
        # 敵が倒れたかチェックはupdate()メソッドで行う
            
    def enemy_attack(self):
        """敵の攻撃"""
        # 敵の攻撃力からプレイヤーの防御力を引いてダメージを計算
        damage = max(1, self.enemy["attack"] - self.player["defense"])
        
        # 回避チャンス（15%の確率）
        if random.random() < 0.15:
            self.message = f"You dodged {self.enemy['name']}'s attack!"
            self.add_to_log(self.message)
        else:
            self.message = f"{self.enemy['name']} attacked you for {damage} damage!"
            self.add_to_log(self.message)
            self.player["hp"] = max(0, self.player["hp"] - damage)
            
            # プレイヤーが倒れたかチェック
            if self.player["hp"] <= 0:
                self.defeat()
                return
                
        # プレイヤーのターンへ
        self.state = "player_turn"
        
    def service_attack(self, service, skill_name):
        """AWSサービスの特殊攻撃"""
        # スキルの効果を計算
        if skill_name == "EC2 Instance":
            damage = 15
            self.message = f"{service['name']} launched an EC2 Instance for {damage} damage!"
        elif skill_name == "S3 Bucket":
            damage = 12
            self.message = f"{service['name']} threw an S3 Bucket for {damage} damage!"
        elif skill_name == "Lambda Function":
            damage = 18
            self.message = f"{service['name']} executed a Lambda Function for {damage} damage!"
        elif skill_name == "DynamoDB Query":
            damage = 14
            self.message = f"{service['name']} performed a DynamoDB Query for {damage} damage!"
        else:
            damage = 10
            self.message = f"{service['name']} used {skill_name} for {damage} damage!"
            
        self.add_to_log(self.message)
        self.enemy["hp"] = max(0, self.enemy["hp"] - damage)
        
        # 敵のダメージアニメーション
        self.state = "enemy_damage"
        self.animation_frame = 12
        
        # パーティスキルモードを終了
        self.party_skill_mode = False
        self.selected_party_member = None
        
        # 敵が倒れたかチェックはupdate()メソッドで行う
            
    def victory(self):
        """勝利処理"""
        self.state = "victory"
        self.message = f"You defeated {self.enemy['name']}!"
        self.add_to_log(self.message)
        
        # 経験値とクレジットの獲得
        exp_gain = self.enemy["exp_reward"]
        credit_gain = self.enemy["credit_reward"]
        
        self.player["exp"] += exp_gain
        self.player["credits"] += credit_gain
        
        # レベルアップチェック
        level_up_exp = self.player["level"] * 100
        if self.player["exp"] >= level_up_exp:
            self.player["level"] += 1
            self.player["exp"] -= level_up_exp
            self.player["max_hp"] += 10
            self.player["hp"] = self.player["max_hp"]
            self.player["max_mp"] += 5
            self.player["mp"] = self.player["max_mp"]
            self.player["attack"] += 2
            self.player["defense"] += 1
            
            self.message += f"\nLevel Up! You are now level {self.player['level']}!"
            self.add_to_log(f"Level Up to {self.player['level']}!")
            
        self.message += f"\nGained {exp_gain} EXP and {credit_gain} Credits!"
        
    def defeat(self):
        """敗北処理"""
        self.state = "defeat"
        self.message = f"You were defeated by {self.enemy['name']}!"
        self.add_to_log(self.message)
        
    def escape(self):
        """逃走処理"""
        # 逃走成功率（70%）
        if random.random() < 0.7:
            self.state = "escape"
            self.message = "You successfully escaped!"
            self.add_to_log(self.message)
        else:
            self.message = "Failed to escape!"
            self.add_to_log(self.message)
            # 敵の攻撃ターンへ
            self.state = "enemy_turn"
            
    def update(self):
        """バトル状態の更新"""
        if self.state == "enemy_turn":
            self.enemy_attack()
        
        # アニメーションフレームが0になったら次の状態に進む
        if self.animation_frame <= 0 and self.state == "enemy_damage":
            if self.enemy["hp"] <= 0:
                self.victory()
            else:
                self.state = "enemy_turn"
            
    def draw(self, screen):
        """バトル画面を描画"""
        # 背景（グラデーション）
        for y in range(SCREEN_HEIGHT):
            color_value = 20 + int((y / SCREEN_HEIGHT) * 30)
            color = (color_value // 2, color_value // 2, color_value)
            pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))
            
        # 敵の描画
        enemy_img = self.assets.get_image("enemy")
        enemy_x = SCREEN_WIDTH // 2 - enemy_img.get_width() // 2
        enemy_y = 150
        
        # 敵のアニメーション（ダメージ時に点滅）
        if self.animation_frame > 0 and self.state == "enemy_damage":
            if self.animation_frame % 4 < 2:  # 点滅効果
                screen.blit(enemy_img, (enemy_x, enemy_y))
            self.animation_frame -= 1
        else:
            screen.blit(enemy_img, (enemy_x, enemy_y))
            
        # 敵の名前と情報
        enemy_name = self.assets.render_text(self.enemy["name"], "normal", WHITE)
        screen.blit(enemy_name, (SCREEN_WIDTH // 2 - enemy_name.get_width() // 2, 120))
        
        # 敵のHPバー
        hp_ratio = max(0, self.enemy["hp"] / self.enemy["max_hp"])
        hp_text = self.assets.render_text(f"HP: {self.enemy['hp']}/{self.enemy['max_hp']}", "small", WHITE)
        screen.blit(hp_text, (SCREEN_WIDTH // 2 - hp_text.get_width() // 2, 250))
        
        hp_bg = pygame.Rect(SCREEN_WIDTH // 2 - 100, 270, 200, 15)
        pygame.draw.rect(screen, (60, 30, 30), hp_bg)
        
        if hp_ratio > 0:
            hp_fill = pygame.Rect(SCREEN_WIDTH // 2 - 100, 270, int(200 * hp_ratio), 15)
            hp_color = (200, 50, 50)  # 赤色のHPバー
            pygame.draw.rect(screen, hp_color, hp_fill)
            
        pygame.draw.rect(screen, WHITE, hp_bg, 1)
        
        # プレイヤー情報
        player_name = self.assets.render_text(self.player["name"], "normal", WHITE)
        screen.blit(player_name, (60, 350))
        
        # プレイヤーのHPとMPバー
        hp_ratio = max(0, self.player["hp"] / self.player["max_hp"])
        mp_ratio = max(0, self.player["mp"] / self.player["max_mp"])
        
        # HPテキスト
        hp_text = self.assets.render_text(f"HP: {self.player['hp']}/{self.player['max_hp']}", "small", WHITE)
        screen.blit(hp_text, (60, 380))
        
        # HPバーの背景
        hp_bg = pygame.Rect(60, 400, 200, 15)
        pygame.draw.rect(screen, (60, 30, 30), hp_bg)
        
        # HPバーの中身
        if hp_ratio > 0:
            hp_fill = pygame.Rect(60, 400, int(200 * hp_ratio), 15)
            
            # HPの残量に応じて色を変える
            if hp_ratio > 0.6:
                hp_color = (50, 200, 50)  # 緑
            elif hp_ratio > 0.3:
                hp_color = (200, 200, 50)  # 黄色
            else:
                hp_color = (200, 50, 50)  # 赤
                
            pygame.draw.rect(screen, hp_color, hp_fill)
            
        # HPバーの枠
        pygame.draw.rect(screen, WHITE, hp_bg, 1)
        
        # MPテキスト
        mp_text = self.assets.render_text(f"MP: {self.player['mp']}/{self.player['max_mp']}", "small", WHITE)
        screen.blit(mp_text, (60, 420))
        
        # MPバーの背景
        mp_bg = pygame.Rect(60, 440, 200, 15)
        pygame.draw.rect(screen, (30, 30, 60), mp_bg)
        
        # MPバーの中身
        if mp_ratio > 0:
            mp_fill = pygame.Rect(60, 440, int(200 * mp_ratio), 15)
            pygame.draw.rect(screen, (50, 50, 200), mp_fill)
            
        # MPバーの枠
        pygame.draw.rect(screen, WHITE, mp_bg, 1)
        
        # パーティメンバーの情報
        for i, member in enumerate(self.party):
            if i >= 3:  # 最大3人まで表示
                break
                
            member_name = self.assets.render_text(member["name"], "small", WHITE)
            screen.blit(member_name, (300 + i * 60, 400))
            
            hp_ratio = max(0, member["hp"] / member["max_hp"])
            hp_bg = pygame.Rect(300 + i * 60, 430, 50, 10)
                
            # HPバーの背景
            pygame.draw.rect(screen, (30, 30, 60), hp_bg)
                
            # HPバーの中身
            if hp_ratio > 0:
                hp_fill = pygame.Rect(300 + i * 60, 430, int(50 * hp_ratio), 10)
                pygame.draw.rect(screen, (50, 50, 200), hp_fill)
                    
            # HPバーの枠
            pygame.draw.rect(screen, WHITE, hp_bg, 1)
        
        # メッセージボックス（装飾付き）
        message_box = pygame.Rect(50, 50, 700, 80)
        # グラデーション背景
        for y in range(80):
            color_val = 50 + int(y / 2)
            color = (color_val // 2, color_val // 2, color_val)
            pygame.draw.line(screen, color, (50, 50 + y), (750, 50 + y))
            
        pygame.draw.rect(screen, WHITE, message_box, 2)
        
        # 装飾
        pygame.draw.line(screen, (100, 100, 200), (60, 60), (740, 60), 1)
        pygame.draw.line(screen, (100, 100, 200), (60, 120), (740, 120), 1)
        
        # メッセージ
        message_text = self.assets.render_text(self.message, "normal", WHITE)
        screen.blit(message_text, (60, 70))
        
        # コマンド
        if self.state == "player_turn":
            # パーティスキルモードの場合
            if self.party_skill_mode and self.selected_party_member is not None:
                # 戻るボタン
                back_button = pygame.Rect(500, 550, 100, 30)
                pygame.draw.rect(screen, (80, 80, 100), back_button)
                pygame.draw.rect(screen, WHITE, back_button, 1)
                back_text = self.assets.render_text("Back", "small", WHITE)
                screen.blit(back_text, (back_button.centerx - back_text.get_width() // 2, 
                                      back_button.centery - back_text.get_height() // 2))
                
                # スキル一覧
                party_member = self.party[self.selected_party_member]
                skill_title = self.assets.render_text(f"{party_member['name']}'s Skills", "normal", WHITE)
                screen.blit(skill_title, (60, 480))
                
                for i, skill in enumerate(party_member["skills"]):
                    skill_button = pygame.Rect(100, 510 + i * 40, 300, 30)
                    pygame.draw.rect(screen, (60, 60, 100), skill_button)
                    pygame.draw.rect(screen, WHITE, skill_button, 1)
                    skill_text = self.assets.render_text(skill["name"], "small", WHITE)
                    screen.blit(skill_text, (skill_button.centerx - skill_text.get_width() // 2, 
                                           skill_button.centery - skill_text.get_height() // 2))
            else:
                # 通常のコマンド
                # 攻撃ボタン
                attack_button = pygame.Rect(60, 510, 100, 30)
                pygame.draw.rect(screen, (100, 60, 60), attack_button)
                pygame.draw.rect(screen, WHITE, attack_button, 1)
                attack_text = self.assets.render_text("Attack", "small", WHITE)
                screen.blit(attack_text, (attack_button.centerx - attack_text.get_width() // 2, 
                                        attack_button.centery - attack_text.get_height() // 2))
                
                # スキルボタン
                skill_button = pygame.Rect(170, 510, 100, 30)
                pygame.draw.rect(screen, (60, 60, 100), skill_button)
                pygame.draw.rect(screen, WHITE, skill_button, 1)
                skill_text = self.assets.render_text("Skills", "small", WHITE)
                screen.blit(skill_text, (skill_button.centerx - skill_text.get_width() // 2, 
                                       skill_button.centery - skill_text.get_height() // 2))
                
                # アイテムボタン
                item_button = pygame.Rect(280, 510, 100, 30)
                pygame.draw.rect(screen, (60, 100, 60), item_button)
                pygame.draw.rect(screen, WHITE, item_button, 1)
                item_text = self.assets.render_text("Items", "small", WHITE)
                screen.blit(item_text, (item_button.centerx - item_text.get_width() // 2, 
                                      item_button.centery - item_text.get_height() // 2))
                
                # パーティスキルボタン
                if len(self.party) > 0:
                    party_button = pygame.Rect(390, 510, 100, 30)
                    pygame.draw.rect(screen, (100, 60, 100), party_button)
                    pygame.draw.rect(screen, WHITE, party_button, 1)
                    party_text = self.assets.render_text("Party", "small", WHITE)
                    screen.blit(party_text, (party_button.centerx - party_text.get_width() // 2, 
                                           party_button.centery - party_text.get_height() // 2))
                
                # 逃走ボタン
                escape_button = pygame.Rect(500, 510, 100, 30)
                pygame.draw.rect(screen, (100, 100, 100), escape_button)
                pygame.draw.rect(screen, WHITE, escape_button, 1)
                escape_text = self.assets.render_text("Escape", "small", WHITE)
                screen.blit(escape_text, (escape_button.centerx - escape_text.get_width() // 2, 
                                        escape_button.centery - escape_text.get_height() // 2))
                
                # パーティメンバー選択（パーティスキルモード時）
                if self.party_skill_mode:
                    for i, member in enumerate(self.party):
                        member_button = pygame.Rect(100 + i * 150, 550, 140, 30)
                        pygame.draw.rect(screen, (80, 60, 100), member_button)
                        pygame.draw.rect(screen, WHITE, member_button, 1)
                        member_text = self.assets.render_text(member["name"], "small", WHITE)
                        screen.blit(member_text, (member_button.centerx - member_text.get_width() // 2, 
                                               member_button.centery - member_text.get_height() // 2))
        
        # 戦闘終了時の続行ボタン
        elif self.state in ["victory", "defeat", "escape"]:
            continue_button = pygame.Rect(300, 500, 200, 50)
            pygame.draw.rect(screen, (60, 60, 100), continue_button)
            pygame.draw.rect(screen, WHITE, continue_button, 1)
            continue_text = self.assets.render_text("Continue", "normal", WHITE)
            screen.blit(continue_text, (continue_button.centerx - continue_text.get_width() // 2, 
                                      continue_button.centery - continue_text.get_height() // 2))
            
    def handle_event(self, event):
        """イベント処理"""
        if event.type != pygame.MOUSEBUTTONDOWN:
            return False
            
        # アニメーション中は入力を受け付けない
        if self.animation_frame > 0:
            return False
            
        # 戦闘終了状態の場合
        if self.state in ["victory", "defeat", "escape"]:
            # 続行ボタンがクリックされた場合のみ終了
            if pygame.Rect(300, 500, 200, 50).collidepoint(event.pos):
                return True
            return False
            
        # 戦闘中の場合
        if self.state == "player_turn":
            # パーティスキルモードの場合
            if self.party_skill_mode and self.selected_party_member is not None:
                # 戻るボタン
                if pygame.Rect(500, 550, 100, 30).collidepoint(event.pos):
                    self.party_skill_mode = False
                    self.selected_party_member = None
                    return False
                    
                # スキル選択
                party_member = self.party[self.selected_party_member]
                for i, skill in enumerate(party_member["skills"]):
                    if pygame.Rect(100, 510 + i * 40, 300, 30).collidepoint(event.pos):
                        self.service_attack(party_member, skill["name"])
                        return False
                        
                return False
                
            # 通常のコマンド選択
            # 攻撃ボタン
            if pygame.Rect(60, 510, 100, 30).collidepoint(event.pos):
                self.player_attack()
                return False
                
            # スキルボタン
            if pygame.Rect(170, 510, 100, 30).collidepoint(event.pos):
                self.message = "Skills are not implemented yet."
                self.add_to_log(self.message)
                return False
                
            # アイテムボタン
            if pygame.Rect(280, 510, 100, 30).collidepoint(event.pos):
                self.message = "Items are not implemented yet."
                self.add_to_log(self.message)
                return False
                
            # パーティスキルボタン
            if len(self.party) > 0 and pygame.Rect(390, 510, 100, 30).collidepoint(event.pos):
                self.party_skill_mode = True
                return False
                
            # パーティメンバー選択（パーティスキルモード時）
            if self.party_skill_mode:
                for i, member in enumerate(self.party):
                    if pygame.Rect(100 + i * 150, 550, 140, 30).collidepoint(event.pos):
                        self.selected_party_member = i
                        return False
                        
            # 逃走ボタン
            if pygame.Rect(500, 510, 100, 30).collidepoint(event.pos):
                self.escape()
                return False
                
        return False
