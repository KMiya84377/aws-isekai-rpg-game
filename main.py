#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import sys
import random
import json
import os
import math
from game_assets import GameAssets, WHITE, BLACK, BLUE, GRAY
from game_map import MapManager
from battle_system import BattleSystem
from menu_system import MenuSystem
from cutscene_system import CutsceneSystem
from quest_system import QuestSystem
from recruitment_system import RecruitmentSystem
from item_system import ItemSystem
from shop_system import ShopSystem
from aws_services import get_service_by_name, get_all_services

# ゲームの定数
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "AWS Cloud Isekai RPG"

# ゲームの状態
STATE_TITLE = 0
STATE_GAME = 1
STATE_BATTLE = 2
STATE_DIALOG = 3
STATE_MENU = 4
STATE_CUTSCENE = 5
STATE_QUEST_LOG = 6
STATE_RECRUITMENT = 7
STATE_SHOP = 8
STATE_INVENTORY = 9
STATE_GAME_OVER = 10

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.state = STATE_TITLE
        self.running = True
        
        # アセットのロード
        self.assets = GameAssets()
        
        # プレイヤーデータ
        self.player = {
            "name": "Rookie Engineer",
            "level": 1,
            "exp": 0,
            "hp": 100,
            "max_hp": 100,
            "mp": 50,
            "max_mp": 50,
            "attack": 10,
            "defense": 5,
            "credits": 1000,
            "position": [25, 25],  # 中央の十字路に変更
            "tile_x": 25,          # 中央の十字路に変更
            "tile_y": 25,          # 中央の十字路に変更
            "completed_quests": [],
            "defeated_bosses": [],
            "recruited_services": []
        }
        
        # パーティメンバー
        self.party = []
        
        # マップ管理
        self.map_manager = MapManager()
        
        # バトルシステム
        self.battle_system = BattleSystem(self.player, self.party, self.assets)
        
        # メニューシステム
        self.menu_system = MenuSystem(self.player, self.party, self.assets)
        
        # カットシーンシステム
        self.cutscene_system = CutsceneSystem(self.assets)
        
        # クエストシステム
        self.quest_system = QuestSystem(self.player, self.assets)
        
        # 仲間システム
        self.recruitment_system = RecruitmentSystem(self.player, self.party, self.assets)
        
        # アイテムシステム
        self.item_system = ItemSystem(self.player, self.assets)
        
        # ショップシステム
        self.shop_system = ShopSystem(self.player, self.assets)
        
        # ダイアログ
        self.dialog = None
        self.dialog_npc = None
        self.dialog_npc_is_service = False
        
        # カメラ位置
        self.camera_x = 0
        self.camera_y = 0
        
        # 歩数カウンター（ランダムエンカウント用）
        self.steps = 0
        
        # タイトル画面のボタン（位置を下部に変更）
        self.title_buttons = {
            "new_game": pygame.Rect(300, 400, 200, 50),
            "continue": pygame.Rect(300, 460, 200, 50),
            "exit": pygame.Rect(300, 520, 200, 50)
        }
        
        # 初期クエストの設定
        self.quest_system.add_quest("meet_ec2")
        self.quest_system.add_quest("explore_computing_town")
        self.dialog_npc = None
        self.dialog_npc_is_service = False
        
        # カメラ位置
        self.camera_x = 0
        self.camera_y = 0
        
        # 歩数カウンター（ランダムエンカウント用）
        self.steps = 0
        
        # タイトル画面のボタン
        self.title_buttons = {
            "new_game": pygame.Rect(300, 250, 200, 50),
            "continue": pygame.Rect(300, 320, 200, 50),
            "exit": pygame.Rect(300, 390, 200, 50)
        }
        
        # 初期クエストの設定
        self.quest_system.add_quest("meet_ec2")
        self.quest_system.add_quest("explore_computing_town")
    def run(self):
        """ゲームのメインループ"""
        try:
            while self.running:
                # イベント処理
                self.handle_events()
                
                # 状態に応じた更新
                if self.state == STATE_BATTLE:
                    self.battle_system.update()
                elif self.state == STATE_CUTSCENE:
                    self.cutscene_system.update()
                
                # 画面クリア
                self.screen.fill(BLACK)
                
                # 状態に応じた描画
                if self.state == STATE_TITLE:
                    self.draw_title_screen()
                elif self.state == STATE_GAME:
                    self.draw_game_screen()
                elif self.state == STATE_BATTLE:
                    self.battle_system.draw(self.screen)
                elif self.state == STATE_DIALOG:
                    self.draw_game_screen()
                    self.draw_dialog()
                elif self.state == STATE_MENU:
                    self.draw_game_screen()
                    self.menu_system.draw(self.screen)
                elif self.state == STATE_CUTSCENE:
                    self.cutscene_system.draw(self.screen)
                elif self.state == STATE_QUEST_LOG:
                    self.draw_game_screen()
                    self.quest_log_close_button = self.quest_system.draw_quest_log(self.screen)
                elif self.state == STATE_SHOP:
                    self.draw_game_screen()
                    self.draw_dialog()
                    self.shop_system.draw(self.screen)
                elif self.state == STATE_INVENTORY:
                    self.draw_game_screen()
                    self.item_system.draw(self.screen)
                elif self.state == STATE_RECRUITMENT:
                    self.recruitment_system.draw(self.screen)
                elif self.state == STATE_GAME_OVER:
                    # ゲームオーバー画面を描画し、ボタンを返す
                    _ = self.draw_game_over_screen()
                
                # 画面の更新
                pygame.display.flip()
                self.clock.tick(FPS)
        except Exception as e:
            print(f"ゲームループでエラーが発生しました: {e}")
            
        pygame.quit()
        sys.exit()
    def draw_game_over_screen(self):
        """ゲームオーバー画面を描画"""
        # 背景（暗い赤色のグラデーション）
        for y in range(SCREEN_HEIGHT):
            color_value = 50 - int((y / SCREEN_HEIGHT) * 30)
            color = (color_value + 50, color_value, color_value)
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))
            
        # タイトル
        game_over_text = self.assets.render_text("GAME OVER", "large", (255, 50, 50))
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 150))
        
        # メッセージ
        message_text = self.assets.render_text("You have been defeated...", "normal", WHITE)
        self.screen.blit(message_text, (SCREEN_WIDTH // 2 - message_text.get_width() // 2, 250))
        
        # 続行ボタン
        continue_button = pygame.Rect(300, 350, 200, 50)
        # グラデーションボタン
        for y_offset in range(50):
            color_val = 50 + int(y_offset / 50 * 100)
            color = (color_val, color_val // 3, color_val // 3)
            pygame.draw.line(self.screen, color, 
                           (continue_button.left, continue_button.top + y_offset),
                           (continue_button.right, continue_button.top + y_offset))
        pygame.draw.rect(self.screen, WHITE, continue_button, 2)
        
        continue_text = self.assets.render_text("Continue from Save", "normal", WHITE)
        self.screen.blit(continue_text, (400 - continue_text.get_width() // 2, 365))
        
        # タイトルに戻るボタン
        title_button = pygame.Rect(300, 420, 200, 50)
        # グラデーションボタン
        for y_offset in range(50):
            color_val = 50 + int(y_offset / 50 * 100)
            color = (color_val // 2, color_val // 2, color_val)
            pygame.draw.line(self.screen, color, 
                           (title_button.left, title_button.top + y_offset),
                           (title_button.right, title_button.top + y_offset))
        pygame.draw.rect(self.screen, WHITE, title_button, 2)
        
        title_text = self.assets.render_text("Return to Title", "normal", WHITE)
        self.screen.blit(title_text, (400 - title_text.get_width() // 2, 435))
        
        return continue_button, title_button
        
        continue_text = self.assets.render_text("Continue from Save", "normal", WHITE)
        self.screen.blit(continue_text, (400 - continue_text.get_width() // 2, 365))
        
        # タイトルに戻るボタン
        title_button = pygame.Rect(300, 420, 200, 50)
        # グラデーションボタン
        for y_offset in range(50):
            color_val = 50 + int(y_offset / 50 * 100)
            color = (color_val // 2, color_val // 2, color_val)
            pygame.draw.line(self.screen, color, 
                           (title_button.left, title_button.top + y_offset),
                           (title_button.right, title_button.top + y_offset))
        pygame.draw.rect(self.screen, WHITE, title_button, 2)
        
        title_text = self.assets.render_text("Return to Title", "normal", WHITE)
        self.screen.blit(title_text, (400 - title_text.get_width() // 2, 435))
        
        return continue_button, title_button
    def handle_events(self):
        """イベント処理"""
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return
                    
                # キー入力
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.state == STATE_TITLE:
                            self.running = False
                        elif self.state == STATE_GAME:
                            self.state = STATE_MENU
                            self.menu_system.active = True  # 直接activeをTrueに設定
                        elif self.state == STATE_MENU:
                            self.state = STATE_GAME
                            self.menu_system.active = False  # 直接activeをFalseに設定
                        elif self.state == STATE_QUEST_LOG:
                            self.state = STATE_GAME
                        elif self.state == STATE_INVENTORY:
                            self.state = STATE_GAME
                            self.item_system.active = False
                        # バトル中はESCキーを無効化
                        elif self.state == STATE_BATTLE:
                            pass  # 何もしない
                        else:
                            # その他の状態ではゲーム画面に戻る
                            self.state = STATE_GAME
                            
                    # クエストログを表示
                    if event.key == pygame.K_q and self.state == STATE_GAME:
                        self.state = STATE_QUEST_LOG
                            
                    # ゲーム画面での操作
                    if self.state == STATE_GAME:
                        moved = False
                        
                        if event.key == pygame.K_UP:
                            moved = self.move_player(0, -1)
                        elif event.key == pygame.K_DOWN:
                            moved = self.move_player(0, 1)
                        elif event.key == pygame.K_LEFT:
                            moved = self.move_player(-1, 0)
                        elif event.key == pygame.K_RIGHT:
                            moved = self.move_player(1, 0)
                        elif event.key == pygame.K_m:
                            self.state = STATE_MENU
                            self.menu_system.active = True  # 直接activeをTrueに設定
                        elif event.key == pygame.K_i:
                            self.state = STATE_INVENTORY
                            self.item_system.active = True
                        
                        # 移動したらランダムエンカウントチェック
                        if moved:
                            self.steps += 1
                            if self.map_manager.current_map.check_random_encounter():
                                self.start_battle()
                                
                # マウス入力
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # タイトル画面
                    if self.state == STATE_TITLE:
                        if self.title_buttons["new_game"].collidepoint(event.pos):
                            self.start_new_game()
                        elif self.title_buttons["continue"].collidepoint(event.pos):
                            self.load_game()
                        elif self.title_buttons["exit"].collidepoint(event.pos):
                            self.running = False
                    
                    # バトル画面
                    elif self.state == STATE_BATTLE:
                        try:
                            # バトルシステムにイベントを渡し、戻り値がTrueの場合のみ状態を変更
                            if self.battle_system.handle_event(event):
                                # 戦闘終了後の処理
                                if self.battle_system.state == "victory":
                                    # ボスを倒した場合
                                    if self.battle_system.enemy["name"] == "DDoS Attack":
                                        # エンディングカットシーンを開始
                                        self.state = STATE_CUTSCENE
                                        self.cutscene_system.start_ending()
                                    else:
                                        self.state = STATE_GAME
                                elif self.battle_system.state == "defeat":
                                    # 敗北時はゲームオーバー画面へ
                                    self.state = STATE_GAME_OVER
                                elif self.battle_system.state == "escape":
                                    self.state = STATE_GAME
                                # それ以外の場合は状態を変更しない（バトル継続）
                        except Exception as e:
                            print(f"バトル処理中のエラー: {e}")
                            # エラー時のみゲーム画面に戻る
                            self.state = STATE_GAME
                    
                    # ダイアログ画面
                    elif self.state == STATE_DIALOG:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            # EC2との会話の場合、クエスト完了処理
                            if self.dialog_npc and self.dialog_npc["name"] == "EC2" and "meet_ec2" in self.quest_system.active_quests:
                                self.quest_system.complete_quest("meet_ec2")
                                # 新しいクエストを追加
                                self.quest_system.add_quest("ec2_quest")
                            
                            self.state = STATE_GAME
                            self.dialog = None
                            self.dialog_npc = None
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and self.dialog_npc_is_service:
                            # 仲間システムを起動
                            if self.dialog_npc and "name" in self.dialog_npc:
                                self.state = STATE_RECRUITMENT
                                self.recruitment_system.start_recruitment(self.dialog_npc["name"])
                            self.dialog = None
                            self.dialog_npc = None
                    
                    # メニュー画面
                    elif self.state == STATE_MENU:
                        try:
                            result = self.menu_system.handle_event(event)
                            if result == "title":
                                self.state = STATE_TITLE
                            elif result:
                                self.state = STATE_GAME
                        except Exception as e:
                            print(f"メニュー処理中のエラー: {e}")
                            self.state = STATE_GAME
                    
                    # カットシーン画面
                    elif self.state == STATE_CUTSCENE:
                        try:
                            if not self.cutscene_system.active or not self.cutscene_system.handle_event(event):
                                # カットシーンが終了した場合
                                self.next_scene()
                        except Exception as e:
                            print(f"カットシーン処理中のエラー: {e}")
                            # エラー時はゲーム画面に戻る
                            self.state = STATE_GAME
                    
                    # クエストログ画面
                    elif self.state == STATE_QUEST_LOG:
                        try:
                            if hasattr(self, 'quest_log_close_button') and self.quest_log_close_button.collidepoint(event.pos):
                                self.state = STATE_GAME
                        except Exception as e:
                            print(f"クエストログ処理中のエラー: {e}")
                            self.state = STATE_GAME
                            
                    # 仲間システム画面
                    elif self.state == STATE_RECRUITMENT:
                        try:
                            if self.recruitment_system.handle_event(event):
                                if self.recruitment_system.state == "inactive":
                                    self.state = STATE_GAME
                        except Exception as e:
                            print(f"仲間システム処理中のエラー: {e}")
                            self.state = STATE_GAME
                            
                    # ショップ画面
                    elif self.state == STATE_SHOP:
                        try:
                            if self.shop_system.handle_event(event):
                                self.state = STATE_GAME
                        except Exception as e:
                            print(f"ショップ処理中のエラー: {e}")
                            self.state = STATE_GAME
                            
                    # インベントリ画面
                    elif self.state == STATE_INVENTORY:
                        try:
                            if self.item_system.handle_event(event):
                                self.state = STATE_GAME
                        except Exception as e:
                            print(f"インベントリ処理中のエラー: {e}")
                            self.state = STATE_GAME
                            
                    # ゲームオーバー画面
                    elif self.state == STATE_GAME_OVER:
                        try:
                            continue_button, title_button = self.draw_game_over_screen()
                            if continue_button.collidepoint(event.pos):
                                # セーブデータからロード
                                self.load_game()
                            elif title_button.collidepoint(event.pos):
                                # タイトル画面に戻る
                                self.state = STATE_TITLE
                        except Exception as e:
                            print(f"ゲームオーバー処理中のエラー: {e}")
                            self.state = STATE_TITLE
                            
        except Exception as e:
            print(f"イベント処理中のエラー: {e}")
            # エラー時はゲーム画面に戻る
            self.state = STATE_GAME
    def next_scene(self):
        """カットシーン終了後の処理"""
        if self.cutscene_system.scene_type == "opening":
            # オープニング終了後はチュートリアルダイアログを表示
            self.show_tutorial()
            self.state = STATE_GAME
        elif self.cutscene_system.scene_type == "ending":
            # エンディング終了後はタイトル画面に戻る
            self.state = STATE_TITLE
            # プレイヤーのステータスをリセット
            self.player = {
                "name": "Rookie Engineer",
                "level": 1,
                "exp": 0,
                "hp": 100,
                "max_hp": 100,
                "mp": 50,
                "max_mp": 50,
                "attack": 10,
                "defense": 5,
                "credits": 1000,
                "position": [25, 25],  # 中央の十字路に変更
                "tile_x": 25,          # 中央の十字路に変更
                "tile_y": 25,          # 中央の十字路に変更
                "completed_quests": [],
                "defeated_bosses": [],
                "recruited_services": []
            }
            
    def start_new_game(self):
        """新しいゲームを開始"""
        try:
            # プレイヤーデータの初期化
            self.player = {
                "name": "Rookie Engineer",
                "level": 1,
                "exp": 0,
                "hp": 100,
                "max_hp": 100,
                "mp": 50,
                "max_mp": 50,
                "attack": 10,
                "defense": 5,
                "credits": 1000,
                "position": [25, 25],  # 中央の十字路に変更
                "tile_x": 25,          # 中央の十字路に変更
                "tile_y": 25,          # 中央の十字路に変更
                "completed_quests": [],
                "defeated_bosses": [],
                "recruited_services": [],
                "inventory": [
                    {"id": "potion_small", "quantity": 5},
                    {"id": "ether_small", "quantity": 3},
                    {"id": "bronze_sword", "quantity": 1}
                ]
            }
            
            # パーティの初期化
            self.party = []
            
            # マップの初期化
            self.map_manager.generate_maps()
            self.map_manager.current_map = self.map_manager.get_map("AWS Cloud World")
            
            # クエストの初期化
            if hasattr(self, 'quest_system'):
                self.quest_system.active_quests = []
                self.quest_system.completed_quests = []
                self.quest_system.add_quest("meet_ec2")
                self.quest_system.add_quest("explore_computing_town")
            
            # オープニングカットシーンを開始
            self.state = STATE_CUTSCENE
            self.cutscene_system.start_opening()
        except Exception as e:
            print(f"新規ゲーム開始中のエラー: {e}")
            # エラー時はタイトル画面に戻る
            self.state = STATE_TITLE
    def show_tutorial(self):
        """チュートリアルダイアログを表示"""
        tutorial_text = """ようこそ、AWS クラウド異世界RPGへ！

あなたは100日徹夜した新人エンジニアで、AWSサービスが住む異世界に転移しました。
まずは「Computing Town」に向かい、EC2と会話してみましょう。

【操作方法】
・移動: 矢印キー
・メニュー: M キー または ESC キー
・クエストログ: Q キー
・会話/決定: マウスクリック
・AWSサービスを仲間にする: 会話中にRキー

現在の目標: Computing Townに向かい、EC2と会話する"""
        
        self.start_dialog(tutorial_text)
        
    def load_game(self):
        """セーブデータをロード"""
        try:
            if os.path.exists("save_data.json"):
                with open("save_data.json", "r") as f:
                    save_data = json.load(f)
                    
                # プレイヤーデータのロード
                self.player = save_data["player"]
                
                # HPが0の場合は最大HPの半分に回復させる
                if self.player["hp"] <= 0:
                    self.player["hp"] = self.player["max_hp"] // 2
                
                # パーティのロード
                self.party = save_data["party"]
                
                # パーティメンバーのHPも回復
                for member in self.party:
                    if member["hp"] <= 0:
                        member["hp"] = member["max_hp"] // 2
                
                # マップのロード
                map_name = save_data["current_map"]
                self.map_manager.current_map = self.map_manager.get_map(map_name)
                
                # 位置のロード
                if "position" in save_data:
                    self.player["tile_x"] = save_data["position"][0]
                    self.player["tile_y"] = save_data["position"][1]
                    
                # ゲーム画面に移行
                self.state = STATE_GAME
                
            else:
                print("No save data found.")
        except Exception as e:
            print(f"ロード中のエラー: {e}")
            self.state = STATE_TITLE
    def draw_title_screen(self):
        """タイトル画面を描画"""
        screen_width = 800
        screen_height = 600
        
        # 背景 - 深い青からのグラデーション
        for y in range(screen_height):
            # 上から下へのグラデーション（深い青から星空のような暗い青へ）
            color_value = 30 + int((y / screen_height) * 50)
            color = (max(0, color_value - 20), max(0, color_value - 10), min(int(color_value * 2), 100))
            pygame.draw.line(self.screen, color, (0, y), (screen_width, y))
        
        # 星を描画
        for i in range(100):
            star_x = random.randint(0, screen_width)
            star_y = random.randint(0, screen_height)
            star_size = random.randint(1, 3)
            star_brightness = random.randint(150, 255)
            pygame.draw.circle(self.screen, (star_brightness, star_brightness, star_brightness), 
                             (star_x, star_y), star_size)
            
        # 雲のような模様を追加
        for i in range(15):
            cloud_x = random.randint(0, screen_width)
            cloud_y = random.randint(0, screen_height // 2)
            cloud_size = 70 + (i % 5) * 30
            
            cloud_surface = pygame.Surface((cloud_size, cloud_size), pygame.SRCALPHA)
            cloud_color = (100, 130, 200, 30)  # 半透明の青い雲
            pygame.draw.ellipse(cloud_surface, cloud_color, (0, 0, cloud_size, cloud_size//2))
            
            self.screen.blit(cloud_surface, (cloud_x, cloud_y))
            
        # AWS風のロゴ背景（オレンジ色の矢印）
        arrow_points = [
            (screen_width//2 - 180, 70),
            (screen_width//2 + 180, 70),
            (screen_width//2 + 150, 110),
            (screen_width//2 - 150, 110)
        ]
        pygame.draw.polygon(self.screen, (255, 153, 0, 180), arrow_points)
        pygame.draw.polygon(self.screen, WHITE, arrow_points, 2)
        
        # タイトルテキスト（影付き）
        title_shadow = self.assets.render_text("AWS Cloud Isekai RPG", "large", (50, 50, 50))
        title_text = self.assets.render_text("AWS Cloud Isekai RPG", "large", WHITE)
        self.screen.blit(title_shadow, (screen_width // 2 - title_text.get_width() // 2 + 3, 83))
        self.screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 80))
        
        # サブタイトル（グロー効果）
        subtitle = "クラウドエンジニアの異世界冒険"
        for offset in range(3, 0, -1):
            glow_color = (100, 150, 255, 100 - offset * 30)
            subtitle_glow = self.assets.render_text(subtitle, "normal", glow_color)
            self.screen.blit(subtitle_glow, 
                           (screen_width // 2 - subtitle_glow.get_width() // 2 + offset, 140 + offset))
        
        subtitle_text = self.assets.render_text(subtitle, "normal", (200, 220, 255))
        self.screen.blit(subtitle_text, (screen_width // 2 - subtitle_text.get_width() // 2, 140))
        
        # キャラクターのシルエットを表示（ボタンの上に表示するため位置を変更）
        character_width = 400  # 幅を広げて間隔を確保
        character_height = 300
        character_surface = pygame.Surface((character_width, character_height), pygame.SRCALPHA)
        
        # EC2キャラクター（左側）
        ec2_img = self.assets.get_image("ec2") if "ec2" in self.assets.images else self.assets.get_image("npc")
        scaled_ec2 = pygame.transform.scale(ec2_img, (80, 80))
        character_surface.blit(scaled_ec2, (40, 100))  # 左に配置
        
        # プレイヤーキャラクター（中央）
        player_img = self.assets.get_image("player")
        scaled_player = pygame.transform.scale(player_img, (100, 100))
        character_surface.blit(scaled_player, (character_width//2 - 50, 80))  # 中央に配置
        
        # S3キャラクター（右側）
        s3_img = self.assets.get_image("s3") if "s3" in self.assets.images else self.assets.get_image("npc")
        scaled_s3 = pygame.transform.scale(s3_img, (80, 80))
        character_surface.blit(scaled_s3, (character_width - 120, 100))  # 右に配置
        
        # キャラクターの名前を表示
        ec2_name = self.assets.render_text("EC2", "small", (255, 200, 100))
        character_surface.blit(ec2_name, (40 + 40 - ec2_name.get_width()//2, 190))
        
        player_name = self.assets.render_text("You", "small", (200, 200, 255))
        character_surface.blit(player_name, (character_width//2 - player_name.get_width()//2, 190))
        
        s3_name = self.assets.render_text("S3", "small", (100, 255, 150))
        character_surface.blit(s3_name, (character_width - 120 + 40 - s3_name.get_width()//2, 190))
        
        # キャラクターシルエットを画面に配置（上部に移動）
        self.screen.blit(character_surface, (screen_width//2 - character_width//2, 150))
        
        # アニメーションエフェクト - 時間に基づく点滅
        current_time = pygame.time.get_ticks()
        pulse = (math.sin(current_time / 300) + 1) / 2  # 0～1の間で脈動
        
        # ボタン（下部に移動）
        button_y_start = 400  # ボタンの開始Y座標を下げる
        button_spacing = 60   # ボタン間の間隔
        
        # ボタンの位置を再設定
        self.title_buttons = {
            "new_game": pygame.Rect(300, button_y_start, 200, 50),
            "continue": pygame.Rect(300, button_y_start + button_spacing, 200, 50),
            "exit": pygame.Rect(300, button_y_start + button_spacing * 2, 200, 50)
        }
        
        for button_name, button_rect in self.title_buttons.items():
            # ボタンの背景（グラデーション）
            for y_offset in range(button_rect.height):
                ratio = y_offset / button_rect.height
                if button_name == "new_game":
                    # 新規ゲームは目立つ色
                    color = (int(50 + 100 * ratio), int(100 + 100 * ratio), int(150 + 100 * ratio))
                elif button_name == "exit":
                    # 終了は控えめな色
                    color = (int(100 + 50 * ratio), int(50 + 50 * ratio), int(50 + 50 * ratio))
                else:
                    # その他のボタン
                    color = (int(70 + 80 * ratio), int(70 + 80 * ratio), int(100 + 100 * ratio))
                
                pygame.draw.line(self.screen, color, 
                               (button_rect.left, button_rect.top + y_offset),
                               (button_rect.right, button_rect.top + y_offset))
            
            # ボタンの枠（アニメーション効果）
            if button_name == "new_game":
                # 新規ゲームボタンは点滅効果
                glow_intensity = int(155 + 100 * pulse)
                border_color = (255, glow_intensity, glow_intensity)
                border_width = 3
            else:
                border_color = WHITE
                border_width = 2
                
            pygame.draw.rect(self.screen, border_color, button_rect, border_width)
            
            # ボタンテキスト
            button_label = button_name.replace("_", " ").title()
            button_text = self.assets.render_text(button_label, "normal", WHITE)
            self.screen.blit(button_text, (button_rect.centerx - button_text.get_width() // 2, 
                                         button_rect.centery - button_text.get_height() // 2))
        
        # 操作ガイド（点滅効果）
        if pulse > 0.5:
            guide_text = self.assets.render_text("Click to Start Your Adventure!", "normal", (200, 200, 255))
            self.screen.blit(guide_text, (screen_width // 2 - guide_text.get_width() // 2, 
                                        screen_height - 80))
        
        # バージョン情報
        version_text = self.assets.render_text("Version 1.0", "small", (150, 150, 200))
        self.screen.blit(version_text, (screen_width - version_text.get_width() - 10, 
                                      screen_height - version_text.get_height() - 10))
        
        # 著作権表示
        copyright_text = self.assets.render_text("© 2025 AWS Cloud RPG Team", "small", (150, 150, 200))
        self.screen.blit(copyright_text, (10, screen_height - copyright_text.get_height() - 10))
    def draw_game_screen(self):
        """ゲーム画面を描画"""
        # マップの描画
        self.draw_map()
        
        # マップ名（小さく表示）
        map_name = self.assets.render_text(self.map_manager.current_map.name, "small", WHITE)
        self.screen.blit(map_name, (10, 10))
        
        # 現在の目標（小さく表示）
        objective_text = self.assets.render_text(self.quest_system.get_current_objective(), "small", WHITE)
        self.screen.blit(objective_text, (10, 30))
        
        # 操作ガイド（小さく表示）
        guide_text = self.assets.render_text("M: Menu  Q: Quests", "small", WHITE)
        self.screen.blit(guide_text, (800 - guide_text.get_width() - 10, 10))
        
        # 方向指示（目的地への矢印）
        self.draw_direction_arrow()
        
    def draw_direction_arrow(self):
        """目的地への方向を示す矢印を描画"""
        # 現在のクエストに基づいて目的地を決定
        destination = None
        
        if "meet_ec2" in self.quest_system.active_quests:
            # EC2がいるComputing Townへの方向
            for portal in self.map_manager.current_map.portals:
                if portal["destination"] == "Computing Town":
                    destination = (portal["x"], portal["y"])
                    break
        
        if destination:
            # プレイヤーから目的地への方向を計算
            dx = destination[0] - self.player["tile_x"]
            dy = destination[1] - self.player["tile_y"]
            
            # 距離が近い場合は矢印を表示しない
            if abs(dx) < 5 and abs(dy) < 5:
                return
                
            # 方向を正規化
            length = (dx**2 + dy**2)**0.5
            if length > 0:
                dx /= length
                dy /= length
                
            # 矢印の色
            arrow_color = (255, 255, 0)  # 黄色
            
            # 矢印の位置（画面端）
            arrow_x = 800 // 2
            arrow_y = 600 // 2
            
            if abs(dx) > abs(dy):
                # 水平方向の矢印
                if dx > 0:
                    arrow_x = 800 - 50
                else:
                    arrow_x = 50
                arrow_y = 600 // 2
            else:
                # 垂直方向の矢印
                if dy > 0:
                    arrow_y = 600 - 50
                else:
                    arrow_y = 50
                arrow_x = 800 // 2
                
            # 矢印を描画
            pygame.draw.circle(self.screen, arrow_color, (arrow_x, arrow_y), 15)
            
            # 矢印の向き
            end_x = arrow_x + dx * 10
            end_y = arrow_y + dy * 10
            pygame.draw.line(self.screen, arrow_color, (arrow_x, arrow_y), (end_x, end_y), 3)
            
            # 矢印の先端
            pygame.draw.polygon(self.screen, arrow_color, [
                (end_x, end_y),
                (end_x - dy * 5 - dx * 5, end_y + dx * 5 - dy * 5),
                (end_x + dy * 5 - dx * 5, end_y - dx * 5 - dy * 5)
            ])
    def draw_map(self):
        """マップを描画"""
        # 表示範囲の計算
        tile_size = 40
        visible_tiles_x = 800 // tile_size + 2
        visible_tiles_y = 600 // tile_size + 2
        
        # カメラ位置の調整（プレイヤーが中心）
        self.camera_x = self.player["tile_x"] * tile_size - 800 // 2
        self.camera_y = self.player["tile_y"] * tile_size - 600 // 2
        
        # カメラ位置の制限
        self.camera_x = max(0, min(self.camera_x, self.map_manager.current_map.width * tile_size - 800))
        self.camera_y = max(0, min(self.camera_y, self.map_manager.current_map.height * tile_size - 600))
        
        # タイルの描画
        start_x = self.camera_x // tile_size
        start_y = self.camera_y // tile_size
        
        for y in range(start_y, start_y + visible_tiles_y):
            for x in range(start_x, start_x + visible_tiles_x):
                # マップ範囲内かチェック
                if 0 <= x < self.map_manager.current_map.width and 0 <= y < self.map_manager.current_map.height:
                    tile_type = self.map_manager.current_map.tiles[y][x]
                    screen_x = x * tile_size - self.camera_x
                    screen_y = y * tile_size - self.camera_y
                
                # タイルタイプに応じた画像を描画
                if tile_type == 0:  # 空
                    # 空のタイルには床を描画（黒いタイルを防ぐため）
                    self.screen.blit(self.assets.get_image("floor"), (screen_x, screen_y))
                elif tile_type == 1:  # 床
                    self.screen.blit(self.assets.get_image("floor"), (screen_x, screen_y))
                elif tile_type == 2:  # 壁
                    self.screen.blit(self.assets.get_image("wall"), (screen_x, screen_y))
                elif tile_type == 3:  # 草
                    self.screen.blit(self.assets.get_image("grass"), (screen_x, screen_y))
                elif tile_type == 4:  # 水
                    self.screen.blit(self.assets.get_image("water"), (screen_x, screen_y))
                elif tile_type == 5:  # 道
                    self.screen.blit(self.assets.get_image("road"), (screen_x, screen_y))
                elif tile_type == 6:  # ドア
                    # ドアの下に床を描画
                    self.screen.blit(self.assets.get_image("floor"), (screen_x, screen_y))
                    self.screen.blit(self.assets.get_image("door"), (screen_x, screen_y))
                elif tile_type == 7:  # NPC
                    self.screen.blit(self.assets.get_image("floor"), (screen_x, screen_y))
                    self.screen.blit(self.assets.get_image("npc"), (screen_x, screen_y))
                elif tile_type == 8:  # ポータル
                    self.screen.blit(self.assets.get_image("floor"), (screen_x, screen_y))
                    
                    # ポータルアニメーション効果
                    current_time = pygame.time.get_ticks()
                    pulse = (math.sin(current_time / 300) + 1) / 2  # 0～1の間で脈動
                    
                    # ポータルの拡大縮小効果
                    scale_factor = 1.0 + pulse * 0.2  # 1.0～1.2の間でサイズ変動
                    portal_img = self.assets.get_image("portal")
                    
                    # 拡大したポータル画像を作成
                    scaled_size = int(tile_size * scale_factor)
                    offset = (scaled_size - tile_size) // 2
                    
                    # 拡大したポータルを中央に配置
                    self.screen.blit(portal_img, (screen_x - offset, screen_y - offset))
                    
                    # ポータルの上に町の名前を表示
                    portal = self.map_manager.current_map.get_portal_at(x, y)
                    if portal and "destination" in portal:
                        # 名前の色をアニメーション（明るさを変化）
                        name_brightness = int(200 + 55 * pulse)  # 200～255の間で明るさ変動
                        name_color = (name_brightness, name_brightness, name_brightness)
                        
                        town_name = self.assets.render_text(portal["destination"], "small", name_color)
                        # 名前を中央に配置
                        name_x = screen_x + (tile_size - town_name.get_width()) // 2
                        name_y = screen_y - 20  # タイルの上に表示（少し上げる）
                        
                        # 背景を少し暗くして読みやすくする
                        name_bg = pygame.Surface((town_name.get_width() + 8, town_name.get_height() + 4))
                        name_bg.fill((0, 0, 50))
                        name_bg.set_alpha(150)  # 半透明
                        self.screen.blit(name_bg, (name_x - 4, name_y - 2))
                        self.screen.blit(town_name, (name_x, name_y))
                elif tile_type == 9:  # ショップ
                    self.screen.blit(self.assets.get_image("floor"), (screen_x, screen_y))
                    self.screen.blit(self.assets.get_image("shop"), (screen_x, screen_y))
                elif tile_type == 10:  # 山
                    self.screen.blit(self.assets.get_image("mountain"), (screen_x, screen_y))
                elif tile_type == 11:  # 森
                    self.screen.blit(self.assets.get_image("forest"), (screen_x, screen_y))
                elif tile_type == 12:  # 砂
                    self.screen.blit(self.assets.get_image("sand"), (screen_x, screen_y))
                # 町の装飾オブジェクト
                elif tile_type == 13:  # 噴水
                    self.screen.blit(self.assets.get_image("floor"), (screen_x, screen_y))
                    self.screen.blit(self.assets.get_image("fountain"), (screen_x, screen_y))
                elif tile_type == 14:  # ベンチ
                    self.screen.blit(self.assets.get_image("floor"), (screen_x, screen_y))
                    self.screen.blit(self.assets.get_image("bench"), (screen_x, screen_y))
                elif tile_type == 15:  # 街灯
                    self.screen.blit(self.assets.get_image("floor"), (screen_x, screen_y))
                    self.screen.blit(self.assets.get_image("lamp"), (screen_x, screen_y))
                elif tile_type == 16:  # 看板
                    self.screen.blit(self.assets.get_image("floor"), (screen_x, screen_y))
                    self.screen.blit(self.assets.get_image("sign"), (screen_x, screen_y))
                elif tile_type == 17:  # 花壇
                    self.screen.blit(self.assets.get_image("floor"), (screen_x, screen_y))
                    self.screen.blit(self.assets.get_image("flowerbed"), (screen_x, screen_y))
                else:  # 未定義のタイルタイプ
                    # デフォルトで床を表示
                    self.screen.blit(self.assets.get_image("floor"), (screen_x, screen_y))
    
        # NPCの描画
        for npc in self.map_manager.current_map.npcs:
            npc_x = npc["x"] * tile_size - self.camera_x
            npc_y = npc["y"] * tile_size - self.camera_y
            
            # 画面内にあるNPCのみ描画
            if -tile_size <= npc_x < 800 + tile_size and -tile_size <= npc_y < 600 + tile_size:
                # NPCの種類に応じた画像を描画
                if "is_service" in npc and npc["is_service"] and "service_id" in npc:
                    # AWSサービスキャラクター
                    service_id = npc["service_id"]
                    if service_id in self.assets.images:
                        self.screen.blit(self.assets.get_image(service_id), (npc_x, npc_y))
                    else:
                        # フォールバック：通常のNPC画像
                        self.screen.blit(self.assets.get_image("npc"), (npc_x, npc_y))
                else:
                    # 通常のNPC
                    self.screen.blit(self.assets.get_image("npc"), (npc_x, npc_y))
                
                # NPCの名前を表示
                npc_name = self.assets.render_text(npc["name"], "small", (255, 255, 255))
                name_x = npc_x + (tile_size - npc_name.get_width()) // 2
                name_y = npc_y - 15
                
                # 名前の背景
                name_bg = pygame.Surface((npc_name.get_width() + 4, npc_name.get_height() + 2))
                name_bg.fill((0, 0, 50))
                name_bg.set_alpha(150)
                self.screen.blit(name_bg, (name_x - 2, name_y - 1))
                self.screen.blit(npc_name, (name_x, name_y))
                
                # プレイヤーがNPCの近くにいるかチェック
                player_x = self.player["tile_x"]
                player_y = self.player["tile_y"]
                if abs(player_x - npc["x"]) <= 1 and abs(player_y - npc["y"]) <= 1:
                    # 吹き出しを表示
                    bubble_x = npc_x + tile_size // 2
                    bubble_y = npc_y - 30
                    
                    # 吹き出しの背景
                    bubble_width = 120
                    bubble_height = 25
                    bubble_rect = pygame.Rect(bubble_x - bubble_width // 2, bubble_y - bubble_height // 2, 
                                            bubble_width, bubble_height)
                    
                    # 吹き出しの形状
                    pygame.draw.ellipse(self.screen, WHITE, bubble_rect)
                    pygame.draw.ellipse(self.screen, BLACK, bubble_rect, 2)
                    
                    # 吹き出しの尖った部分
                    point_x = bubble_x
                    point_y = bubble_y + bubble_height // 2
                    pygame.draw.polygon(self.screen, WHITE, [
                        (point_x - 5, point_y),
                        (point_x + 5, point_y),
                        (point_x, point_y + 10)
                    ])
                    pygame.draw.line(self.screen, BLACK, (point_x - 5, point_y), (point_x, point_y + 10), 2)
                    pygame.draw.line(self.screen, BLACK, (point_x + 5, point_y), (point_x, point_y + 10), 2)
                    
                    # 吹き出しのテキスト
                    bubble_text = self.assets.render_text("Press E to talk", "small", BLACK)
                    self.screen.blit(bubble_text, (bubble_x - bubble_text.get_width() // 2, 
                                                bubble_y - bubble_text.get_height() // 2))
    
        # ショップの描画
        for shop in self.map_manager.current_map.shops:
            shop_x = shop["x"] * tile_size - self.camera_x
            shop_y = shop["y"] * tile_size - self.camera_y
            
            # 画面内にあるショップのみ描画
            if -tile_size <= shop_x < 800 + tile_size and -tile_size <= shop_y < 600 + tile_size:
                # ショップアイコン
                self.screen.blit(self.assets.get_image("shop"), (shop_x, shop_y))
            
                # ショップ名を表示
                shop_name = self.assets.render_text(shop["name"], "small", (255, 255, 0))
                name_x = shop_x + (tile_size - shop_name.get_width()) // 2
                name_y = shop_y - 15
                
                # 名前の背景
                name_bg = pygame.Surface((shop_name.get_width() + 4, shop_name.get_height() + 2))
                name_bg.fill((50, 30, 0))
                name_bg.set_alpha(150)
                self.screen.blit(name_bg, (name_x - 2, name_y - 1))
                self.screen.blit(shop_name, (name_x, name_y))
                
                # プレイヤーがショップの近くにいるかチェック
                player_x = self.player["tile_x"]
                player_y = self.player["tile_y"]
                if abs(player_x - shop["x"]) <= 1 and abs(player_y - shop["y"]) <= 1:
                    # 吹き出しを表示
                    bubble_x = shop_x + tile_size // 2
                    bubble_y = shop_y - 30
                    
                    # 吹き出しの背景
                    bubble_width = 120
                    bubble_height = 25
                    bubble_rect = pygame.Rect(bubble_x - bubble_width // 2, bubble_y - bubble_height // 2, 
                                            bubble_width, bubble_height)
                    
                    # 吹き出しの形状
                    pygame.draw.ellipse(self.screen, WHITE, bubble_rect)
                    pygame.draw.ellipse(self.screen, BLACK, bubble_rect, 2)
                    
                    # 吹き出しの尖った部分
                    point_x = bubble_x
                    point_y = bubble_y + bubble_height // 2
                    pygame.draw.polygon(self.screen, WHITE, [
                        (point_x - 5, point_y),
                        (point_x + 5, point_y),
                        (point_x, point_y + 10)
                    ])
                    pygame.draw.line(self.screen, BLACK, (point_x - 5, point_y), (point_x, point_y + 10), 2)
                    pygame.draw.line(self.screen, BLACK, (point_x + 5, point_y), (point_x, point_y + 10), 2)
                    
                    # 吹き出しのテキスト
                    bubble_text = self.assets.render_text("Press E to shop", "small", BLACK)
                    self.screen.blit(bubble_text, (bubble_x - bubble_text.get_width() // 2, 
                                                bubble_y - bubble_text.get_height() // 2))
    
        # プレイヤーの描画
        player_x = self.player["tile_x"] * tile_size - self.camera_x
        player_y = self.player["tile_y"] * tile_size - self.camera_y
        self.screen.blit(self.assets.get_image("player"), (player_x, player_y))
    
    def draw_dialog(self):
        """ダイアログを描画"""
        if not self.dialog:
            return
            
        # ダイアログボックス
        dialog_box = pygame.Rect(50, 400, 700, 150)
        pygame.draw.rect(self.screen, (50, 50, 50), dialog_box)
        pygame.draw.rect(self.screen, WHITE, dialog_box, 3)
        
        # NPCの名前
        if self.dialog_npc:
            npc_name = self.assets.render_text(self.dialog_npc["name"], "normal", (255, 255, 0))
            self.screen.blit(npc_name, (70, 420))
        
        # ダイアログテキスト
        dialog_text = self.assets.render_text(self.dialog, "normal", WHITE)
        self.screen.blit(dialog_text, (70, 460))
        
        # 続行指示
        continue_text = self.assets.render_text("Click to continue", "small", (200, 200, 200))
        self.screen.blit(continue_text, (650, 520))
        
    def move_player(self, dx, dy):
        """プレイヤーを移動"""
        try:
            new_x = self.player["tile_x"] + dx
            new_y = self.player["tile_y"] + dy
            
            # マップ範囲内かつ歩行可能かチェック
            if self.map_manager.current_map.is_walkable(new_x, new_y):
                self.player["tile_x"] = new_x
                self.player["tile_y"] = new_y
                
                # NPCとの会話
                npc = self.map_manager.current_map.get_npc_at(new_x, new_y)
                if npc:
                    self.start_dialog(npc["dialog"], npc)
                    
                # ポータルでのマップ移動
                portal = self.map_manager.current_map.get_portal_at(new_x, new_y)
                if portal:
                    self.change_map(portal["destination"], portal["dest_x"], portal["dest_y"])
                    
                    # Computing Townに入った場合、クエスト進行状況を更新
                    if portal["destination"] == "Computing Town" and "explore_computing_town" in self.quest_system.active_quests:
                        self.quest_system.complete_quest("explore_computing_town")
                        # 新しいクエストを追加
                        self.quest_system.add_quest("defeat_sql_injection")
                    
                # ショップ
                shop = self.map_manager.current_map.get_shop_at(new_x, new_y)
                if shop:
                    self.start_shop(shop)
                    
                # ランダムエンカウント
                if random.random() < self.map_manager.current_map.encounter_rate:
                    # クエスト進行状況に応じて敵タイプを変更
                    if "defeat_sql_injection" in self.quest_system.active_quests:
                        self.start_battle("sql_injection")
                        # クエスト完了
                        self.quest_system.complete_quest("defeat_sql_injection")
                        # 最終クエストを追加
                        self.quest_system.add_quest("final_battle")
                    elif "final_battle" in self.quest_system.active_quests:
                        # 最終ボス戦
                        self.start_battle("boss")
                        # クエスト完了
                        self.quest_system.complete_quest("final_battle")
                    else:
                        self.start_battle(random.choice(["weak", "normal", "strong"]))
                    
                return True
                
            return False
        except Exception as e:
            print(f"プレイヤー移動中のエラー: {e}")
            return False
    def start_dialog(self, text, npc=None):
        """ダイアログを開始"""
        self.state = STATE_DIALOG
        self.dialog = text
        self.dialog_npc = npc
        
        # NPCがAWSサービスの場合、仲間にするオプションを表示
        if npc and "is_service" in npc and npc["is_service"]:
            self.dialog += "\n\n[R]キーを押して仲間にするクイズに挑戦"
            self.dialog_npc_is_service = True
        else:
            self.dialog_npc_is_service = False
            
    def start_battle(self, enemy_type="normal"):
        """バトルを開始"""
        try:
            self.state = STATE_BATTLE
            # ボス戦の場合
            if enemy_type == "boss":
                self.battle_system.start_battle("ddos")
            else:
                self.battle_system.start_battle(enemy_type)
        except Exception as e:
            print(f"バトル開始中のエラー: {e}")
            self.state = STATE_GAME
            
    def change_map(self, map_name, player_x, player_y):
        """マップを変更"""
        try:
            new_map = self.map_manager.get_map(map_name)
            if new_map:
                self.map_manager.current_map = new_map
                self.player["tile_x"] = player_x
                self.player["tile_y"] = player_y
        except Exception as e:
            print(f"マップ変更中のエラー: {e}")

    def start_shop(self, shop):
        """ショップを開始"""
        self.state = STATE_SHOP
        self.shop_system.set_shop_type(shop["type"])
        self.shop_system.active = True
        self.start_dialog(shop["dialog"], {"name": shop["name"]})

if __name__ == "__main__":
    game = Game()
    game.run()


if __name__ == "__main__":
    game = Game()
    game.run()
    def handle_event(self, event):
        """イベント処理"""
        if self.state == STATE_TITLE:
            # タイトル画面
            if event.type == pygame.MOUSEBUTTONDOWN:
                start_button, load_button, quit_button = self.draw_title_screen()
                if start_button.collidepoint(event.pos):
                    self.state = STATE_GAME
                    self.init_game()
                elif load_button.collidepoint(event.pos):
                    self.load_game()
                elif quit_button.collidepoint(event.pos):
                    self.running = False
                    
        elif self.state == STATE_GAME:
            # ゲーム画面
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.move_player(0, -1)
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.move_player(0, 1)
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.move_player(-1, 0)
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.move_player(1, 0)
                elif event.key == pygame.K_m:
                    self.state = STATE_MENU
                elif event.key == pygame.K_q:
                    self.state = STATE_QUEST_LOG
                elif event.key == pygame.K_i:
                    self.state = STATE_INVENTORY
                elif event.key == pygame.K_r and self.dialog_npc_is_service and self.dialog_npc and "name" in self.dialog_npc:
                    # AWSサービスの仲間にするクイズを開始
                    self.state = STATE_RECRUITMENT
                    self.recruitment_system.start_recruitment(self.dialog_npc["name"].lower())
                    
        elif self.state == STATE_DIALOG:
            # ダイアログ画面
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.state = STATE_GAME
                
        elif self.state == STATE_BATTLE:
            # バトル画面
            self.battle_system.handle_event(event)
            if self.battle_system.battle_ended:
                if self.battle_system.battle_result == "win":
                    self.state = STATE_GAME
                else:
                    self.state = STATE_GAME_OVER
                    
        elif self.state == STATE_MENU:
            # メニュー画面
            if event.type == pygame.MOUSEBUTTONDOWN:
                save_button, quit_button, back_button = self.draw_menu_screen()
                if save_button.collidepoint(event.pos):
                    self.save_game()
                elif quit_button.collidepoint(event.pos):
                    self.running = False
                elif back_button.collidepoint(event.pos):
                    self.state = STATE_GAME
                    
        elif self.state == STATE_CUTSCENE:
            # カットシーン画面
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.cutscene_system.proceed():
                    self.state = STATE_GAME
                    
        elif self.state == STATE_QUEST_LOG:
            # クエストログ画面
            if event.type == pygame.MOUSEBUTTONDOWN:
                back_button = self.draw_quest_log_screen()
                if back_button.collidepoint(event.pos):
                    self.state = STATE_GAME
                    
        elif self.state == STATE_RECRUITMENT:
            # 仲間にする画面
            if self.recruitment_system.handle_event(event):
                if self.recruitment_system.state == "inactive":
                    self.state = STATE_GAME
                    
        elif self.state == STATE_SHOP:
            # ショップ画面
            if self.shop_system.handle_event(event):
                if not self.shop_system.active:
                    self.state = STATE_GAME
                    
        elif self.state == STATE_INVENTORY:
            # インベントリ画面
            if event.type == pygame.MOUSEBUTTONDOWN:
                back_button = self.draw_inventory_screen()
                if back_button.collidepoint(event.pos):
                    self.state = STATE_GAME
                    
        elif self.state == STATE_GAME_OVER:
            # ゲームオーバー画面
            if event.type == pygame.MOUSEBUTTONDOWN:
                continue_button, title_button = self.draw_game_over_screen()
                if continue_button.collidepoint(event.pos):
                    self.load_game()
                elif title_button.collidepoint(event.pos):
                    self.state = STATE_TITLE
