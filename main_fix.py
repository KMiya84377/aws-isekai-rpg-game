#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import sys
import random
import json
import os
import math
from game_assets import GameAssets, WHITE, BLACK, BLUE, GRAY
from game_map import GameMap, MapManager, TILE_EMPTY, TILE_FLOOR, TILE_WALL, TILE_GRASS, TILE_WATER, TILE_ROAD, TILE_DOOR, TILE_NPC, TILE_PORTAL, TILE_SHOP, TILE_MOUNTAIN, TILE_FOREST, TILE_SAND, TILE_FOUNTAIN, TILE_BENCH, TILE_LAMP, TILE_SIGN, TILE_FLOWERBED, TILE_STATUE, TILE_TABLE, TILE_CHAIR, TILE_INN
from battle_system import BattleSystem
from menu_system import MenuSystem
from cutscene_system import CutsceneSystem
from quest_system import QuestSystem
from recruitment_system import RecruitmentSystem
from item_system import ItemSystem
from shop_system import ShopSystem
from aws_services import get_service_by_name, get_all_services

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "AWS Cloud Isekai RPG"

# Game states
STATE_TITLE = 0
STATE_GAME = 1
STATE_BATTLE = 2
STATE_DIALOG = 3
STATE_MENU = 4
STATE_CUTSCENE = 5
STATE_QUEST_LOG = 6
STATE_RECRUITMENT = 7
STATE_SHOP = 8
STATE_INVENTORY = 9
STATE_GAME_OVER = 10

class Game:
    instance = None  # Class variable to store the singleton instance
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.state = STATE_TITLE
        self.running = True
        
        # Load assets
        self.assets = GameAssets()
        
        # Player data
        self.player = {
            "name": "Rookie Engineer",
            "level": 1,
            "exp": 0,
            "hp": 100,
            "max_hp": 100,
            "mp": 50,
            "max_mp": 50,
            "attack": 10,
            "defense": 5,
            "credits": 1000,
            "position": [25, 25],  # Central crossroads
            "tile_x": 25,          # Central crossroads
            "tile_y": 25,          # Central crossroads
            "completed_quests": [],
            "defeated_bosses": [],
            "recruited_services": []
        }
        
        # Party members
        self.party = []
        
        # Map management
        self.map_manager = MapManager()
        
        # Battle system
        self.battle_system = BattleSystem(self.player, self.party, self.assets)
        
        # Menu system
        self.menu_system = MenuSystem(self.player, self.party, self.assets)
        
        # Cutscene system
        self.cutscene_system = CutsceneSystem(self.assets)
        
        # Quest system
        self.quest_system = QuestSystem(self.player, self.assets)
        
        # Recruitment system
        self.recruitment_system = RecruitmentSystem(self.player, self.party, self.assets)
        
        # Item system
        self.item_system = ItemSystem(self.player, self.assets)
        
        # Shop system
        self.shop_system = ShopSystem(self.player, self.assets)
        
        # Save file
        self.save_file = "save_data.json"
        
        # Discovered towns - initially only Computing Town is discovered
        self.discovered_towns = ["Computing Town"]
        
        # Dialog
        self.dialog = None
        self.dialog_npc = None
        self.dialog_npc_is_service = False
        
        # Camera position
        self.camera_x = 0
        self.camera_y = 0
        
        # Step counter (for random encounters)
        self.steps = 0
        
        # Title screen buttons
        self.title_buttons = {
            "new_game": pygame.Rect(300, 400, 200, 50),
            "continue": pygame.Rect(300, 460, 200, 50),
            "exit": pygame.Rect(300, 520, 200, 50)
        }
        
        # Initial quests
        self.quest_system.add_quest("meet_ec2")
        
        # Load saved game if exists
        self.save_file = "save_data.json"
        
    def save_game(self):
        """Save the current game state"""
        try:
            save_data = {
                "player": self.player,
                "party": self.party,
                "current_map": self.map_manager.current_map.name,
                "position": [self.player["tile_x"], self.player["tile_y"]],
                "quests": {
                    "active": self.quest_system.active_quests,
                    "completed": self.quest_system.completed_quests
                },
                "discovered_towns": self.discovered_towns
            }
            
            with open(self.save_file, 'w') as f:
                json.dump(save_data, f)
                
            print(f"Game saved successfully to {self.save_file}")
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False

# Set the Game.instance at the end of the file
if __name__ == "__main__":
    from main import Game
    Game.instance = Game()
    Game.instance.run()
