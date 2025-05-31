#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
from game_assets import WHITE, BLACK, BLUE, GRAY

# アイテムの種類
ITEM_TYPE_CONSUMABLE = 0  # 消費アイテム
ITEM_TYPE_EQUIPMENT = 1   # 装備アイテム
ITEM_TYPE_KEY = 2         # キーアイテム

class ItemSystem:
    def __init__(self, player, assets):
        self.player = player
        self.assets = assets
        self.active = False
        self.selected_item = None
        self.message = ""
        self.scroll_offset = 0
        self.max_items_per_page = 8
        
        # プレイヤーのインベントリがなければ初期化
        if "inventory" not in self.player:
            self.player["inventory"] = []
            
    def add_item(self, item_id, quantity=1):
        """アイテムを追加"""
        item_data = get_item_by_id(item_id)
        if not item_data:
            return False
            
        # 既に持っているアイテムかチェック
        for item in self.player["inventory"]:
            if item["id"] == item_id:
                # 消費アイテムなら数量を増やす
                if item_data["type"] == ITEM_TYPE_CONSUMABLE:
                    item["quantity"] += quantity
                    return True
                # 装備品やキーアイテムは1つだけ
                elif item_data["type"] in [ITEM_TYPE_EQUIPMENT, ITEM_TYPE_KEY]:
                    return False
        
        # 新しいアイテムを追加
        self.player["inventory"].append({
            "id": item_id,
            "quantity": quantity
        })
        return True
        
    def remove_item(self, item_id, quantity=1):
        """アイテムを減らす"""
        for i, item in enumerate(self.player["inventory"]):
            if item["id"] == item_id:
                item["quantity"] -= quantity
                if item["quantity"] <= 0:
                    self.player["inventory"].pop(i)
                return True
        return False
        
    def use_item(self, item_index):
        """アイテムを使用"""
        if item_index < 0 or item_index >= len(self.player["inventory"]):
            return False
            
        item = self.player["inventory"][item_index]
        item_data = get_item_by_id(item["id"])
        
        if not item_data:
            return False
            
        # アイテムタイプに応じた効果
        if item_data["type"] == ITEM_TYPE_CONSUMABLE:
            # 回復アイテム
            if "heal_hp" in item_data:
                self.player["hp"] = min(self.player["hp"] + item_data["heal_hp"], self.player["max_hp"])
                self.message = f"{item_data['name']}を使用。HPが{item_data['heal_hp']}回復した！"
                self.remove_item(item["id"], 1)
                return True
            # MP回復アイテム
            elif "heal_mp" in item_data:
                self.player["mp"] = min(self.player["mp"] + item_data["heal_mp"], self.player["max_mp"])
                self.message = f"{item_data['name']}を使用。MPが{item_data['heal_mp']}回復した！"
                self.remove_item(item["id"], 1)
                return True
            # ステータスアップアイテム
            elif "boost_stat" in item_data:
                stat = item_data["boost_stat"]
                value = item_data["boost_value"]
                if stat == "attack":
                    self.player["attack"] += value
                    self.message = f"{item_data['name']}を使用。攻撃力が{value}上昇した！"
                elif stat == "defense":
                    self.player["defense"] += value
                    self.message = f"{item_data['name']}を使用。防御力が{value}上昇した！"
                elif stat == "max_hp":
                    self.player["max_hp"] += value
                    self.player["hp"] += value
                    self.message = f"{item_data['name']}を使用。最大HPが{value}上昇した！"
                elif stat == "max_mp":
                    self.player["max_mp"] += value
                    self.player["mp"] += value
                    self.message = f"{item_data['name']}を使用。最大MPが{value}上昇した！"
                self.remove_item(item["id"], 1)
                return True
        
        # 装備アイテム
        elif item_data["type"] == ITEM_TYPE_EQUIPMENT:
            # 装備処理（今回は簡易的に）
            self.message = f"{item_data['name']}を装備した！"
            return True
            
        # キーアイテム
        elif item_data["type"] == ITEM_TYPE_KEY:
            self.message = f"{item_data['name']}は大切なアイテムだ。"
            return True
            
        return False
        
    def draw(self, screen):
        """インベントリ画面を描画"""
        if not self.active:
            return
            
        # 背景
        inventory_bg = pygame.Rect(50, 50, 700, 500)
        pygame.draw.rect(screen, (30, 30, 50), inventory_bg)
        pygame.draw.rect(screen, WHITE, inventory_bg, 2)
        
        # タイトル
        title_text = self.assets.render_text("インベントリ", "large", WHITE)
        screen.blit(title_text, (400 - title_text.get_width() // 2, 70))
        
        # アイテム一覧
        start_index = self.scroll_offset
        end_index = min(start_index + self.max_items_per_page, len(self.player["inventory"]))
        
        for i in range(start_index, end_index):
            item = self.player["inventory"][i]
            item_data = get_item_by_id(item["id"])
            
            if not item_data:
                continue
                
            # アイテム背景
            item_bg = pygame.Rect(100, 120 + (i - start_index) * 50, 600, 40)
            
            # 選択中のアイテムはハイライト
            if i == self.selected_item:
                pygame.draw.rect(screen, (60, 60, 100), item_bg)
            else:
                pygame.draw.rect(screen, (40, 40, 70), item_bg)
                
            pygame.draw.rect(screen, WHITE, item_bg, 1)
            
            # アイテム名と数量
            item_name = self.assets.render_text(item_data["name"], "normal", WHITE)
            screen.blit(item_name, (120, 130 + (i - start_index) * 50))
            
            # 消費アイテムは数量を表示
            if item_data["type"] == ITEM_TYPE_CONSUMABLE:
                quantity_text = self.assets.render_text(f"x{item['quantity']}", "normal", WHITE)
                screen.blit(quantity_text, (650, 130 + (i - start_index) * 50))
                
            # アイテムタイプに応じたアイコン
            if item_data["type"] == ITEM_TYPE_CONSUMABLE:
                icon_color = (100, 200, 100)  # 緑
            elif item_data["type"] == ITEM_TYPE_EQUIPMENT:
                icon_color = (100, 100, 200)  # 青
            else:  # キーアイテム
                icon_color = (200, 200, 100)  # 黄
                
            pygame.draw.rect(screen, icon_color, (110, 130 + (i - start_index) * 50, 5, 20))
            
        # スクロールバー
        if len(self.player["inventory"]) > self.max_items_per_page:
            scroll_height = 400
            thumb_height = scroll_height * self.max_items_per_page / len(self.player["inventory"])
            thumb_pos = scroll_height * self.scroll_offset / len(self.player["inventory"])
            
            pygame.draw.rect(screen, (80, 80, 80), (720, 120, 10, scroll_height))
            pygame.draw.rect(screen, WHITE, (720, 120 + thumb_pos, 10, thumb_height))
            
        # アイテム詳細
        if self.selected_item is not None and 0 <= self.selected_item < len(self.player["inventory"]):
            item = self.player["inventory"][self.selected_item]
            item_data = get_item_by_id(item["id"])
            
            if item_data:
                # 詳細背景
                detail_bg = pygame.Rect(100, 450, 600, 80)
                pygame.draw.rect(screen, (50, 50, 80), detail_bg)
                pygame.draw.rect(screen, WHITE, detail_bg, 1)
                
                # アイテム説明
                desc_text = self.assets.render_text(item_data["description"], "normal", WHITE)
                screen.blit(desc_text, (120, 460))
                
                # 使用ボタン（消費アイテムのみ）
                if item_data["type"] == ITEM_TYPE_CONSUMABLE:
                    use_button = pygame.Rect(550, 480, 100, 30)
                    pygame.draw.rect(screen, (80, 120, 80), use_button)
                    pygame.draw.rect(screen, WHITE, use_button, 1)
                    
                    use_text = self.assets.render_text("使用", "normal", WHITE)
                    screen.blit(use_text, (580, 485))
                    
        # メッセージ
        if self.message:
            message_text = self.assets.render_text(self.message, "normal", WHITE)
            screen.blit(message_text, (400 - message_text.get_width() // 2, 530))
            
        # 戻るボタン
        back_button = pygame.Rect(650, 70, 80, 30)
        pygame.draw.rect(screen, (120, 80, 80), back_button)
        pygame.draw.rect(screen, WHITE, back_button, 1)
        
        back_text = self.assets.render_text("戻る", "normal", WHITE)
        screen.blit(back_text, (670, 75))
        
    def handle_event(self, event):
        """イベント処理"""
        if not self.active:
            return False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.active = False
                return True
                
            # 上下キーでアイテム選択
            elif event.key == pygame.K_UP:
                if self.selected_item is None:
                    self.selected_item = 0
                else:
                    self.selected_item = max(0, self.selected_item - 1)
                    
                    # スクロール調整
                    if self.selected_item < self.scroll_offset:
                        self.scroll_offset = self.selected_item
                        
            elif event.key == pygame.K_DOWN:
                if self.selected_item is None and len(self.player["inventory"]) > 0:
                    self.selected_item = 0
                elif self.selected_item is not None:
                    self.selected_item = min(len(self.player["inventory"]) - 1, self.selected_item + 1)
                    
                    # スクロール調整
                    if self.selected_item >= self.scroll_offset + self.max_items_per_page:
                        self.scroll_offset = self.selected_item - self.max_items_per_page + 1
                        
            # Enterキーでアイテム使用
            elif event.key == pygame.K_RETURN:
                if self.selected_item is not None:
                    self.use_item(self.selected_item)
                    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 戻るボタン
            back_button = pygame.Rect(650, 70, 80, 30)
            if back_button.collidepoint(event.pos):
                self.active = False
                return True
                
            # アイテム選択
            for i in range(self.scroll_offset, min(self.scroll_offset + self.max_items_per_page, len(self.player["inventory"]))):
                item_bg = pygame.Rect(100, 120 + (i - self.scroll_offset) * 50, 600, 40)
                if item_bg.collidepoint(event.pos):
                    self.selected_item = i
                    break
                    
            # 使用ボタン
            if self.selected_item is not None:
                item = self.player["inventory"][self.selected_item]
                item_data = get_item_by_id(item["id"])
                
                if item_data and item_data["type"] == ITEM_TYPE_CONSUMABLE:
                    use_button = pygame.Rect(550, 480, 100, 30)
                    if use_button.collidepoint(event.pos):
                        self.use_item(self.selected_item)
                        
            # スクロールホイール
            if event.button == 4:  # 上スクロール
                self.scroll_offset = max(0, self.scroll_offset - 1)
            elif event.button == 5:  # 下スクロール
                self.scroll_offset = min(max(0, len(self.player["inventory"]) - self.max_items_per_page), self.scroll_offset + 1)
                
        return False

# アイテムデータ
def get_item_by_id(item_id):
    """IDからアイテムデータを取得"""
    items = {
        # 回復アイテム
        "potion_small": {
            "id": "potion_small",
            "name": "小さいポーション",
            "description": "HPを30回復する。",
            "type": ITEM_TYPE_CONSUMABLE,
            "heal_hp": 30,
            "price": 50
        },
        "potion_medium": {
            "id": "potion_medium",
            "name": "ポーション",
            "description": "HPを80回復する。",
            "type": ITEM_TYPE_CONSUMABLE,
            "heal_hp": 80,
            "price": 120
        },
        "potion_large": {
            "id": "potion_large",
            "name": "大きいポーション",
            "description": "HPを200回復する。",
            "type": ITEM_TYPE_CONSUMABLE,
            "heal_hp": 200,
            "price": 300
        },
        "ether_small": {
            "id": "ether_small",
            "name": "小さいエーテル",
            "description": "MPを20回復する。",
            "type": ITEM_TYPE_CONSUMABLE,
            "heal_mp": 20,
            "price": 80
        },
        "ether_medium": {
            "id": "ether_medium",
            "name": "エーテル",
            "description": "MPを50回復する。",
            "type": ITEM_TYPE_CONSUMABLE,
            "heal_mp": 50,
            "price": 200
        },
        "elixir": {
            "id": "elixir",
            "name": "エリクサー",
            "description": "HPとMPを全回復する。",
            "type": ITEM_TYPE_CONSUMABLE,
            "heal_hp": 9999,
            "heal_mp": 9999,
            "price": 1000
        },
        
        # ステータスアップアイテム
        "power_crystal": {
            "id": "power_crystal",
            "name": "パワークリスタル",
            "description": "攻撃力が5上昇する。",
            "type": ITEM_TYPE_CONSUMABLE,
            "boost_stat": "attack",
            "boost_value": 5,
            "price": 500
        },
        "defense_crystal": {
            "id": "defense_crystal",
            "name": "ディフェンスクリスタル",
            "description": "防御力が5上昇する。",
            "type": ITEM_TYPE_CONSUMABLE,
            "boost_stat": "defense",
            "boost_value": 5,
            "price": 500
        },
        "life_crystal": {
            "id": "life_crystal",
            "name": "ライフクリスタル",
            "description": "最大HPが20上昇する。",
            "type": ITEM_TYPE_CONSUMABLE,
            "boost_stat": "max_hp",
            "boost_value": 20,
            "price": 600
        },
        "mana_crystal": {
            "id": "mana_crystal",
            "name": "マナクリスタル",
            "description": "最大MPが10上昇する。",
            "type": ITEM_TYPE_CONSUMABLE,
            "boost_stat": "max_mp",
            "boost_value": 10,
            "price": 600
        },
        
        # 装備アイテム
        "bronze_sword": {
            "id": "bronze_sword",
            "name": "ブロンズソード",
            "description": "初心者向けの剣。攻撃力+10",
            "type": ITEM_TYPE_EQUIPMENT,
            "equip_type": "weapon",
            "attack": 10,
            "price": 300
        },
        "iron_sword": {
            "id": "iron_sword",
            "name": "アイアンソード",
            "description": "標準的な剣。攻撃力+25",
            "type": ITEM_TYPE_EQUIPMENT,
            "equip_type": "weapon",
            "attack": 25,
            "price": 800
        },
        "silver_sword": {
            "id": "silver_sword",
            "name": "シルバーソード",
            "description": "上質な剣。攻撃力+40",
            "type": ITEM_TYPE_EQUIPMENT,
            "equip_type": "weapon",
            "attack": 40,
            "price": 1500
        },
        "leather_armor": {
            "id": "leather_armor",
            "name": "レザーアーマー",
            "description": "初心者向けの鎧。防御力+5",
            "type": ITEM_TYPE_EQUIPMENT,
            "equip_type": "armor",
            "defense": 5,
            "price": 200
        },
        "chain_mail": {
            "id": "chain_mail",
            "name": "チェインメイル",
            "description": "標準的な鎧。防御力+15",
            "type": ITEM_TYPE_EQUIPMENT,
            "equip_type": "armor",
            "defense": 15,
            "price": 600
        },
        "plate_armor": {
            "id": "plate_armor",
            "name": "プレートアーマー",
            "description": "上質な鎧。防御力+30",
            "type": ITEM_TYPE_EQUIPMENT,
            "equip_type": "armor",
            "defense": 30,
            "price": 1200
        },
        
        # キーアイテム
        "aws_key": {
            "id": "aws_key",
            "name": "AWSアクセスキー",
            "description": "AWSサービスにアクセスするための重要なキー。",
            "type": ITEM_TYPE_KEY,
            "price": 0  # 売買不可
        },
        "ec2_manual": {
            "id": "ec2_manual",
            "name": "EC2マニュアル",
            "description": "EC2の使い方が書かれた貴重な本。",
            "type": ITEM_TYPE_KEY,
            "price": 0  # 売買不可
        },
        "s3_bucket": {
            "id": "s3_bucket",
            "name": "S3バケット",
            "description": "データを保存できる不思議な容器。",
            "type": ITEM_TYPE_KEY,
            "price": 0  # 売買不可
        }
    }
    
    return items.get(item_id, None)

def get_all_items():
    """すべてのアイテムのリストを取得"""
    items = []
    for item_id in ["potion_small", "potion_medium", "potion_large", 
                   "ether_small", "ether_medium", "elixir",
                   "power_crystal", "defense_crystal", "life_crystal", "mana_crystal",
                   "bronze_sword", "iron_sword", "silver_sword",
                   "leather_armor", "chain_mail", "plate_armor",
                   "aws_key", "ec2_manual", "s3_bucket"]:
        item = get_item_by_id(item_id)
        if item:
            items.append(item)
    return items
