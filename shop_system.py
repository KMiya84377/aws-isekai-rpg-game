#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
from game_assets import WHITE, BLACK, BLUE, GRAY
from item_system import get_item_by_id, get_all_items

class ShopSystem:
    def __init__(self, player, assets):
        self.player = player
        self.assets = assets
        self.active = False
        self.selected_item = None
        self.message = ""
        self.scroll_offset = 0
        self.max_items_per_page = 8
        self.shop_type = "general"  # general, weapon, armor, magic
        self.mode = "buy"  # buy, sell
        
    def set_shop_type(self, shop_type):
        """ショップタイプを設定"""
        self.shop_type = shop_type
        self.selected_item = None
        self.scroll_offset = 0
        self.message = ""
        
    def get_shop_items(self):
        """ショップタイプに応じた商品リストを取得"""
        all_items = get_all_items()
        shop_items = []
        
        for item in all_items:
            # キーアイテムは販売しない
            if item["type"] == 2:  # ITEM_TYPE_KEY
                continue
                
            # ショップタイプに応じたフィルタリング
            if self.shop_type == "general":
                # 一般ショップは消費アイテムのみ
                if item["type"] == 0:  # ITEM_TYPE_CONSUMABLE
                    shop_items.append(item)
            elif self.shop_type == "weapon":
                # 武器ショップは武器のみ
                if item["type"] == 1 and item.get("equip_type") == "weapon":  # ITEM_TYPE_EQUIPMENT
                    shop_items.append(item)
            elif self.shop_type == "armor":
                # 防具ショップは防具のみ
                if item["type"] == 1 and item.get("equip_type") == "armor":  # ITEM_TYPE_EQUIPMENT
                    shop_items.append(item)
            elif self.shop_type == "magic":
                # 魔法ショップはMP回復アイテムとマナクリスタルのみ
                if item["type"] == 0 and ("heal_mp" in item or item["id"] == "mana_crystal"):
                    shop_items.append(item)
                    
        return shop_items
        
    def get_player_items(self):
        """プレイヤーのインベントリアイテムを取得"""
        player_items = []
        
        if "inventory" in self.player:
            for item in self.player["inventory"]:
                item_data = get_item_by_id(item["id"])
                if item_data:
                    # キーアイテムは売却不可
                    if item_data["type"] != 2:  # ITEM_TYPE_KEY
                        player_items.append({
                            "data": item_data,
                            "quantity": item["quantity"]
                        })
                        
        return player_items
        
    def buy_item(self, item_index):
        """アイテムを購入"""
        shop_items = self.get_shop_items()
        
        if item_index < 0 or item_index >= len(shop_items):
            return False
            
        item = shop_items[item_index]
        
        # 所持金チェック
        if self.player["credits"] < item["price"]:
            self.message = "クレジットが足りません！"
            return False
            
        # 購入処理
        self.player["credits"] -= item["price"]
        
        # プレイヤーのインベントリにアイテムを追加
        if "inventory" not in self.player:
            self.player["inventory"] = []
            
        # 既に持っているアイテムかチェック
        for inv_item in self.player["inventory"]:
            if inv_item["id"] == item["id"]:
                # 消費アイテムなら数量を増やす
                if item["type"] == 0:  # ITEM_TYPE_CONSUMABLE
                    inv_item["quantity"] += 1
                    self.message = f"{item['name']}を購入しました！"
                    return True
                # 装備品は1つだけ
                elif item["type"] == 1:  # ITEM_TYPE_EQUIPMENT
                    self.message = "既に持っています！"
                    return False
        
        # 新しいアイテムを追加
        self.player["inventory"].append({
            "id": item["id"],
            "quantity": 1
        })
        
        self.message = f"{item['name']}を購入しました！"
        return True
        
    def sell_item(self, item_index):
        """アイテムを売却"""
        player_items = self.get_player_items()
        
        if item_index < 0 or item_index >= len(player_items):
            return False
            
        item = player_items[item_index]
        item_data = item["data"]
        
        # 売却価格は購入価格の半額
        sell_price = item_data["price"] // 2
        
        # 売却処理
        self.player["credits"] += sell_price
        
        # プレイヤーのインベントリからアイテムを減らす
        for i, inv_item in enumerate(self.player["inventory"]):
            if inv_item["id"] == item_data["id"]:
                inv_item["quantity"] -= 1
                if inv_item["quantity"] <= 0:
                    self.player["inventory"].pop(i)
                break
                
        self.message = f"{item_data['name']}を{sell_price}クレジットで売却しました！"
        return True
        
    def draw(self, screen):
        """ショップ画面を描画"""
        if not self.active:
            return
            
        # 背景
        shop_bg = pygame.Rect(50, 50, 700, 500)
        pygame.draw.rect(screen, (30, 30, 50), shop_bg)
        pygame.draw.rect(screen, WHITE, shop_bg, 2)
        
        # タイトル
        shop_titles = {
            "general": "一般ショップ",
            "weapon": "武器ショップ",
            "armor": "防具ショップ",
            "magic": "魔法ショップ"
        }
        title_text = self.assets.render_text(shop_titles.get(self.shop_type, "ショップ"), "large", WHITE)
        screen.blit(title_text, (400 - title_text.get_width() // 2, 70))
        
        # モードタブ
        buy_tab = pygame.Rect(100, 120, 100, 30)
        sell_tab = pygame.Rect(200, 120, 100, 30)
        
        # 購入タブ
        if self.mode == "buy":
            pygame.draw.rect(screen, (80, 100, 150), buy_tab)
        else:
            pygame.draw.rect(screen, (50, 50, 80), buy_tab)
        pygame.draw.rect(screen, WHITE, buy_tab, 1)
        
        buy_text = self.assets.render_text("購入", "normal", WHITE)
        screen.blit(buy_text, (130, 125))
        
        # 売却タブ
        if self.mode == "sell":
            pygame.draw.rect(screen, (80, 100, 150), sell_tab)
        else:
            pygame.draw.rect(screen, (50, 50, 80), sell_tab)
        pygame.draw.rect(screen, WHITE, sell_tab, 1)
        
        sell_text = self.assets.render_text("売却", "normal", WHITE)
        screen.blit(sell_text, (230, 125))
        
        # 所持金表示
        credits_text = self.assets.render_text(f"所持金: {self.player['credits']}クレジット", "normal", WHITE)
        screen.blit(credits_text, (500, 125))
        
        # アイテム一覧
        if self.mode == "buy":
            items = self.get_shop_items()
        else:  # sell
            items = self.get_player_items()
            
        start_index = self.scroll_offset
        end_index = min(start_index + self.max_items_per_page, len(items))
        
        for i in range(start_index, end_index):
            if self.mode == "buy":
                item_data = items[i]
                quantity = None
            else:  # sell
                item_data = items[i]["data"]
                quantity = items[i]["quantity"]
                
            # アイテム背景
            item_bg = pygame.Rect(100, 170 + (i - start_index) * 40, 600, 35)
            
            # 選択中のアイテムはハイライト
            if i == self.selected_item:
                pygame.draw.rect(screen, (60, 60, 100), item_bg)
            else:
                pygame.draw.rect(screen, (40, 40, 70), item_bg)
                
            pygame.draw.rect(screen, WHITE, item_bg, 1)
            
            # アイテム名
            item_name = self.assets.render_text(item_data["name"], "normal", WHITE)
            screen.blit(item_name, (120, 175 + (i - start_index) * 40))
            
            # 価格または売却価格
            if self.mode == "buy":
                price_text = self.assets.render_text(f"{item_data['price']}クレジット", "normal", WHITE)
            else:  # sell
                price_text = self.assets.render_text(f"{item_data['price'] // 2}クレジット", "normal", WHITE)
                
            screen.blit(price_text, (500, 175 + (i - start_index) * 40))
            
            # 数量（売却モードのみ）
            if self.mode == "sell" and quantity is not None:
                quantity_text = self.assets.render_text(f"x{quantity}", "normal", WHITE)
                screen.blit(quantity_text, (650, 175 + (i - start_index) * 40))
                
        # スクロールバー
        if len(items) > self.max_items_per_page:
            scroll_height = 320
            thumb_height = scroll_height * self.max_items_per_page / len(items)
            thumb_pos = scroll_height * self.scroll_offset / len(items)
            
            pygame.draw.rect(screen, (80, 80, 80), (720, 170, 10, scroll_height))
            pygame.draw.rect(screen, WHITE, (720, 170 + thumb_pos, 10, thumb_height))
            
        # アイテム詳細
        if self.selected_item is not None:
            if self.mode == "buy" and 0 <= self.selected_item < len(items):
                item_data = items[self.selected_item]
            elif self.mode == "sell" and 0 <= self.selected_item < len(items):
                item_data = items[self.selected_item]["data"]
            else:
                item_data = None
                
            if item_data:
                # 詳細背景
                detail_bg = pygame.Rect(100, 450, 600, 60)
                pygame.draw.rect(screen, (50, 50, 80), detail_bg)
                pygame.draw.rect(screen, WHITE, detail_bg, 1)
                
                # アイテム説明
                desc_text = self.assets.render_text(item_data["description"], "normal", WHITE)
                screen.blit(desc_text, (120, 460))
                
                # 購入/売却ボタン
                if self.mode == "buy":
                    action_button = pygame.Rect(550, 470, 100, 30)
                    pygame.draw.rect(screen, (80, 120, 80), action_button)
                    pygame.draw.rect(screen, WHITE, action_button, 1)
                    
                    action_text = self.assets.render_text("購入", "normal", WHITE)
                    screen.blit(action_text, (580, 475))
                else:  # sell
                    action_button = pygame.Rect(550, 470, 100, 30)
                    pygame.draw.rect(screen, (120, 80, 80), action_button)
                    pygame.draw.rect(screen, WHITE, action_button, 1)
                    
                    action_text = self.assets.render_text("売却", "normal", WHITE)
                    screen.blit(action_text, (580, 475))
                    
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
                items = self.get_shop_items() if self.mode == "buy" else self.get_player_items()
                
                if self.selected_item is None and len(items) > 0:
                    self.selected_item = 0
                elif self.selected_item is not None:
                    self.selected_item = min(len(items) - 1, self.selected_item + 1)
                    
                    # スクロール調整
                    if self.selected_item >= self.scroll_offset + self.max_items_per_page:
                        self.scroll_offset = self.selected_item - self.max_items_per_page + 1
                        
            # Enterキーでアイテム購入/売却
            elif event.key == pygame.K_RETURN:
                if self.selected_item is not None:
                    if self.mode == "buy":
                        self.buy_item(self.selected_item)
                    else:  # sell
                        self.sell_item(self.selected_item)
                        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 戻るボタン
            back_button = pygame.Rect(650, 70, 80, 30)
            if back_button.collidepoint(event.pos):
                self.active = False
                return True
                
            # 購入タブ
            buy_tab = pygame.Rect(100, 120, 100, 30)
            if buy_tab.collidepoint(event.pos):
                self.mode = "buy"
                self.selected_item = None
                self.scroll_offset = 0
                return False
                
            # 売却タブ
            sell_tab = pygame.Rect(200, 120, 100, 30)
            if sell_tab.collidepoint(event.pos):
                self.mode = "sell"
                self.selected_item = None
                self.scroll_offset = 0
                return False
                
            # アイテム選択
            items = self.get_shop_items() if self.mode == "buy" else self.get_player_items()
            for i in range(self.scroll_offset, min(self.scroll_offset + self.max_items_per_page, len(items))):
                item_bg = pygame.Rect(100, 170 + (i - self.scroll_offset) * 40, 600, 35)
                if item_bg.collidepoint(event.pos):
                    self.selected_item = i
                    break
                    
            # 購入/売却ボタン
            if self.selected_item is not None:
                action_button = pygame.Rect(550, 470, 100, 30)
                if action_button.collidepoint(event.pos):
                    if self.mode == "buy":
                        self.buy_item(self.selected_item)
                    else:  # sell
                        self.sell_item(self.selected_item)
                        
            # スクロールホイール
            if event.button == 4:  # 上スクロール
                self.scroll_offset = max(0, self.scroll_offset - 1)
            elif event.button == 5:  # 下スクロール
                items = self.get_shop_items() if self.mode == "buy" else self.get_player_items()
                self.scroll_offset = min(max(0, len(items) - self.max_items_per_page), self.scroll_offset + 1)
                
        return False
