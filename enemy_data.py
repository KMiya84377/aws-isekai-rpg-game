#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 敵データの定義
ENEMY_DATA = {
    # 弱い敵
    "sql_injection": {
        "name": "SQL Injection",
        "hp": 40,
        "max_hp": 40,
        "attack": 8,
        "defense": 4,
        "exp_reward": 30,
        "credit_reward": 50,
        "description": "データベースを攻撃する脆弱性。入力値の検証とパラメータ化クエリで対策可能。"
    },
    "xss": {
        "name": "Cross-Site Scripting",
        "hp": 45,
        "max_hp": 45,
        "attack": 10,
        "defense": 3,
        "exp_reward": 35,
        "credit_reward": 55,
        "description": "Webページにスクリプトを注入する攻撃。入力のサニタイズで対策可能。"
    },
    "csrf": {
        "name": "CSRF Attack",
        "hp": 42,
        "max_hp": 42,
        "attack": 9,
        "defense": 5,
        "exp_reward": 32,
        "credit_reward": 52,
        "description": "ユーザーの意図しないリクエストを送信させる攻撃。トークン検証で対策可能。"
    },
    
    # 通常の敵
    "auth_bypass": {
        "name": "Authentication Bypass",
        "hp": 65,
        "max_hp": 65,
        "attack": 12,
        "defense": 6,
        "exp_reward": 50,
        "credit_reward": 100,
        "description": "認証をバイパスする攻撃。多要素認証と適切なセッション管理で対策可能。"
    },
    "path_traversal": {
        "name": "Path Traversal",
        "hp": 70,
        "max_hp": 70,
        "attack": 11,
        "defense": 8,
        "exp_reward": 55,
        "credit_reward": 105,
        "description": "ファイルパスを操作して不正アクセスする攻撃。入力検証とアクセス制限で対策可能。"
    },
    "insecure_deserialization": {
        "name": "Insecure Deserialization",
        "hp": 75,
        "max_hp": 75,
        "attack": 13,
        "defense": 7,
        "exp_reward": 60,
        "credit_reward": 110,
        "description": "シリアライズされたデータを悪用する攻撃。データの検証と型チェックで対策可能。"
    },
    
    # 強い敵
    "privilege_escalation": {
        "name": "Privilege Escalation",
        "hp": 100,
        "max_hp": 100,
        "attack": 16,
        "defense": 10,
        "exp_reward": 80,
        "credit_reward": 150,
        "description": "権限を不正に昇格させる攻撃。最小権限の原則と適切なアクセス制御で対策可能。"
    },
    "data_breach": {
        "name": "Data Breach",
        "hp": 110,
        "max_hp": 110,
        "attack": 18,
        "defense": 9,
        "exp_reward": 85,
        "credit_reward": 160,
        "description": "データの漏洩を引き起こす攻撃。暗号化と適切なアクセス管理で対策可能。"
    },
    "zero_day": {
        "name": "Zero-Day Exploit",
        "hp": 120,
        "max_hp": 120,
        "attack": 20,
        "defense": 11,
        "exp_reward": 90,
        "credit_reward": 170,
        "description": "未知の脆弱性を突く攻撃。定期的なアップデートと多層防御で対策可能。"
    },
    
    # ボス
    "ddos": {
        "name": "DDoS Attack",
        "hp": 150,
        "max_hp": 150,
        "attack": 22,
        "defense": 12,
        "exp_reward": 150,
        "credit_reward": 300,
        "description": "サービスを利用不能にする大規模な攻撃。AWS Shield と Auto Scaling で対策可能。"
    },
    "ransomware": {
        "name": "Ransomware",
        "hp": 180,
        "max_hp": 180,
        "attack": 24,
        "defense": 14,
        "exp_reward": 160,
        "credit_reward": 320,
        "description": "データを暗号化して身代金を要求する攻撃。バックアップと最小権限で対策可能。"
    },
    "apt": {
        "name": "Advanced Persistent Threat",
        "hp": 200,
        "max_hp": 200,
        "attack": 26,
        "defense": 15,
        "exp_reward": 180,
        "credit_reward": 350,
        "description": "長期間にわたる高度な攻撃。包括的なセキュリティ対策と監視で対応。"
    }
}

def get_enemy_by_type(enemy_type):
    """敵タイプに基づいて敵データを取得"""
    if enemy_type == "weak":
        import random
        weak_enemies = ["sql_injection", "xss", "csrf"]
        return ENEMY_DATA[random.choice(weak_enemies)].copy()
    elif enemy_type == "normal":
        import random
        normal_enemies = ["auth_bypass", "path_traversal", "insecure_deserialization"]
        return ENEMY_DATA[random.choice(normal_enemies)].copy()
    elif enemy_type == "strong":
        import random
        strong_enemies = ["privilege_escalation", "data_breach", "zero_day"]
        return ENEMY_DATA[random.choice(strong_enemies)].copy()
    elif enemy_type == "boss":
        import random
        boss_enemies = ["ddos", "ransomware", "apt"]
        return ENEMY_DATA[random.choice(boss_enemies)].copy()
    elif enemy_type in ENEMY_DATA:
        return ENEMY_DATA[enemy_type].copy()
    else:
        # デフォルト
        return ENEMY_DATA["auth_bypass"].copy()
