#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import random
from game_assets import WHITE, BLACK, BLUE, GRAY, GREEN, YELLOW
from aws_services import get_service_by_name, get_all_services

class RecruitmentSystem:
    def __init__(self, player, party, assets):
        self.player = player
        self.party = party
        self.assets = assets
        self.state = "inactive"  # inactive, intro, question, result
        self.current_service = None
        self.current_question = 0
        self.selected_answer = None
        self.correct_answers = 0
        self.message = ""
        self.quiz_questions = {}
        self._init_quiz_questions()
        
    def _init_quiz_questions(self):
        """クイズの質問を初期化"""
        self.quiz_questions = {
            "ec2": [
                {
                    "question": "EC2とは何の略称ですか？", 
                    "options": ["Elastic Compute Cloud", "Electronic Cloud Computing", 
                              "Enterprise Cloud Center", "Easy Cloud Control"],
                    "correct": 0
                },
                {
                    "question": "EC2インスタンスタイプの「t3.micro」の特徴は？",
                    "options": ["高性能コンピューティング", "バーストパフォーマンス", 
                              "GPUコンピューティング", "メモリ最適化"],
                    "correct": 1
                },
                {
                    "question": "EC2インスタンスを保護するために使用するAWSサービスは？",
                    "options": ["S3", "RDS", "Security Groups", "DynamoDB"],
                    "correct": 2
                }
            ],
            "s3": [
                {
                    "question": "S3はどのようなサービスですか？", 
                    "options": ["仮想サーバー", "オブジェクトストレージ", 
                              "リレーショナルデータベース", "コンテンツ配信"],
                    "correct": 1
                },
                {
                    "question": "S3のストレージクラスで、アクセス頻度が低いデータに最適なものは？",
                    "options": ["S3 Standard", "S3 Intelligent-Tiering", 
                              "S3 Standard-IA", "S3 One Zone-IA"],
                    "correct": 2
                },
                {
                    "question": "S3バケットのアクセス制御に使用されるものは？",
                    "options": ["Security Groups", "バケットポリシー", "ネットワークACL", "VPC Endpoints"],
                    "correct": 1
                }
            ],
            "lambda": [
                {
                    "question": "Lambdaの主な特徴は？", 
                    "options": ["仮想サーバーの提供", "サーバーレスコンピューティング", 
                              "リレーショナルデータベース", "コンテンツ配信"],
                    "correct": 1
                },
                {
                    "question": "Lambdaの実行時間の最大制限は？",
                    "options": ["5分", "15分", "1時間", "無制限"],
                    "correct": 1
                },
                {
                    "question": "Lambdaをトリガーできるイベントソースは？",
                    "options": ["S3バケットの変更", "EC2インスタンスの起動", "RDSのバックアップ", "以上すべて"],
                    "correct": 3
                }
            ],
            "dynamodb": [
                {
                    "question": "DynamoDBはどのタイプのデータベースですか？", 
                    "options": ["リレーショナル", "NoSQL", "グラフ", "時系列"],
                    "correct": 1
                },
                {
                    "question": "DynamoDBのプライマリキーの構成要素として正しいものは？",
                    "options": ["パーティションキーのみ", "ソートキーのみ", 
                              "パーティションキーとソートキー", "外部キー"],
                    "correct": 2
                },
                {
                    "question": "DynamoDBの一貫性のあるリードとは？",
                    "options": ["最新のデータを読み取る保証", "低レイテンシーの読み取り", 
                              "バッチ処理での読み取り", "クロスリージョンの読み取り"],
                    "correct": 0
                }
            ],
            "rds": [
                {
                    "question": "RDSでサポートされているデータベースエンジンは？", 
                    "options": ["MongoDB", "MySQL", "Cassandra", "Redis"],
                    "correct": 1
                },
                {
                    "question": "RDSの主な利点は？",
                    "options": ["NoSQLの柔軟性", "自動バックアップと復元", 
                              "サーバーレス実行", "静的コンテンツのホスティング"],
                    "correct": 1
                },
                {
                    "question": "RDSのマルチAZ配置の目的は？",
                    "options": ["パフォーマンスの向上", "コスト削減", 
                              "高可用性の確保", "ストレージの拡張"],
                    "correct": 2
                }
            ],
            "iam": [
                {
                    "question": "IAMの主な機能は？", 
                    "options": ["コンテンツ配信", "データベース管理", 
                              "アクセス管理", "コンピューティングリソースの提供"],
                    "correct": 2
                },
                {
                    "question": "IAMポリシーの基本構造は？",
                    "options": ["XML形式", "JSON形式", 
                              "YAML形式", "HTML形式"],
                    "correct": 1
                },
                {
                    "question": "IAMの最小権限の原則とは？",
                    "options": ["すべてのユーザーに管理者権限を与える", "必要最小限の権限のみを付与する", 
                              "すべての権限を拒否する", "権限を定期的に変更する"],
                    "correct": 1
                }
            ],
            "cloudfront": [
                {
                    "question": "CloudFrontの主な機能は？", 
                    "options": ["データベース管理", "コンテンツ配信ネットワーク", 
                              "仮想サーバーの提供", "アイデンティティ管理"],
                    "correct": 1
                },
                {
                    "question": "CloudFrontのエッジロケーションの目的は？",
                    "options": ["データの永続的な保存", "コンテンツのキャッシュと配信", 
                              "データベースのバックアップ", "コードの実行"],
                    "correct": 1
                },
                {
                    "question": "CloudFrontと連携できるAWSサービスは？",
                    "options": ["S3", "EC2", "Lambda@Edge", "すべて正解"],
                    "correct": 3
                }
            ]
        }
        
    def start_recruitment(self, service_name):
        """指定したサービスの仲間にするプロセスを開始"""
        service = get_service_by_name(service_name)
        if service:
            self.current_service = service
            self.state = "intro"
            self.current_question = 0
            self.correct_answers = 0
            self.selected_answer = None
            self.message = service["name"] + "を仲間にするためのクイズに挑戦します！"
            return True
                
        return False
        
    def proceed(self):
        """次のステップに進む"""
        if self.state == "inactive" or not self.current_service:
            return False
            
        if self.state == "intro":
            self.state = "question"
            service_name = self.current_service["name"].lower()
            if service_name in self.quiz_questions:
                self.message = self.quiz_questions[service_name][self.current_question]["question"]
            else:
                self.message = "このサービスのクイズはまだ準備されていません。"
                self.state = "inactive"
                return False
            
        elif self.state == "question" and self.selected_answer is not None:
            # 回答チェック
            service_name = self.current_service["name"].lower()
            correct = self.quiz_questions[service_name][self.current_question]["correct"]
            if self.selected_answer == correct:
                self.correct_answers += 1
                result_msg = "正解です！"
            else:
                options = self.quiz_questions[service_name][self.current_question]["options"]
                result_msg = f"不正解です。正解は「{options[correct]}」でした。"
                
            # 次の問題へ
            self.current_question += 1
            
            # クイズ終了チェック
            if self.current_question >= len(self.quiz_questions[service_name]):
                self.state = "result"
                # 合格判定（すべて正解で合格）
                if self.correct_answers == len(self.quiz_questions[service_name]):
                    self._add_service_to_party()
                    self.message = result_msg + "\nおめでとうございます！" + self.current_service["name"] + "があなたの仲間になりました！"
                else:
                    self.message = f"{result_msg}\n残念ながら不合格です。もう一度チャレンジしてください。"
            else:
                # 次の問題
                self.state = "question"
                self.selected_answer = None
                self.message = result_msg + "\n\n" + self.quiz_questions[service_name][self.current_question]["question"]
                
        elif self.state == "result":
            # 終了
            self.state = "inactive"
            self.current_service = None
            return True
            
        return True
        
    def select_answer(self, index):
        """回答を選択"""
        if self.state == "question":
            self.selected_answer = index
            
    def _add_service_to_party(self):
        """サービスをパーティに追加"""
        if len(self.party) >= 3:
            # パーティが満員の場合
            return False
            
        # 新しいパーティメンバーを作成
        new_member = {
            "name": self.current_service["name"],
            "full_name": self.current_service["full_name"],
            "category": self.current_service["category"],
            "hp": self.current_service["hp"],
            "max_hp": self.current_service["max_hp"],
            "mp": self.current_service["mp"],
            "max_mp": self.current_service["max_mp"],
            "attack": self.current_service["attack"],
            "defense": self.current_service["defense"],
            "level": self.current_service["level"],
            "skills": self.current_service["skills"].copy(),
            "icon": self.current_service["icon"],
            "color": self.current_service["color"]
        }
        
        self.party.append(new_member)
        
        # プレイヤーの仲間リストに追加
        if "recruited_services" not in self.player:
            self.player["recruited_services"] = []
        self.player["recruited_services"].append(self.current_service["name"])
        
        return True
        
    def draw(self, screen):
        """画面描画"""
        if self.state == "inactive" or not self.current_service:
            return
            
        # 背景オーバーレイ
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        # メインパネル
        panel = pygame.Rect(100, 100, 600, 400)
        pygame.draw.rect(screen, (50, 50, 80), panel)
        pygame.draw.rect(screen, (255, 255, 255), panel, 2)
        
        # サービス名
        service_name = self.assets.render_text(self.current_service["name"], "large", (255, 255, 255))
        screen.blit(service_name, (400 - service_name.get_width() // 2, 120))
        
        if self.state == "intro":
            # 説明
            description = self.assets.render_text(self.current_service["description"], "normal", (255, 255, 255))
            screen.blit(description, (400 - description.get_width() // 2, 180))
            
            # 開始ボタン
            start_button = pygame.Rect(300, 400, 200, 50)
            pygame.draw.rect(screen, (100, 100, 200), start_button)
            pygame.draw.rect(screen, (255, 255, 255), start_button, 2)
            
            start_text = self.assets.render_text("クイズを開始", "normal", (255, 255, 255))
            screen.blit(start_text, (400 - start_text.get_width() // 2, 415))
            
        elif self.state == "question":
            # 問題
            question = self.assets.render_text(self.message, "normal", (255, 255, 255))
            screen.blit(question, (400 - question.get_width() // 2, 180))
            
            # 選択肢
            service_name = self.current_service["name"].lower()
            options = self.quiz_questions[service_name][self.current_question]["options"]
            for i, option in enumerate(options):
                option_rect = pygame.Rect(150, 250 + i * 60, 500, 40)
                
                # 選択中の選択肢は色を変える
                if self.selected_answer == i:
                    pygame.draw.rect(screen, (100, 100, 200), option_rect)
                else:
                    pygame.draw.rect(screen, (70, 70, 100), option_rect)
                    
                pygame.draw.rect(screen, (255, 255, 255), option_rect, 1)
                
                option_text = self.assets.render_text(f"{i+1}. {option}", "normal", (255, 255, 255))
                screen.blit(option_text, (160, 260 + i * 60))
                
            # 決定ボタン（選択肢を選んだ場合のみ）
            if self.selected_answer is not None:
                submit_button = pygame.Rect(300, 430, 200, 50)
                pygame.draw.rect(screen, (100, 100, 200), submit_button)
                pygame.draw.rect(screen, (255, 255, 255), submit_button, 2)
                
                submit_text = self.assets.render_text("決定", "normal", (255, 255, 255))
                screen.blit(submit_text, (400 - submit_text.get_width() // 2, 445))
                
        elif self.state == "result":
            # 結果
            result_lines = self.message.split("\n")
            for i, line in enumerate(result_lines):
                result_text = self.assets.render_text(line, "normal", (255, 255, 255))
                screen.blit(result_text, (400 - result_text.get_width() // 2, 200 + i * 40))
                
            # 続行ボタン
            continue_button = pygame.Rect(300, 400, 200, 50)
            pygame.draw.rect(screen, (100, 100, 200), continue_button)
            pygame.draw.rect(screen, (255, 255, 255), continue_button, 2)
            
            continue_text = self.assets.render_text("続ける", "normal", (255, 255, 255))
            screen.blit(continue_text, (400 - continue_text.get_width() // 2, 415))
            
    def handle_event(self, event):
        """イベント処理"""
        if self.state == "inactive" or not self.current_service:
            return False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.state == "intro":
                # 開始ボタン
                if pygame.Rect(300, 400, 200, 50).collidepoint(event.pos):
                    self.proceed()
                    return True
                    
            elif self.state == "question":
                # 選択肢
                service_name = self.current_service["name"].lower()
                options = self.quiz_questions[service_name][self.current_question]["options"]
                for i in range(len(options)):
                    if pygame.Rect(150, 250 + i * 60, 500, 40).collidepoint(event.pos):
                        self.select_answer(i)
                        return True
                        
                # 決定ボタン
                if self.selected_answer is not None and pygame.Rect(300, 430, 200, 50).collidepoint(event.pos):
                    self.proceed()
                    return True
                    
            elif self.state == "result":
                # 続行ボタン
                if pygame.Rect(300, 400, 200, 50).collidepoint(event.pos):
                    self.proceed()
                    return True
                    
        return False
