#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import os
import random
import math

# 色の定数
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 100, 150)
LIGHT_BLUE = (173, 216, 230)
ORANGE = (255, 165, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# タイルサイズ
TILE_SIZE = 40

class GameAssets:
    def __init__(self):
        self.images = {}
        self.fonts = {}
        self.load_assets()
        
    def load_assets(self):
        """ゲームアセットをロードする"""
        # フォントの読み込み
        self.fonts["small"] = pygame.font.SysFont(None, 24)
        self.fonts["normal"] = pygame.font.SysFont(None, 32)
        self.fonts["large"] = pygame.font.SysFont(None, 48)
        
        # 町のオブジェクト用の追加アセット
        self.town_objects = {}
        # プレイヤー画像の作成（人間のピクセルアート）
        player_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        # 頭
        pygame.draw.circle(player_surface, (255, 220, 180), (TILE_SIZE//2, TILE_SIZE//4), TILE_SIZE//6)
        # 髪の毛
        pygame.draw.arc(player_surface, (50, 50, 50), 
                      (TILE_SIZE//2 - TILE_SIZE//6, TILE_SIZE//4 - TILE_SIZE//6, 
                       TILE_SIZE//3, TILE_SIZE//3), 0, math.pi, 3)
        # 目
        pygame.draw.circle(player_surface, (255, 255, 255), 
                         (TILE_SIZE//2 - TILE_SIZE//12, TILE_SIZE//4), TILE_SIZE//20)
        pygame.draw.circle(player_surface, (255, 255, 255), 
                         (TILE_SIZE//2 + TILE_SIZE//12, TILE_SIZE//4), TILE_SIZE//20)
        pygame.draw.circle(player_surface, (0, 0, 0), 
                         (TILE_SIZE//2 - TILE_SIZE//12, TILE_SIZE//4), TILE_SIZE//40)
        pygame.draw.circle(player_surface, (0, 0, 0), 
                         (TILE_SIZE//2 + TILE_SIZE//12, TILE_SIZE//4), TILE_SIZE//40)
        # 体
        pygame.draw.rect(player_surface, (70, 130, 230), 
                        (TILE_SIZE//3, TILE_SIZE//3, TILE_SIZE//3, TILE_SIZE//2))
        # 腕と足
        pygame.draw.rect(player_surface, (70, 130, 230), 
                        (TILE_SIZE//6, TILE_SIZE//3, TILE_SIZE//6, TILE_SIZE//2))
        pygame.draw.rect(player_surface, (70, 130, 230), 
                        (TILE_SIZE*2//3, TILE_SIZE//3, TILE_SIZE//6, TILE_SIZE//2))
        # 靴
        pygame.draw.rect(player_surface, (120, 100, 80), 
                        (TILE_SIZE//4, TILE_SIZE*3//4, TILE_SIZE//5, TILE_SIZE//4))
        pygame.draw.rect(player_surface, (120, 100, 80), 
                        (TILE_SIZE*3//5, TILE_SIZE*3//4, TILE_SIZE//5, TILE_SIZE//4))
        self.images["player"] = player_surface
        
        # マップタイルの作成
        # 床タイル（石畳模様）
        floor_tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
        floor_tile.fill((220, 220, 220))  # より明るい色
        for y in range(4):  # より細かい石畳
            for x in range(4):
                if (x + y) % 2 == 0:
                    pygame.draw.rect(floor_tile, (200, 200, 200), 
                                   (x*TILE_SIZE//4, y*TILE_SIZE//4, TILE_SIZE//4, TILE_SIZE//4))
                pygame.draw.rect(floor_tile, (180, 180, 180), 
                               (x*TILE_SIZE//4, y*TILE_SIZE//4, TILE_SIZE//4, TILE_SIZE//4), 1)
        self.images["floor"] = floor_tile
        
        # 壁タイル（レンガ模様）
        wall_tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
        wall_tile.fill((150, 120, 100))  # より明るい茶色
        for y in range(4):
            for x in range(4):
                if (x + y) % 2 == 0:
                    pygame.draw.rect(wall_tile, (170, 140, 120), 
                                   (x*TILE_SIZE//4, y*TILE_SIZE//4, TILE_SIZE//4, TILE_SIZE//4))
                pygame.draw.rect(wall_tile, (130, 100, 80), 
                               (x*TILE_SIZE//4, y*TILE_SIZE//4, TILE_SIZE//4, TILE_SIZE//4), 1)
        self.images["wall"] = wall_tile
        
        # 草タイル（より詳細な草）
        grass_tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
        grass_tile.fill((120, 200, 120))  # より明るい緑
        for i in range(25):  # より多くの草
            x = random.randint(2, TILE_SIZE-3)
            y = random.randint(2, TILE_SIZE-3)
            h = random.randint(5, 15)  # より長い草も
            pygame.draw.line(grass_tile, (70, 170, 70), (x, y), (x, y-h), 2)
        self.images["grass"] = grass_tile
        
        # 水タイル（波のアニメーション効果）
        water_tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
        water_tile.fill((70, 130, 230))  # より鮮やかな青
        for i in range(5):  # より多くの波
            pygame.draw.line(water_tile, (120, 180, 255), 
                           (0, 5 + i*8), (TILE_SIZE, 10 + i*8), 2)
        self.images["water"] = water_tile
        
        # 道タイル（砂利道）
        road_tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
        road_tile.fill((220, 200, 170))  # より明るい色
        for i in range(30):  # より多くの砂利
            x = random.randint(2, TILE_SIZE-3)
            y = random.randint(2, TILE_SIZE-3)
            r = random.randint(1, 4)  # より大きな砂利も
            pygame.draw.circle(road_tile, (200, 180, 150), (x, y), r)
        # 道の端を強調
        pygame.draw.line(road_tile, (190, 170, 140), (0, 0), (TILE_SIZE, 0), 2)
        pygame.draw.line(road_tile, (190, 170, 140), (0, TILE_SIZE-1), (TILE_SIZE, TILE_SIZE-1), 2)
        self.images["road"] = road_tile
        
        # ドアタイル（木製ドア）- より目立つデザイン
        door_tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
        door_tile.fill((150, 100, 50))
        # ドアの枠
        pygame.draw.rect(door_tile, (100, 50, 0), (0, 0, TILE_SIZE, TILE_SIZE), 3)
        # ドアのパネル
        pygame.draw.rect(door_tile, (120, 70, 20), (TILE_SIZE//4, TILE_SIZE//8, TILE_SIZE//2, TILE_SIZE*3//4), 0)
        # ドアノブ
        pygame.draw.circle(door_tile, (255, 215, 0), (TILE_SIZE*3//4, TILE_SIZE//2), 4)
        # ドアの装飾
        pygame.draw.rect(door_tile, (80, 40, 0), (TILE_SIZE//4, TILE_SIZE//8, TILE_SIZE//2, TILE_SIZE*3//4), 1)
        pygame.draw.rect(door_tile, (80, 40, 0), (TILE_SIZE//4, TILE_SIZE//2, TILE_SIZE//2, 1), 2)
        # 入口感を強調する光の効果
        for i in range(3):
            pygame.draw.rect(door_tile, (200+i*15, 150+i*15, 100+i*15), 
                           (TILE_SIZE//4+i, TILE_SIZE//8+i, TILE_SIZE//2-i*2, TILE_SIZE*3//4-i*2), 1)
        self.images["door"] = door_tile
        
        # NPCタイル（より人間らしい形）
        npc_tile = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        # 頭
        pygame.draw.circle(npc_tile, (255, 220, 180), (TILE_SIZE//2, TILE_SIZE//4), TILE_SIZE//6)
        # 体
        pygame.draw.rect(npc_tile, (0, 150, 0), 
                        (TILE_SIZE//3, TILE_SIZE//3, TILE_SIZE//3, TILE_SIZE//2))
        self.images["npc"] = npc_tile
        
        # ポータルタイル（魔法陣風）
        portal_tile = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        # 外側の円
        pygame.draw.circle(portal_tile, (200, 0, 200), (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//2 - 2, 2)
        # 内側の円
        pygame.draw.circle(portal_tile, (220, 100, 220), (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//3, 2)
        # 中心の円
        pygame.draw.circle(portal_tile, (240, 200, 240), (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//6)
        # 魔法陣の模様（線）
        for i in range(8):
            angle = i * math.pi / 4
            x1 = TILE_SIZE//2 + int(math.cos(angle) * TILE_SIZE//4)
            y1 = TILE_SIZE//2 + int(math.sin(angle) * TILE_SIZE//4)
            x2 = TILE_SIZE//2 + int(math.cos(angle + math.pi) * TILE_SIZE//4)
            y2 = TILE_SIZE//2 + int(math.sin(angle + math.pi) * TILE_SIZE//4)
            pygame.draw.line(portal_tile, (240, 200, 240), (x1, y1), (x2, y2), 1)
        # 光るエフェクト
        glow = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        for radius in range(TILE_SIZE//2, 0, -5):
            alpha = 100 - radius * 2
            if alpha > 0:
                pygame.draw.circle(glow, (255, 200, 255, alpha), (TILE_SIZE//2, TILE_SIZE//2), radius)
        portal_tile.blit(glow, (0, 0))
        
        # 町のアイコンを追加（より目立つように）
        town_icon = pygame.Surface((TILE_SIZE//2, TILE_SIZE//2), pygame.SRCALPHA)
        # 建物の形（小さな家）
        pygame.draw.rect(town_icon, (255, 255, 255), (2, 8, 16, 12))
        # 屋根
        pygame.draw.polygon(town_icon, (255, 100, 100), [(0, 8), (10, 0), (20, 8)])
        # ドア
        pygame.draw.rect(town_icon, (150, 100, 50), (8, 14, 4, 6))
        # 窓
        pygame.draw.rect(town_icon, (200, 200, 255), (4, 10, 3, 3))
        pygame.draw.rect(town_icon, (200, 200, 255), (13, 10, 3, 3))
        
        # ポータルタイルに町アイコンを合成
        portal_tile.blit(town_icon, (TILE_SIZE//4, TILE_SIZE//4))
        
        self.images["portal"] = portal_tile
        
        # 町のオブジェクト追加
        # 1. 噴水
        fountain = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        # 噴水の基部
        pygame.draw.circle(fountain, (180, 180, 200), (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//3)
        # 噴水の水
        pygame.draw.circle(fountain, (100, 150, 255), (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//4)
        # 噴水の中央部分
        pygame.draw.circle(fountain, (180, 180, 200), (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//8)
        # 水しぶき
        for i in range(8):
            angle = i * math.pi / 4
            length = random.randint(5, 10)
            x = TILE_SIZE//2 + int(math.cos(angle) * length)
            y = TILE_SIZE//2 + int(math.sin(angle) * length) - 5  # 少し上向きに
            pygame.draw.line(fountain, (200, 230, 255), (TILE_SIZE//2, TILE_SIZE//2 - 5), (x, y), 2)
        self.images["fountain"] = fountain
        
        # 2. ベンチ
        bench = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        # ベンチの座面
        pygame.draw.rect(bench, (120, 80, 40), (5, TILE_SIZE//2, TILE_SIZE-10, 5))
        # ベンチの脚
        pygame.draw.rect(bench, (100, 70, 30), (8, TILE_SIZE//2+5, 4, 10))
        pygame.draw.rect(bench, (100, 70, 30), (TILE_SIZE-12, TILE_SIZE//2+5, 4, 10))
        # ベンチの背もたれ
        for i in range(3):
            pygame.draw.rect(bench, (120, 80, 40), (10+i*8, TILE_SIZE//2-10, 3, 10))
        self.images["bench"] = bench
        
        # 3. 街灯
        lamp = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        # 街灯の柱
        pygame.draw.rect(lamp, (60, 60, 60), (TILE_SIZE//2-2, TILE_SIZE//3, 4, TILE_SIZE*2//3))
        # 街灯の頭
        pygame.draw.circle(lamp, (255, 240, 150), (TILE_SIZE//2, TILE_SIZE//3), 8)
        # 光の効果
        glow = pygame.Surface((20, 20), pygame.SRCALPHA)
        for r in range(10, 0, -2):
            alpha = 150 - r * 15
            if alpha > 0:
                pygame.draw.circle(glow, (255, 255, 200, alpha), (10, 10), r)
        lamp.blit(glow, (TILE_SIZE//2-10, TILE_SIZE//3-10))
        self.images["lamp"] = lamp
        
        # 4. 看板
        sign = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        # 看板の柱
        pygame.draw.rect(sign, (100, 70, 40), (TILE_SIZE//2-2, TILE_SIZE//2, 4, TILE_SIZE//2))
        # 看板本体
        pygame.draw.rect(sign, (120, 80, 40), (TILE_SIZE//4, TILE_SIZE//4, TILE_SIZE//2, TILE_SIZE//4))
        # 看板の文字（線で表現）
        pygame.draw.line(sign, (60, 40, 20), (TILE_SIZE//4+5, TILE_SIZE//4+5), (TILE_SIZE*3//4-5, TILE_SIZE//4+5), 2)
        pygame.draw.line(sign, (60, 40, 20), (TILE_SIZE//4+5, TILE_SIZE//4+10), (TILE_SIZE*3//4-5, TILE_SIZE//4+10), 2)
        pygame.draw.line(sign, (60, 40, 20), (TILE_SIZE//4+5, TILE_SIZE//4+15), (TILE_SIZE*3//4-5, TILE_SIZE//4+15), 2)
        self.images["sign"] = sign
        
        # 5. 花壇
        flowerbed = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        # 土の部分
        pygame.draw.rect(flowerbed, (139, 69, 19), (5, 5, TILE_SIZE-10, TILE_SIZE-10))
        # 花々（ランダムな色と位置）
        flower_colors = [(255, 0, 0), (255, 255, 0), (255, 165, 0), (255, 192, 203), (255, 0, 255)]
        for _ in range(15):
            x = random.randint(8, TILE_SIZE-8)
            y = random.randint(8, TILE_SIZE-8)
            color = random.choice(flower_colors)
            pygame.draw.circle(flowerbed, color, (x, y), 3)
            # 茎
            pygame.draw.line(flowerbed, (0, 100, 0), (x, y+3), (x, y+6), 1)
        self.images["flowerbed"] = flowerbed
        
        # 敵キャラクター（より詳細なデザイン）
        enemy_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        # 本体（三角形）
        pygame.draw.polygon(enemy_surface, (200, 50, 50), 
                          [(TILE_SIZE//2, 5), (TILE_SIZE-5, TILE_SIZE-5), (5, TILE_SIZE-5)])
        # 目
        pygame.draw.circle(enemy_surface, (255, 255, 255), (TILE_SIZE//3, TILE_SIZE//2), 5)
        pygame.draw.circle(enemy_surface, (255, 255, 255), (TILE_SIZE*2//3, TILE_SIZE//2), 5)
        pygame.draw.circle(enemy_surface, (0, 0, 0), (TILE_SIZE//3, TILE_SIZE//2), 2)
        pygame.draw.circle(enemy_surface, (0, 0, 0), (TILE_SIZE*2//3, TILE_SIZE//2), 2)
        # 口
        pygame.draw.arc(enemy_surface, (0, 0, 0), (TILE_SIZE//4, TILE_SIZE*2//3, TILE_SIZE//2, TILE_SIZE//4), 0, math.pi, 2)
        self.images["enemy"] = enemy_surface
        
        # ボスキャラクター（より大きく、詳細なデザイン）
        boss_surface = pygame.Surface((TILE_SIZE*2, TILE_SIZE*2), pygame.SRCALPHA)
        # 本体（大きな三角形）
        pygame.draw.polygon(boss_surface, (150, 0, 0), 
                          [(TILE_SIZE, 10), (TILE_SIZE*2-10, TILE_SIZE*2-10), (10, TILE_SIZE*2-10)])
        # 目
        pygame.draw.circle(boss_surface, (255, 255, 255), (TILE_SIZE//2 + 10, TILE_SIZE), 10)
        pygame.draw.circle(boss_surface, (255, 255, 255), (TILE_SIZE*3//2 - 10, TILE_SIZE), 10)
        pygame.draw.circle(boss_surface, (0, 0, 0), (TILE_SIZE//2 + 10, TILE_SIZE), 5)
        pygame.draw.circle(boss_surface, (0, 0, 0), (TILE_SIZE*3//2 - 10, TILE_SIZE), 5)
        # 口
        pygame.draw.arc(boss_surface, (0, 0, 0), (TILE_SIZE//2, TILE_SIZE*3//2, TILE_SIZE, TILE_SIZE//3), 0, math.pi, 3)
        # 角
        pygame.draw.polygon(boss_surface, (100, 0, 0), 
                          [(TILE_SIZE//2, 20), (TILE_SIZE//2 + 15, 5), (TILE_SIZE//2 + 30, 20)])
        pygame.draw.polygon(boss_surface, (100, 0, 0), 
                          [(TILE_SIZE*3//2 - 30, 20), (TILE_SIZE*3//2 - 15, 5), (TILE_SIZE*3//2, 20)])
        self.images["boss"] = boss_surface
        
        # AWSサービスキャラクター
        # EC2
        ec2_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        # 背景（オレンジ色の四角）
        pygame.draw.rect(ec2_surface, (255, 153, 0), (5, 5, TILE_SIZE-10, TILE_SIZE-10))
        pygame.draw.rect(ec2_surface, BLACK, (5, 5, TILE_SIZE-10, TILE_SIZE-10), 2)
        # EC2のロゴ風デザイン（サーバーアイコン）
        pygame.draw.rect(ec2_surface, (255, 255, 255), (10, 12, TILE_SIZE-20, TILE_SIZE-24))
        pygame.draw.rect(ec2_surface, (255, 153, 0), (10, 12, TILE_SIZE-20, 5))
        # サーバーのディテール
        for i in range(3):
            pygame.draw.line(ec2_surface, (200, 200, 200), 
                           (15, 22 + i*8), (TILE_SIZE-15, 22 + i*8), 1)
        self.images["ec2"] = ec2_surface
        
        # S3
        s3_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        # 背景（緑色の四角）
        pygame.draw.rect(s3_surface, (0, 153, 102), (5, 5, TILE_SIZE-10, TILE_SIZE-10))
        pygame.draw.rect(s3_surface, BLACK, (5, 5, TILE_SIZE-10, TILE_SIZE-10), 2)
        # S3のロゴ風デザイン（バケットアイコン）
        pygame.draw.polygon(s3_surface, (255, 255, 255), 
                          [(15, 15), (TILE_SIZE-15, 15), (TILE_SIZE-10, TILE_SIZE-15), (10, TILE_SIZE-15)])
        # バケットのディテール
        pygame.draw.line(s3_surface, (0, 153, 102), (15, 25), (TILE_SIZE-15, 25), 2)
        self.images["s3"] = s3_surface
        
        # Lambda
        lambda_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        # 背景（紫色の四角）
        pygame.draw.rect(lambda_surface, (153, 51, 255), (5, 5, TILE_SIZE-10, TILE_SIZE-10))
        pygame.draw.rect(lambda_surface, BLACK, (5, 5, TILE_SIZE-10, TILE_SIZE-10), 2)
        # Lambdaのロゴ風デザイン（λ文字）
        pygame.draw.line(lambda_surface, (255, 255, 255), (15, TILE_SIZE-15), (TILE_SIZE//2, 15), 3)
        pygame.draw.line(lambda_surface, (255, 255, 255), (TILE_SIZE//2, 15), (TILE_SIZE-15, TILE_SIZE-15), 3)
        self.images["lambda"] = lambda_surface
        
        # DynamoDB
        dynamodb_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        # 背景（青色の四角）
        pygame.draw.rect(dynamodb_surface, (0, 102, 204), (5, 5, TILE_SIZE-10, TILE_SIZE-10))
        pygame.draw.rect(dynamodb_surface, BLACK, (5, 5, TILE_SIZE-10, TILE_SIZE-10), 2)
        # DynamoDBのロゴ風デザイン（テーブルアイコン）
        pygame.draw.rect(dynamodb_surface, (255, 255, 255), (10, 15, TILE_SIZE-20, 5))
        pygame.draw.rect(dynamodb_surface, (255, 255, 255), (10, TILE_SIZE//2-2, TILE_SIZE-20, 4))
        pygame.draw.rect(dynamodb_surface, (255, 255, 255), (10, TILE_SIZE-20, TILE_SIZE-20, 5))
        # 縦線
        pygame.draw.line(dynamodb_surface, (255, 255, 255), (TILE_SIZE//3, 15), (TILE_SIZE//3, TILE_SIZE-15), 2)
        pygame.draw.line(dynamodb_surface, (255, 255, 255), (TILE_SIZE*2//3, 15), (TILE_SIZE*2//3, TILE_SIZE-15), 2)
        self.images["dynamodb"] = dynamodb_surface
        
        # RDS
        rds_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        # 背景（青色の四角）
        pygame.draw.rect(rds_surface, (51, 102, 255), (5, 5, TILE_SIZE-10, TILE_SIZE-10))
        pygame.draw.rect(rds_surface, BLACK, (5, 5, TILE_SIZE-10, TILE_SIZE-10), 2)
        # RDSのロゴ風デザイン（データベースアイコン）
        pygame.draw.ellipse(rds_surface, (255, 255, 255), (10, 10, TILE_SIZE-20, 10))
        pygame.draw.rect(rds_surface, (255, 255, 255), (10, 15, TILE_SIZE-20, TILE_SIZE-25))
        pygame.draw.ellipse(rds_surface, (255, 255, 255), (10, TILE_SIZE-20, TILE_SIZE-20, 10))
        # 線
        pygame.draw.line(rds_surface, (51, 102, 255), (10, TILE_SIZE//3), (TILE_SIZE-10, TILE_SIZE//3), 1)
        pygame.draw.line(rds_surface, (51, 102, 255), (10, TILE_SIZE*2//3), (TILE_SIZE-10, TILE_SIZE*2//3), 1)
        self.images["rds"] = rds_surface
        
        # IAM
        iam_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        # 背景（赤色の四角）
        pygame.draw.rect(iam_surface, (204, 51, 0), (5, 5, TILE_SIZE-10, TILE_SIZE-10))
        pygame.draw.rect(iam_surface, BLACK, (5, 5, TILE_SIZE-10, TILE_SIZE-10), 2)
        # IAMのロゴ風デザイン（ユーザーアイコン）
        # 頭
        pygame.draw.circle(iam_surface, (255, 255, 255), (TILE_SIZE//2, TILE_SIZE//3), TILE_SIZE//6)
        # 体
        pygame.draw.rect(iam_surface, (255, 255, 255), 
                       (TILE_SIZE//2-TILE_SIZE//6, TILE_SIZE//2, TILE_SIZE//3, TILE_SIZE//3))
        # 鍵アイコン
        pygame.draw.circle(iam_surface, (255, 255, 0), (TILE_SIZE*3//4, TILE_SIZE*3//4), TILE_SIZE//10)
        pygame.draw.rect(iam_surface, (255, 255, 0), 
                       (TILE_SIZE*3//4-TILE_SIZE//20, TILE_SIZE*3//4, TILE_SIZE//10, TILE_SIZE//8))
        self.images["iam"] = iam_surface
        
        # CloudFront
        cloudfront_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        # 背景（水色の四角）
        pygame.draw.rect(cloudfront_surface, (0, 153, 204), (5, 5, TILE_SIZE-10, TILE_SIZE-10))
        pygame.draw.rect(cloudfront_surface, BLACK, (5, 5, TILE_SIZE-10, TILE_SIZE-10), 2)
        # CloudFrontのロゴ風デザイン（地球アイコン）
        pygame.draw.circle(cloudfront_surface, (255, 255, 255), (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//3)
        # 経線
        pygame.draw.ellipse(cloudfront_surface, (0, 153, 204), 
                          (TILE_SIZE//2-TILE_SIZE//3, TILE_SIZE//2-TILE_SIZE//6, TILE_SIZE*2//3, TILE_SIZE//3))
        pygame.draw.ellipse(cloudfront_surface, (0, 153, 204), 
                          (TILE_SIZE//2-TILE_SIZE//6, TILE_SIZE//2-TILE_SIZE//3, TILE_SIZE//3, TILE_SIZE*2//3))
        # 矢印
        pygame.draw.line(cloudfront_surface, (255, 255, 0), 
                       (TILE_SIZE//4, TILE_SIZE//4), (TILE_SIZE*3//4, TILE_SIZE*3//4), 2)
        pygame.draw.polygon(cloudfront_surface, (255, 255, 0), 
                          [(TILE_SIZE*3//4, TILE_SIZE*3//4), 
                           (TILE_SIZE*3//4-8, TILE_SIZE*3//4), 
                           (TILE_SIZE*3//4, TILE_SIZE*3//4-8)])
        self.images["cloudfront"] = cloudfront_surface
        
        # ショップアイコン
        shop_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        # 背景（茶色の四角）
        pygame.draw.rect(shop_surface, (153, 102, 51), (5, 5, TILE_SIZE-10, TILE_SIZE-10))
        pygame.draw.rect(shop_surface, BLACK, (5, 5, TILE_SIZE-10, TILE_SIZE-10), 2)
        # ショップのアイコン（コイン）
        pygame.draw.circle(shop_surface, (255, 215, 0), (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//4)
        pygame.draw.circle(shop_surface, (153, 102, 51), (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//6)
        # $マーク
        text = pygame.font.SysFont(None, 24).render("$", True, (255, 255, 255))
        shop_surface.blit(text, (TILE_SIZE//2-text.get_width()//2, TILE_SIZE//2-text.get_height()//2))
        self.images["shop"] = shop_surface
        # 背景（緑色の四角）
        pygame.draw.rect(s3_surface, (0, 153, 102), (5, 5, TILE_SIZE-10, TILE_SIZE-10))
        pygame.draw.rect(s3_surface, BLACK, (5, 5, TILE_SIZE-10, TILE_SIZE-10), 2)
        # S3のロゴ風デザイン（バケットアイコン）
        pygame.draw.polygon(s3_surface, (255, 255, 255), 
                          [(15, 15), (TILE_SIZE-15, 15), (TILE_SIZE-10, TILE_SIZE-15), (10, TILE_SIZE-15)])
        # バケットのディテール
        pygame.draw.line(s3_surface, (0, 153, 102), (15, 25), (TILE_SIZE-15, 25), 2)
        self.images["s3"] = s3_surface
        # 背景（赤茶色の四角）
        pygame.draw.rect(s3_surface, (227, 86, 0), (5, 5, TILE_SIZE-10, TILE_SIZE-10))
        pygame.draw.rect(s3_surface, BLACK, (5, 5, TILE_SIZE-10, TILE_SIZE-10), 2)
        # S3のロゴ風デザイン（バケットアイコン）
        pygame.draw.polygon(s3_surface, (255, 255, 255), 
                          [(15, 15), (TILE_SIZE-15, 15), (TILE_SIZE-10, 30), (10, 30)])
        pygame.draw.rect(s3_surface, (255, 255, 255), (10, 30, TILE_SIZE-20, TILE_SIZE-40))
        self.images["s3"] = s3_surface
        
        # Lambda
        lambda_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        # 背景（紫色の四角）
        pygame.draw.rect(lambda_surface, (147, 47, 194), (5, 5, TILE_SIZE-10, TILE_SIZE-10))
        pygame.draw.rect(lambda_surface, BLACK, (5, 5, TILE_SIZE-10, TILE_SIZE-10), 2)
        # Lambdaのロゴ風デザイン（λ記号）
        points = [(15, 15), (25, 15), (15, 30), (25, 30)]
        pygame.draw.lines(lambda_surface, (255, 255, 255), False, points, 3)
        self.images["lambda"] = lambda_surface
        
        # DynamoDB
        dynamo_surface = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        # 背景（青色の四角）
        pygame.draw.rect(dynamo_surface, (61, 133, 198), (5, 5, TILE_SIZE-10, TILE_SIZE-10))
        pygame.draw.rect(dynamo_surface, BLACK, (5, 5, TILE_SIZE-10, TILE_SIZE-10), 2)
        # DynamoDBのロゴ風デザイン（データベースアイコン）
        pygame.draw.ellipse(dynamo_surface, (255, 255, 255), (10, 10, TILE_SIZE-20, 8))
        pygame.draw.rect(dynamo_surface, (255, 255, 255), (10, 14, TILE_SIZE-20, TILE_SIZE-24))
        pygame.draw.ellipse(dynamo_surface, (255, 255, 255), (10, TILE_SIZE-14, TILE_SIZE-20, 8))
        self.images["dynamodb"] = dynamo_surface
        
        # UI要素
        # ボタン
        button_surface = pygame.Surface((200, 50))
        # グラデーション効果
        for y in range(50):
            color_value = 100 + int(y * 0.5)
            color = (color_value, color_value + 50, color_value + 100)
            pygame.draw.line(button_surface, color, (0, y), (200, y))
        pygame.draw.rect(button_surface, WHITE, (0, 0, 200, 50), 2)
        self.images["button"] = button_surface
        
        # ホバーボタン
        hover_button = pygame.Surface((200, 50))
        # グラデーション効果（明るめ）
        for y in range(50):
            color_value = 120 + int(y * 0.5)
            color = (color_value, color_value + 50, color_value + 100)
            pygame.draw.line(hover_button, color, (0, y), (200, y))
        pygame.draw.rect(hover_button, WHITE, (0, 0, 200, 50), 2)
        self.images["hover_button"] = hover_button
        
        # ダイアログボックス
        dialog_box = pygame.Surface((700, 150), pygame.SRCALPHA)
        # 半透明の背景
        dialog_box.fill((50, 50, 50, 220))
        # 枠線（装飾付き）
        pygame.draw.rect(dialog_box, WHITE, (0, 0, 700, 150), 3)
        # 角の装飾
        pygame.draw.line(dialog_box, WHITE, (10, 0), (10, 10), 2)
        pygame.draw.line(dialog_box, WHITE, (0, 10), (10, 10), 2)
        pygame.draw.line(dialog_box, WHITE, (690, 0), (690, 10), 2)
        pygame.draw.line(dialog_box, WHITE, (690, 10), (700, 10), 2)
        pygame.draw.line(dialog_box, WHITE, (10, 150), (10, 140), 2)
        pygame.draw.line(dialog_box, WHITE, (0, 140), (10, 140), 2)
        pygame.draw.line(dialog_box, WHITE, (690, 150), (690, 140), 2)
        pygame.draw.line(dialog_box, WHITE, (690, 140), (700, 140), 2)
        self.images["dialog_box"] = dialog_box
        
        # メニューパネル
        menu_panel = pygame.Surface((250, 400), pygame.SRCALPHA)
        # 半透明の背景
        menu_panel.fill((50, 50, 80, 220))
        # 枠線
        pygame.draw.rect(menu_panel, WHITE, (0, 0, 250, 400), 2)
        # 装飾ライン
        pygame.draw.line(menu_panel, (100, 100, 200), (10, 30), (240, 30), 2)
        pygame.draw.line(menu_panel, (100, 100, 200), (10, 370), (240, 370), 2)
        self.images["menu_panel"] = menu_panel
        
        # HPバー
        hp_bar_bg = pygame.Surface((100, 15))
        hp_bar_bg.fill((100, 100, 100))
        self.images["hp_bar_bg"] = hp_bar_bg
        
        hp_bar = pygame.Surface((100, 15))
        hp_bar.fill((255, 0, 0))
        self.images["hp_bar"] = hp_bar
        
        # MPバー
        mp_bar_bg = pygame.Surface((100, 15))
        mp_bar_bg.fill((100, 100, 100))
        self.images["mp_bar_bg"] = mp_bar_bg
        
        mp_bar = pygame.Surface((100, 15))
        mp_bar.fill((0, 0, 255))
        self.images["mp_bar"] = mp_bar
        
        # EXPバー
        exp_bar_bg = pygame.Surface((200, 10))
        exp_bar_bg.fill((100, 100, 100))
        self.images["exp_bar_bg"] = exp_bar_bg
        
        exp_bar = pygame.Surface((200, 10))
        exp_bar.fill((0, 255, 0))
        self.images["exp_bar"] = exp_bar
        
    def get_image(self, name):
        """名前で画像を取得"""
        image = self.images.get(name)
        if image is None:
            # 画像が見つからない場合は、タイルタイプに応じた代替画像を返す
            default_image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            
            # 名前に基づいて適切な代替画像を作成
            if "mountain" in name:
                # 山の代替表現
                default_image.fill((150, 140, 130))
                pygame.draw.polygon(default_image, (180, 170, 160), 
                                  [(TILE_SIZE//2, 5), (TILE_SIZE-5, TILE_SIZE-5), (5, TILE_SIZE-5)])
                pygame.draw.polygon(default_image, (220, 220, 220), 
                                  [(TILE_SIZE//2, 5), (TILE_SIZE//2+5, 10), (TILE_SIZE//2-5, 10)])
            elif "forest" in name:
                # 森の代替表現
                default_image.fill((100, 180, 100))
                for i in range(3):
                    x = 10 + i * 10
                    pygame.draw.rect(default_image, (100, 70, 40), (x, 20, 4, 15))
                    pygame.draw.circle(default_image, (50, 120, 50), (x+2, 15), 7)
            elif "water" in name:
                # 水の代替表現
                default_image.fill((70, 130, 230))
                for i in range(3):
                    pygame.draw.line(default_image, (120, 180, 255), 
                                   (0, 10 + i*10), (TILE_SIZE, 15 + i*10), 2)
            elif "sand" in name:
                # 砂の代替表現
                default_image.fill((230, 210, 160))
                for i in range(10):
                    x = random.randint(5, TILE_SIZE-5)
                    y = random.randint(5, TILE_SIZE-5)
                    pygame.draw.circle(default_image, (210, 190, 140), (x, y), 2)
            elif "road" in name:
                # 道の代替表現
                default_image.fill((200, 190, 170))
                pygame.draw.line(default_image, (180, 170, 150), (0, 0), (TILE_SIZE, 0), 2)
                pygame.draw.line(default_image, (180, 170, 150), (0, TILE_SIZE-1), (TILE_SIZE, TILE_SIZE-1), 2)
            elif "wall" in name:
                # 壁の代替表現
                default_image.fill((150, 120, 100))
                for y in range(0, TILE_SIZE, 8):
                    for x in range(0, TILE_SIZE, 16):
                        offset = 8 if y % 16 == 0 else 0
                        pygame.draw.rect(default_image, (130, 100, 80), 
                                       (x + offset, y, 8, 8))
            elif "floor" in name:
                # 床の代替表現
                default_image.fill((220, 220, 220))
                for y in range(0, TILE_SIZE, 10):
                    for x in range(0, TILE_SIZE, 10):
                        if (x + y) % 20 == 0:
                            pygame.draw.rect(default_image, (200, 200, 200), 
                                           (x, y, 10, 10))
            elif "portal" in name:
                # ポータルの代替表現
                default_image.fill((50, 50, 50))
                pygame.draw.circle(default_image, (200, 100, 200), 
                                 (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//3)
                pygame.draw.circle(default_image, (50, 50, 50), 
                                 (TILE_SIZE//2, TILE_SIZE//2), TILE_SIZE//6)
            else:
                # その他の未知のタイル - 識別できるパターン
                default_image.fill((200, 200, 200))  # 灰色の背景
                # 疑問符を描画
                font = pygame.font.SysFont(None, 30)
                text = font.render("?", True, (0, 0, 0))
                default_image.blit(text, (TILE_SIZE//2 - text.get_width()//2, 
                                        TILE_SIZE//2 - text.get_height()//2))
                pygame.draw.rect(default_image, (100, 100, 100), (0, 0, TILE_SIZE, TILE_SIZE), 2)
                
            return default_image
        return image
        
    def get_font(self, size="normal"):
        """サイズでフォントを取得"""
        return self.fonts.get(size)
        
    def render_text(self, text, font_size="normal", color=WHITE):
        """テキストをレンダリング"""
        font = self.get_font(font_size)
        return font.render(text, True, color)
        # 山タイル
        mountain_tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
        # 山の背景色
        mountain_tile.fill((100, 90, 80))
        # 山の形状
        mountain_points = [
            (TILE_SIZE//2, 5),  # 頂点
            (TILE_SIZE-5, TILE_SIZE-5),  # 右下
            (5, TILE_SIZE-5)  # 左下
        ]
        pygame.draw.polygon(mountain_tile, (150, 140, 130), mountain_points)
        # 雪冠
        snow_points = [
            (TILE_SIZE//2, 5),  # 頂点
            (TILE_SIZE//2 + 8, 12),
            (TILE_SIZE//2 - 8, 12)
        ]
        pygame.draw.polygon(mountain_tile, (240, 240, 250), snow_points)
        # 山の陰影
        pygame.draw.line(mountain_tile, (80, 70, 60), (TILE_SIZE//2, 5), (5, TILE_SIZE-5), 2)
        self.images["mountain"] = mountain_tile
        
        # 森タイル
        forest_tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
        forest_tile.fill((100, 180, 100))  # 森の背景
        
        # 複数の木を描画
        tree_positions = [(10, 10), (25, 8), (15, 25), (30, 20)]
        for tx, ty in tree_positions:
            # 木の幹
            pygame.draw.rect(forest_tile, (100, 70, 40), (tx, ty+10, 5, 10))
            # 木の葉
            pygame.draw.circle(forest_tile, (50, 120, 50), (tx+2, ty+5), 8)
            pygame.draw.circle(forest_tile, (70, 140, 70), (tx+7, ty+7), 6)
        
        self.images["forest"] = forest_tile
        
        # 砂タイル
        sand_tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
        sand_tile.fill((230, 210, 160))  # 砂の基本色
        
        # 砂の質感を追加
        for _ in range(40):
            x = random.randint(0, TILE_SIZE-1)
            y = random.randint(0, TILE_SIZE-1)
            r = random.randint(1, 2)
            color_var = random.randint(-20, 20)
            color = (230 + color_var, 210 + color_var, 160 + color_var)
            pygame.draw.circle(sand_tile, color, (x, y), r)
            
        self.images["sand"] = sand_tile
        # 山タイル
        mountain_tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
        # 山の背景色
        mountain_tile.fill((100, 90, 80))
        # 山の形状
        mountain_points = [
            (TILE_SIZE//2, 5),  # 頂点
            (TILE_SIZE-5, TILE_SIZE-5),  # 右下
            (5, TILE_SIZE-5)  # 左下
        ]
        pygame.draw.polygon(mountain_tile, (150, 140, 130), mountain_points)
        # 雪冠
        snow_points = [
            (TILE_SIZE//2, 5),  # 頂点
            (TILE_SIZE//2 + 8, 12),
            (TILE_SIZE//2 - 8, 12)
        ]
        pygame.draw.polygon(mountain_tile, (240, 240, 250), snow_points)
        # 山の陰影
        pygame.draw.line(mountain_tile, (80, 70, 60), (TILE_SIZE//2, 5), (5, TILE_SIZE-5), 2)
        self.images["mountain"] = mountain_tile
        
        # 森タイル
        forest_tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
        forest_tile.fill((100, 180, 100))  # 森の背景
        
        # 複数の木を描画
        tree_positions = [(10, 10), (25, 8), (15, 25), (30, 20)]
        for tx, ty in tree_positions:
            # 木の幹
            pygame.draw.rect(forest_tile, (100, 70, 40), (tx, ty+10, 5, 10))
            # 木の葉
            pygame.draw.circle(forest_tile, (50, 120, 50), (tx+2, ty+5), 8)
            pygame.draw.circle(forest_tile, (70, 140, 70), (tx+7, ty+7), 6)
        
        self.images["forest"] = forest_tile
        
        # 砂タイル
        sand_tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
        sand_tile.fill((230, 210, 160))  # 砂の基本色
        
        # 砂の質感を追加
        for _ in range(40):
            x = random.randint(0, TILE_SIZE-1)
            y = random.randint(0, TILE_SIZE-1)
            r = random.randint(1, 2)
            color_var = random.randint(-20, 20)
            color = (230 + color_var, 210 + color_var, 160 + color_var)
            pygame.draw.circle(sand_tile, color, (x, y), r)
            
        self.images["sand"] = sand_tile

        # ドアタイル（より詳細なドア）
        door_tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
        door_tile.fill((120, 80, 40))  # 茶色の背景
        # ドアの枠
        pygame.draw.rect(door_tile, (80, 50, 20), (2, 2, TILE_SIZE-4, TILE_SIZE-4), 2)
        # ドアノブ
        pygame.draw.circle(door_tile, (200, 200, 0), (TILE_SIZE-10, TILE_SIZE//2), 3)
        # ドアの装飾（木目調）
        for i in range(3):
            pygame.draw.line(door_tile, (80, 50, 20), 
                           (TILE_SIZE//4, 5 + i*10), (TILE_SIZE//4, 15 + i*10), 2)
            pygame.draw.line(door_tile, (80, 50, 20), 
                           (TILE_SIZE*3//4, 5 + i*10), (TILE_SIZE*3//4, 15 + i*10), 2)
        self.images["door"] = door_tile
