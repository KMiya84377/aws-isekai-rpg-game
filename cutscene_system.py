#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
import math

# 画面サイズ定数
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class CutsceneSystem:
    def __init__(self, assets):
        self.assets = assets
        self.current_scene = 0
        self.active = False
        self.scenes = []
        self.scene_type = None  # "opening" または "ending"
        self.fade_alpha = 0
        self.fade_direction = 1  # 1: フェードイン, -1: フェードアウト
        self.fade_speed = 5
        self.text_display_progress = 0
        self.text_speed = 2
        
        # 背景画像（仮の実装）
        self.backgrounds = {
            "office_bg": (20, 20, 50),
            "light_bg": (200, 200, 255),
            "aws_world_bg": (50, 100, 150),
            "battle_bg": (100, 50, 50),
            "credits_bg": (0, 0, 0)
        }
        
        # キャラクター画像（仮の実装）
        self.characters = {
            "player": self.assets.get_image("player"),
            "ec2": self.assets.get_image("ec2"),
            "s3": self.assets.get_image("s3"),
            "lambda": self.assets.get_image("lambda"),
            "dynamodb": self.assets.get_image("dynamodb")
        }
        
    def start_opening(self):
        """オープニングシーケンスを開始"""
        self.scenes = self.create_opening_sequence()
        self.scene_type = "opening"
        self.current_scene = 0
        self.active = True
        self.fade_alpha = 255
        self.fade_direction = -1  # フェードアウト
        self.text_display_progress = 0
        
    def start_ending(self):
        """エンディングシーケンスを開始"""
        self.scenes = self.create_ending_sequence()
        self.scene_type = "ending"
        self.current_scene = 0
        self.active = True
        self.fade_alpha = 255
        self.fade_direction = -1  # フェードアウト
        self.text_display_progress = 0
        
    def create_opening_sequence(self):
        """オープニングシーケンスを作成"""
        return [
            {
                "background": "office_bg",
                "text": "とある企業のオフィスにて...",
                "character": None
            },
            {
                "background": "office_bg",
                "text": "「このプロジェクト、納期に間に合わせないと...」",
                "character": "player"
            },
            {
                "background": "office_bg",
                "text": "新人エンジニアは100日間徹夜を続けていた。",
                "character": None
            },
            {
                "background": "office_bg",
                "text": "「もう...限界...」",
                "character": "player"
            },
            {
                "background": "office_bg",
                "text": "その時、モニターから謎の光が溢れ出した。",
                "character": None
            },
            {
                "background": "light_bg",
                "text": "「な、なんだ!?」",
                "character": "player"
            },
            {
                "background": "light_bg",
                "text": "光に包まれ、意識が遠のいていく...",
                "character": None
            },
            {
                "background": "aws_world_bg",
                "text": "目を覚ますと、そこは見知らぬ世界だった。",
                "character": None
            },
            {
                "background": "aws_world_bg",
                "text": "「ここは...どこだ？」",
                "character": "player"
            },
            {
                "background": "aws_world_bg",
                "text": "「ようこそ、AWSクラウド世界へ。あなたは異世界から来たようですね。」",
                "character": "ec2"
            },
            {
                "background": "aws_world_bg",
                "text": "「AWSクラウド世界？まさか、あのAmazon Web Servicesの？」",
                "character": "player"
            },
            {
                "background": "aws_world_bg",
                "text": "「そうです。私はEC2、この世界のコンピューティング町の住人です。」",
                "character": "ec2"
            },
            {
                "background": "aws_world_bg",
                "text": "「この世界は今、セキュリティ脆弱性という敵に襲われています。」",
                "character": "ec2"
            },
            {
                "background": "aws_world_bg",
                "text": "「あなたが持つ知識が、この世界を救う鍵になるかもしれません。」",
                "character": "ec2"
            },
            {
                "background": "aws_world_bg",
                "text": "「まずはComputing Townに来てください。そこで詳しく説明します。」",
                "character": "ec2"
            }
        ]
        
    def create_ending_sequence(self):
        """エンディングシーケンスを作成"""
        return [
            {
                "background": "battle_bg",
                "text": "DDoS攻撃が倒れ、世界に平和が戻った。",
                "character": None
            },
            {
                "background": "aws_world_bg",
                "text": "「君のおかげで世界は救われた。本当にありがとう。」",
                "character": "ec2"
            },
            {
                "background": "aws_world_bg",
                "text": "「いや、みんなの力があったからこそだ。」",
                "character": "player"
            },
            {
                "background": "aws_world_bg",
                "text": "「元の世界に戻る時が来たようだね。」",
                "character": "s3"
            },
            {
                "background": "aws_world_bg",
                "text": "「ああ、でもこの世界で学んだことは一生の宝物だ。」",
                "character": "player"
            },
            {
                "background": "light_bg",
                "text": "主人公は再び光に包まれ、元の世界へと戻っていった。",
                "character": None
            },
            {
                "background": "office_bg",
                "text": "目を覚ますと、オフィスのデスクで眠っていた。",
                "character": None
            },
            {
                "background": "office_bg",
                "text": "「不思議な夢を見たな...でも、なぜかAWSの知識がすごく頭に入っている...」",
                "character": "player"
            },
            {
                "background": "office_bg",
                "text": "その日から、主人公は一流のクラウドエンジニアとして活躍するのであった。",
                "character": None
            },
            {
                "background": "credits_bg",
                "text": "THE END",
                "character": None
            }
        ]
        
    def update(self):
        """カットシーンの状態を更新"""
        if not self.active:
            return False
            
        # フェードエフェクトの更新
        self.fade_alpha += self.fade_direction * self.fade_speed
        if self.fade_alpha <= 0:
            self.fade_alpha = 0
            self.fade_direction = 0  # フェード停止
        elif self.fade_alpha >= 255:
            self.fade_alpha = 255
            self.fade_direction = 0  # フェード停止
            
        # テキスト表示の進行
        if self.fade_direction == 0:  # フェードが完了している場合
            current_text = self.scenes[self.current_scene]["text"]
            if self.text_display_progress < len(current_text):
                self.text_display_progress += self.text_speed
                self.text_display_progress = min(self.text_display_progress, len(current_text))
                
        return True
        
    def next_scene(self):
        """次のシーンに進む"""
        if not self.active:
            return False
            
        # テキストがまだ全部表示されていない場合は、全て表示する
        current_text = self.scenes[self.current_scene]["text"]
        if self.text_display_progress < len(current_text):
            self.text_display_progress = len(current_text)
            return True
            
        # 次のシーンに進む
        self.current_scene += 1
        self.text_display_progress = 0
        
        # フェードイン開始
        self.fade_alpha = 255
        self.fade_direction = -1
        
        # 全てのシーンが終了した場合
        if self.current_scene >= len(self.scenes):
            self.active = False
            return False
            
        return True
        
    def draw(self, screen):
        """カットシーンを描画"""
        if not self.active or self.current_scene >= len(self.scenes):
            return
            
        scene = self.scenes[self.current_scene]
        
        # 背景色
        bg_color = self.backgrounds.get(scene["background"], (0, 0, 0))
        
        # グラデーション背景
        for y in range(600):
            # 背景に応じたグラデーション
            if scene["background"] == "office_bg":
                # オフィス - 暗い青から暗い灰色へ
                color_value = 20 + int((y / 600) * 30)
                color = (color_value, color_value, color_value + 10)
            elif scene["background"] == "light_bg":
                # 光 - 白から青へ
                color_value = 200 - int((y / 600) * 50)
                color = (color_value, color_value, min(255, color_value + 50))
            elif scene["background"] == "aws_world_bg":
                # AWS世界 - 青から緑へ
                color_value = 50 + int((y / 600) * 100)
                color = (color_value // 2, color_value, color_value)
            elif scene["background"] == "battle_bg":
                # バトル - 赤から黒へ
                color_value = 100 - int((y / 600) * 50)
                color = (color_value, color_value // 2, color_value // 2)
            else:
                # デフォルト
                color_value = 50 + int((y / 600) * 50)
                color = (color_value // 2, color_value // 2, color_value)
                
            pygame.draw.line(screen, color, (0, y), (800, y))
            
        # 背景の装飾
        if scene["background"] == "office_bg":
            # オフィスの窓
            window = pygame.Rect(500, 100, 200, 150)
            pygame.draw.rect(screen, (50, 100, 150), window)
            pygame.draw.rect(screen, (100, 100, 100), window, 2)
            
            # デスク
            desk = pygame.Rect(100, 300, 400, 50)
            pygame.draw.rect(screen, (100, 70, 40), desk)
            pygame.draw.rect(screen, (80, 50, 30), desk, 2)
            
            # モニター
            monitor = pygame.Rect(200, 200, 200, 150)
            pygame.draw.rect(screen, (30, 30, 30), monitor)
            pygame.draw.rect(screen, (50, 50, 50), monitor, 2)
            
            # モニター画面
            screen_rect = pygame.Rect(210, 210, 180, 130)
            pygame.draw.rect(screen, (100, 150, 200), screen_rect)
            
        elif scene["background"] == "light_bg":
            # 光の効果
            for i in range(20):
                radius = 100 + i * 20
                pygame.draw.circle(screen, (255, 255, 255, 100 - i * 5), 
                                 (800 // 2, 600 // 2), radius, 2)
                                 
        elif scene["background"] == "aws_world_bg":
            # クラウドのような模様
            for i in range(10):
                cloud_x = (i * 100) % 800
                cloud_y = (i * 50) % (600 // 2)
                cloud_size = 50 + (i % 5) * 20
                
                cloud_surface = pygame.Surface((cloud_size, cloud_size), pygame.SRCALPHA)
                pygame.draw.ellipse(cloud_surface, (255, 255, 255, 50), 
                                  (0, 0, cloud_size, cloud_size//2))
                
                screen.blit(cloud_surface, (cloud_x, cloud_y))
        
        # キャラクター
        if scene["character"] and scene["character"] in self.characters:
            char_img = self.characters[scene["character"]]
            # キャラクターを画面中央下部に配置
            char_x = (screen.get_width() - char_img.get_width()) // 2
            char_y = screen.get_height() - char_img.get_height() - 150
            screen.blit(char_img, (char_x, char_y))
        
        # テキストボックス（装飾付き）
        text_box = pygame.Rect(50, screen.get_height() - 150, screen.get_width() - 100, 100)
        # グラデーション背景
        for y in range(100):
            color_val = 0 + int(y / 2)
            color = (color_val, color_val, color_val, 180)
            pygame.draw.line(screen, color, 
                           (50, screen.get_height() - 150 + y), 
                           (screen.get_width() - 50, screen.get_height() - 150 + y))
            
        pygame.draw.rect(screen, (255, 255, 255), text_box, 2)
        
        # 装飾
        pygame.draw.line(screen, (200, 200, 200), 
                       (60, screen.get_height() - 140), 
                       (screen.get_width() - 60, screen.get_height() - 140), 1)
        pygame.draw.line(screen, (200, 200, 200), 
                       (60, screen.get_height() - 60), 
                       (screen.get_width() - 60, screen.get_height() - 60), 1)
        
        # テキスト（徐々に表示）
        full_text = scene["text"]
        display_text = full_text[:int(self.text_display_progress)]
        
        # テキストを複数行に分割
        lines = self._wrap_text(display_text, 50)
        for i, line in enumerate(lines):
            text_surf = self.assets.render_text(line, "normal", (255, 255, 255))
            screen.blit(text_surf, (70, screen.get_height() - 130 + i * 30))
        
        # 続行指示（テキストが全て表示された場合のみ）
        if self.text_display_progress >= len(full_text):
            continue_text = self.assets.render_text("Click to continue", "small", (200, 200, 200))
            screen.blit(continue_text, (screen.get_width() - continue_text.get_width() - 70, 
                                      screen.get_height() - 70))
        
        # フェードエフェクト
        if self.fade_alpha > 0:
            fade_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            fade_surface.fill((0, 0, 0, self.fade_alpha))
            screen.blit(fade_surface, (0, 0))
            
    def _wrap_text(self, text, chars_per_line):
        """テキストを指定した文字数で折り返す"""
        words = text.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            if len(test_line) > chars_per_line:
                lines.append(current_line)
                current_line = word + " "
            else:
                current_line = test_line
                
        if current_line:
            lines.append(current_line)
            
        return lines
        
    def handle_event(self, event):
        """イベント処理"""
        if not self.active:
            return False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 配列の範囲外アクセスを防止
            if self.current_scene < len(self.scenes):
                return self.next_scene()
            else:
                self.active = False
                return False
                
        return True
