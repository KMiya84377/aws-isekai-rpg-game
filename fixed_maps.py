#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import random

# Tile type constants
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
TILE_STATUE = 18
TILE_TABLE = 19
TILE_CHAIR = 20
TILE_INN = 21  # Added inn tile type
TILE_SIGN = 16
TILE_FLOWERBED = 17

# 固定マップデータ
def get_world_map():
    """Return the main world map data"""
    # Create a 50x50 map
    width = 50
    height = 50
    tiles = [[TILE_GRASS for _ in range(width)] for _ in range(height)]
    
    # Surround with walls
    for x in range(width):
        tiles[0][x] = TILE_WALL
        tiles[height-1][x] = TILE_WALL
    for y in range(height):
        tiles[y][0] = TILE_WALL
        tiles[y][width-1] = TILE_WALL
    
    # 固定の地形パターン
    
    # 中央に大きな湖（固定形状）
    for y in range(20, 30):
        for x in range(15, 35):
            # 円形の湖
            if (x - 25) ** 2 + (y - 25) ** 2 <= 100:
                tiles[y][x] = TILE_WATER
    
    # 北側に山脈（固定パターン）
    for y in range(5, 15):
        for x in range(10, 40):
            if (x + y) % 3 == 0 or (x - y) % 5 == 0:
                tiles[y][x] = TILE_MOUNTAIN
    
    # 南側に森（固定パターン）
    for y in range(35, 45):
        for x in range(10, 40):
            if (x * y) % 7 == 0 or (x + y) % 8 == 0:
                tiles[y][x] = TILE_FOREST
    
    # 東側に砂漠（固定領域）
    for y in range(15, 35):
        for x in range(35, 45):
            tiles[y][x] = TILE_SAND
    
    # 道路ネットワーク（固定パターン）
    # 中央の十字路 - プレイヤーの初期位置
    for x in range(1, width-1):
        tiles[25][x] = TILE_ROAD
    
    for y in range(1, height-1):
        tiles[y][25] = TILE_ROAD
    
    # 中央周辺の安全地帯（プレイヤーの初期位置の周り）
    for y in range(23, 28):
        for x in range(23, 28):
            tiles[y][x] = TILE_ROAD
    
    # 町への道路（直線）
    # Computing Town (北西)
    for x in range(10, 25):
        tiles[10][x] = TILE_ROAD
    for y in range(10, 25):
        tiles[y][10] = TILE_ROAD
    
    # Storage Town (北東)
    for x in range(25, 40):
        tiles[10][x] = TILE_ROAD
    for y in range(10, 25):
        tiles[y][40] = TILE_ROAD
    
    # Database Town (南西)
    for x in range(10, 25):
        tiles[40][x] = TILE_ROAD
    for y in range(25, 40):
        tiles[y][10] = TILE_ROAD
    
    # Security Town (南東)
    for x in range(25, 40):
        tiles[40][x] = TILE_ROAD
    for y in range(25, 40):
        tiles[y][40] = TILE_ROAD
    
    # 町の位置（ポータル）
    portal_positions = [
        (10, 10),  # Computing Town (北西)
        (40, 10),  # Storage Town (北東)
        (10, 40),  # Database Town (南西)
        (40, 40)   # Security Town (南東)
    ]
    
    # ポータル周辺を整備（町への入口を確保）
    for px, py in portal_positions:
        # ポータルを設置
        tiles[py][px] = TILE_PORTAL
        
        # ポータル周辺の安全地帯（3マス圏内）
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                nx, ny = px + dx, py + dy
                if 1 <= nx < width - 1 and 1 <= ny < height - 1:
                    # 山や森を除去し、草原に変更（ポータル自体は上書きしない）
                    if tiles[ny][nx] in [TILE_MOUNTAIN, TILE_FOREST] and tiles[ny][nx] != TILE_PORTAL:
                        tiles[ny][nx] = TILE_GRASS
    
    # 固定の地形特徴（装飾的な要素）
    
    # 小さな湖（北西）
    for y in range(5, 10):
        for x in range(5, 10):
            if (x - 7) ** 2 + (y - 7) ** 2 <= 4:
                tiles[y][x] = TILE_WATER
    
    # 小さな湖（北東）
    for y in range(5, 10):
        for x in range(40, 45):
            if (x - 42) ** 2 + (y - 7) ** 2 <= 4:
                tiles[y][x] = TILE_WATER
    
    # 小さな湖（南西）
    for y in range(40, 45):
        for x in range(5, 10):
            if (x - 7) ** 2 + (y - 42) ** 2 <= 4:
                tiles[y][x] = TILE_WATER
    
    # 小さな湖（南東）
    for y in range(40, 45):
        for x in range(40, 45):
            if (x - 42) ** 2 + (y - 42) ** 2 <= 4:
                tiles[y][x] = TILE_WATER
    
    # 森林クラスター（固定位置）- プレイヤーの初期位置（25,25）を避ける
    forest_clusters = [
        (15, 15, 3),  # (x, y, サイズ)
        (35, 35, 4),
        (15, 35, 3),
        (35, 15, 4)
    ]
    
    for cx, cy, size in forest_clusters:
        for dy in range(-size, size + 1):
            for dx in range(-size, size + 1):
                x, y = cx + dx, cy + dy
                if 1 <= x < width - 1 and 1 <= y < height - 1:
                    # 中心からの距離
                    distance = dx**2 + dy**2
                    # 距離に応じてタイルを配置
                    if distance <= size**2:
                        # 道路や水、ポータルは上書きしない
                        if tiles[y][x] not in [TILE_ROAD, TILE_WATER, TILE_PORTAL]:
                            tiles[y][x] = TILE_FOREST
    
    # 山岳クラスター（固定位置）
    mountain_clusters = [
        (20, 10, 2),  # (x, y, サイズ)
        (30, 10, 3),
        (20, 40, 3),
        (30, 40, 2)
    ]
    
    for cx, cy, size in mountain_clusters:
        for dy in range(-size, size + 1):
            for dx in range(-size, size + 1):
                x, y = cx + dx, cy + dy
                if 1 <= x < width - 1 and 1 <= y < height - 1:
                    # 中心からの距離
                    distance = dx**2 + dy**2
                    # 距離に応じてタイルを配置
                    if distance <= size**2:
                        # 道路や水、ポータルは上書きしない
                        if tiles[y][x] not in [TILE_ROAD, TILE_WATER, TILE_PORTAL]:
                            tiles[y][x] = TILE_MOUNTAIN
    
    # ポータルデータ
    portals = [
        {
            "x": 10,
            "y": 10,
            "destination": "Computing Town",
            "dest_x": 15,
            "dest_y": 25
        },
        {
            "x": 40,
            "y": 10,
            "destination": "Storage Town",
            "dest_x": 15,
            "dest_y": 25
        },
        {
            "x": 10,
            "y": 40,
            "destination": "Database Town",
            "dest_x": 15,
            "dest_y": 25
        },
        {
            "x": 40,
            "y": 40,
            "destination": "Security Town",
            "dest_x": 15,
            "dest_y": 25
        }
    ]
    
    # NPCデータ
    npcs = [
        {
            "x": 25,
            "y": 20,
            "name": "Traveler",
            "dialog": "I've heard there's a town called Computing Town to the northwest. You should check it out! They say there are other towns in this world too, but I haven't found them yet."
        },
        {
            "x": 20,
            "y": 15,
            "name": "Explorer",
            "dialog": "This world is full of mysteries! I've been trying to find all the towns, but some seem to be hidden. Maybe completing quests will reveal their locations?"
        },
        {
            "x": 30,
            "y": 15,
            "name": "Merchant",
            "dialog": "I travel between towns selling my wares. Computing Town is the only one I know of right now, but I've heard rumors of other towns with unique AWS services."
        }
    ]
    
    # マップデータを辞書として返す
    return {
        "name": "AWS Cloud World",
        "width": width,
        "height": height,
        "tiles": tiles,
        "portals": portals,
        "npcs": npcs,
        "shops": [],
        "encounter_rate": 0.03
    }

def get_computing_town_map():
    """Computing Town map data"""
    width = 30
    height = 30
    tiles = [[TILE_FLOOR for _ in range(width)] for _ in range(height)]
    
    # Surround with walls
    for x in range(width):
        tiles[0][x] = TILE_WALL
        tiles[height-1][x] = TILE_WALL
    for y in range(height):
        tiles[y][0] = TILE_WALL
        tiles[y][width-1] = TILE_WALL
    
    # Main roads - wider and more natural
    center_x = width // 2
    center_y = height // 2
    
    # Horizontal main road (wider)
    for x in range(1, width-1):
        tiles[center_y][x] = TILE_ROAD
        tiles[center_y-1][x] = TILE_ROAD
        tiles[center_y+1][x] = TILE_ROAD
        
    # Vertical main road (wider)
    for y in range(1, height-1):
        tiles[y][center_x] = TILE_ROAD
        tiles[y][center_x-1] = TILE_ROAD
        tiles[y][center_x+1] = TILE_ROAD
    
    # Secondary roads - more natural, curved paths
    # North area road
    for x in range(5, width-5):
        road_y = center_y - 6
        if 1 <= road_y < height-1:
            tiles[road_y][x] = TILE_ROAD
            # Add some variation
            if x % 5 == 0 and road_y > 2:
                tiles[road_y-1][x] = TILE_ROAD
    
    # South area road
    for x in range(5, width-5):
        road_y = center_y + 6
        if 1 <= road_y < height-1:
            tiles[road_y][x] = TILE_ROAD
            # Add some variation
            if x % 5 == 0 and road_y < height-2:
                tiles[road_y+1][x] = TILE_ROAD
                
    # East area road
    for y in range(5, height-5):
        road_x = center_x + 6
        if 1 <= road_x < width-1:
            tiles[y][road_x] = TILE_ROAD
            # Add some variation
            if y % 5 == 0 and road_x < width-2:
                tiles[y][road_x+1] = TILE_ROAD
                
    # West area road
    for y in range(5, height-5):
        road_x = center_x - 6
        if 1 <= road_x < width-1:
            tiles[y][road_x] = TILE_ROAD
            # Add some variation
            if y % 5 == 0 and road_x > 2:
                tiles[y][road_x-1] = TILE_ROAD
    
    # Buildings - properly enclosed with single doors
    buildings = []
    
    # Create shop buildings first (to ensure they're in good locations)
    # Weapon shop building
    weapon_shop_x, weapon_shop_y = 5, 5
    weapon_shop_w, weapon_shop_h = 5, 5
    
    # Create weapon shop building
    for bx in range(weapon_shop_x, weapon_shop_x+weapon_shop_w):
        for by in range(weapon_shop_y, weapon_shop_y+weapon_shop_h):
            if 1 <= bx < width-1 and 1 <= by < height-1:
                if bx == weapon_shop_x or bx == weapon_shop_x+weapon_shop_w-1 or by == weapon_shop_y or by == weapon_shop_y+weapon_shop_h-1:
                    tiles[by][bx] = TILE_WALL
                else:
                    tiles[by][bx] = TILE_FLOOR
    
    # Add door to weapon shop
    door_x = weapon_shop_x + weapon_shop_w//2
    door_y = weapon_shop_y + weapon_shop_h - 1
    tiles[door_y][door_x] = TILE_DOOR
    
    # Place shop tile inside the building
    shop_x = weapon_shop_x + weapon_shop_w//2
    shop_y = weapon_shop_y + weapon_shop_h//2
    tiles[shop_y][shop_x] = TILE_SHOP
    
    # Armor shop building
    armor_shop_x, armor_shop_y = 20, 5
    armor_shop_w, armor_shop_h = 5, 5
    
    # Create armor shop building
    for bx in range(armor_shop_x, armor_shop_x+armor_shop_w):
        for by in range(armor_shop_y, armor_shop_y+armor_shop_h):
            if 1 <= bx < width-1 and 1 <= by < height-1:
                if bx == armor_shop_x or bx == armor_shop_x+armor_shop_w-1 or by == armor_shop_y or by == armor_shop_y+armor_shop_h-1:
                    tiles[by][bx] = TILE_WALL
                else:
                    tiles[by][bx] = TILE_FLOOR
    
    # Add door to armor shop
    door_x = armor_shop_x + armor_shop_w//2
    door_y = armor_shop_y + armor_shop_h - 1
    tiles[door_y][door_x] = TILE_DOOR
    
    # Place shop tile inside the building
    shop_x = armor_shop_x + armor_shop_w//2
    shop_y = armor_shop_y + armor_shop_h//2
    tiles[shop_y][shop_x] = TILE_SHOP
    
    # Item shop building
    item_shop_x, item_shop_y = 5, 20
    item_shop_w, item_shop_h = 5, 5
    
    # Create item shop building
    for bx in range(item_shop_x, item_shop_x+item_shop_w):
        for by in range(item_shop_y, item_shop_y+item_shop_h):
            if 1 <= bx < width-1 and 1 <= by < height-1:
                if bx == item_shop_x or bx == item_shop_x+item_shop_w-1 or by == item_shop_y or by == item_shop_y+item_shop_h-1:
                    tiles[by][bx] = TILE_WALL
                else:
                    tiles[by][bx] = TILE_FLOOR
    
    # Add door to item shop
    door_x = item_shop_x + item_shop_w//2
    door_y = item_shop_y + item_shop_h - 1
    tiles[door_y][door_x] = TILE_DOOR
    
    # Place shop tile inside the building
    shop_x = item_shop_x + item_shop_w//2
    shop_y = item_shop_y + item_shop_h//2
    tiles[shop_y][shop_x] = TILE_SHOP
    
    # Inn building
    inn_x, inn_y = 20, 20
    inn_w, inn_h = 6, 6
    
    # Create inn building
    for bx in range(inn_x, inn_x+inn_w):
        for by in range(inn_y, inn_y+inn_h):
            if 1 <= bx < width-1 and 1 <= by < height-1:
                if bx == inn_x or bx == inn_x+inn_w-1 or by == inn_y or by == inn_y+inn_h-1:
                    tiles[by][bx] = TILE_WALL
                else:
                    tiles[by][bx] = TILE_FLOOR
    
    # Add door to inn
    door_x = inn_x + inn_w//2
    door_y = inn_y + inn_h - 1
    tiles[door_y][door_x] = TILE_DOOR
    
    # Place inn tile inside the building
    inn_tile_x = inn_x + inn_w//2
    inn_tile_y = inn_y + inn_h//2
    tiles[inn_tile_y][inn_tile_x] = TILE_INN
    
    # Main service buildings (for AWS services)
    service_buildings = [
        (12, 12, 6, 6),  # Center - EC2
        (3, 3, 4, 4),    # Northwest corner - Lambda
        (23, 3, 4, 4),   # Northeast corner - SQS
    ]
    
    for x, y, w, h in service_buildings:
        # Create building
        for bx in range(x, x+w):
            for by in range(y, y+h):
                if 1 <= bx < width-1 and 1 <= by < height-1:
                    if bx == x or bx == x+w-1 or by == y or by == y+h-1:
                        tiles[by][bx] = TILE_WALL
                    else:
                        tiles[by][bx] = TILE_FLOOR
        
        # Add door (only one door per building)
        door_x = x + w//2
        door_y = y + h - 1
        if 1 <= door_x < width-1 and 1 <= door_y < height-1:
            tiles[door_y][door_x] = TILE_DOOR
        
        buildings.append((x, y, w, h))
    
    # Smaller houses (more of them, scattered around)
    for _ in range(8):
        w = random.randint(3, 4)
        h = random.randint(3, 4)
        x = random.randint(2, width-w-2)
        y = random.randint(2, height-h-2)
        
        # Check if overlaps with roads or other buildings
        valid = True
        for bx in range(x-1, x+w+1):
            for by in range(y-1, y+h+1):
                if 0 <= bx < width and 0 <= by < height:
                    if tiles[by][bx] in [TILE_ROAD, TILE_WALL, TILE_DOOR, TILE_SHOP, TILE_INN]:
                        valid = False
                        break
        
        if valid:
            # Create building with proper walls
            for bx in range(x, x+w):
                for by in range(y, y+h):
                    if bx == x or bx == x+w-1 or by == y or by == y+h-1:
                        tiles[by][bx] = TILE_WALL
                    else:
                        tiles[by][bx] = TILE_FLOOR
            
            # Add door (only one door per building)
            door_x = x + w//2
            door_y = y + h - 1
            tiles[door_y][door_x] = TILE_DOOR
            
            buildings.append((x, y, w, h))
    
    # Decorations
    for _ in range(5):
        x = random.randint(1, width-2)
        y = random.randint(1, height-2)
        if tiles[y][x] == TILE_ROAD:
            tiles[y][x] = TILE_FOUNTAIN
    
    for _ in range(10):
        x = random.randint(1, width-2)
        y = random.randint(1, height-2)
        if tiles[y][x] == TILE_ROAD:
            tiles[y][x] = TILE_BENCH
    
    for _ in range(15):
        x = random.randint(1, width-2)
        y = random.randint(1, height-2)
        if tiles[y][x] == TILE_ROAD:
            tiles[y][x] = TILE_LAMP
            
    # Portal back to world map
    tiles[height-2][width//2] = TILE_PORTAL
    
    # NPCs
    npcs = [
        {
            "x": 14,
            "y": 14,
            "name": "EC2",
            "dialog": "Hello, I'm EC2. I'm the core computing service of AWS. How can I help you?",
            "is_service": True,
            "service_id": "ec2"
        },
        {
            "x": 5,
            "y": 5,
            "name": "Lambda",
            "dialog": "Hi, I'm Lambda. I handle serverless computing. Just write your code and don't worry about infrastructure!",
            "is_service": True,
            "service_id": "lambda"
        },
        {
            "x": 25,
            "y": 5,
            "name": "SQS",
            "dialog": "I'm SQS, Simple Queue Service. I handle messaging between microservices. I'm useful for loosely coupled application designs.",
            "is_service": True,
            "service_id": "sqs"
        }
    ]
    
    # Portal data
    portals = [
        {
            "x": width//2,
            "y": height-2,
            "destination": "AWS Cloud World",
            "dest_x": 10,
            "dest_y": 11
        }
    ]
    
    # Shop data
    shops = [
        {
            "x": weapon_shop_x + weapon_shop_w//2,
            "y": weapon_shop_y + weapon_shop_h//2,
            "name": "Computing Weapons",
            "type": "weapons",
            "dialog": "Transform computing power into weapons!",
            "items": ["bronze_sword", "iron_sword", "silver_sword", "compute_blade", "serverless_dagger"]
        },
        {
            "x": armor_shop_x + armor_shop_w//2,
            "y": armor_shop_y + armor_shop_h//2,
            "name": "Instance Armory",
            "type": "armor",
            "dialog": "Protect yourself with the best instance types!",
            "items": ["leather_armor", "chain_mail", "instance_shield", "auto_scaling_helmet"]
        },
        {
            "x": item_shop_x + item_shop_w//2,
            "y": item_shop_y + item_shop_h//2,
            "name": "EC2 Potions",
            "type": "items",
            "dialog": "Recover with computing power!",
            "items": ["potion_small", "potion_medium", "ether_small", "compute_elixir"]
        }
    ]
    
    # Return map data
    return {
        "name": "Computing Town",
        "width": width,
        "height": height,
        "tiles": tiles,
        "npcs": npcs,
        "portals": portals,
        "shops": shops,
        "encounter_rate": 0.0  # No random encounters in town
    }
    
    # データセンターのドア
    tiles[15][14] = TILE_DOOR
    tiles[15][15] = TILE_DOOR
    
    # 出口ポータル
    tiles[height-2][width//2] = TILE_PORTAL
    
    # 町の装飾オブジェクトを追加
    add_town_objects(tiles, width, height)
    
    # ショップ位置
    tiles[3][15] = TILE_SHOP
    tiles[15][3] = TILE_SHOP
    tiles[27][15] = TILE_SHOP
    
    # NPCデータ
    npcs = [
        {
            "x": 14,
            "y": 12,
            "name": "EC2",
            "dialog": "Hello, I'm EC2. I'm the core computing service of AWS. How can I help you?",
            "is_service": True,
            "service_id": "ec2"
        },
        {
            "x": 8,
            "y": 8,
            "name": "Lambda",
            "dialog": "Hi, I'm Lambda. I handle serverless computing. Just write your code and don't worry about infrastructure!",
            "is_service": True,
            "service_id": "lambda"
        },
        {
            "x": 20,
            "y": 8,
            "name": "ECS",
            "dialog": "I'm ECS, Elastic Container Service. I can help you run and manage containerized applications easily.",
            "is_service": True,
            "service_id": "ecs"
        },
        {
            "x": 8,
            "y": 20,
            "name": "Fargate",
            "dialog": "I'm Fargate. I can run ECS and EKS containers in a serverless way. Free yourself from infrastructure management!",
            "is_service": True,
            "service_id": "fargate"
        },
        {
            "x": 20,
            "y": 20,
            "name": "Elastic Beanstalk",
            "dialog": "I'm Elastic Beanstalk. I simplify application deployment and management. Just upload your code and I'll build the environment for you.",
            "is_service": True,
            "service_id": "beanstalk"
        },
        {
            "x": 13,
            "y": 13,
            "name": "CloudWatch",
            "dialog": "I'm CloudWatch. I monitor AWS resources and applications. I can collect metrics, analyze logs, and set up alarms for you.",
            "is_service": True,
            "service_id": "cloudwatch"
        },
        {
            "x": 16,
            "y": 13,
            "name": "CloudFormation",
            "dialog": "I'm CloudFormation. I help you manage infrastructure as code. You can easily deploy resources using templates.",
            "is_service": True,
            "service_id": "cloudformation"
        },
        {
            "x": 13,
            "y": 16,
            "name": "Step Functions",
            "dialog": "I'm Step Functions. I help you build serverless workflows visually. You can easily coordinate complex processes with me.",
            "is_service": True,
            "service_id": "stepfunctions"
        },
        {
            "x": 16,
            "y": 16,
            "name": "SQS",
            "dialog": "I'm SQS, Simple Queue Service. I handle messaging between microservices. I'm useful for loosely coupled application designs.",
            "is_service": True,
            "service_id": "sqs"
        }
    ]
    
    # ポータルデータ
    portals = [
        {
            "x": width//2,
            "y": height-2,
            "destination": "AWS Cloud World",
            "dest_x": 10,
            "dest_y": 11
        }
    ]
    
    # ショップデータ
    shops = [
        {
            "x": 3,
            "y": 15,
            "name": "Computing Weapons",
            "type": "weapons",
            "dialog": "Transform computing power into weapons!",
            "items": ["bronze_sword", "iron_sword", "silver_sword", "compute_blade", "serverless_dagger"]
        },
        {
            "x": 15,
            "y": 3,
            "name": "Instance Armory",
            "type": "armor",
            "dialog": "Protect yourself with the best instance types!",
            "items": ["leather_armor", "chain_mail", "instance_shield", "auto_scaling_helmet"]
        },
        {
            "x": 27,
            "y": 15,
            "name": "EC2 Potions",
            "type": "items",
            "dialog": "Recover with computing power!",
            "items": ["potion_small", "potion_medium", "ether_small", "compute_elixir"]
        }
    ]
    
    # タイルにNPCを配置
    for npc in npcs:
        x, y = npc["x"], npc["y"]
        if 0 <= x < width and 0 <= y < height:
            tiles[y][x] = TILE_NPC
    
    return {
        "name": "Computing Town",
        "width": width,
        "height": height,
        "tiles": tiles,
        "portals": portals,
        "npcs": npcs,
        "shops": shops,
        "encounter_rate": 0.0
    }

def get_storage_town_map():
    """Storage Townのマップデータを返す"""
    width = 30
    height = 30
    tiles = [[TILE_FLOOR for _ in range(width)] for _ in range(height)]
    
    # 外周を壁に
    for x in range(width):
        tiles[0][x] = TILE_WALL
        tiles[height-1][x] = TILE_WALL
    for y in range(height):
        tiles[y][0] = TILE_WALL
        tiles[y][width-1] = TILE_WALL
    
    # 放射状の道路（固定パターン）
    center_x = width // 2
    center_y = height // 2
    
    # 十字の道路
    for x in range(width):
        tiles[center_y][x] = TILE_ROAD
    for y in range(height):
        tiles[y][center_x] = TILE_ROAD
    
    # 斜めの道路
    for i in range(-15, 16):
        x = center_x + i
        y = center_y + i
        if 0 <= x < width and 0 <= y < height:
            tiles[y][x] = TILE_ROAD
        
        x = center_x + i
        y = center_y - i
        if 0 <= x < width and 0 <= y < height:
            tiles[y][x] = TILE_ROAD
    
    # 倉庫風の建物（固定位置）
    warehouse_positions = [
        (5, 5, 8, 8),  # (x, y, 幅, 高さ)
        (17, 5, 8, 8),
        (5, 17, 8, 8),
        (17, 17, 8, 8)
    ]
    
    for x, y, w, h in warehouse_positions:
        # 建物の外周を壁に
        for bx in range(x, min(x+w, width-1)):
            for by in range(y, min(y+h, height-1)):
                if bx == x or bx == min(x+w-1, width-2) or by == y or by == min(y+h-1, height-2):
                    tiles[by][bx] = TILE_WALL
                else:
                    tiles[by][bx] = TILE_FLOOR
        
        # ドアを追加（建物の下側中央）
        door_x = x + w // 2
        door_y = y + h - 1
        if 0 <= door_x < width and 0 <= door_y < height:
            tiles[door_y][door_x] = TILE_DOOR
        
        # 側面にもドアを追加（建物の右側中央）
        door_x = x + w - 1
        door_y = y + h // 2
        if 0 <= door_x < width and 0 <= door_y < height:
            tiles[door_y][door_x] = TILE_DOOR
    
    # 出口ポータル
    tiles[height-2][width//2] = TILE_PORTAL
    
    # 町の装飾オブジェクトを追加
    add_town_objects(tiles, width, height)
    
    # ショップ位置
    tiles[7][7] = TILE_SHOP
    tiles[22][7] = TILE_SHOP
    tiles[7][22] = TILE_SHOP
    
    # NPCデータ
    npcs = [
        {
            "x": 14,
            "y": 12,
            "name": "S3",
            "dialog": "こんにちは、私はS3です。Simple Storage Serviceの略で、データを安全に保存するサービスです。",
            "is_service": True,
            "service_id": "s3"
        },
        {
            "x": 8,
            "y": 8,
            "name": "EBS",
            "dialog": "私はEBS、Elastic Block Storeです。EC2インスタンス用の永続ストレージを提供しています。",
            "is_service": True,
            "service_id": "ebs"
        },
        {
            "x": 20,
            "y": 20,
            "name": "Glacier",
            "dialog": "私はGlacierです。長期保存用の低コストストレージを提供しています。アクセス頻度の低いデータの保管に最適ですよ。",
            "is_service": True,
            "service_id": "glacier"
        },
        {
            "x": 20,
            "y": 8,
            "name": "EFS",
            "dialog": "私はEFS、Elastic File Systemです。複数のEC2インスタンスで共有できるファイルシステムを提供します。",
            "is_service": True,
            "service_id": "efs"
        },
        {
            "x": 8,
            "y": 20,
            "name": "Storage Gateway",
            "dialog": "私はStorage Gatewayです。オンプレミスとAWSストレージを橋渡しします。ハイブリッドクラウドの強い味方ですよ。",
            "is_service": True,
            "service_id": "storage_gateway"
        },
        {
            "x": 13,
            "y": 13,
            "name": "Snow Family",
            "dialog": "私はSnow Familyです。大量のデータを物理デバイスでAWSに転送するサービスです。Snowball、Snowcone、Snowmobileなどがありますよ。",
            "is_service": True,
            "service_id": "snow"
        },
        {
            "x": 16,
            "y": 13,
            "name": "FSx",
            "dialog": "私はFSxです。Windows File ServerやLustreなど、様々なファイルシステムをマネージドサービスとして提供しています。",
            "is_service": True,
            "service_id": "fsx"
        },
        {
            "x": 13,
            "y": 16,
            "name": "Backup",
            "dialog": "私はAWS Backupです。AWSリソースのバックアップを一元管理できるサービスです。データ保護が簡単になりますよ。",
            "is_service": True,
            "service_id": "backup"
        },
        {
            "x": 16,
            "y": 16,
            "name": "S3 Glacier Deep Archive",
            "dialog": "私はS3 Glacier Deep Archiveです。最も低コストのアーカイブストレージを提供しています。長期保存に最適ですよ。",
            "is_service": True,
            "service_id": "glacier_deep_archive"
        }
    ]
    
    # ポータルデータ
    portals = [
        {
            "x": width//2,
            "y": height-2,
            "destination": "AWS Cloud World",
            "dest_x": 40,
            "dest_y": 11
        }
    ]
    
    # ショップデータ
    shops = [
        {
            "x": 7,
            "y": 7,
            "name": "S3 Armory",
            "type": "armor",
            "dialog": "最高のストレージ防具で身を守りましょう！",
            "items": ["leather_armor", "chain_mail", "plate_armor", "s3_shield", "glacier_helmet"]
        },
        {
            "x": 22,
            "y": 7,
            "name": "Storage Weapons",
            "type": "weapons",
            "dialog": "ストレージの力を武器に変えましょう！",
            "items": ["bronze_sword", "iron_sword", "storage_blade", "ebs_hammer"]
        },
        {
            "x": 7,
            "y": 22,
            "name": "Bucket Potions",
            "type": "items",
            "dialog": "S3バケットから取り出した回復アイテムです！",
            "items": ["potion_small", "potion_medium", "ether_small", "storage_elixir"]
        }
    ]
    
    return {
        "name": "Storage Town",
        "width": width,
        "height": height,
        "tiles": tiles,
        "portals": portals,
        "npcs": npcs,
        "shops": shops,
        "encounter_rate": 0.0
    }

def get_database_town_map():
    """Database Townのマップデータを返す"""
    width = 30
    height = 30
    tiles = [[TILE_FLOOR for _ in range(width)] for _ in range(height)]
    
    # 外周を壁に
    for x in range(width):
        tiles[0][x] = TILE_WALL
        tiles[height-1][x] = TILE_WALL
    for y in range(height):
        tiles[y][0] = TILE_WALL
        tiles[y][width-1] = TILE_WALL
    
    # テーブル風の建物と円形の道路（固定パターン）
    center_x = width // 2
    center_y = height // 2
    
    # 円形の道路
    radius = 10
    for angle in range(0, 360, 5):
        rad = math.radians(angle)
        x = int(center_x + radius * math.cos(rad))
        y = int(center_y + radius * math.sin(rad))
        if 0 <= x < width and 0 <= y < height:
            tiles[y][x] = TILE_ROAD
    
    # テーブル風の建物（固定位置）
    table_positions = [
        (5, 5, 6, 6),  # (x, y, 幅, 高さ)
        (19, 5, 6, 6),
        (5, 19, 6, 6),
        (19, 19, 6, 6),
        (12, 12, 6, 6)  # 中央
    ]
    
    for x, y, w, h in table_positions:
        # 建物の外周を壁に
        for bx in range(x, min(x+w, width-1)):
            for by in range(y, min(y+h, height-1)):
                if bx == x or bx == min(x+w-1, width-2) or by == y or by == min(y+h-1, height-2):
                    tiles[by][bx] = TILE_WALL
                else:
                    tiles[by][bx] = TILE_FLOOR
    
    # 出口ポータル
    tiles[height-2][width//2] = TILE_PORTAL
    
    # NPCデータ
    npcs = [
        {
            "x": 14,
            "y": 12,
            "name": "DynamoDB",
            "dialog": "こんにちは、私はDynamoDBです。NoSQLデータベースサービスとして、高速で柔軟なデータ管理を提供しています。",
            "is_service": True,
            "service_id": "dynamodb"
        },
        {
            "x": 8,
            "y": 8,
            "name": "RDS",
            "dialog": "私はRDS、Relational Database Serviceです。MySQLやPostgreSQLなどのリレーショナルデータベースを簡単に設定・運用できます。",
            "is_service": True,
            "service_id": "rds"
        },
        {
            "x": 20,
            "y": 20,
            "name": "Redshift",
            "dialog": "私はRedshiftです。データウェアハウスサービスとして、大規模なデータ分析を高速に実行できます。",
            "is_service": True,
            "service_id": "redshift"
        },
        {
            "x": 7,
            "y": 14,
            "name": "Aurora",
            "dialog": "私はAuroraです。MySQLやPostgreSQLと互換性のある高性能なリレーショナルデータベースです。クラウドに最適化されていますよ。",
            "is_service": True,
            "service_id": "aurora"
        },
        {
            "x": 14,
            "y": 7,
            "name": "ElastiCache",
            "dialog": "私はElastiCacheです。RedisやMemcachedのマネージドサービスとして、インメモリキャッシュを提供しています。アプリケーションの高速化に役立ちますよ。",
            "is_service": True,
            "service_id": "elasticache"
        },
        {
            "x": 21,
            "y": 14,
            "name": "DocumentDB",
            "dialog": "私はDocumentDBです。MongoDBと互換性のあるドキュメントデータベースサービスです。スケーラブルで高可用性があります。",
            "is_service": True,
            "service_id": "documentdb"
        },
        {
            "x": 14,
            "y": 21,
            "name": "Neptune",
            "dialog": "私はNeptuneです。グラフデータベースサービスとして、高度に接続されたデータセットを簡単に構築・実行できます。",
            "is_service": True,
            "service_id": "neptune"
        },
        {
            "x": 7,
            "y": 7,
            "name": "Timestream",
            "dialog": "私はTimestreamです。IoTアプリケーションやデバイスからの時系列データを効率的に保存・分析できる時系列データベースです。",
            "is_service": True,
            "service_id": "timestream"
        },
        {
            "x": 21,
            "y": 21,
            "name": "QLDB",
            "dialog": "私はQLDBです。Quantum Ledger Database の略で、完全に検証可能な台帳データベースサービスです。変更履歴を追跡できますよ。",
            "is_service": True,
            "service_id": "qldb"
        }
    ]
    
    # ポータルデータ
    portals = [
        {
            "x": width//2,
            "y": height-2,
            "destination": "AWS Cloud World",
            "dest_x": 10,
            "dest_y": 39
        }
    ]
    
    # ショップデータ
    shops = [
        {
            "x": 22,
            "y": 8,
            "name": "Database Shop",
            "items": ["potion_small", "potion_medium", "potion_large", "ether_small", "ether_medium"]
        }
    ]
    
    return {
        "name": "Database Town",
        "width": width,
        "height": height,
        "tiles": tiles,
        "portals": portals,
        "npcs": npcs,
        "shops": shops,
        "encounter_rate": 0.0
    }

def get_security_town_map():
    """Security Townのマップデータを返す"""
    width = 30
    height = 30
    tiles = [[TILE_FLOOR for _ in range(width)] for _ in range(height)]
    
    # 外周を壁に
    for x in range(width):
        tiles[0][x] = TILE_WALL
        tiles[height-1][x] = TILE_WALL
    for y in range(height):
        tiles[y][0] = TILE_WALL
        tiles[y][width-1] = TILE_WALL
    
    # 要塞風の建物と同心円状の道路（固定パターン）
    center_x = width // 2
    center_y = height // 2
    
    # 同心円状の道路
    for radius in range(5, 15, 3):
        for angle in range(0, 360, 5):
            rad = math.radians(angle)
            x = int(center_x + radius * math.cos(rad))
            y = int(center_y + radius * math.sin(rad))
            if 0 <= x < width and 0 <= y < height:
                tiles[y][x] = TILE_ROAD
    
    # 要塞風の建物（固定位置）
    # 中央の要塞
    for x in range(center_x-4, min(center_x+5, width-1)):
        for y in range(center_y-4, min(center_y+5, height-1)):
            if x == center_x-4 or x == min(center_x+4, width-2) or y == center_y-4 or y == min(center_y+4, height-2):
                tiles[y][x] = TILE_WALL
            else:
                tiles[y][x] = TILE_FLOOR
    
    # 監視塔（四隅）
    tower_positions = [(5, 5), (5, height-6), (width-6, 5), (width-6, height-6)]
    for tx, ty in tower_positions:
        for x in range(tx, min(tx+3, width-1)):
            for y in range(ty, min(ty+3, height-1)):
                if x == tx or x == min(tx+2, width-2) or y == ty or y == min(ty+2, height-2):
                    tiles[y][x] = TILE_WALL
                else:
                    tiles[y][x] = TILE_FLOOR
    
    # 出口ポータル
    tiles[height-2][width//2] = TILE_PORTAL
    
    # NPCデータ
    npcs = [
        {
            "x": 14,
            "y": 12,
            "name": "IAM",
            "dialog": "こんにちは、私はIAMです。Identity and Access Managementの略で、AWSリソースへのアクセス制御を担当しています。",
            "is_service": True,
            "service_id": "iam"
        },
        {
            "x": 8,
            "y": 8,
            "name": "WAF",
            "dialog": "私はWAF、Web Application Firewallです。ウェブアプリケーションを攻撃から守ります。",
            "is_service": True,
            "service_id": "waf"
        },
        {
            "x": 20,
            "y": 20,
            "name": "Shield",
            "dialog": "私はShieldです。DDoS攻撃からアプリケーションを保護するサービスです。常に警戒を怠りません。",
            "is_service": True,
            "service_id": "shield"
        },
        {
            "x": 7,
            "y": 14,
            "name": "GuardDuty",
            "dialog": "私はGuardDutyです。インテリジェントな脅威検出サービスとして、AWSアカウントとワークロードを継続的にモニタリングしています。",
            "is_service": True,
            "service_id": "guardduty"
        },
        {
            "x": 14,
            "y": 7,
            "name": "KMS",
            "dialog": "私はKMS、Key Management Serviceです。暗号化キーの作成と管理を簡単にします。データの安全を守りましょう。",
            "is_service": True,
            "service_id": "kms"
        },
        {
            "x": 21,
            "y": 14,
            "name": "Cognito",
            "dialog": "私はCognitoです。ウェブおよびモバイルアプリのユーザー認証、認可、ユーザー管理を提供します。",
            "is_service": True,
            "service_id": "cognito"
        },
        {
            "x": 14,
            "y": 21,
            "name": "Secrets Manager",
            "dialog": "私はSecrets Managerです。データベース認証情報、APIキー、その他のシークレットを安全に保存・管理します。",
            "is_service": True,
            "service_id": "secrets_manager"
        },
        {
            "x": 7,
            "y": 7,
            "name": "Inspector",
            "dialog": "私はInspectorです。AWSリソースの自動セキュリティ評価サービスです。脆弱性やベストプラクティスからの逸脱を検出します。",
            "is_service": True,
            "service_id": "inspector"
        },
        {
            "x": 21,
            "y": 21,
            "name": "Macie",
            "dialog": "私はMacieです。機械学習を使用して、S3に保存された機密データを自動的に検出、分類、保護します。",
            "is_service": True,
            "service_id": "macie"
        }
    ]
    
    # ポータルデータ
    portals = [
        {
            "x": width//2,
            "y": height-2,
            "destination": "AWS Cloud World",
            "dest_x": 40,
            "dest_y": 39
        }
    ]
    
    # ショップデータ
    shops = [
        {
            "x": 22,
            "y": 8,
            "name": "Security Shop",
            "items": ["fire_scroll", "ice_scroll", "thunder_scroll", "barrier_amulet", "speed_boots"]
        }
    ]
    
    return {
        "name": "Security Town",
        "width": width,
        "height": height,
        "tiles": tiles,
        "portals": portals,
        "npcs": npcs,
        "shops": shops,
        "encounter_rate": 0.0
    }
    # 町の装飾オブジェクトを追加
    add_town_objects(tiles, width, height)
# 町中のオブジェクトを追加する関数
def add_town_objects(tiles, width, height):
    """町中のオブジェクトを追加する"""
    # 噴水（中央広場）
    center_x = width // 2
    center_y = height // 2
    tiles[center_y][center_x] = TILE_FOUNTAIN
    
    # ベンチ（噴水の周り）
    for dx, dy in [(0, -2), (0, 2), (-2, 0), (2, 0)]:
        x, y = center_x + dx, center_y + dy
        if 0 <= x < width and 0 <= y < height:
            tiles[y][x] = TILE_BENCH
    
    # 街灯（道路沿い）
    for i in range(5, width-5, 5):
        for j in range(5, height-5, 5):
            if (i % 10 == 0 or j % 10 == 0) and tiles[j][i] == TILE_ROAD:
                tiles[j][i] = TILE_LAMP
    
    # 看板（ショップの近く）
    for i in range(1, width-1):
        for j in range(1, height-1):
            if tiles[j][i] == TILE_SHOP:
                # ショップの周囲に看板を配置
                for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                    nx, ny = i + dx, j + dy
                    if 0 <= nx < width and 0 <= ny < height and tiles[ny][nx] == TILE_FLOOR:
                        tiles[ny][nx] = TILE_SIGN
                        break
    
    # 花壇（装飾用）
    for i in range(3, width-3, 7):
        for j in range(3, height-3, 7):
            if tiles[j][i] == TILE_FLOOR:
                tiles[j][i] = TILE_FLOWERBED
def get_storage_town_map():
    """Storage Town map data"""
    width = 30
    height = 30
    tiles = [[TILE_FLOOR for _ in range(width)] for _ in range(height)]
    
    # Surround with walls
    for x in range(width):
        tiles[0][x] = TILE_WALL
        tiles[height-1][x] = TILE_WALL
    for y in range(height):
        tiles[y][0] = TILE_WALL
        tiles[y][width-1] = TILE_WALL
    
    # Main roads - wider and more natural
    center_x = width // 2
    center_y = height // 2
    
    # Horizontal main road (wider)
    for x in range(1, width-1):
        tiles[center_y][x] = TILE_ROAD
        tiles[center_y-1][x] = TILE_ROAD
        tiles[center_y+1][x] = TILE_ROAD
        
    # Vertical main road (wider)
    for y in range(1, height-1):
        tiles[y][center_x] = TILE_ROAD
        tiles[y][center_x-1] = TILE_ROAD
        tiles[y][center_x+1] = TILE_ROAD
    
    # Secondary roads - more natural, curved paths
    # North area road
    for x in range(5, width-5):
        road_y = center_y - 6
        if 1 <= road_y < height-1:
            tiles[road_y][x] = TILE_ROAD
            # Add some variation
            if x % 5 == 0 and road_y > 2:
                tiles[road_y-1][x] = TILE_ROAD
    
    # South area road
    for x in range(5, width-5):
        road_y = center_y + 6
        if 1 <= road_y < height-1:
            tiles[road_y][x] = TILE_ROAD
            # Add some variation
            if x % 5 == 0 and road_y < height-2:
                tiles[road_y+1][x] = TILE_ROAD
                
    # East area road
    for y in range(5, height-5):
        road_x = center_x + 6
        if 1 <= road_x < width-1:
            tiles[y][road_x] = TILE_ROAD
            # Add some variation
            if y % 5 == 0 and road_x < width-2:
                tiles[y][road_x+1] = TILE_ROAD
                
    # West area road
    for y in range(5, height-5):
        road_x = center_x - 6
        if 1 <= road_x < width-1:
            tiles[y][road_x] = TILE_ROAD
            # Add some variation
            if y % 5 == 0 and road_x > 2:
                tiles[y][road_x-1] = TILE_ROAD
    
    # Buildings - properly enclosed with single doors
    buildings = []
    
    # Create shop buildings first (to ensure they're in good locations)
    # S3 Storage shop building
    s3_shop_x, s3_shop_y = 5, 5
    s3_shop_w, s3_shop_h = 5, 5
    
    # Create S3 shop building
    for bx in range(s3_shop_x, s3_shop_x+s3_shop_w):
        for by in range(s3_shop_y, s3_shop_y+s3_shop_h):
            if 1 <= bx < width-1 and 1 <= by < height-1:
                if bx == s3_shop_x or bx == s3_shop_x+s3_shop_w-1 or by == s3_shop_y or by == s3_shop_y+s3_shop_h-1:
                    tiles[by][bx] = TILE_WALL
                else:
                    tiles[by][bx] = TILE_FLOOR
    
    # Add door to S3 shop
    door_x = s3_shop_x + s3_shop_w//2
    door_y = s3_shop_y + s3_shop_h - 1
    tiles[door_y][door_x] = TILE_DOOR
    
    # Place shop tile inside the building
    shop_x = s3_shop_x + s3_shop_w//2
    shop_y = s3_shop_y + s3_shop_h//2
    tiles[shop_y][shop_x] = TILE_SHOP
    
    # Glacier Archive shop building
    glacier_shop_x, glacier_shop_y = 20, 5
    glacier_shop_w, glacier_shop_h = 5, 5
    
    # Create Glacier shop building
    for bx in range(glacier_shop_x, glacier_shop_x+glacier_shop_w):
        for by in range(glacier_shop_y, glacier_shop_y+glacier_shop_h):
            if 1 <= bx < width-1 and 1 <= by < height-1:
                if bx == glacier_shop_x or bx == glacier_shop_x+glacier_shop_w-1 or by == glacier_shop_y or by == glacier_shop_y+glacier_shop_h-1:
                    tiles[by][bx] = TILE_WALL
                else:
                    tiles[by][bx] = TILE_FLOOR
    
    # Add door to Glacier shop
    door_x = glacier_shop_x + glacier_shop_w//2
    door_y = glacier_shop_y + glacier_shop_h - 1
    tiles[door_y][door_x] = TILE_DOOR
    
    # Place shop tile inside the building
    shop_x = glacier_shop_x + glacier_shop_w//2
    shop_y = glacier_shop_y + glacier_shop_h//2
    tiles[shop_y][shop_x] = TILE_SHOP
    
    # EFS shop building
    efs_shop_x, efs_shop_y = 5, 20
    efs_shop_w, efs_shop_h = 5, 5
    
    # Create EFS shop building
    for bx in range(efs_shop_x, efs_shop_x+efs_shop_w):
        for by in range(efs_shop_y, efs_shop_y+efs_shop_h):
            if 1 <= bx < width-1 and 1 <= by < height-1:
                if bx == efs_shop_x or bx == efs_shop_x+efs_shop_w-1 or by == efs_shop_y or by == efs_shop_y+efs_shop_h-1:
                    tiles[by][bx] = TILE_WALL
                else:
                    tiles[by][bx] = TILE_FLOOR
    
    # Add door to EFS shop
    door_x = efs_shop_x + efs_shop_w//2
    door_y = efs_shop_y + efs_shop_h - 1
    tiles[door_y][door_x] = TILE_DOOR
    
    # Place shop tile inside the building
    shop_x = efs_shop_x + efs_shop_w//2
    shop_y = efs_shop_y + efs_shop_h//2
    tiles[shop_y][shop_x] = TILE_SHOP
    
    # Inn building
    inn_x, inn_y = 20, 20
    inn_w, inn_h = 6, 6
    
    # Create inn building
    for bx in range(inn_x, inn_x+inn_w):
        for by in range(inn_y, inn_y+inn_h):
            if 1 <= bx < width-1 and 1 <= by < height-1:
                if bx == inn_x or bx == inn_x+inn_w-1 or by == inn_y or by == inn_y+inn_h-1:
                    tiles[by][bx] = TILE_WALL
                else:
                    tiles[by][bx] = TILE_FLOOR
    
    # Add door to inn
    door_x = inn_x + inn_w//2
    door_y = inn_y + inn_h - 1
    tiles[door_y][door_x] = TILE_DOOR
    
    # Place inn tile inside the building
    inn_tile_x = inn_x + inn_w//2
    inn_tile_y = inn_y + inn_h//2
    tiles[inn_tile_y][inn_tile_x] = TILE_INN
    
    # Main service buildings (for AWS services)
    service_buildings = [
        (12, 12, 6, 6),  # Center - S3
        (3, 3, 4, 4),    # Northwest corner - EBS
        (23, 3, 4, 4),   # Northeast corner - EFS
    ]
    
    for x, y, w, h in service_buildings:
        # Create building
        for bx in range(x, x+w):
            for by in range(y, y+h):
                if 1 <= bx < width-1 and 1 <= by < height-1:
                    if bx == x or bx == x+w-1 or by == y or by == y+h-1:
                        tiles[by][bx] = TILE_WALL
                    else:
                        tiles[by][bx] = TILE_FLOOR
        
        # Add door (only one door per building)
        door_x = x + w//2
        door_y = y + h - 1
        if 1 <= door_x < width-1 and 1 <= door_y < height-1:
            tiles[door_y][door_x] = TILE_DOOR
        
        buildings.append((x, y, w, h))
    
    # Smaller houses (more of them, scattered around)
    for _ in range(8):
        w = random.randint(3, 4)
        h = random.randint(3, 4)
        x = random.randint(2, width-w-2)
        y = random.randint(2, height-h-2)
        
        # Check if overlaps with roads or other buildings
        valid = True
        for bx in range(x-1, x+w+1):
            for by in range(y-1, y+h+1):
                if 0 <= bx < width and 0 <= by < height:
                    if tiles[by][bx] in [TILE_ROAD, TILE_WALL, TILE_DOOR, TILE_SHOP, TILE_INN]:
                        valid = False
                        break
        
        if valid:
            # Create building with proper walls
            for bx in range(x, x+w):
                for by in range(y, y+h):
                    if bx == x or bx == x+w-1 or by == y or by == y+h-1:
                        tiles[by][bx] = TILE_WALL
                    else:
                        tiles[by][bx] = TILE_FLOOR
            
            # Add door (only one door per building)
            door_x = x + w//2
            door_y = y + h - 1
            tiles[door_y][door_x] = TILE_DOOR
            
            buildings.append((x, y, w, h))
    
    # Decorations
    for _ in range(5):
        x = random.randint(1, width-2)
        y = random.randint(1, height-2)
        if tiles[y][x] == TILE_ROAD:
            tiles[y][x] = TILE_FOUNTAIN
    
    for _ in range(10):
        x = random.randint(1, width-2)
        y = random.randint(1, height-2)
        if tiles[y][x] == TILE_ROAD:
            tiles[y][x] = TILE_BENCH
    
    for _ in range(15):
        x = random.randint(1, width-2)
        y = random.randint(1, height-2)
        if tiles[y][x] == TILE_ROAD:
            tiles[y][x] = TILE_LAMP
            
    # Portal back to world map
    tiles[height-2][width//2] = TILE_PORTAL
    
    # NPCs
    npcs = [
        {
            "x": 14,
            "y": 14,
            "name": "S3",
            "dialog": "Hello, I'm S3. I provide scalable object storage for all your data needs. You can store and retrieve any amount of data, anytime, anywhere!",
            "is_service": True,
            "service_id": "s3"
        },
        {
            "x": 5,
            "y": 5,
            "name": "EBS",
            "dialog": "Hi, I'm EBS. I provide block storage volumes for your EC2 instances. I'm like a hard drive for your cloud servers!",
            "is_service": True,
            "service_id": "ebs"
        },
        {
            "x": 25,
            "y": 5,
            "name": "EFS",
            "dialog": "I'm EFS, Elastic File System. I provide scalable file storage for your EC2 instances. Multiple instances can access me simultaneously!",
            "is_service": True,
            "service_id": "efs"
        },
        {
            "x": 5,
            "y": 25,
            "name": "Glacier",
            "dialog": "I'm Glacier. I provide low-cost archive storage. If you don't need to access your data frequently, I'm your best choice!",
            "is_service": True,
            "service_id": "glacier"
        },
        {
            "x": 25,
            "y": 25,
            "name": "Storage Gateway",
            "dialog": "I'm Storage Gateway. I connect your on-premises applications with AWS cloud storage. I'm the bridge between your data center and the cloud!",
            "is_service": True,
            "service_id": "storage_gateway"
        }
    ]
    
    # Portal data
    portals = [
        {
            "x": width//2,
            "y": height-2,
            "destination": "AWS Cloud World",
            "dest_x": 10,
            "dest_y": 11
        }
    ]
    
    # Shop data
    shops = [
        {
            "x": s3_shop_x + s3_shop_w//2,
            "y": s3_shop_y + s3_shop_h//2,
            "name": "S3 Storage Shop",
            "type": "items",
            "dialog": "Welcome to S3 Storage Shop! We have the best storage items!",
            "items": ["storage_potion", "backup_scroll", "data_shield", "cloud_elixir"]
        },
        {
            "x": glacier_shop_x + glacier_shop_w//2,
            "y": glacier_shop_y + glacier_shop_h//2,
            "name": "Glacier Archive",
            "type": "weapons",
            "dialog": "Welcome to Glacier Archive! Our weapons are cold but powerful!",
            "items": ["ice_sword", "frost_dagger", "glacier_axe", "archive_staff"]
        },
        {
            "x": efs_shop_x + efs_shop_w//2,
            "y": efs_shop_y + efs_shop_h//2,
            "name": "EFS Equipment",
            "type": "armor",
            "dialog": "Welcome to EFS Equipment! Our armor is shared across all warriors!",
            "items": ["elastic_shield", "scalable_helmet", "shared_breastplate", "file_boots"]
        }
    ]
    
    # Return map data
    return {
        "name": "Storage Town",
        "width": width,
        "height": height,
        "tiles": tiles,
        "npcs": npcs,
        "portals": portals,
        "shops": shops,
        "encounter_rate": 0.0  # No random encounters in town
    }
def get_database_town_map():
    """Database Town map data"""
    width = 30
    height = 30
    tiles = [[TILE_FLOOR for _ in range(width)] for _ in range(height)]
    
    # Surround with walls
    for x in range(width):
        tiles[0][x] = TILE_WALL
        tiles[height-1][x] = TILE_WALL
    for y in range(height):
        tiles[y][0] = TILE_WALL
        tiles[y][width-1] = TILE_WALL
    
    # Main roads - wider and more natural
    center_x = width // 2
    center_y = height // 2
    
    # Horizontal main road (wider)
    for x in range(1, width-1):
        tiles[center_y][x] = TILE_ROAD
        tiles[center_y-1][x] = TILE_ROAD
        tiles[center_y+1][x] = TILE_ROAD
        
    # Vertical main road (wider)
    for y in range(1, height-1):
        tiles[y][center_x] = TILE_ROAD
        tiles[y][center_x-1] = TILE_ROAD
        tiles[y][center_x+1] = TILE_ROAD
    
    # Secondary roads - more natural, curved paths
    # North area road
    for x in range(5, width-5):
        road_y = center_y - 6
        if 1 <= road_y < height-1:
            tiles[road_y][x] = TILE_ROAD
            # Add some variation
            if x % 5 == 0 and road_y > 2:
                tiles[road_y-1][x] = TILE_ROAD
    
    # South area road
    for x in range(5, width-5):
        road_y = center_y + 6
        if 1 <= road_y < height-1:
            tiles[road_y][x] = TILE_ROAD
            # Add some variation
            if x % 5 == 0 and road_y < height-2:
                tiles[road_y+1][x] = TILE_ROAD
                
    # East area road
    for y in range(5, height-5):
        road_x = center_x + 6
        if 1 <= road_x < width-1:
            tiles[y][road_x] = TILE_ROAD
            # Add some variation
            if y % 5 == 0 and road_x < width-2:
                tiles[y][road_x+1] = TILE_ROAD
                
    # West area road
    for y in range(5, height-5):
        road_x = center_x - 6
        if 1 <= road_x < width-1:
            tiles[y][road_x] = TILE_ROAD
            # Add some variation
            if y % 5 == 0 and road_x > 2:
                tiles[y][road_x-1] = TILE_ROAD
    
    # Buildings - properly enclosed with single doors
    buildings = []
    
    # Create shop buildings first (to ensure they're in good locations)
    # RDS shop building
    rds_shop_x, rds_shop_y = 5, 5
    rds_shop_w, rds_shop_h = 5, 5
    
    # Create RDS shop building
    for bx in range(rds_shop_x, rds_shop_x+rds_shop_w):
        for by in range(rds_shop_y, rds_shop_y+rds_shop_h):
            if 1 <= bx < width-1 and 1 <= by < height-1:
                if bx == rds_shop_x or bx == rds_shop_x+rds_shop_w-1 or by == rds_shop_y or by == rds_shop_y+rds_shop_h-1:
                    tiles[by][bx] = TILE_WALL
                else:
                    tiles[by][bx] = TILE_FLOOR
    
    # Add door to RDS shop
    door_x = rds_shop_x + rds_shop_w//2
    door_y = rds_shop_y + rds_shop_h - 1
    tiles[door_y][door_x] = TILE_DOOR
    
    # Place shop tile inside the building
    shop_x = rds_shop_x + rds_shop_w//2
    shop_y = rds_shop_y + rds_shop_h//2
    tiles[shop_y][shop_x] = TILE_SHOP
    
    # DynamoDB shop building
    dynamo_shop_x, dynamo_shop_y = 20, 5
    dynamo_shop_w, dynamo_shop_h = 5, 5
    
    # Create DynamoDB shop building
    for bx in range(dynamo_shop_x, dynamo_shop_x+dynamo_shop_w):
        for by in range(dynamo_shop_y, dynamo_shop_y+dynamo_shop_h):
            if 1 <= bx < width-1 and 1 <= by < height-1:
                if bx == dynamo_shop_x or bx == dynamo_shop_x+dynamo_shop_w-1 or by == dynamo_shop_y or by == dynamo_shop_y+dynamo_shop_h-1:
                    tiles[by][bx] = TILE_WALL
                else:
                    tiles[by][bx] = TILE_FLOOR
    
    # Add door to DynamoDB shop
    door_x = dynamo_shop_x + dynamo_shop_w//2
    door_y = dynamo_shop_y + dynamo_shop_h - 1
    tiles[door_y][door_x] = TILE_DOOR
    
    # Place shop tile inside the building
    shop_x = dynamo_shop_x + dynamo_shop_w//2
    shop_y = dynamo_shop_y + dynamo_shop_h//2
    tiles[shop_y][shop_x] = TILE_SHOP
    
    # Aurora shop building
    aurora_shop_x, aurora_shop_y = 5, 20
    aurora_shop_w, aurora_shop_h = 5, 5
    
    # Create Aurora shop building
    for bx in range(aurora_shop_x, aurora_shop_x+aurora_shop_w):
        for by in range(aurora_shop_y, aurora_shop_y+aurora_shop_h):
            if 1 <= bx < width-1 and 1 <= by < height-1:
                if bx == aurora_shop_x or bx == aurora_shop_x+aurora_shop_w-1 or by == aurora_shop_y or by == aurora_shop_y+aurora_shop_h-1:
                    tiles[by][bx] = TILE_WALL
                else:
                    tiles[by][bx] = TILE_FLOOR
    
    # Add door to Aurora shop
    door_x = aurora_shop_x + aurora_shop_w//2
    door_y = aurora_shop_y + aurora_shop_h - 1
    tiles[door_y][door_x] = TILE_DOOR
    
    # Place shop tile inside the building
    shop_x = aurora_shop_x + aurora_shop_w//2
    shop_y = aurora_shop_y + aurora_shop_h//2
    tiles[shop_y][shop_x] = TILE_SHOP
    
    # Inn building
    inn_x, inn_y = 20, 20
    inn_w, inn_h = 6, 6
    
    # Create inn building
    for bx in range(inn_x, inn_x+inn_w):
        for by in range(inn_y, inn_y+inn_h):
            if 1 <= bx < width-1 and 1 <= by < height-1:
                if bx == inn_x or bx == inn_x+inn_w-1 or by == inn_y or by == inn_y+inn_h-1:
                    tiles[by][bx] = TILE_WALL
                else:
                    tiles[by][bx] = TILE_FLOOR
    
    # Add door to inn
    door_x = inn_x + inn_w//2
    door_y = inn_y + inn_h - 1
    tiles[door_y][door_x] = TILE_DOOR
    
    # Place inn tile inside the building
    inn_tile_x = inn_x + inn_w//2
    inn_tile_y = inn_y + inn_h//2
    tiles[inn_tile_y][inn_tile_x] = TILE_INN
    
    # Main service buildings (for AWS services)
    service_buildings = [
        (12, 12, 6, 6),  # Center - RDS
        (3, 3, 4, 4),    # Northwest corner - DynamoDB
        (23, 3, 4, 4),   # Northeast corner - Aurora
    ]
    
    for x, y, w, h in service_buildings:
        # Create building
        for bx in range(x, x+w):
            for by in range(y, y+h):
                if 1 <= bx < width-1 and 1 <= by < height-1:
                    if bx == x or bx == x+w-1 or by == y or by == y+h-1:
                        tiles[by][bx] = TILE_WALL
                    else:
                        tiles[by][bx] = TILE_FLOOR
        
        # Add door (only one door per building)
        door_x = x + w//2
        door_y = y + h - 1
        if 1 <= door_x < width-1 and 1 <= door_y < height-1:
            tiles[door_y][door_x] = TILE_DOOR
        
        buildings.append((x, y, w, h))
    
    # Smaller houses (more of them, scattered around)
    for _ in range(8):
        w = random.randint(3, 4)
        h = random.randint(3, 4)
        x = random.randint(2, width-w-2)
        y = random.randint(2, height-h-2)
        
        # Check if overlaps with roads or other buildings
        valid = True
        for bx in range(x-1, x+w+1):
            for by in range(y-1, y+h+1):
                if 0 <= bx < width and 0 <= by < height:
                    if tiles[by][bx] in [TILE_ROAD, TILE_WALL, TILE_DOOR, TILE_SHOP, TILE_INN]:
                        valid = False
                        break
        
        if valid:
            # Create building with proper walls
            for bx in range(x, x+w):
                for by in range(y, y+h):
                    if bx == x or bx == x+w-1 or by == y or by == y+h-1:
                        tiles[by][bx] = TILE_WALL
                    else:
                        tiles[by][bx] = TILE_FLOOR
            
            # Add door (only one door per building)
            door_x = x + w//2
            door_y = y + h - 1
            tiles[door_y][door_x] = TILE_DOOR
            
            buildings.append((x, y, w, h))
    
    # Decorations
    for _ in range(5):
        x = random.randint(1, width-2)
        y = random.randint(1, height-2)
        if tiles[y][x] == TILE_ROAD:
            tiles[y][x] = TILE_FOUNTAIN
    
    for _ in range(10):
        x = random.randint(1, width-2)
        y = random.randint(1, height-2)
        if tiles[y][x] == TILE_ROAD:
            tiles[y][x] = TILE_BENCH
    
    for _ in range(15):
        x = random.randint(1, width-2)
        y = random.randint(1, height-2)
        if tiles[y][x] == TILE_ROAD:
            tiles[y][x] = TILE_LAMP
            
    # Portal back to world map
    tiles[height-2][width//2] = TILE_PORTAL
    
    # NPCs
    npcs = [
        {
            "x": 14,
            "y": 14,
            "name": "RDS",
            "dialog": "Hello, I'm RDS. I provide managed relational database services. I support MySQL, PostgreSQL, MariaDB, Oracle, and SQL Server!",
            "is_service": True,
            "service_id": "rds"
        },
        {
            "x": 5,
            "y": 5,
            "name": "DynamoDB",
            "dialog": "Hi, I'm DynamoDB. I'm a NoSQL database service that provides fast and predictable performance with seamless scalability!",
            "is_service": True,
            "service_id": "dynamodb"
        },
        {
            "x": 25,
            "y": 5,
            "name": "Aurora",
            "dialog": "I'm Aurora. I'm a MySQL and PostgreSQL-compatible relational database built for the cloud. I'm up to five times faster than standard MySQL databases!",
            "is_service": True,
            "service_id": "aurora"
        },
        {
            "x": 5,
            "y": 25,
            "name": "ElastiCache",
            "dialog": "I'm ElastiCache. I make it easy to deploy, operate, and scale an in-memory cache in the cloud. I can improve the performance of your applications!",
            "is_service": True,
            "service_id": "elasticache"
        },
        {
            "x": 25,
            "y": 25,
            "name": "Neptune",
            "dialog": "I'm Neptune. I'm a fast, reliable, fully-managed graph database service. I support popular graph models and their query languages!",
            "is_service": True,
            "service_id": "neptune"
        }
    ]
    
    # Portal data
    portals = [
        {
            "x": width//2,
            "y": height-2,
            "destination": "AWS Cloud World",
            "dest_x": 10,
            "dest_y": 11
        }
    ]
    
    # Shop data
    shops = [
        {
            "x": rds_shop_x + rds_shop_w//2,
            "y": rds_shop_y + rds_shop_h//2,
            "name": "RDS Relational Shop",
            "type": "items",
            "dialog": "Welcome to RDS Relational Shop! Our items are well-structured!",
            "items": ["sql_potion", "relation_scroll", "index_shield", "transaction_elixir"]
        },
        {
            "x": dynamo_shop_x + dynamo_shop_w//2,
            "y": dynamo_shop_y + dynamo_shop_h//2,
            "name": "DynamoDB NoSQL Shop",
            "type": "weapons",
            "dialog": "Welcome to DynamoDB NoSQL Shop! Our weapons scale infinitely!",
            "items": ["nosql_sword", "document_dagger", "key_value_axe", "partition_staff"]
        },
        {
            "x": aurora_shop_x + aurora_shop_w//2,
            "y": aurora_shop_y + aurora_shop_h//2,
            "name": "Aurora Equipment",
            "type": "armor",
            "dialog": "Welcome to Aurora Equipment! Our armor is compatible with all your needs!",
            "items": ["mysql_shield", "postgres_helmet", "cluster_breastplate", "replica_boots"]
        }
    ]
    
    # Return map data
    return {
        "name": "Database Town",
        "width": width,
        "height": height,
        "tiles": tiles,
        "npcs": npcs,
        "portals": portals,
        "shops": shops,
        "encounter_rate": 0.0  # No random encounters in town
    }
def get_security_town_map():
    """Security Town map data"""
    width = 30
    height = 30
    tiles = [[TILE_FLOOR for _ in range(width)] for _ in range(height)]
    
    # Surround with walls
    for x in range(width):
        tiles[0][x] = TILE_WALL
        tiles[height-1][x] = TILE_WALL
    for y in range(height):
        tiles[y][0] = TILE_WALL
        tiles[y][width-1] = TILE_WALL
    
    # Main roads - wider and more natural
    center_x = width // 2
    center_y = height // 2
    
    # Horizontal main road (wider)
    for x in range(1, width-1):
        tiles[center_y][x] = TILE_ROAD
        tiles[center_y-1][x] = TILE_ROAD
        tiles[center_y+1][x] = TILE_ROAD
        
    # Vertical main road (wider)
    for y in range(1, height-1):
        tiles[y][center_x] = TILE_ROAD
        tiles[y][center_x-1] = TILE_ROAD
        tiles[y][center_x+1] = TILE_ROAD
    
    # Secondary roads - more natural, curved paths
    # North area road
    for x in range(5, width-5):
        road_y = center_y - 6
        if 1 <= road_y < height-1:
            tiles[road_y][x] = TILE_ROAD
            # Add some variation
            if x % 5 == 0 and road_y > 2:
                tiles[road_y-1][x] = TILE_ROAD
    
    # South area road
    for x in range(5, width-5):
        road_y = center_y + 6
        if 1 <= road_y < height-1:
            tiles[road_y][x] = TILE_ROAD
            # Add some variation
            if x % 5 == 0 and road_y < height-2:
                tiles[road_y+1][x] = TILE_ROAD
                
    # East area road
    for y in range(5, height-5):
        road_x = center_x + 6
        if 1 <= road_x < width-1:
            tiles[y][road_x] = TILE_ROAD
            # Add some variation
            if y % 5 == 0 and road_x < width-2:
                tiles[y][road_x+1] = TILE_ROAD
                
    # West area road
    for y in range(5, height-5):
        road_x = center_x - 6
        if 1 <= road_x < width-1:
            tiles[y][road_x] = TILE_ROAD
            # Add some variation
            if y % 5 == 0 and road_x > 2:
                tiles[y][road_x-1] = TILE_ROAD
    
    # Buildings - properly enclosed with single doors
    buildings = []
    
    # Create shop buildings first (to ensure they're in good locations)
    # IAM shop building
    iam_shop_x, iam_shop_y = 5, 5
    iam_shop_w, iam_shop_h = 5, 5
    
    # Create IAM shop building
    for bx in range(iam_shop_x, iam_shop_x+iam_shop_w):
        for by in range(iam_shop_y, iam_shop_y+iam_shop_h):
            if 1 <= bx < width-1 and 1 <= by < height-1:
                if bx == iam_shop_x or bx == iam_shop_x+iam_shop_w-1 or by == iam_shop_y or by == iam_shop_y+iam_shop_h-1:
                    tiles[by][bx] = TILE_WALL
                else:
                    tiles[by][bx] = TILE_FLOOR
    
    # Add door to IAM shop
    door_x = iam_shop_x + iam_shop_w//2
    door_y = iam_shop_y + iam_shop_h - 1
    tiles[door_y][door_x] = TILE_DOOR
    
    # Place shop tile inside the building
    shop_x = iam_shop_x + iam_shop_w//2
    shop_y = iam_shop_y + iam_shop_h//2
    tiles[shop_y][shop_x] = TILE_SHOP
    
    # WAF shop building
    waf_shop_x, waf_shop_y = 20, 5
    waf_shop_w, waf_shop_h = 5, 5
    
    # Create WAF shop building
    for bx in range(waf_shop_x, waf_shop_x+waf_shop_w):
        for by in range(waf_shop_y, waf_shop_y+waf_shop_h):
            if 1 <= bx < width-1 and 1 <= by < height-1:
                if bx == waf_shop_x or bx == waf_shop_x+waf_shop_w-1 or by == waf_shop_y or by == waf_shop_y+waf_shop_h-1:
                    tiles[by][bx] = TILE_WALL
                else:
                    tiles[by][bx] = TILE_FLOOR
    
    # Add door to WAF shop
    door_x = waf_shop_x + waf_shop_w//2
    door_y = waf_shop_y + waf_shop_h - 1
    tiles[door_y][door_x] = TILE_DOOR
    
    # Place shop tile inside the building
    shop_x = waf_shop_x + waf_shop_w//2
    shop_y = waf_shop_y + waf_shop_h//2
    tiles[shop_y][shop_x] = TILE_SHOP
    
    # Shield shop building
    shield_shop_x, shield_shop_y = 5, 20
    shield_shop_w, shield_shop_h = 5, 5
    
    # Create Shield shop building
    for bx in range(shield_shop_x, shield_shop_x+shield_shop_w):
        for by in range(shield_shop_y, shield_shop_y+shield_shop_h):
            if 1 <= bx < width-1 and 1 <= by < height-1:
                if bx == shield_shop_x or bx == shield_shop_x+shield_shop_w-1 or by == shield_shop_y or by == shield_shop_y+shield_shop_h-1:
                    tiles[by][bx] = TILE_WALL
                else:
                    tiles[by][bx] = TILE_FLOOR
    
    # Add door to Shield shop
    door_x = shield_shop_x + shield_shop_w//2
    door_y = shield_shop_y + shield_shop_h - 1
    tiles[door_y][door_x] = TILE_DOOR
    
    # Place shop tile inside the building
    shop_x = shield_shop_x + shield_shop_w//2
    shop_y = shield_shop_y + shield_shop_h//2
    tiles[shop_y][shop_x] = TILE_SHOP
    
    # Inn building
    inn_x, inn_y = 20, 20
    inn_w, inn_h = 6, 6
    
    # Create inn building
    for bx in range(inn_x, inn_x+inn_w):
        for by in range(inn_y, inn_y+inn_h):
            if 1 <= bx < width-1 and 1 <= by < height-1:
                if bx == inn_x or bx == inn_x+inn_w-1 or by == inn_y or by == inn_y+inn_h-1:
                    tiles[by][bx] = TILE_WALL
                else:
                    tiles[by][bx] = TILE_FLOOR
    
    # Add door to inn
    door_x = inn_x + inn_w//2
    door_y = inn_y + inn_h - 1
    tiles[door_y][door_x] = TILE_DOOR
    
    # Place inn tile inside the building
    inn_tile_x = inn_x + inn_w//2
    inn_tile_y = inn_y + inn_h//2
    tiles[inn_tile_y][inn_tile_x] = TILE_INN
    
    # Main service buildings (for AWS services)
    service_buildings = [
        (12, 12, 6, 6),  # Center - IAM
        (3, 3, 4, 4),    # Northwest corner - WAF
        (23, 3, 4, 4),   # Northeast corner - Shield
    ]
    
    for x, y, w, h in service_buildings:
        # Create building
        for bx in range(x, x+w):
            for by in range(y, y+h):
                if 1 <= bx < width-1 and 1 <= by < height-1:
                    if bx == x or bx == x+w-1 or by == y or by == y+h-1:
                        tiles[by][bx] = TILE_WALL
                    else:
                        tiles[by][bx] = TILE_FLOOR
        
        # Add door (only one door per building)
        door_x = x + w//2
        door_y = y + h - 1
        if 1 <= door_x < width-1 and 1 <= door_y < height-1:
            tiles[door_y][door_x] = TILE_DOOR
        
        buildings.append((x, y, w, h))
    
    # Smaller houses (more of them, scattered around)
    for _ in range(8):
        w = random.randint(3, 4)
        h = random.randint(3, 4)
        x = random.randint(2, width-w-2)
        y = random.randint(2, height-h-2)
        
        # Check if overlaps with roads or other buildings
        valid = True
        for bx in range(x-1, x+w+1):
            for by in range(y-1, y+h+1):
                if 0 <= bx < width and 0 <= by < height:
                    if tiles[by][bx] in [TILE_ROAD, TILE_WALL, TILE_DOOR, TILE_SHOP, TILE_INN]:
                        valid = False
                        break
        
        if valid:
            # Create building with proper walls
            for bx in range(x, x+w):
                for by in range(y, y+h):
                    if bx == x or bx == x+w-1 or by == y or by == y+h-1:
                        tiles[by][bx] = TILE_WALL
                    else:
                        tiles[by][bx] = TILE_FLOOR
            
            # Add door (only one door per building)
            door_x = x + w//2
            door_y = y + h - 1
            tiles[door_y][door_x] = TILE_DOOR
            
            buildings.append((x, y, w, h))
    
    # Decorations
    for _ in range(5):
        x = random.randint(1, width-2)
        y = random.randint(1, height-2)
        if tiles[y][x] == TILE_ROAD:
            tiles[y][x] = TILE_FOUNTAIN
    
    for _ in range(10):
        x = random.randint(1, width-2)
        y = random.randint(1, height-2)
        if tiles[y][x] == TILE_ROAD:
            tiles[y][x] = TILE_BENCH
    
    for _ in range(15):
        x = random.randint(1, width-2)
        y = random.randint(1, height-2)
        if tiles[y][x] == TILE_ROAD:
            tiles[y][x] = TILE_LAMP
            
    # Portal back to world map
    tiles[height-2][width//2] = TILE_PORTAL
    
    # NPCs
    npcs = [
        {
            "x": 14,
            "y": 14,
            "name": "IAM",
            "dialog": "Hello, I'm IAM. I help you securely control access to AWS resources. I manage permissions that determine which actions users can perform.",
            "is_service": True,
            "service_id": "iam"
        },
        {
            "x": 5,
            "y": 5,
            "name": "WAF",
            "dialog": "Hi, I'm WAF. I protect your web applications from common web exploits that could affect application availability or compromise security.",
            "is_service": True,
            "service_id": "waf"
        },
        {
            "x": 25,
            "y": 5,
            "name": "Shield",
            "dialog": "I'm Shield. I provide protection against DDoS attacks. I safeguard your applications running on AWS.",
            "is_service": True,
            "service_id": "shield"
        },
        {
            "x": 5,
            "y": 25,
            "name": "GuardDuty",
            "dialog": "I'm GuardDuty. I'm a threat detection service that continuously monitors for malicious activity and unauthorized behavior.",
            "is_service": True,
            "service_id": "guardduty"
        },
        {
            "x": 25,
            "y": 25,
            "name": "Macie",
            "dialog": "I'm Macie. I use machine learning to automatically discover, classify, and protect sensitive data stored in S3.",
            "is_service": True,
            "service_id": "macie"
        }
    ]
    
    # Portal data
    portals = [
        {
            "x": width//2,
            "y": height-2,
            "destination": "AWS Cloud World",
            "dest_x": 40,
            "dest_y": 39
        }
    ]
    
    # Shop data
    shops = [
        {
            "x": iam_shop_x + iam_shop_w//2,
            "y": iam_shop_y + iam_shop_h//2,
            "name": "IAM Identity Shop",
            "type": "items",
            "dialog": "Welcome to IAM Identity Shop! Our items will protect your identity!",
            "items": ["role_potion", "policy_scroll", "permission_shield", "identity_elixir"]
        },
        {
            "x": waf_shop_x + waf_shop_w//2,
            "y": waf_shop_y + waf_shop_h//2,
            "name": "WAF Weapons",
            "type": "weapons",
            "dialog": "Welcome to WAF Weapons! Our weapons will protect your applications!",
            "items": ["firewall_sword", "rule_dagger", "filter_axe", "protection_staff"]
        },
        {
            "x": shield_shop_x + shield_shop_w//2,
            "y": shield_shop_y + shield_shop_h//2,
            "name": "Shield Armory",
            "type": "armor",
            "dialog": "Welcome to Shield Armory! Our armor will protect you from any attack!",
            "items": ["ddos_shield", "protection_helmet", "advanced_breastplate", "standard_boots"]
        }
    ]
    
    # Return map data
    return {
        "name": "Security Town",
        "width": width,
        "height": height,
        "tiles": tiles,
        "npcs": npcs,
        "portals": portals,
        "shops": shops,
        "encounter_rate": 0.0  # No random encounters in town
    }
