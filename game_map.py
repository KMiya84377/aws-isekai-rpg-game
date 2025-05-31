#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import math
from fixed_maps import get_world_map, get_computing_town_map, get_storage_town_map, get_database_town_map, get_security_town_map

# タイルタイプ
TILE_EMPTY = 0
TILE_FLOOR = 1
TILE_WALL = 2
TILE_GRASS = 3
TILE_WATER = 4
TILE_ROAD = 5
TILE_DOOR = 6
TILE_NPC = 7
TILE_PORTAL = 8
TILE_SHOP = 9
TILE_MOUNTAIN = 10
TILE_FOREST = 11
TILE_SAND = 12
TILE_FOUNTAIN = 13
TILE_BENCH = 14
TILE_LAMP = 15
TILE_SIGN = 16
TILE_FLOWERBED = 17

# マップタイプ
MAP_WORLD = 0
MAP_TOWN = 1
MAP_DUNGEON = 2

class GameMap:
    def __init__(self, name, width, height, map_type=MAP_WORLD):
        self.name = name
        self.width = width
        self.height = height
        self.map_type = map_type
        self.tiles = [[TILE_EMPTY for _ in range(width)] for _ in range(height)]
        self.npcs = []
        self.portals = []
        self.enemies = []
        self.shops = []
        self.encounter_rate = 0.05  # エンカウント率（マップタイプによって変更）
        
        # マップタイプに応じた初期化
        if map_type == MAP_WORLD:
            self.generate_world_map()
            self.encounter_rate = 0.03
        elif map_type == MAP_TOWN:
            self.generate_town_map()
            self.encounter_rate = 0.0  # 町ではエンカウントなし
        elif map_type == MAP_DUNGEON:
            self.generate_dungeon_map()
            self.encounter_rate = 0.08  # ダンジョンではエンカウント率高め
            
    @classmethod
    def from_map_data(cls, map_data):
        """マップデータからGameMapオブジェクトを作成"""
        game_map = cls(map_data["name"], map_data["width"], map_data["height"])
        game_map.tiles = map_data["tiles"]
        game_map.portals = map_data["portals"]
        game_map.npcs = map_data["npcs"]
        
        if "encounter_rate" in map_data:
            game_map.encounter_rate = map_data["encounter_rate"]
            
        if "shops" in map_data:
            game_map.shops = map_data["shops"]
        else:
            game_map.shops = []
            
        return game_map
            
    def generate_world_map(self):
        """ワールドマップを生成"""
        # 固定マップデータを使用
        map_data = get_world_map()
        self.tiles = map_data["tiles"]
        self.portals = map_data["portals"]
        self.npcs = map_data["npcs"] if "npcs" in map_data else []
        
    def _add_mountain_range(self, start_x, start_y, length, width):
        """山脈を追加"""
        direction_x = random.choice([-1, 0, 1])
        direction_y = random.choice([-1, 0, 1]) if direction_x == 0 else 0
        
        if direction_x == 0 and direction_y == 0:
            direction_x = 1  # デフォルトは右方向
            
        x, y = start_x, start_y
        for _ in range(length):
            # 山の幅に応じて周囲にも山を配置
            for w in range(-width//2, width//2 + 1):
                for h in range(-width//2, width//2 + 1):
                    nx, ny = x + w, y + h
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        # 距離に応じて山か丘を配置
                        distance = abs(w) + abs(h)
                        if distance <= width // 2:
                            self.tiles[ny][nx] = TILE_MOUNTAIN
            
            # 次の位置へ移動（少しランダム性を持たせる）
            x += direction_x + random.choice([-1, 0, 1])
            y += direction_y + random.choice([-1, 0, 1])
            
            # マップ範囲内に収める
            x = max(0, min(x, self.width - 1))
            y = max(0, min(y, self.height - 1))
            
    def _add_river(self, start_x, start_y, end_x, end_y):
        """川を追加（蛇行する自然な川）"""
        # 川の経路を計算
        points = []
        x, y = start_x, start_y
        target_x, target_y = end_x, end_y
        
        # 始点と終点を追加
        points.append((x, y))
        
        # 中間点を生成（蛇行効果）
        steps = max(abs(end_x - start_x), abs(end_y - start_y))
        if steps == 0:
            return
            
        for i in range(1, steps):
            progress = i / steps
            # 直線補間
            line_x = start_x + (end_x - start_x) * progress
            line_y = start_y + (end_y - start_y) * progress
            
            # 蛇行効果（サイン波）
            amplitude = min(10, steps / 5)  # 蛇行の振幅
            frequency = 2 * math.pi / steps * 3  # 蛇行の頻度
            
            # 進行方向に垂直な方向に蛇行
            if abs(end_x - start_x) > abs(end_y - start_y):
                # 主に水平方向の川
                offset = math.sin(progress * frequency * steps) * amplitude
                river_x = int(line_x)
                river_y = int(line_y + offset)
            else:
                # 主に垂直方向の川
                offset = math.sin(progress * frequency * steps) * amplitude
                river_x = int(line_x + offset)
                river_y = int(line_y)
                
            # マップ範囲内に収める
            river_x = max(0, min(river_x, self.width - 1))
            river_y = max(0, min(river_y, self.height - 1))
            
            points.append((river_x, river_y))
        
        # 終点を追加
        points.append((target_x, target_y))
        
        # 川を描画
        for x, y in points:
            if 0 <= x < self.width and 0 <= y < self.height:
                self.tiles[y][x] = TILE_WATER
                
                # 川幅を広げる（周囲も水にする）
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height:
                            # 確率で水タイルにする（自然な川岸）
                            if random.random() < 0.7:
                                self.tiles[ny][nx] = TILE_WATER
                                
    def _add_forest_area(self, start_x, start_y, width, height):
        """森林地帯を追加"""
        for y in range(start_y, min(start_y + height, self.height)):
            for x in range(start_x, min(start_x + width, self.width)):
                # ランダムに森を配置
                if random.random() < 0.7:  # 70%の確率で森
                    self.tiles[y][x] = TILE_FOREST
                            
    def generate_town_map(self):
        """町マップを生成"""
        # 外周を壁にする
        for x in range(self.width):
            self.tiles[0][x] = TILE_WALL
            self.tiles[self.height-1][x] = TILE_WALL
        for y in range(self.height):
            self.tiles[y][0] = TILE_WALL
            self.tiles[y][self.width-1] = TILE_WALL
            
        # 内側を床にする
        for y in range(1, self.height-1):
            for x in range(1, self.width-1):
                self.tiles[y][x] = TILE_FLOOR
                
        # 町の種類に応じたカスタマイズ
        if "Computing" in self.name:
            # Computing Town - サーバーラック風の建物と格子状の道路
            self._create_computing_town()
        elif "Storage" in self.name:
            # Storage Town - 倉庫風の大きな建物と放射状の道路
            self._create_storage_town()
        elif "Database" in self.name:
            # Database Town - テーブル風の建物と円形の道路
            self._create_database_town()
        elif "Security" in self.name:
            # Security Town - 要塞風の建物と同心円状の道路
            self._create_security_town()
        else:
            # デフォルト - 通常の町
            self._create_town_roads()
            
            # 建物を配置
            building_positions = [
                (3, 3, 5, 5),      # ショップ
                (12, 3, 5, 5),     # 宿屋
                (21, 3, 5, 5),     # クイズハウス
                (3, 12, 6, 4),     # 住宅1
                (12, 12, 4, 6),    # 住宅2
                (21, 12, 5, 5),    # 住宅3
                (3, 18, 7, 3),     # 倉庫
                (15, 18, 8, 3)     # 図書館
            ]
            
            for x, y, w, h in building_positions:
                if x + w < self.width and y + h < self.height:
                    self.place_building(x, y, w, h)
        
        # NPCを配置（町の種類に応じて）
        self._place_town_npcs()
        
        # 出口ポータルを配置
        self.add_portal(self.width//2, self.height-2, "AWS Cloud World", 15, 15)
        
    def _create_computing_town(self):
        """Computing Town専用のマップ生成"""
        # 基本的な床タイル
        for y in range(1, self.height-1):
            for x in range(1, self.width-1):
                self.tiles[y][x] = TILE_FLOOR
        
        # 不規則な道路パターン（サーバールーム風）
        for x in range(3, self.width-3, 6):
            for y in range(1, self.height-1):
                # 道の幅をランダムに変える
                width = random.randint(1, 2)
                for w in range(width):
                    if x+w < self.width-1:
                        self.tiles[y][x+w] = TILE_ROAD
        
        for y in range(3, self.height-3, 6):
            for x in range(1, self.width-1):
                # 道の幅をランダムに変える
                width = random.randint(1, 2)
                for w in range(width):
                    if y+w < self.height-1:
                        self.tiles[y+w][x] = TILE_ROAD
        
        # サーバーラック風の建物（不規則に配置）
        rack_positions = []
        for i in range(5):
            for j in range(4):
                # 位置をランダムに少しずらす
                offset_x = random.randint(-1, 1)
                offset_y = random.randint(-1, 1)
                x = 4 + i * 6 + offset_x
                y = 4 + j * 6 + offset_y
                
                # 既存のラックと重ならないように
                valid = True
                for rx, ry in rack_positions:
                    if abs(rx - x) < 4 and abs(ry - y) < 4:
                        valid = False
                        break
                
                if valid and x > 2 and y > 2 and x < self.width-5 and y < self.height-5:
                    rack_positions.append((x, y))
                    
                    # ラックのサイズをランダムに
                    width = random.randint(2, 4)
                    height = random.randint(3, 5)
                    
                    # 建物を配置
                    for bx in range(x, min(x+width, self.width-2)):
                        for by in range(y, min(y+height, self.height-2)):
                            if bx == x or bx == min(x+width-1, self.width-3) or by == y or by == min(y+height-1, self.height-3):
                                self.tiles[by][bx] = TILE_WALL
                            else:
                                self.tiles[by][bx] = TILE_FLOOR
        
        # 中央に大きなデータセンター
        center_x = self.width // 2
        center_y = self.height // 2
        center_width = random.randint(6, 8)
        center_height = random.randint(6, 8)
        
        # 中央のデータセンターを配置
        for x in range(center_x-center_width//2, center_x+center_width//2):
            for y in range(center_y-center_height//2, center_y+center_height//2):
                if 0 <= x < self.width and 0 <= y < self.height:
                    if x == center_x-center_width//2 or x == center_x+center_width//2-1 or y == center_y-center_height//2 or y == center_y+center_height//2-1:
                        self.tiles[y][x] = TILE_WALL
                    else:
                        self.tiles[y][x] = TILE_FLOOR
        
    def _create_storage_town(self):
        """Storage Town専用のマップ生成"""
        # 基本的な床タイル
        for y in range(1, self.height-1):
            for x in range(1, self.width-1):
                self.tiles[y][x] = TILE_FLOOR
        
        # 放射状の道路（より自然な曲線）
        center_x = self.width // 2
        center_y = self.height // 2
        
        # 主要な道路（中心から放射状）
        num_roads = random.randint(5, 8)
        for i in range(num_roads):
            angle = i * (2 * math.pi / num_roads)
            length = min(self.width, self.height) // 2 - 2
            
            # 道路の曲がり具合
            curve = random.uniform(-0.3, 0.3)
            
            # 道路を描画
            for dist in range(1, length):
                # 曲線を加える
                curved_angle = angle + curve * math.sin(dist / length * math.pi)
                x = center_x + int(dist * math.cos(curved_angle))
                y = center_y + int(dist * math.sin(curved_angle))
                
                if 1 <= x < self.width-1 and 1 <= y < self.height-1:
                    self.tiles[y][x] = TILE_ROAD
                    
                    # 道の幅を広げる（ランダムに）
                    if random.random() < 0.3:
                        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                            nx, ny = x + dx, y + dy
                            if 1 <= nx < self.width-1 and 1 <= ny < self.height-1:
                                self.tiles[ny][nx] = TILE_ROAD
        
        # 同心円状の道路
        for radius in range(5, min(self.width, self.height)//2-2, 5):
            # 円の不規則さ
            irregularity = random.uniform(0.7, 1.3)
            
            # 円を描画
            for angle in range(0, 360, 5):
                rad = math.radians(angle)
                # 不規則な円
                r = radius * (1 + irregularity * 0.1 * math.sin(3 * rad))
                x = center_x + int(r * math.cos(rad))
                y = center_y + int(r * math.sin(rad))
                
                if 1 <= x < self.width-1 and 1 <= y < self.height-1:
                    self.tiles[y][x] = TILE_ROAD
        
        # 倉庫風の建物（不規則に配置）
        warehouse_positions = []
        
        # 大きな倉庫を配置
        for _ in range(8):
            # ランダムな位置
            x = random.randint(3, self.width-10)
            y = random.randint(3, self.height-10)
            
            # 既存の倉庫と重ならないように
            valid = True
            for wx, wy in warehouse_positions:
                if abs(wx - x) < 10 and abs(wy - y) < 10:
                    valid = False
                    break
            
            if valid:
                warehouse_positions.append((x, y))
                
                # 倉庫のサイズをランダムに
                width = random.randint(5, 9)
                height = random.randint(4, 8)
                
                # 倉庫を配置
                for bx in range(x, min(x+width, self.width-2)):
                    for by in range(y, min(y+height, self.height-2)):
                        if bx == x or bx == min(x+width-1, self.width-3) or by == y or by == min(y+height-1, self.height-3):
                            self.tiles[by][bx] = TILE_WALL
                        else:
                            self.tiles[by][bx] = TILE_FLOOR
                
                # ドアを配置
                door_x = x + width // 2
                door_y = y + height - 1
                if 0 <= door_x < self.width and 0 <= door_y < self.height:
                    self.tiles[door_y][door_x] = TILE_DOOR
        for i in range(1, min(self.width, self.height) // 2):
            # 右下方向
            x = center_x + i
            y = center_y + i
            if 0 <= x < self.width and 0 <= y < self.height:
                self.tiles[y][x] = TILE_ROAD
                
            # 左下方向
            x = center_x - i
            y = center_y + i
            if 0 <= x < self.width and 0 <= y < self.height:
                self.tiles[y][x] = TILE_ROAD
                
            # 右上方向
            x = center_x + i
            y = center_y - i
            if 0 <= x < self.width and 0 <= y < self.height:
                self.tiles[y][x] = TILE_ROAD
                
            # 左上方向
            x = center_x - i
            y = center_y - i
            if 0 <= x < self.width and 0 <= y < self.height:
                self.tiles[y][x] = TILE_ROAD
                
        # 大きな倉庫風の建物
        self.place_building(5, 5, 8, 8)
        self.place_building(18, 5, 8, 8)
        self.place_building(5, 15, 8, 8)
        self.place_building(18, 15, 8, 8)
        
    def _create_database_town(self):
        """Database Town専用のマップ生成"""
        # 基本的な床タイル
        for y in range(1, self.height-1):
            for x in range(1, self.width-1):
                self.tiles[y][x] = TILE_FLOOR
        
        # テーブル風の建物と有機的な道路パターン
        center_x = self.width // 2
        center_y = self.height // 2
        
        # 有機的な円形の道路（データベースのテーブル関係を表現）
        for i in range(3):
            radius = 5 + i * 5
            center_offset_x = random.randint(-3, 3)
            center_offset_y = random.randint(-3, 3)
            
            # 楕円の比率
            x_ratio = random.uniform(0.8, 1.2)
            y_ratio = random.uniform(0.8, 1.2)
            
            # 円の不規則さ
            irregularity = random.uniform(0.8, 1.2)
            
            # 円を描画
            for angle in range(0, 360, 5):
                rad = math.radians(angle)
                # 不規則な楕円
                r = radius * (1 + 0.1 * math.sin(3 * rad) * irregularity)
                x = center_x + center_offset_x + int(r * x_ratio * math.cos(rad))
                y = center_y + center_offset_y + int(r * y_ratio * math.sin(rad))
                
                if 1 <= x < self.width-1 and 1 <= y < self.height-1:
                    self.tiles[y][x] = TILE_ROAD
        
        # 接続線（テーブル間の関係）
        for _ in range(6):
            start_angle = random.uniform(0, 2 * math.pi)
            end_angle = start_angle + random.uniform(math.pi/2, 3*math.pi/2)
            
            start_radius = random.randint(5, 15)
            end_radius = random.randint(5, 15)
            
            start_x = center_x + int(start_radius * math.cos(start_angle))
            start_y = center_y + int(start_radius * math.sin(start_angle))
            
            end_x = center_x + int(end_radius * math.cos(end_angle))
            end_y = center_y + int(end_radius * math.sin(end_angle))
            
            # ベジェ曲線風の道を描画
            steps = 20
            for i in range(steps + 1):
                t = i / steps
                # 制御点（ベジェ曲線用）
                control_x = center_x + random.randint(-5, 5)
                control_y = center_y + random.randint(-5, 5)
                
                # 二次ベジェ曲線
                x = int((1-t)**2 * start_x + 2*(1-t)*t * control_x + t**2 * end_x)
                y = int((1-t)**2 * start_y + 2*(1-t)*t * control_y + t**2 * end_y)
                
                if 1 <= x < self.width-1 and 1 <= y < self.height-1:
                    self.tiles[y][x] = TILE_ROAD
        
        # テーブル風の建物（不規則に配置）
        table_positions = []
        
        # テーブル（建物）を配置
        for _ in range(10):
            # ランダムな位置
            x = random.randint(3, self.width-8)
            y = random.randint(3, self.height-8)
            
            # 既存のテーブルと重ならないように
            valid = True
            for tx, ty in table_positions:
                if abs(tx - x) < 8 and abs(ty - y) < 8:
                    valid = False
                    break
            
            # 道路の上には配置しない
            if valid:
                for check_y in range(y, y+6):
                    for check_x in range(x, x+6):
                        if 0 <= check_x < self.width and 0 <= check_y < self.height:
                            if self.tiles[check_y][check_x] == TILE_ROAD:
                                valid = False
                                break
            
            if valid:
                table_positions.append((x, y))
                
                # テーブルのサイズをランダムに
                width = random.randint(4, 7)
                height = random.randint(4, 7)
                
                # テーブルを配置
                for bx in range(x, min(x+width, self.width-2)):
                    for by in range(y, min(y+height, self.height-2)):
                        if bx == x or bx == min(x+width-1, self.width-3) or by == y or by == min(y+height-1, self.height-3):
                            self.tiles[by][bx] = TILE_WALL
                        else:
                            self.tiles[by][bx] = TILE_FLOOR
                
                # ドアを配置
                door_x = x + width // 2
                door_y = y + height - 1
                if 0 <= door_x < self.width and 0 <= door_y < self.height:
                    self.tiles[door_y][door_x] = TILE_DOOR
        # 円形の道路
        center_x = self.width // 2
        center_y = self.height // 2
        
        # 同心円状の道路
        for radius in [5, 10]:
            for angle in range(0, 360, 5):
                x = center_x + int(radius * math.cos(math.radians(angle)))
                y = center_y + int(radius * math.sin(math.radians(angle)))
                if 0 <= x < self.width and 0 <= y < self.height:
                    self.tiles[y][x] = TILE_ROAD
                    
        # テーブル風の建物（長方形の建物が並ぶ）
        for i in range(3):
            # 上部
            self.place_building(5 + i*8, 5, 6, 3)
            # 下部
            self.place_building(5 + i*8, 15, 6, 3)
            
        # 中央に大きなデータベースエンジン風の建物
        self.place_building(center_x-3, center_y-3, 6, 6)
        
    def _create_security_town(self):
        """Security Town専用のマップ生成"""
        # 基本的な床タイル
        for y in range(1, self.height-1):
            for x in range(1, self.width-1):
                self.tiles[y][x] = TILE_FLOOR
        
        # 要塞風の建物と同心円状の道路
        center_x = self.width // 2
        center_y = self.height // 2
        
        # 同心円状の道路（セキュリティレイヤーを表現）
        for radius in range(5, min(self.width, self.height)//2-2, 4):
            # 円の不規則さ
            irregularity = random.uniform(0.9, 1.1)
            
            # 円を描画
            for angle in range(0, 360, 5):
                rad = math.radians(angle)
                # 不規則な円
                r = radius * (1 + irregularity * 0.05 * math.sin(4 * rad))
                x = center_x + int(r * math.cos(rad))
                y = center_y + int(r * math.sin(rad))
                
                if 1 <= x < self.width-1 and 1 <= y < self.height-1:
                    self.tiles[y][x] = TILE_ROAD
        
        # 放射状の道路（アクセス経路を表現）
        num_spokes = random.randint(6, 10)
        for i in range(num_spokes):
            angle = i * (2 * math.pi / num_spokes)
            length = min(self.width, self.height) // 2 - 2
            
            # 道路を描画
            for dist in range(1, length):
                x = center_x + int(dist * math.cos(angle))
                y = center_y + int(dist * math.sin(angle))
                
                if 1 <= x < self.width-1 and 1 <= y < self.height-1:
                    self.tiles[y][x] = TILE_ROAD
        
        # 中央の要塞（メインセキュリティセンター）
        fortress_size = random.randint(6, 8)
        for x in range(center_x-fortress_size//2, center_x+fortress_size//2):
            for y in range(center_y-fortress_size//2, center_y+fortress_size//2):
                if 1 <= x < self.width-1 and 1 <= y < self.height-1:
                    if x == center_x-fortress_size//2 or x == center_x+fortress_size//2-1 or y == center_y-fortress_size//2 or y == center_y+fortress_size//2-1:
                        self.tiles[y][x] = TILE_WALL
                    else:
                        self.tiles[y][x] = TILE_FLOOR
        
        # 監視塔（四隅と中間点）
        tower_positions = [
            (5, 5), (5, self.height-6), 
            (self.width-6, 5), (self.width-6, self.height-6),
            (5, self.height//2), (self.width-6, self.height//2),
            (self.width//2, 5), (self.width//2, self.height-6)
        ]
        
        for tx, ty in tower_positions:
            # 塔のサイズをランダムに
            tower_size = random.randint(2, 4)
            
            # 塔を配置
            for x in range(tx, min(tx+tower_size, self.width-1)):
                for y in range(ty, min(ty+tower_size, self.height-1)):
                    if 1 <= x < self.width-1 and 1 <= y < self.height-1:
                        if x == tx or x == min(tx+tower_size-1, self.width-2) or y == ty or y == min(ty+tower_size-1, self.height-2):
                            self.tiles[y][x] = TILE_WALL
                        else:
                            self.tiles[y][x] = TILE_FLOOR
        
        # 小さなセキュリティチェックポイント（ランダムに配置）
        for _ in range(8):
            # ランダムな位置
            x = random.randint(8, self.width-9)
            y = random.randint(8, self.height-9)
            
            # 既存の建物と重ならないように
            valid = True
            for check_y in range(y-3, y+6):
                for check_x in range(x-3, x+6):
                    if 0 <= check_x < self.width and 0 <= check_y < self.height:
                        if self.tiles[check_y][check_x] in [TILE_WALL, TILE_DOOR]:
                            valid = False
                            break
            
            if valid:
                # チェックポイントのサイズ
                width = random.randint(3, 5)
                height = random.randint(3, 5)
                
                # チェックポイントを配置
                for bx in range(x, min(x+width, self.width-2)):
                    for by in range(y, min(y+height, self.height-2)):
                        if bx == x or bx == min(x+width-1, self.width-3) or by == y or by == min(y+height-1, self.height-3):
                            self.tiles[by][bx] = TILE_WALL
                        else:
                            self.tiles[by][bx] = TILE_FLOOR
                
                # ドアを配置
                door_x = x + width // 2
                door_y = y + height - 1
                if 0 <= door_x < self.width and 0 <= door_y < self.height:
                    self.tiles[door_y][door_x] = TILE_DOOR
        # 同心円状の道路と要塞風の建物
        center_x = self.width // 2
        center_y = self.height // 2
        
        # 外周の要塞壁
        for angle in range(0, 360, 5):
            x = center_x + int(12 * math.cos(math.radians(angle)))
            y = center_y + int(12 * math.sin(math.radians(angle)))
            if 0 <= x < self.width and 0 <= y < self.height:
                self.tiles[y][x] = TILE_WALL
                
        # 内側の道路
        for angle in range(0, 360, 5):
            x = center_x + int(8 * math.cos(math.radians(angle)))
            y = center_y + int(8 * math.sin(math.radians(angle)))
            if 0 <= x < self.width and 0 <= y < self.height:
                self.tiles[y][x] = TILE_ROAD
                
        # 中央の要塞
        self.place_building(center_x-4, center_y-4, 8, 8)
        
        # 四隅に小さな監視塔風の建物
        self.place_building(5, 5, 3, 3)
        self.place_building(self.width-8, 5, 3, 3)
        self.place_building(5, self.height-8, 3, 3)
        self.place_building(self.width-8, self.height-8, 3, 3)
        
    def _place_town_npcs(self):
        """町の種類に応じてNPCを配置"""
        if "Computing" in self.name:
            # Computing Town - EC2, Lambda, Elastic Beanstalk
            self.add_npc(15, 10, "EC2", "私はEC2、AWSの仮想サーバーサービスだ。柔軟なコンピューティングリソースが必要なら任せてくれ。")
            self.add_npc(8, 15, "Lambda", "私はLambda、AWSのサーバーレスコンピューティングサービスだ。コードの実行なら私に任せてくれ。")
            self.add_npc(22, 8, "Elastic Beanstalk", "私はElastic Beanstalk、アプリケーションのデプロイと管理を簡単にするサービスだ。")
        elif "Storage" in self.name:
            # Storage Town - S3, EBS, Glacier
            self.add_npc(15, 10, "S3", "私はS3、AWSのオブジェクトストレージサービスだ。データの保存なら私に任せてくれ。")
            self.add_npc(8, 15, "EBS", "私はEBS、EC2インスタンス用の永続ブロックストレージだ。高性能なストレージが必要なら私を使ってくれ。")
            self.add_npc(22, 8, "Glacier", "私はGlacier、長期保存用の低コストストレージだ。アーカイブデータの保存に最適だよ。")
        elif "Database" in self.name:
            # Database Town - DynamoDB, RDS, Aurora
            self.add_npc(15, 10, "DynamoDB", "私はDynamoDB、AWSのNoSQLデータベースサービスだ。スケーラブルなデータ管理が必要なら任せてくれ。")
            self.add_npc(8, 15, "RDS", "私はRDS、AWSのリレーショナルデータベースサービスだ。堅牢なデータ管理が必要なら任せてくれ。")
            self.add_npc(22, 8, "Aurora", "私はAurora、高性能なMySQLおよびPostgreSQLと互換性のあるデータベースだ。")
        elif "Security" in self.name:
            # Security Town - IAM, CloudFront, Shield
            self.add_npc(15, 10, "IAM", "私はIAM、AWSのアイデンティティ管理サービスだ。セキュアなアクセス制御が必要なら任せてくれ。")
            self.add_npc(8, 15, "CloudFront", "私はCloudFront、AWSのCDNサービスだ。高速なコンテンツ配信が必要なら任せてくれ。")
            self.add_npc(22, 8, "Shield", "私はShield、DDoS攻撃からの保護を提供するサービスだ。セキュリティを強化したいなら私を使ってくれ。")
        else:
            # デフォルトのNPC配置
            self.add_npc(5, 10, "EC2", "I'm EC2, a virtual server in the cloud.")
            self.add_npc(15, 10, "S3", "I'm S3, an object storage service.")
            self.add_npc(25, 10, "Lambda", "I'm Lambda, a serverless compute service.")
        
    def _create_town_roads(self):
        """町の道路を作成"""
        # 十字の道路
        center_x = self.width // 2
        center_y = self.height // 2
        
        for x in range(1, self.width-1):
            self.tiles[center_y][x] = TILE_ROAD
            
        for y in range(1, self.height-1):
            self.tiles[y][center_x] = TILE_ROAD
            
    def generate_dungeon_map(self):
        """ダンジョンマップを生成"""
        # 外周を壁にする
        for x in range(self.width):
            self.tiles[0][x] = TILE_WALL
            self.tiles[self.height-1][x] = TILE_WALL
        for y in range(self.height):
            self.tiles[y][0] = TILE_WALL
            self.tiles[y][self.width-1] = TILE_WALL
            
        # 内側を壁で埋める
        for y in range(1, self.height-1):
            for x in range(1, self.width-1):
                self.tiles[y][x] = TILE_WALL
                
        # 部屋を生成
        rooms = []
        for _ in range(10):
            room_width = random.randint(4, 8)
            room_height = random.randint(4, 8)
            room_x = random.randint(1, self.width - room_width - 1)
            room_y = random.randint(1, self.height - room_height - 1)
            
            # 部屋が重ならないかチェック
            overlap = False
            for room in rooms:
                rx, ry, rw, rh = room
                if (room_x < rx + rw + 1 and room_x + room_width + 1 > rx and
                    room_y < ry + rh + 1 and room_y + room_height + 1 > ry):
                    overlap = True
                    break
                    
            if not overlap:
                # 部屋を作成
                for y in range(room_y, room_y + room_height):
                    for x in range(room_x, room_x + room_width):
                        self.tiles[y][x] = TILE_FLOOR
                        
                rooms.append((room_x, room_y, room_width, room_height))
                
        # 部屋同士を通路で繋ぐ
        for i in range(len(rooms) - 1):
            room1 = rooms[i]
            room2 = rooms[i + 1]
            
            # 部屋の中心を計算
            x1 = room1[0] + room1[2] // 2
            y1 = room1[1] + room1[3] // 2
            x2 = room2[0] + room2[2] // 2
            y2 = room2[1] + room2[3] // 2
            
            # 通路を作成
            if random.random() < 0.5:
                # 水平→垂直
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    self.tiles[y1][x] = TILE_FLOOR
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    self.tiles[y][x2] = TILE_FLOOR
            else:
                # 垂直→水平
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    self.tiles[y][x1] = TILE_FLOOR
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    self.tiles[y2][x] = TILE_FLOOR
                    
        # 出口ポータルを配置（最後の部屋）
        if rooms:
            last_room = rooms[-1]
            portal_x = last_room[0] + last_room[2] // 2
            portal_y = last_room[1] + last_room[3] // 2
            self.add_portal(portal_x, portal_y, "AWS Cloud World", 25, 25)
            
        # 敵をランダムに配置
        self.place_random_enemies(20)
        
    def place_building(self, x, y, width, height):
        """建物を配置"""
        # 範囲チェック
        if x < 0 or y < 0 or x + width >= self.width or y + height >= self.height:
            return False
            
        # 建物の外周を壁にする
        for dx in range(width):
            for dy in range(height):
                if dx == 0 or dx == width - 1 or dy == 0 or dy == height - 1:
                    # 範囲チェック
                    if 0 <= y+dy < self.height and 0 <= x+dx < self.width:
                        self.tiles[y+dy][x+dx] = TILE_WALL
                else:
                    # 範囲チェック
                    if 0 <= y+dy < self.height and 0 <= x+dx < self.width:
                        self.tiles[y+dy][x+dx] = TILE_FLOOR
                    
        # ドアを配置（下側の中央）
        door_x = x + width // 2
        door_y = y + height - 1
        # 範囲チェック
        if 0 <= door_y < self.height and 0 <= door_x < self.width:
            self.tiles[door_y][door_x] = TILE_DOOR
            
        return True
        
    def add_npc(self, x, y, name, dialog):
        """NPCを追加"""
        self.tiles[y][x] = TILE_NPC
        self.npcs.append({
            "x": x,
            "y": y,
            "name": name,
            "dialog": dialog
        })
        
    def add_portal(self, x, y, destination, dest_x, dest_y):
        """ポータルを追加"""
        self.tiles[y][x] = TILE_PORTAL
        self.portals.append({
            "x": x,
            "y": y,
            "destination": destination,
            "dest_x": dest_x,
            "dest_y": dest_y
        })
        
    def add_shop(self, x, y, name, shop_type, dialog):
        """ショップを追加"""
        self.tiles[y][x] = TILE_SHOP
        self.shops.append({
            "x": x,
            "y": y,
            "name": name,
            "type": shop_type,
            "dialog": dialog
        })
        
    def place_random_enemies(self, count):
        """敵をランダムに配置"""
        # フィールド上の敵アイコンは不要なので、敵データのみ保持
        self.enemies = []
        for _ in range(count):
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)
            
            # 床、草、道の上にのみ敵を配置
            if self.tiles[y][x] in [TILE_FLOOR, TILE_GRASS, TILE_ROAD]:
                enemy_type = random.choice(["weak", "normal", "strong"])
                self.enemies.append({
                    "type": enemy_type
                })
                
    def is_walkable(self, x, y):
        """指定位置が歩行可能かどうか"""
        # マップ範囲外は歩行不可
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return False
            
        # タイルタイプによって歩行可能かどうかを判定
        tile_type = self.tiles[y][x]
        
        # 歩行可能なタイル
        walkable_tiles = [TILE_FLOOR, TILE_GRASS, TILE_ROAD, TILE_DOOR, TILE_NPC, TILE_PORTAL, TILE_SHOP,
                          TILE_FOUNTAIN, TILE_BENCH, TILE_LAMP, TILE_SIGN, TILE_FLOWERBED]
        
        return tile_type in walkable_tiles
        
    def get_npc_at(self, x, y):
        """指定位置にいるNPCを取得"""
        if self.tiles[y][x] == TILE_NPC:
            for npc in self.npcs:
                if npc["x"] == x and npc["y"] == y:
                    return npc
        return None
        
    def get_portal_at(self, x, y):
        """指定位置にあるポータルを取得"""
        if self.tiles[y][x] == TILE_PORTAL:
            for portal in self.portals:
                if portal["x"] == x and portal["y"] == y:
                    return portal
        return None
        
    def get_shop_at(self, x, y):
        """指定位置にあるショップを取得"""
        if self.tiles[y][x] == TILE_SHOP:
            for shop in self.shops:
                if shop["x"] == x and shop["y"] == y:
                    return shop
        return None
        
    def check_random_encounter(self):
        """ランダムエンカウントのチェック"""
        return random.random() < self.encounter_rate

class MapManager:
    def __init__(self):
        self.maps = {}
        self.current_map = None
        self.generate_maps()
        
    def generate_maps(self):
        """マップを生成"""
        # 固定マップを使用
        self.maps["AWS Cloud World"] = GameMap.from_map_data(get_world_map())
        self.maps["Computing Town"] = GameMap.from_map_data(get_computing_town_map())
        self.maps["Storage Town"] = GameMap.from_map_data(get_storage_town_map())
        self.maps["Database Town"] = GameMap.from_map_data(get_database_town_map())
        self.maps["Security Town"] = GameMap.from_map_data(get_security_town_map())
        
    def get_map(self, map_name):
        """マップ名からマップを取得"""
        return self.maps.get(map_name, None)
    def get_portal_at(self, x, y):
        """指定座標のポータル情報を取得"""
        for portal in self.portals:
            if portal["x"] == x and portal["y"] == y:
                return portal
        return None
        
    def place_building(self, x, y, width, height):
        """建物を配置（壁と床）"""
        # 外周を壁に
        for bx in range(x, x + width):
            for by in range(y, y + height):
                if bx == x or bx == x + width - 1 or by == y or by == y + height - 1:
                    self.tiles[by][bx] = TILE_WALL
                else:
                    self.tiles[by][bx] = TILE_FLOOR
                    
        # ドアを配置（建物の下側中央）
        door_x = x + width // 2
        door_y = y + height - 1
        self.tiles[door_y][door_x] = TILE_DOOR
    def get_portal_at(self, x, y):
        """指定座標のポータル情報を取得"""
        for portal in self.portals:
            if portal["x"] == x and portal["y"] == y:
                return portal
        return None
class MapManager:
    def __init__(self):
        self.maps = {}
        self.current_map = None
        self.generate_maps()
        
    def generate_maps(self):
        """マップを生成"""
        # ワールドマップ
        self.maps["AWS Cloud World"] = GameMap.from_map_data(get_world_map())
        
        # 町マップ
        self.maps["Computing Town"] = GameMap.from_map_data(get_computing_town_map())
        self.maps["Storage Town"] = GameMap.from_map_data(get_storage_town_map())
        self.maps["Database Town"] = GameMap.from_map_data(get_database_town_map())
        self.maps["Security Town"] = GameMap.from_map_data(get_security_town_map())
        
        # 初期マップを設定
        self.current_map = self.maps["AWS Cloud World"]
        
    def get_map(self, map_name):
        """名前でマップを取得"""
        return self.maps.get(map_name)
        
    def change_map(self, map_name, x, y):
        """マップを変更"""
        if map_name in self.maps:
            self.current_map = self.maps[map_name]
            return x, y
        return None, None
