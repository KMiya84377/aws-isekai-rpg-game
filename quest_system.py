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
        
        # Quest data
        self.quest_data = {
            "meet_ec2": {
                "title": "Meet EC2",
                "description": "Talk to EC2 in Computing Town",
                "reward": {"exp": 50, "credits": 100}
            },
            "explore_computing_town": {
                "title": "Explore Computing Town",
                "description": "Explore Computing Town thoroughly",
                "reward": {"exp": 50, "credits": 100},
                "unlocks_town": "Storage Town"
            },
            "ec2_quest": {
                "title": "EC2's Request",
                "description": "Complete the request from EC2",
                "reward": {"exp": 100, "credits": 200}
            },
            "defeat_sql_injection": {
                "title": "Defeat SQL Injection",
                "description": "Defeat the SQL Injection attacking Computing Town",
                "reward": {"exp": 150, "credits": 300},
                "unlocks_town": "Database Town"
            },
            "s3_quest": {
                "title": "S3's Request",
                "description": "Complete the request from S3",
                "reward": {"exp": 100, "credits": 200}
            },
            "secure_data": {
                "title": "Secure the Data",
                "description": "Prevent data leakage in Storage Town",
                "reward": {"exp": 150, "credits": 300},
                "unlocks_town": "Security Town"
            },
            "dynamodb_quest": {
                "title": "DynamoDB's Request",
                "description": "Complete the request from DynamoDB",
                "reward": {"exp": 100, "credits": 200}
            },
            "rds_quest": {
                "title": "RDS's Request",
                "description": "Complete the request from RDS",
                "reward": {"exp": 100, "credits": 200}
            },
            "iam_quest": {
                "title": "IAM's Request",
                "description": "Complete the request from IAM",
                "reward": {"exp": 100, "credits": 200}
            },
            "final_battle": {
                "title": "Final Battle",
                "description": "Protect the world from the DDoS Attack",
                "reward": {"exp": 300, "credits": 500}
            }
        }
        
    def add_quest(self, quest_id):
        """Add a quest"""
        if quest_id in self.quest_data and quest_id not in self.active_quests and quest_id not in self.completed_quests:
            self.active_quests.append(quest_id)
            return True
        return False
        
    def complete_quest(self, quest_id):
        """Complete a quest"""
        if quest_id in self.active_quests:
            self.active_quests.remove(quest_id)
            self.completed_quests.append(quest_id)
            
            # Add to player's completed quests list
            if "completed_quests" not in self.player:
                self.player["completed_quests"] = []
            self.player["completed_quests"].append(quest_id)
            
            # Give rewards
            reward = self.quest_data[quest_id]["reward"]
            self.player["exp"] += reward["exp"]
            self.player["credits"] += reward["credits"]
            
            # Check if this quest unlocks a new town
            if "unlocks_town" in self.quest_data[quest_id]:
                town_name = self.quest_data[quest_id]["unlocks_town"]
                # Add the town to discovered towns if it's not already there
                from main import Game
                if Game.instance and town_name not in Game.instance.discovered_towns:
                    Game.instance.discovered_towns.append(town_name)
                    Game.instance.start_dialog(f"You have discovered {town_name}! You can now travel there.")
                    
            return reward
        return None
        
    def get_quest_details(self, quest_id):
        """Get quest details"""
        return self.quest_data.get(quest_id)
        
    def draw_quest_log(self, screen):
        """Draw the quest log"""
        try:
            # Background overlay
            overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            
            # Panel
            panel = pygame.Rect(100, 100, 600, 400)
            pygame.draw.rect(screen, (50, 50, 80), panel)
            pygame.draw.rect(screen, WHITE, panel, 2)
            
            # Title
            title_text = self.assets.render_text("Quest Log", "large", WHITE)
            screen.blit(title_text, (400 - title_text.get_width() // 2, 120))
            
            # Active quests
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
                
            # Completed quests
            if self.completed_quests:
                completed_text = self.assets.render_text("Completed Quests:", "normal", GREEN)
                screen.blit(completed_text, (120, 300))
                
                for i, quest_id in enumerate(self.completed_quests[-5:]):  # Show only the latest 5
                    if quest_id in self.quest_data:
                        quest = self.quest_data[quest_id]
                        quest_text = self.assets.render_text(quest['title'], "small", (200, 200, 200))
                        screen.blit(quest_text, (140, 330 + i * 25))
                    
            # Close button
            close_button = pygame.Rect(350, 450, 100, 30)
            pygame.draw.rect(screen, (100, 100, 200), close_button)
            pygame.draw.rect(screen, WHITE, close_button, 1)
            
            close_text = self.assets.render_text("Close", "normal", WHITE)
            screen.blit(close_text, (400 - close_text.get_width() // 2, 455))
            
            return close_button
        except Exception as e:
            print(f"Error drawing quest log: {e}")
            # Return a simple button on error
            close_button = pygame.Rect(350, 450, 100, 30)
            pygame.draw.rect(screen, (100, 100, 200), close_button)
            return close_button
        
    def get_current_objective(self):
        """Get the current objective"""
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
            print(f"Error getting objective: {e}")
            return "Objective: Continue your adventure"
