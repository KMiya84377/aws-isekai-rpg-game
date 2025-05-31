#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
from game_assets import WHITE, BLACK, BLUE, GRAY, GREEN, YELLOW

class QuestSystem:
    def __init__(self, player, assets):
        self.player = player
        self.assets = assets
        self.active_quests = []
        self.completed_quests = []
        
        # クエストデータ
        self.quest_data = {
            "meet_ec2": {
                "title": "EC2と出会う",
                "description": "コンピューティング町でEC2と会話する",
                "reward": {"exp": 50, "credits": 100}
            },
            "explore_computing_town": {
                "title": "コンピューティング町を探索",
                "description": "コンピューティング町を隅々まで探索する",
                "reward": {"exp": 50, "credits": 100}
            },
            "ec2_quest": {
                "title": "EC2の依頼",
                "description": "EC2からの依頼を完了する",
                "reward": {"exp": 100, "credits": 200}
            },
            "defeat_sql_injection": {
                "title": "SQLインジェクションを撃退",
                "description": "コンピューティング町を襲うSQLインジェクションを倒す",
                "reward": {"exp": 150, "credits": 300}
            },
            "s3_quest": {
                "title": "S3の依頼",
                "description": "S3からの依頼を完了する",
                "reward": {"exp": 100, "credits": 200}
            },
            "secure_data": {
                "title": "データを保護",
                "description": "ストレージ町のデータ漏洩を防ぐ",
                "reward": {"exp": 150, "credits": 300}
            },
            "dynamodb_quest": {
                "title": "DynamoDBの依頼",
                "description": "DynamoDBからの依頼を完了する",
                "reward": {"exp": 100, "credits": 200}
            },
            "rds_quest": {
                "title": "RDSの依頼",
                "description": "RDSからの依頼を完了する",
                "reward": {"exp": 100, "credits": 200}
            },
            "iam_quest": {
                "title": "IAMの依頼",
                "description": "IAMからの依頼を完了する",
                "reward": {"exp": 100, "credits": 200}
            },
            "final_battle": {
                "title": "最終決戦",
                "description": "DDoS攻撃から世界を守る",
                "reward": {"exp": 300, "credits": 500}
            }
        }
        
    def add_quest(self, quest_id):
        """クエストを追加"""
        if quest_id in self.quest_data and quest_id not in self.active_quests and quest_id not in self.completed_quests:
            self.active_quests.append(quest_id)
            return True
        return False
        
    def complete_quest(self, quest_id):
        """クエストを完了"""
        if quest_id in self.active_quests:
            self.active_quests.remove(quest_id)
            self.completed_quests.append(quest_id)
            
            # プレイヤーの完了クエストリストに追加
            if "completed_quests" not in self.player:
                self.player["completed_quests"] = []
            self.player["completed_quests"].append(quest_id)
            
            # 報酬の付与
            reward = self.quest_data[quest_id]["reward"]
            self.player["exp"] += reward["exp"]
            self.player["credits"] += reward["credits"]
            
            return reward
        return None
        
    def get_quest_details(self, quest_id):
        """クエストの詳細を取得"""
        return self.quest_data.get(quest_id)
        
    def draw_quest_log(self, screen):
        """クエストログを描画"""
        try:
            # 背景オーバーレイ
            overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            
            # パネル
            panel = pygame.Rect(100, 100, 600, 400)
            pygame.draw.rect(screen, (50, 50, 80), panel)
            pygame.draw.rect(screen, WHITE, panel, 2)
            
            # タイトル
            title_text = self.assets.render_text("Quest Log", "large", WHITE)
            screen.blit(title_text, (400 - title_text.get_width() // 2, 120))
            
            # アクティブなクエスト
            if self.active_quests:
                active_text = self.assets.render_text("Active Quests:", "normal", YELLOW)
                screen.blit(active_text, (120, 170))
                
                for i, quest_id in enumerate(self.active_quests):
                    if quest_id in self.quest_data:
                        quest = self.quest_data[quest_id]
                        quest_text = self.assets.render_text(f"{quest['title']}: {quest['description']}", "small", WHITE)
                        screen.blit(quest_text, (140, 200 + i * 25))
            else:
                no_quest_text = self.assets.render_text("No active quests", "normal", WHITE)
                screen.blit(no_quest_text, (120, 200))
                
            # 完了したクエスト
            if self.completed_quests:
                completed_text = self.assets.render_text("Completed Quests:", "normal", GREEN)
                screen.blit(completed_text, (120, 300))
                
                for i, quest_id in enumerate(self.completed_quests[-5:]):  # 最新の5つだけ表示
                    if quest_id in self.quest_data:
                        quest = self.quest_data[quest_id]
                        quest_text = self.assets.render_text(quest['title'], "small", (200, 200, 200))
                        screen.blit(quest_text, (140, 330 + i * 25))
                    
            # 閉じるボタン
            close_button = pygame.Rect(350, 450, 100, 30)
            pygame.draw.rect(screen, (100, 100, 200), close_button)
            pygame.draw.rect(screen, WHITE, close_button, 1)
            
            close_text = self.assets.render_text("Close", "normal", WHITE)
            screen.blit(close_text, (400 - close_text.get_width() // 2, 455))
            
            return close_button
        except Exception as e:
            print(f"クエストログ描画中のエラー: {e}")
            # エラー時は単純なボタンを返す
            close_button = pygame.Rect(350, 450, 100, 30)
            pygame.draw.rect(screen, (100, 100, 200), close_button)
            return close_button
        
    def get_current_objective(self):
        """現在の目標を取得"""
        try:
            if not self.active_quests:
                return "No active quests"
                
            quest_id = self.active_quests[0]
            if quest_id in self.quest_data:
                quest = self.quest_data[quest_id]
                return f"Objective: {quest['title']}"
            else:
                return "Objective: Unknown"
        except Exception as e:
            print(f"目標取得中のエラー: {e}")
            return "Objective: Continue your adventure"
