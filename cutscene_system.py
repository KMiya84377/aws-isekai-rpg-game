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
        """Create the opening sequence"""
        return [
            {
                "background": "office_bg",
                "text": "In a corporate office somewhere...",
                "character": None
            },
            {
                "background": "office_bg",
                "text": "\"I need to meet this project deadline somehow...\"",
                "character": "player"
            },
            {
                "background": "office_bg",
                "text": "The rookie engineer had been working for 100 days straight.",
                "character": None
            },
            {
                "background": "office_bg",
                "text": "\"I've reached... my limit...\"",
                "character": "player"
            },
            {
                "background": "office_bg",
                "text": "Suddenly, a mysterious light began to emanate from the monitor.",
                "character": None
            },
            {
                "background": "light_bg",
                "text": "\"What's happening!?\"",
                "character": "player"
            },
            {
                "background": "light_bg",
                "text": "Enveloped in light, consciousness began to fade...",
                "character": None
            },
            {
                "background": "aws_world_bg",
                "text": "Upon awakening, an unfamiliar world appeared.",
                "character": None
            },
            {
                "background": "aws_world_bg",
                "text": "\"Where... am I?\"",
                "character": "player"
            },
            {
                "background": "aws_world_bg",
                "text": "\"Welcome to the AWS Cloud World. You seem to have come from another world.\"",
                "character": "ec2"
            },
            {
                "background": "aws_world_bg",
                "text": "\"AWS Cloud World? You mean Amazon Web Services?\"",
                "character": "player"
            },
            {
                "background": "aws_world_bg",
                "text": "\"That's right. I'm EC2, a resident of Computing Town in this world.\"",
                "character": "ec2"
            },
            {
                "background": "aws_world_bg",
                "text": "\"This world is currently under attack by security vulnerabilities.\"",
                "character": "ec2"
            },
            {
                "background": "aws_world_bg",
                "text": "\"Your knowledge might be the key to saving our world.\"",
                "character": "ec2"
            },
            {
                "background": "aws_world_bg",
                "text": "\"Please come to Computing Town. I'll explain everything in detail there.\"",
                "character": "ec2"
            }
        ]
        
    def create_ending_sequence(self):
        """Create the ending sequence"""
        return [
            {
                "background": "battle_bg",
                "text": "The DDoS attack was defeated, and peace returned to the world.",
                "character": None
            },
            {
                "background": "aws_world_bg",
                "text": "\"Thanks to you, our world has been saved. Thank you so much.\"",
                "character": "ec2"
            },
            {
                "background": "aws_world_bg",
                "text": "\"No, it was only possible because of everyone's help.\"",
                "character": "player"
            },
            {
                "background": "aws_world_bg",
                "text": "\"It seems like it's time for you to return to your world.\"",
                "character": "s3"
            },
            {
                "background": "aws_world_bg",
                "text": "\"Yes, but the knowledge I've gained in this world will be my treasure forever.\"",
                "character": "player"
            },
            {
                "background": "light_bg",
                "text": "The hero was once again enveloped in light, returning to the original world.",
                "character": None
            },
            {
                "background": "office_bg",
                "text": "Upon awakening, they found themselves asleep at their office desk.",
                "character": None
            },
            {
                "background": "office_bg",
                "text": "\"What a strange dream... but somehow, I understand AWS much better now...\"",
                "character": "player"
            },
            {
                "background": "office_bg",
                "text": "From that day forward, the hero thrived as a top-tier cloud engineer.",
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
