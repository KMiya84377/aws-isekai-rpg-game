#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

def save_test_data():
    """Create a test save file"""
    save_data = {
        "player": {
            "name": "Test Player",
            "level": 5,
            "exp": 500,
            "hp": 200,
            "max_hp": 200,
            "mp": 100,
            "max_mp": 100,
            "attack": 20,
            "defense": 10,
            "credits": 2000,
            "position": [30, 30],
            "tile_x": 30,
            "tile_y": 30,
            "completed_quests": ["meet_ec2"],
            "defeated_bosses": [],
            "recruited_services": []
        },
        "party": [],
        "current_map": "Computing Town",
        "position": [30, 30],
        "quests": {
            "active": ["explore_computing_town"],
            "completed": ["meet_ec2"]
        },
        "discovered_towns": ["Computing Town", "Storage Town"]
    }
    
    with open("save_data.json", 'w') as f:
        json.dump(save_data, f)
        
    print("Test save file created successfully!")
    
def load_test_data():
    """Load and display the save file"""
    if not os.path.exists("save_data.json"):
        print("No save file found")
        return
        
    with open("save_data.json", 'r') as f:
        save_data = json.load(f)
        
    print("Save file contents:")
    print(f"Player: {save_data['player']['name']}, Level {save_data['player']['level']}")
    print(f"Position: {save_data['position']}")
    print(f"Current Map: {save_data['current_map']}")
    print(f"Active Quests: {save_data['quests']['active']}")
    print(f"Completed Quests: {save_data['quests']['completed']}")
    print(f"Discovered Towns: {save_data['discovered_towns']}")
    
if __name__ == "__main__":
    save_test_data()
    load_test_data()
