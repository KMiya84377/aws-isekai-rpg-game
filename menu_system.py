#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import json
import os
from game_assets import WHITE, BLACK, BLUE, GRAY

class MenuSystem:
    def __init__(self, player, party, assets):
        self.player = player
        self.party = party
        self.assets = assets
        self.active = False
        self.current_tab = "status"  # status, party, items, save, settings
        self.selected_party_member = None
        self.message = ""
        
    def toggle(self):
        """メニューの表示/非表示を切り替え"""
        self.active = not self.active
        self.current_tab = "status"
        self.selected_party_member = None
        self.message = ""
        
    def draw(self, screen):
        """メニュー画面を描画"""
        if not self.active:
            return
            
        # 半透明の背景
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        # メニューパネル
        menu_panel = pygame.Rect(50, 50, 700, 500)
        pygame.draw.rect(screen, (50, 50, 80), menu_panel)
        pygame.draw.rect(screen, WHITE, menu_panel, 2)
        
        # タブ
        self.draw_tabs(screen)
        
        # 現在のタブの内容を描画
        if self.current_tab == "status":
            self.draw_status_tab(screen)
        elif self.current_tab == "party":
            self.draw_party_tab(screen)
        elif self.current_tab == "items":
            self.draw_items_tab(screen)
        elif self.current_tab == "save":
            self.draw_save_tab(screen)
        elif self.current_tab == "settings":
            self.draw_settings_tab(screen)
            
        # メッセージ
        if self.message:
            message_text = self.assets.render_text(self.message, "normal", WHITE)
            screen.blit(message_text, (400 - message_text.get_width() // 2, 520))
            
    def draw_tabs(self, screen):
        """タブを描画"""
        tabs = ["status", "party", "items", "save", "settings"]
        tab_width = 140
        tab_height = 40
        start_x = 50
        
        for i, tab in enumerate(tabs):
            tab_rect = pygame.Rect(start_x + i * tab_width, 50, tab_width, tab_height)
            
            # 選択中のタブは色を変える
            if self.current_tab == tab:
                pygame.draw.rect(screen, (80, 80, 120), tab_rect)
            else:
                pygame.draw.rect(screen, (50, 50, 80), tab_rect)
                
            pygame.draw.rect(screen, WHITE, tab_rect, 1)
            
            # タブ名
            tab_text = self.assets.render_text(tab.capitalize(), "normal", WHITE)
            screen.blit(tab_text, (start_x + i * tab_width + tab_width // 2 - tab_text.get_width() // 2, 60))
            
    def draw_status_tab(self, screen):
        """ステータスタブを描画"""
        # プレイヤー情報
        player_name = self.assets.render_text(f"Name: {self.player['name']}", "normal", WHITE)
        screen.blit(player_name, (100, 120))
        
        player_level = self.assets.render_text(f"Level: {self.player['level']}", "normal", WHITE)
        screen.blit(player_level, (100, 160))
        
        player_hp = self.assets.render_text(f"HP: {self.player['hp']}/{self.player['max_hp']}", "normal", WHITE)
        screen.blit(player_hp, (100, 200))
        
        player_mp = self.assets.render_text(f"MP: {self.player['mp']}/{self.player['max_mp']}", "normal", WHITE)
        screen.blit(player_mp, (100, 240))
        
        player_attack = self.assets.render_text(f"Attack: {self.player['attack']}", "normal", WHITE)
        screen.blit(player_attack, (100, 280))
        
        player_defense = self.assets.render_text(f"Defense: {self.player['defense']}", "normal", WHITE)
        screen.blit(player_defense, (100, 320))
        
        player_exp = self.assets.render_text(f"EXP: {self.player['exp']}/{self.player['level'] * 100}", "normal", WHITE)
        screen.blit(player_exp, (100, 360))
        
        player_credits = self.assets.render_text(f"AWS Credits: {self.player['credits']}", "normal", WHITE)
        screen.blit(player_credits, (100, 400))
        
        # 経験値バー
        exp_needed = self.player["level"] * 100
        exp_ratio = min(1.0, self.player["exp"] / exp_needed)
        
        pygame.draw.rect(screen, (100, 100, 100), (100, 440, 300, 20))
        pygame.draw.rect(screen, (0, 200, 0), (100, 440, int(300 * exp_ratio), 20))
        
        exp_text = self.assets.render_text(f"EXP: {self.player['exp']}/{exp_needed}", "small", WHITE)
        screen.blit(exp_text, (250 - exp_text.get_width() // 2, 442))
        
        # プレイヤーアイコン
        player_image = self.assets.get_image("player")
        screen.blit(pygame.transform.scale(player_image, (100, 100)), (500, 150))
        
        # 戻るボタン
        back_button = pygame.Rect(600, 500, 100, 30)
        pygame.draw.rect(screen, (100, 100, 200), back_button)
        pygame.draw.rect(screen, WHITE, back_button, 1)
        
        back_text = self.assets.render_text("Back", "small", WHITE)
        screen.blit(back_text, (650 - back_text.get_width() // 2, 510))
        
    def draw_party_tab(self, screen):
        """パーティタブを描画"""
        if not self.party:
            no_party_text = self.assets.render_text("No party members yet.", "normal", WHITE)
            screen.blit(no_party_text, (350, 250))
            return
            
        # パーティメンバーのリスト
        for i, member in enumerate(self.party):
            member_rect = pygame.Rect(100, 120 + i * 60, 600, 50)
            
            # 選択中のメンバーは色を変える
            if self.selected_party_member == i:
                pygame.draw.rect(screen, (80, 80, 120), member_rect)
            else:
                pygame.draw.rect(screen, (50, 50, 80), member_rect)
                
            pygame.draw.rect(screen, WHITE, member_rect, 1)
            
            # メンバー情報
            member_image = self.assets.get_image(member["name"].lower())
            screen.blit(member_image, (110, 125 + i * 60))
            
            member_name = self.assets.render_text(member["name"], "normal", WHITE)
            screen.blit(member_name, (160, 125 + i * 60))
            
            member_level = self.assets.render_text(f"Lv.{member['level']}", "normal", WHITE)
            screen.blit(member_level, (300, 125 + i * 60))
            
            # HPバー
            hp_ratio = max(0, member["hp"] / member["max_hp"])
            pygame.draw.rect(screen, (100, 100, 100), (350, 130 + i * 60, 100, 15))
            pygame.draw.rect(screen, (255, 0, 0), (350, 130 + i * 60, int(100 * hp_ratio), 15))
            
            hp_text = self.assets.render_text(f"HP: {member['hp']}/{member['max_hp']}", "small", WHITE)
            screen.blit(hp_text, (460, 130 + i * 60))
            
            # MPバー
            mp_ratio = max(0, member["mp"] / member["max_mp"])
            pygame.draw.rect(screen, (100, 100, 100), (350, 150 + i * 60, 100, 15))
            pygame.draw.rect(screen, (0, 0, 255), (350, 150 + i * 60, int(100 * mp_ratio), 15))
            
            mp_text = self.assets.render_text(f"MP: {member['mp']}/{member['max_mp']}", "small", WHITE)
            screen.blit(mp_text, (460, 150 + i * 60))
            
        # 選択中のメンバーの詳細情報
        if self.selected_party_member is not None:
            member = self.party[self.selected_party_member]
            
            detail_rect = pygame.Rect(100, 350, 600, 150)
            pygame.draw.rect(screen, (60, 60, 90), detail_rect)
            pygame.draw.rect(screen, WHITE, detail_rect, 1)
            
            # スキル情報
            skills_text = self.assets.render_text("Skills:", "normal", WHITE)
            screen.blit(skills_text, (120, 370))
            
            for i, skill in enumerate(member["skills"]):
                skill_text = self.assets.render_text(f"{skill['name']} - Power: {skill['power']}, Cost: {skill['cost']}", "small", WHITE)
                screen.blit(skill_text, (150, 400 + i * 25))
                
    def draw_items_tab(self, screen):
        """アイテムタブを描画"""
        # 未実装メッセージ
        not_implemented_text = self.assets.render_text("Items feature not implemented yet.", "normal", WHITE)
        screen.blit(not_implemented_text, (250, 250))
        
    def draw_save_tab(self, screen):
        """セーブタブを描画"""
        save_text = self.assets.render_text("Save your game progress", "normal", WHITE)
        screen.blit(save_text, (300, 150))
        
        # セーブボタン
        save_button_rect = pygame.Rect(300, 200, 200, 50)
        pygame.draw.rect(screen, (80, 80, 120), save_button_rect)
        pygame.draw.rect(screen, WHITE, save_button_rect, 1)
        
        save_button_text = self.assets.render_text("Save Game", "normal", WHITE)
        screen.blit(save_button_text, (350, 215))
        
        # セーブデータの情報
        if os.path.exists("save_data.json"):
            try:
                with open("save_data.json", "r") as f:
                    save_data = json.load(f)
                    
                save_info_text = self.assets.render_text(f"Last save: Level {save_data['player']['level']} {save_data['player']['name']}", "normal", WHITE)
                screen.blit(save_info_text, (250, 300))
                
                save_location_text = self.assets.render_text(f"Location: {save_data['current_map']}", "normal", WHITE)
                screen.blit(save_location_text, (250, 340))
                
                save_credits_text = self.assets.render_text(f"AWS Credits: {save_data['player']['credits']}", "normal", WHITE)
                screen.blit(save_credits_text, (250, 380))
            except:
                save_error_text = self.assets.render_text("Error reading save data.", "normal", WHITE)
                screen.blit(save_error_text, (300, 300))
        else:
            no_save_text = self.assets.render_text("No save data found.", "normal", WHITE)
            screen.blit(no_save_text, (300, 300))
            
    def draw_settings_tab(self, screen):
        """設定タブを描画"""
        # タイトル
        settings_title = self.assets.render_text("Settings", "large", WHITE)
        screen.blit(settings_title, (400 - settings_title.get_width() // 2, 120))
        
        # 音量設定
        volume_title = self.assets.render_text("Volume", "normal", WHITE)
        screen.blit(volume_title, (100, 180))
        
        # BGM音量
        bgm_text = self.assets.render_text("BGM:", "normal", WHITE)
        screen.blit(bgm_text, (120, 220))
        
        # BGM音量バー
        pygame.draw.rect(screen, (100, 100, 100), (200, 225, 200, 15))
        pygame.draw.rect(screen, (0, 200, 200), (200, 225, int(200 * 0.7), 15))  # 仮の値
        
        # 効果音音量
        sfx_text = self.assets.render_text("SFX:", "normal", WHITE)
        screen.blit(sfx_text, (120, 260))
        
        # 効果音音量バー
        pygame.draw.rect(screen, (100, 100, 100), (200, 265, 200, 15))
        pygame.draw.rect(screen, (0, 200, 200), (200, 265, int(200 * 0.8), 15))  # 仮の値
        
        # 操作説明
        controls_title = self.assets.render_text("Controls", "normal", WHITE)
        screen.blit(controls_title, (100, 300))
        
        controls_text = [
            "Arrow keys: Move",
            "M: Menu",
            "ESC: Return to title",
            "Enter/Click: Interact"
        ]
        
        for i, text in enumerate(controls_text):
            control_text = self.assets.render_text(text, "normal", WHITE)
            screen.blit(control_text, (120, 340 + i * 30))
            
        # タイトルに戻るボタン
        title_button = pygame.Rect(300, 480, 200, 50)
        pygame.draw.rect(screen, (200, 100, 100), title_button)
        pygame.draw.rect(screen, WHITE, title_button, 2)
        
        title_text = self.assets.render_text("Return to Title", "normal", WHITE)
        screen.blit(title_text, (400 - title_text.get_width() // 2, 495))
        
        # 戻るボタン
        back_button = pygame.Rect(600, 500, 100, 30)
        pygame.draw.rect(screen, (100, 100, 200), back_button)
        pygame.draw.rect(screen, WHITE, back_button, 1)
        
        back_text = self.assets.render_text("Back", "small", WHITE)
        screen.blit(back_text, (650 - back_text.get_width() // 2, 510))
        
    def handle_event(self, event):
        """イベント処理"""
        if not self.active:
            return False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.toggle()
                return True
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            # タブの切り替え
            tabs = ["status", "party", "items", "save", "settings"]
            tab_width = 140
            tab_height = 40
            start_x = 50
            
            for i, tab in enumerate(tabs):
                tab_rect = pygame.Rect(start_x + i * tab_width, 50, tab_width, tab_height)
                if tab_rect.collidepoint(event.pos):
                    self.current_tab = tab
                    self.selected_party_member = None
                    self.message = ""
                    return False  # タブ切り替え時にメニューを閉じないように変更
                    
            # 各タブ固有の処理
            if self.current_tab == "party":
                # パーティメンバーの選択
                for i, _ in enumerate(self.party):
                    member_rect = pygame.Rect(100, 120 + i * 60, 600, 50)
                    if member_rect.collidepoint(event.pos):
                        self.selected_party_member = i
                        return False
                        
            elif self.current_tab == "save":
                # セーブボタン
                save_button_rect = pygame.Rect(300, 200, 200, 50)
                if save_button_rect.collidepoint(event.pos):
                    self.save_game()
                    return False
                    
            elif self.current_tab == "settings":
                # タイトルに戻るボタン
                title_button = pygame.Rect(300, 480, 200, 50)
                if title_button.collidepoint(event.pos):
                    self.toggle()
                    return "title"  # タイトル画面に戻る信号
                    
            # 戻るボタン（すべてのタブ共通）
            back_button = pygame.Rect(600, 500, 100, 30)
            if back_button.collidepoint(event.pos):
                self.toggle()
                return True
                
        return False
        
    def save_game(self):
        """ゲームをセーブ"""
        try:
            # プレイヤーデータ
            game_data = {
                "player": self.player,
                "party": self.party,
                "current_map": "AWS Cloud World",  # 現在のマップ名
                "position": self.player["position"]  # プレイヤーの位置
            }
            
            with open("save_data.json", "w") as f:
                json.dump(game_data, f)
                
            self.message = "Game saved successfully!"
        except Exception as e:
            self.message = f"Error saving game: {str(e)}"
