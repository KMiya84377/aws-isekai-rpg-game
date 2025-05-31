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
    
    # プレイヤーの描画
    player_x = self.player["tile_x"] * tile_size - self.camera_x
    player_y = self.player["tile_y"] * tile_size - self.camera_y
    self.screen.blit(self.assets.get_image("player"), (player_x, player_y))
