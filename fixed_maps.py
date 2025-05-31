#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import random

# タイルタイプの定数
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
TILE_FOUNTAIN = 13
TILE_BENCH = 14
TILE_LAMP = 15
TILE_SIGN = 16
TILE_FLOWERBED = 17

# 固定マップデータ
def get_world_map():
    """メインワールドマップのデータを返す"""
    # 50x50のマップを作成
    width = 50
    height = 50
    tiles = [[TILE_GRASS for _ in range(width)] for _ in range(height)]
    
    # 外周を壁に
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
            "name": "旅人",
            "dialog": "この世界には4つの町があるよ。北西にComputing Town、北東にStorage Town、南西にDatabase Town、南東にSecurity Townだ。"
        },
        {
            "x": 30,
            "y": 25,
            "name": "商人",
            "dialog": "各町にはそれぞれ特色のあるショップがあるぞ。Computing Townは武器、Storage Townは防具、Database Townは回復アイテム、Security Townは特殊アイテムを扱っている。"
        },
        {
            "x": 20,
            "y": 30,
            "name": "老人",
            "dialog": "AWSサービスたちは町に住んでいるが、彼らの力を借りるにはクイズに答えなければならない。しっかり勉強するんだぞ。"
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
        "encounter_rate": 0.03
    }

def get_computing_town_map():
    """Computing Townのマップデータを返す"""
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
    
    # 格子状の道路（固定パターン）
    for x in range(width):
        if x % 6 == 0:
            for y in range(height):
                tiles[y][x] = TILE_ROAD
    
    for y in range(height):
        if y % 6 == 0:
            for x in range(width):
                tiles[y][x] = TILE_ROAD
    
    # サーバーラック風の建物（固定位置）
    rack_positions = [
        (3, 3, 3, 5),  # (x, y, 幅, 高さ)
        (10, 3, 3, 5),
        (17, 3, 3, 5),
        (24, 3, 3, 5),
        (3, 10, 3, 5),
        (10, 10, 3, 5),
        (17, 10, 3, 5),
        (24, 10, 3, 5),
        (3, 17, 3, 5),
        (10, 17, 3, 5),
        (17, 17, 3, 5),
        (24, 17, 3, 5)
    ]
    
    for x, y, w, h in rack_positions:
        # 建物の外周を壁に
        for bx in range(x, x+w):
            for by in range(y, y+h):
                if bx == x or bx == x+w-1 or by == y or by == y+h-1:
                    tiles[by][bx] = TILE_WALL
                else:
                    tiles[by][bx] = TILE_FLOOR
        
        # ドアを追加（建物の下側中央）
        door_x = x + w // 2
        door_y = y + h - 1
        if 0 <= door_x < width and 0 <= door_y < height:
            tiles[door_y][door_x] = TILE_DOOR
    
    # 中央に大きなデータセンター
    for x in range(12, 18):
        for y in range(10, 16):
            if x == 12 or x == 17 or y == 10 or y == 15:
                tiles[y][x] = TILE_WALL
            else:
                tiles[y][x] = TILE_FLOOR
    
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
            "dialog": "やあ、私はEC2だ。AWSの中核となるコンピューティングサービスだよ。何か手伝えることはある？",
            "is_service": True,
            "service_id": "ec2"
        },
        {
            "x": 8,
            "y": 8,
            "name": "Lambda",
            "dialog": "こんにちは、私はLambdaです。サーバーレスコンピューティングを担当しています。コードを実行するだけで、インフラの心配はいりませんよ。",
            "is_service": True,
            "service_id": "lambda"
        },
        {
            "x": 20,
            "y": 8,
            "name": "ECS",
            "dialog": "私はECS、Elastic Container Serviceです。コンテナ化されたアプリケーションを簡単に実行・管理できますよ。",
            "is_service": True,
            "service_id": "ecs"
        },
        {
            "x": 8,
            "y": 20,
            "name": "Fargate",
            "dialog": "私はFargateです。ECSやEKSのコンテナをサーバーレスで実行できます。インフラ管理から解放されましょう。",
            "is_service": True,
            "service_id": "fargate"
        },
        {
            "x": 20,
            "y": 20,
            "name": "Elastic Beanstalk",
            "dialog": "私はElastic Beanstalkです。アプリケーションのデプロイと管理を簡素化します。コードをアップロードするだけで環境を自動構築しますよ。",
            "is_service": True,
            "service_id": "beanstalk"
        },
        {
            "x": 13,
            "y": 13,
            "name": "CloudWatch",
            "dialog": "私はCloudWatchです。AWSリソースとアプリケーションのモニタリングを担当しています。メトリクスの収集、ログの分析、アラームの設定ができますよ。",
            "is_service": True,
            "service_id": "cloudwatch"
        },
        {
            "x": 16,
            "y": 13,
            "name": "CloudFormation",
            "dialog": "私はCloudFormationです。インフラをコードとして管理できるサービスです。テンプレートを使ってリソースを簡単にデプロイできますよ。",
            "is_service": True,
            "service_id": "cloudformation"
        },
        {
            "x": 13,
            "y": 16,
            "name": "Step Functions",
            "dialog": "私はStep Functionsです。サーバーレスワークフローを視覚的に構築できます。複雑な処理を簡単に連携させられますよ。",
            "is_service": True,
            "service_id": "stepfunctions"
        },
        {
            "x": 16,
            "y": 16,
            "name": "SQS",
            "dialog": "私はSQS、Simple Queue Serviceです。マイクロサービス間のメッセージングを担当しています。疎結合なアプリケーション設計に役立ちますよ。",
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
            "dialog": "コンピューティングの力を武器に変えましょう！",
            "items": ["bronze_sword", "iron_sword", "silver_sword", "compute_blade", "serverless_dagger"]
        },
        {
            "x": 15,
            "y": 3,
            "name": "Instance Armory",
            "type": "armor",
            "dialog": "最高のインスタンスタイプで身を守りましょう！",
            "items": ["leather_armor", "chain_mail", "instance_shield", "auto_scaling_helmet"]
        },
        {
            "x": 27,
            "y": 15,
            "name": "EC2 Potions",
            "type": "items",
            "dialog": "コンピューティングパワーで回復しましょう！",
            "items": ["potion_small", "potion_medium", "ether_small", "compute_elixir"]
        }
    ]
    
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
