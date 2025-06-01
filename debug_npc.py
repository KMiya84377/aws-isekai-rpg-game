#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import sys
from game_map import MapManager

# デバッグ用のスクリプト
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("NPC Debug")
clock = pygame.time.Clock()

# マップマネージャーの初期化
map_manager = MapManager()
computing_town = map_manager.maps["Computing Town"]

# デバッグ情報の表示
print("Computing Town NPCs:")
for npc in computing_town.npcs:
    print(f"  {npc['name']} at ({npc['x']}, {npc['y']}), is_service: {npc.get('is_service', False)}")

# プレイヤーの位置（テスト用）
player_x = 14
player_y = 11  # EC2の1マス上

# デバッグ: get_npc_at関数のテスト
print("\nget_npc_at関数のテスト:")
for dx in [-1, 0, 1]:
    for dy in [-1, 0, 1]:
        if dx == 0 and dy == 0:
            continue
        check_x = player_x + dx
        check_y = player_y + dy
        npc = computing_town.get_npc_at(check_x, check_y)
        print(f"  位置({check_x}, {check_y})のNPC: {npc['name'] if npc else 'なし'}")

# デバッグ: タイルの確認
print("\nタイルの確認:")
for y in range(player_y-1, player_y+3):
    for x in range(player_x-1, player_x+2):
        if 0 <= x < computing_town.width and 0 <= y < computing_town.height:
            tile_type = computing_town.tiles[y][x]
            print(f"  位置({x}, {y})のタイル: {tile_type}")

# EC2の位置のタイルを確認
ec2_x = 14
ec2_y = 12
if 0 <= ec2_x < computing_town.width and 0 <= ec2_y < computing_town.height:
    tile_type = computing_town.tiles[ec2_y][ec2_x]
    print(f"\nEC2の位置({ec2_x}, {ec2_y})のタイル: {tile_type}")

# タイルタイプの定数を表示
print("\nタイルタイプの定数:")
print("TILE_NPC =", 7)  # NPCのタイルタイプ

print("\nデバッグ完了")
