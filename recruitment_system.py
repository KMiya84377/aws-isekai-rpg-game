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
                    "question": "What does EC2 stand for?", 
                    "options": ["Elastic Compute Cloud", "Electronic Cloud Computing", 
                              "Enterprise Cloud Center", "Easy Cloud Control"],
                    "correct": 0
                },
                {
                    "question": "What is the characteristic of EC2 instance type 't3.micro'?",
                    "options": ["High-performance computing", "Burstable performance", 
                              "GPU computing", "Memory optimization"],
                    "correct": 1
                },
                {
                    "question": "Which AWS service is used to protect EC2 instances?",
                    "options": ["S3", "RDS", "Security Groups", "DynamoDB"],
                    "correct": 2
                }
            ],
            "s3": [
                {
                    "question": "What type of service is S3?", 
                    "options": ["Virtual server", "Object storage", 
                              "Relational database", "Content delivery"],
                    "correct": 1
                },
                {
                    "question": "Which S3 storage class is optimal for infrequently accessed data?",
                    "options": ["S3 Standard", "S3 Intelligent-Tiering", 
                              "S3 Standard-IA", "S3 One Zone-IA"],
                    "correct": 2
                },
                {
                    "question": "What is used for S3 bucket access control?",
                    "options": ["Security Groups", "Bucket policies", "Network ACLs", "VPC Endpoints"],
                    "correct": 1
                }
            ],
            "lambda": [
                {
                    "question": "What is the main feature of Lambda?", 
                    "options": ["Virtual server provision", "Serverless computing", 
                              "Relational database", "Content delivery"],
                    "correct": 1
                },
                {
                    "question": "What is the maximum execution time limit for Lambda?",
                    "options": ["5 minutes", "15 minutes", "1 hour", "Unlimited"],
                    "correct": 1
                },
                {
                    "question": "What can trigger Lambda functions?",
                    "options": ["S3 bucket changes", "EC2 instance launches", "RDS backups", "All of the above"],
                    "correct": 3
                }
            ],
            "dynamodb": [
                {
                    "question": "What type of database is DynamoDB?", 
                    "options": ["Relational", "NoSQL", "Graph", "Time series"],
                    "correct": 1
                },
                {
                    "question": "What are the components of a DynamoDB primary key?",
                    "options": ["Partition key only", "Sort key only", 
                              "Partition key and sort key", "Foreign key"],
                    "correct": 2
                },
                {
                    "question": "What is a strongly consistent read in DynamoDB?",
                    "options": ["Guarantee to read the latest data", "Low-latency read", 
                              "Batch processing read", "Cross-region read"],
                    "correct": 0
                }
            ],
            "rds": [
                {
                    "question": "Which database engine is supported by RDS?", 
                    "options": ["MongoDB", "MySQL", "Cassandra", "Redis"],
                    "correct": 1
                },
                {
                    "question": "What is a main advantage of RDS?",
                    "options": ["NoSQL flexibility", "Automatic backup and restore", 
                              "Serverless execution", "Static content hosting"],
                    "correct": 1
                },
                {
                    "question": "What is the purpose of RDS Multi-AZ deployment?",
                    "options": ["Performance improvement", "Cost reduction", 
                              "High availability", "Storage expansion"],
                    "correct": 2
                }
            ],
            "iam": [
                {
                    "question": "What is the main function of IAM?", 
                    "options": ["Content delivery", "Database management", 
                              "Access management", "Computing resource provision"],
                    "correct": 2
                },
                {
                    "question": "What is the basic structure of IAM policies?",
                    "options": ["XML format", "JSON format", 
                              "YAML format", "HTML format"],
                    "correct": 1
                },
                {
                    "question": "What is the principle of least privilege in IAM?",
                    "options": ["Give admin rights to all users", "Grant only necessary permissions", 
                              "Deny all permissions", "Change permissions regularly"],
                    "correct": 1
                }
            ],
            "cloudfront": [
                {
                    "question": "What is the main function of CloudFront?", 
                    "options": ["Database management", "Content Delivery Network", 
                              "Virtual server provision", "Identity management"],
                    "correct": 1
                },
                {
                    "question": "What is the purpose of CloudFront edge locations?",
                    "options": ["Persistent data storage", "Content caching and delivery", 
                              "Database backup", "Code execution"],
                    "correct": 1
                },
                {
                    "question": "Which AWS services can integrate with CloudFront?",
                    "options": ["S3", "EC2", "Lambda@Edge", "All of the above"],
                    "correct": 3
                }
            ],
            "ecs": [
                {
                    "question": "What does ECS stand for?", 
                    "options": ["Elastic Container Service", "Enterprise Computing System", 
                              "Enhanced Cloud Storage", "External Control System"],
                    "correct": 0
                },
                {
                    "question": "What does ECS help you manage?",
                    "options": ["Virtual machines", "Containerized applications", 
                              "Database tables", "Network configurations"],
                    "correct": 1
                },
                {
                    "question": "Which of these is a component of ECS?",
                    "options": ["Instances", "Tasks", "Volumes", "Subnets"],
                    "correct": 1
                }
            ],
            "fargate": [
                {
                    "question": "What is AWS Fargate?", 
                    "options": ["A database service", "A serverless compute engine for containers", 
                              "A storage service", "A networking service"],
                    "correct": 1
                },
                {
                    "question": "What do you NOT need to manage when using Fargate?",
                    "options": ["Container images", "Application code", 
                              "Underlying servers", "Task definitions"],
                    "correct": 2
                },
                {
                    "question": "Which services can use Fargate as a compute platform?",
                    "options": ["EC2", "ECS and EKS", "Lambda", "RDS"],
                    "correct": 1
                }
            ],
            "beanstalk": [
                {
                    "question": "What is Elastic Beanstalk?", 
                    "options": ["A database service", "A compute service", 
                              "A PaaS for deploying applications", "A storage service"],
                    "correct": 2
                },
                {
                    "question": "What does Elastic Beanstalk manage for you?",
                    "options": ["Only the application code", "Infrastructure, capacity provisioning, and application health", 
                              "Only the database", "Only load balancing"],
                    "correct": 1
                },
                {
                    "question": "Which programming languages does Elastic Beanstalk support?",
                    "options": ["Only Java", "Only Python and Ruby", 
                              "Java, .NET, PHP, Node.js, Python, Ruby, Go, and Docker", "Only compiled languages"],
                    "correct": 2
                }
            ],
            "cloudwatch": [
                {
                    "question": "What is CloudWatch primarily used for?", 
                    "options": ["Content delivery", "Monitoring and observability", 
                              "Database management", "Code deployment"],
                    "correct": 1
                },
                {
                    "question": "What can you create in CloudWatch to notify you when thresholds are breached?",
                    "options": ["Logs", "Metrics", "Alarms", "Dashboards"],
                    "correct": 2
                },
                {
                    "question": "What is the CloudWatch agent used for?",
                    "options": ["To collect logs and metrics from EC2 instances", "To deploy applications", 
                              "To manage databases", "To configure networks"],
                    "correct": 0
                }
            ],
            "cloudformation": [
                {
                    "question": "What is CloudFormation used for?", 
                    "options": ["Monitoring resources", "Infrastructure as Code", 
                              "Content delivery", "Database management"],
                    "correct": 1
                },
                {
                    "question": "What format are CloudFormation templates written in?",
                    "options": ["XML only", "JSON or YAML", "HTML", "Python"],
                    "correct": 1
                },
                {
                    "question": "What is a CloudFormation stack?",
                    "options": ["A collection of AWS resources", "A type of EC2 instance", 
                              "A monitoring dashboard", "A network configuration"],
                    "correct": 0
                }
            ],
            "stepfunctions": [
                {
                    "question": "What is AWS Step Functions?", 
                    "options": ["A database service", "A serverless workflow service", 
                              "A compute service", "A storage service"],
                    "correct": 1
                },
                {
                    "question": "How do you define workflows in Step Functions?",
                    "options": ["Using Python code", "Using Amazon States Language (ASL)", 
                              "Using SQL queries", "Using shell scripts"],
                    "correct": 1
                },
                {
                    "question": "What can you coordinate using Step Functions?",
                    "options": ["Only Lambda functions", "Only EC2 instances", 
                              "Multiple AWS services", "Only S3 buckets"],
                    "correct": 2
                }
            ],
            "sqs": [
                {
                    "question": "What does SQS stand for?", 
                    "options": ["Simple Query Service", "Simple Queue Service", 
                              "Secure Query System", "System Query Standard"],
                    "correct": 1
                },
                {
                    "question": "What type of service is SQS?",
                    "options": ["Database service", "Compute service", 
                              "Messaging service", "Storage service"],
                    "correct": 2
                },
                {
                    "question": "What are the two types of SQS queues?",
                    "options": ["Fast and slow", "Standard and FIFO", 
                              "Public and private", "Internal and external"],
                    "correct": 1
                }
            ],
            "ebs": [
                {
                    "question": "What does EBS stand for?", 
                    "options": ["Elastic Block Store", "Enterprise Backup System", 
                              "Extended Binary Storage", "External Backup Service"],
                    "correct": 0
                },
                {
                    "question": "What is EBS used for?",
                    "options": ["Object storage", "Block-level storage volumes for EC2", 
                              "File storage", "Database hosting"],
                    "correct": 1
                },
                {
                    "question": "Which EBS volume type is best for high-performance databases?",
                    "options": ["Standard (HDD)", "Cold HDD", "General Purpose SSD", "Provisioned IOPS SSD"],
                    "correct": 3
                }
            ],
            "glacier": [
                {
                    "question": "What is Amazon Glacier designed for?", 
                    "options": ["High-performance computing", "Frequently accessed data", 
                              "Long-term, low-cost archival storage", "Real-time data processing"],
                    "correct": 2
                },
                {
                    "question": "What is the retrieval time for Glacier data?",
                    "options": ["Immediate", "Minutes to hours", 
                              "Hours to days", "Weeks"],
                    "correct": 2
                },
                {
                    "question": "Which of these is a Glacier retrieval option?",
                    "options": ["Fast Track", "Expedited", "Immediate", "Instant"],
                    "correct": 1
                }
            ],
            "aurora": [
                {
                    "question": "What is Amazon Aurora?", 
                    "options": ["NoSQL database", "Relational database compatible with MySQL and PostgreSQL", 
                              "In-memory database", "Time-series database"],
                    "correct": 1
                },
                {
                    "question": "How much faster is Aurora compared to standard MySQL?",
                    "options": ["2x", "3x", "5x", "Up to 5x"],
                    "correct": 3
                },
                {
                    "question": "What is a key feature of Aurora's architecture?",
                    "options": ["Single AZ deployment", "Shared storage volume with 6 copies of data", 
                              "Maximum of 5 read replicas", "Manual failover only"],
                    "correct": 1
                }
            ],
            "shield": [
                {
                    "question": "What is AWS Shield designed to protect against?", 
                    "options": ["SQL injection", "DDoS attacks", 
                              "Malware", "Physical intrusion"],
                    "correct": 1
                },
                {
                    "question": "Which AWS Shield tier is included at no additional cost?",
                    "options": ["Shield Advanced", "Shield Standard", 
                              "Shield Premium", "Shield Basic"],
                    "correct": 1
                },
                {
                    "question": "Which services are protected by AWS Shield Standard?",
                    "options": ["Only EC2", "Only CloudFront", 
                              "CloudFront, Route 53, and Global Accelerator", "All AWS services"],
                    "correct": 2
                }
            ]
        }
        
    def start_recruitment(self, service_name):
        """指定したサービスの仲間にするプロセスを開始"""
        print(f"start_recruitment({service_name})が呼び出されました")
        
        # Handle special cases for service names
        if service_name == "elastic beanstalk":
            service_name = "beanstalk"
        elif service_name == "step functions":
            service_name = "stepfunctions"
            
        service = get_service_by_name(service_name)
        if service:
            print(f"サービスが見つかりました: {service['name']}")
            self.current_service = service
            self.state = "intro"
            self.current_question = 0
            self.correct_answers = 0
            self.selected_answer = None
            self.message = f"Take the quiz to recruit {service['name']} as a party member!"
            return True
        
        print(f"サービスが見つかりませんでした: {service_name}")
        return False
        
    def proceed(self):
        """次のステップに進む"""
        if self.state == "inactive" or not self.current_service:
            return False
            
        if self.state == "intro":
            self.state = "question"
            service_name = self.current_service["name"].lower()
            # Handle special cases for service names
            if service_name == "elastic beanstalk":
                service_name = "beanstalk"
            elif service_name == "step functions":
                service_name = "stepfunctions"
                
            print(f"Proceeding to question for service: {service_name}")
            
            if service_name in self.quiz_questions:
                self.message = self.quiz_questions[service_name][self.current_question]["question"]
                print(f"Question loaded: {self.message}")
            else:
                self.message = f"Quiz for {service_name} is not available yet."
                print(f"Quiz not found for service: {service_name}")
                self.state = "inactive"
                return False
            
        elif self.state == "question" and self.selected_answer is not None:
            # 回答チェック
            service_name = self.current_service["name"].lower()
            # Handle special cases for service names
            if service_name == "elastic beanstalk":
                service_name = "beanstalk"
            elif service_name == "step functions":
                service_name = "stepfunctions"
                
            correct = self.quiz_questions[service_name][self.current_question]["correct"]
            if self.selected_answer == correct:
                self.correct_answers += 1
                result_msg = "Correct!"
            else:
                options = self.quiz_questions[service_name][self.current_question]["options"]
                result_msg = f"Incorrect. The correct answer is '{options[correct]}'."
                
            # 次の問題へ
            self.current_question += 1
            
            # クイズ終了チェック
            if self.current_question >= len(self.quiz_questions[service_name]):
                self.state = "result"
                # 合格判定（1問以上正解で合格）
                if self.correct_answers > 0:
                    success = self._add_service_to_party()
                    if success:
                        self.message = result_msg + f"\nCongratulations! {self.current_service['name']} has joined your party!"
                        print(f"{self.current_service['name']} has joined your party!")
                    else:
                        self.message = result_msg + "\nYour party is full. Please remove someone before trying again."
                        print("Party is full")
                else:
                    self.message = f"{result_msg}\nSorry, you failed the quiz. Please try again."
                    print("Quiz failed")
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
            print(f"Answer selected: {index}")
            # 選択肢を選んだ後に自動的に決定ボタンをクリックする
            self.proceed()
            
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
        
        # Add to player's recruited services list
        if "recruited_services" not in self.player:
            self.player["recruited_services"] = []
        self.player["recruited_services"].append(self.current_service["name"])
        
        return True
        
    def draw(self, screen):
        """Draw the recruitment interface"""
        try:
            if self.state == "inactive" or not self.current_service:
                print("draw: Skipping drawing because state is inactive or current_service is None")
                return
                
            print(f"draw: state={self.state}, service={self.current_service['name']}")
            
            # Background overlay
            overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            
            # Main panel
            panel = pygame.Rect(100, 100, 600, 400)
            pygame.draw.rect(screen, (50, 50, 80), panel)
            pygame.draw.rect(screen, (255, 255, 255), panel, 2)
            
            # Service name
            service_name = self.assets.render_text(self.current_service["name"], "large", (255, 255, 255))
            screen.blit(service_name, (400 - service_name.get_width() // 2, 120))
            
            if self.state == "intro":
                # Description
                description = self.assets.render_text(self.current_service["description"], "normal", (255, 255, 255))
                screen.blit(description, (400 - description.get_width() // 2, 180))
                
                # Start button
                start_button = pygame.Rect(300, 400, 200, 50)
                pygame.draw.rect(screen, (100, 100, 200), start_button)
                pygame.draw.rect(screen, (255, 255, 255), start_button, 2)
                
                start_text = self.assets.render_text("Start Quiz", "normal", (255, 255, 255))
                screen.blit(start_text, (400 - start_text.get_width() // 2, 415))
                
            elif self.state == "question":
                # Question
                question = self.assets.render_text(self.message, "normal", (255, 255, 255))
                screen.blit(question, (400 - question.get_width() // 2, 180))
                
                # Options
                service_name = self.current_service["name"].lower()
                # Handle special cases for service names
                if service_name == "elastic beanstalk":
                    service_name = "beanstalk"
                elif service_name == "step functions":
                    service_name = "stepfunctions"
                    
                if service_name in self.quiz_questions and self.current_question < len(self.quiz_questions[service_name]):
                    options = self.quiz_questions[service_name][self.current_question]["options"]
                    for i, option in enumerate(options):
                        option_rect = pygame.Rect(150, 250 + i * 60, 500, 40)
                        
                        # Change color for selected option
                        if self.selected_answer == i:
                            pygame.draw.rect(screen, (100, 100, 200), option_rect)
                        else:
                            pygame.draw.rect(screen, (70, 70, 100), option_rect)
                            
                        pygame.draw.rect(screen, (255, 255, 255), option_rect, 1)
                        
                        # Make text smaller for laptop screens
                        option_text = self.assets.render_text(f"{i+1}. {option}", "small", (255, 255, 255))
                        screen.blit(option_text, (160, 260 + i * 60))
                    
                    # Submit button (only if an option is selected)
                    if self.selected_answer is not None:
                        submit_button = pygame.Rect(300, 430, 200, 50)
                        pygame.draw.rect(screen, (100, 100, 200), submit_button)
                        pygame.draw.rect(screen, (255, 255, 255), submit_button, 2)
                        
                        submit_text = self.assets.render_text("Submit", "normal", (255, 255, 255))
                        screen.blit(submit_text, (400 - submit_text.get_width() // 2, 445))
                        
                        # Debug info
                        print(f"Submit button drawn at: {submit_button}, selected answer: {self.selected_answer}")
                else:
                    error_text = self.assets.render_text("Error: Quiz data not found", "normal", (255, 100, 100))
                    screen.blit(error_text, (400 - error_text.get_width() // 2, 250))
                
            elif self.state == "result":
                # Results
                result_lines = self.message.split("\n")
                for i, line in enumerate(result_lines):
                    result_text = self.assets.render_text(line, "normal", (255, 255, 255))
                    screen.blit(result_text, (400 - result_text.get_width() // 2, 200 + i * 40))
                    
                # Continue button
                continue_button = pygame.Rect(300, 400, 200, 50)
                pygame.draw.rect(screen, (100, 100, 200), continue_button)
                pygame.draw.rect(screen, (255, 255, 255), continue_button, 2)
                
                continue_text = self.assets.render_text("Continue", "normal", (255, 255, 255))
                screen.blit(continue_text, (400 - continue_text.get_width() // 2, 415))
        except Exception as e:
            print(f"Error during recruitment system drawing: {e}")
            
    def handle_event(self, event):
        """Handle events for the recruitment system"""
        try:
            if self.state == "inactive" or not self.current_service:
                print("handle_event: Skipping event handling because state is inactive or current_service is None")
                return False
                
            print(f"handle_event: state={self.state}, event={event.type}")
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                print(f"Mouse clicked at: {mouse_pos}")
                
                if self.state == "intro":
                    # Start button
                    start_button = pygame.Rect(300, 400, 200, 50)
                    if start_button.collidepoint(mouse_pos):
                        print("Start button clicked")
                        self.proceed()
                        return True
                        
                elif self.state == "question":
                    # 選択肢
                    service_name = self.current_service["name"].lower()
                    # Handle special cases for service names
                    if service_name == "elastic beanstalk":
                        service_name = "beanstalk"
                    elif service_name == "step functions":
                        service_name = "stepfunctions"
                        
                    if service_name in self.quiz_questions and self.current_question < len(self.quiz_questions[service_name]):
                        options = self.quiz_questions[service_name][self.current_question]["options"]
                        
                        # 選択肢のクリックチェック
                        for i in range(len(options)):
                            option_rect = pygame.Rect(150, 250 + i * 60, 500, 40)
                            if option_rect.collidepoint(mouse_pos):
                                print(f"選択肢 {i+1} がクリックされました")
                                self.select_answer(i)
                                # 選択肢を選んだ後に自動的に決定ボタンをクリックする
                                self.proceed()
                                return True
                        
                        # 決定ボタンのクリックチェック
                        submit_button = pygame.Rect(300, 430, 200, 50)
                        if self.selected_answer is not None and submit_button.collidepoint(mouse_pos):
                            print(f"決定ボタンがクリックされました。選択された回答: {self.selected_answer}")
                            self.proceed()
                            return True
                        
                elif self.state == "result":
                    # 続行ボタン
                    continue_button = pygame.Rect(300, 400, 200, 50)
                    if continue_button.collidepoint(mouse_pos):
                        print("続行ボタンがクリックされました")
                        self.proceed()
                        return True
                        
            return False
        except Exception as e:
            print(f"仲間システムイベント処理中のエラー: {e}")
            import traceback
            traceback.print_exc()
            return False
