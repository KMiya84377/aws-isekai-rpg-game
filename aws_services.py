#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# AWSサービスデータの定義
AWS_SERVICES = {
    # コンピューティングサービス
    "ec2": {
        "name": "EC2",
        "full_name": "Elastic Compute Cloud",
        "category": "Compute",
        "hp": 120,
        "max_hp": 120,
        "mp": 60,
        "max_mp": 60,
        "attack": 15,
        "defense": 10,
        "level": 1,
        "icon": "ec2.png",
        "color": (255, 153, 0),  # オレンジ
        "description": "クラウド上の仮想サーバー。スケーラブルなコンピューティング能力を提供。",
        "skills": [
            {"name": "インスタンス起動", "power": 30, "cost": 10, "description": "新しいインスタンスを起動して攻撃"},
            {"name": "オートスケーリング", "power": 50, "cost": 25, "description": "負荷に応じて自動的にスケールして攻撃"}
        ],
        "recruitment_quest": "ec2_quest",
        "dialog": "私はEC2、AWSの仮想サーバーサービスだ。柔軟なコンピューティングリソースが必要なら任せてくれ。"
    },
    
    # ストレージサービス
    "s3": {
        "name": "S3",
        "full_name": "Simple Storage Service",
        "category": "Storage",
        "hp": 100,
        "max_hp": 100,
        "mp": 80,
        "max_mp": 80,
        "attack": 10,
        "defense": 15,
        "level": 1,
        "icon": "s3.png",
        "color": (227, 86, 0),  # 赤茶色
        "description": "スケーラブルなオブジェクトストレージサービス。高い耐久性と可用性を提供。",
        "skills": [
            {"name": "バケット作成", "power": 20, "cost": 5, "description": "新しいストレージバケットを作成して防御"},
            {"name": "データアーカイブ", "power": 40, "cost": 15, "description": "データをアーカイブして強力な攻撃"}
        ],
        "recruitment_quest": "s3_quest",
        "dialog": "私はS3、AWSのオブジェクトストレージサービスだ。データの保存なら私に任せてくれ。"
    },
    
    # サーバーレスサービス
    "lambda": {
        "name": "Lambda",
        "full_name": "AWS Lambda",
        "category": "Serverless",
        "hp": 90,
        "max_hp": 90,
        "mp": 100,
        "max_mp": 100,
        "attack": 20,
        "defense": 8,
        "level": 1,
        "icon": "lambda.png",
        "color": (147, 47, 194),  # 紫
        "description": "サーバーレスでコードを実行するサービス。イベント駆動型アプリケーションに最適。",
        "skills": [
            {"name": "関数デプロイ", "power": 25, "cost": 8, "description": "新しい関数をデプロイして攻撃"},
            {"name": "イベント駆動実行", "power": 45, "cost": 20, "description": "イベントに応じて関数を実行して攻撃"}
        ],
        "recruitment_quest": "lambda_quest",
        "dialog": "私はLambda、AWSのサーバーレスコンピューティングサービスだ。コードの実行なら私に任せてくれ。"
    },
    
    # データベースサービス
    "dynamodb": {
        "name": "DynamoDB",
        "full_name": "Amazon DynamoDB",
        "category": "Database",
        "hp": 110,
        "max_hp": 110,
        "mp": 70,
        "max_mp": 70,
        "attack": 12,
        "defense": 12,
        "level": 1,
        "icon": "dynamodb.png",
        "color": (61, 133, 198),  # 青
        "description": "フルマネージド型NoSQLデータベースサービス。シームレスなスケーラビリティを提供。",
        "skills": [
            {"name": "テーブル作成", "power": 22, "cost": 7, "description": "新しいテーブルを作成して防御"},
            {"name": "クエリ実行", "power": 42, "cost": 18, "description": "高速クエリを実行して攻撃"}
        ],
        "recruitment_quest": "dynamodb_quest",
        "dialog": "私はDynamoDB、AWSのNoSQLデータベースサービスだ。スケーラブルなデータ管理が必要なら任せてくれ。"
    },
    
    "rds": {
        "name": "RDS",
        "full_name": "Relational Database Service",
        "category": "Database",
        "hp": 115,
        "max_hp": 115,
        "mp": 75,
        "max_mp": 75,
        "attack": 14,
        "defense": 14,
        "level": 1,
        "icon": "rds.png",
        "color": (0, 115, 207),  # 濃い青
        "description": "リレーショナルデータベースを簡単にセットアップ、運用、スケールできるサービス。",
        "skills": [
            {"name": "インスタンス作成", "power": 24, "cost": 9, "description": "新しいDBインスタンスを作成して防御"},
            {"name": "SQL実行", "power": 44, "cost": 22, "description": "複雑なSQLクエリを実行して攻撃"}
        ],
        "recruitment_quest": "rds_quest",
        "dialog": "私はRDS、AWSのリレーショナルデータベースサービスだ。堅牢なデータ管理が必要なら任せてくれ。"
    },
    
    # セキュリティサービス
    "iam": {
        "name": "IAM",
        "full_name": "Identity and Access Management",
        "category": "Security",
        "hp": 95,
        "max_hp": 95,
        "mp": 90,
        "max_mp": 90,
        "attack": 13,
        "defense": 18,
        "level": 1,
        "icon": "iam.png",
        "color": (232, 116, 0),  # オレンジ
        "description": "AWSリソースへのアクセスを安全に制御するサービス。最小権限の原則を実現。",
        "skills": [
            {"name": "ポリシー作成", "power": 26, "cost": 12, "description": "セキュリティポリシーを作成して防御"},
            {"name": "アクセス制御", "power": 46, "cost": 24, "description": "厳格なアクセス制御で攻撃を防ぐ"}
        ],
        "recruitment_quest": "iam_quest",
        "dialog": "私はIAM、AWSのアイデンティティ管理サービスだ。セキュアなアクセス制御が必要なら任せてくれ。"
    },
    
    "cloudfront": {
        "name": "CloudFront",
        "full_name": "Amazon CloudFront",
        "category": "Networking",
        "hp": 105,
        "max_hp": 105,
        "mp": 85,
        "max_mp": 85,
        "attack": 16,
        "defense": 13,
        "level": 1,
        "icon": "cloudfront.png",
        "color": (143, 78, 173),  # 薄紫
        "description": "グローバルなコンテンツ配信ネットワーク（CDN）サービス。低レイテンシーでコンテンツを配信。",
        "skills": [
            {"name": "エッジロケーション", "power": 28, "cost": 14, "description": "世界中のエッジロケーションから攻撃"},
            {"name": "キャッシュ最適化", "power": 48, "cost": 26, "description": "コンテンツをキャッシュして高速攻撃"}
        ],
        "recruitment_quest": "cloudfront_quest",
        "dialog": "私はCloudFront、AWSのCDNサービスだ。高速なコンテンツ配信が必要なら任せてくれ。"
    }
}

def get_service_by_name(name):
    """サービス名からサービスデータを取得"""
    name_lower = name.lower()
    if name_lower in AWS_SERVICES:
        return AWS_SERVICES[name_lower].copy()
    return None

def get_all_services():
    """すべてのサービスのリストを取得"""
    return list(AWS_SERVICES.values())

def get_services_by_category(category):
    """カテゴリでフィルタリングしたサービスのリストを取得"""
    return [service for service in AWS_SERVICES.values() if service["category"] == category]

    return list(AWS_SERVICES.values())

def get_services_by_category(category):
    """カテゴリでフィルタリングしたサービスのリストを取得"""
    return [service for service in AWS_SERVICES.values() if service["category"] == category]

# 追加のAWSサービス
AWS_SERVICES["ecs"] = {
    "name": "ECS",
    "full_name": "Elastic Container Service",
    "category": "Compute",
    "hp": 110,
    "max_hp": 110,
    "mp": 70,
    "max_mp": 70,
    "attack": 14,
    "defense": 12,
    "level": 1,
    "icon": "ecs.png",
    "color": (255, 153, 0),  # オレンジ
    "description": "コンテナ化されたアプリケーションを簡単に実行・管理できるサービス。",
    "skills": [
        {"name": "タスク起動", "power": 25, "cost": 10, "description": "コンテナタスクを起動して攻撃"},
        {"name": "クラスター管理", "power": 45, "cost": 20, "description": "コンテナクラスターを最適化して攻撃"}
    ],
    "recruitment_quest": "ecs_quest",
    "dialog": "私はECS、AWSのコンテナオーケストレーションサービスだ。コンテナ管理が必要なら任せてくれ。"
}

AWS_SERVICES["fargate"] = {
    "name": "Fargate",
    "full_name": "AWS Fargate",
    "category": "Compute",
    "hp": 100,
    "max_hp": 100,
    "mp": 85,
    "max_mp": 85,
    "attack": 16,
    "defense": 10,
    "level": 1,
    "icon": "fargate.png",
    "color": (255, 153, 0),  # オレンジ
    "description": "サーバーレスコンテナ実行環境。インフラ管理なしでコンテナを実行できる。",
    "skills": [
        {"name": "サーバーレス実行", "power": 28, "cost": 12, "description": "インフラ管理なしでコンテナを実行して攻撃"},
        {"name": "リソース最適化", "power": 48, "cost": 22, "description": "リソースを最適化して強力な攻撃"}
    ],
    "recruitment_quest": "fargate_quest",
    "dialog": "私はFargate、AWSのサーバーレスコンテナサービスだ。インフラ管理から解放されたいなら任せてくれ。"
}

AWS_SERVICES["beanstalk"] = {
    "name": "Elastic Beanstalk",
    "full_name": "AWS Elastic Beanstalk",
    "category": "Compute",
    "hp": 105,
    "max_hp": 105,
    "mp": 75,
    "max_mp": 75,
    "attack": 13,
    "defense": 13,
    "level": 1,
    "icon": "beanstalk.png",
    "color": (255, 153, 0),  # オレンジ
    "description": "アプリケーションのデプロイと管理を簡素化するサービス。",
    "skills": [
        {"name": "環境作成", "power": 26, "cost": 11, "description": "新しい環境を作成して攻撃"},
        {"name": "自動スケーリング", "power": 46, "cost": 21, "description": "自動的にスケールして強力な攻撃"}
    ],
    "recruitment_quest": "beanstalk_quest",
    "dialog": "私はElastic Beanstalk、AWSのPaaSサービスだ。アプリケーションのデプロイと管理を簡単にしたいなら任せてくれ。"
}

AWS_SERVICES["ebs"] = {
    "name": "EBS",
    "full_name": "Elastic Block Store",
    "category": "Storage",
    "hp": 115,
    "max_hp": 115,
    "mp": 65,
    "max_mp": 65,
    "attack": 12,
    "defense": 16,
    "level": 1,
    "icon": "ebs.png",
    "color": (227, 86, 0),  # 赤茶色
    "description": "EC2インスタンス用の永続ストレージを提供するブロックストレージサービス。",
    "skills": [
        {"name": "ボリューム作成", "power": 24, "cost": 9, "description": "新しいボリュームを作成して防御"},
        {"name": "スナップショット", "power": 44, "cost": 19, "description": "スナップショットを取得して攻撃"}
    ],
    "recruitment_quest": "ebs_quest",
    "dialog": "私はEBS、AWSのブロックストレージサービスだ。永続的なストレージが必要なら任せてくれ。"
}

AWS_SERVICES["efs"] = {
    "name": "EFS",
    "full_name": "Elastic File System",
    "category": "Storage",
    "hp": 105,
    "max_hp": 105,
    "mp": 75,
    "max_mp": 75,
    "attack": 13,
    "defense": 14,
    "level": 1,
    "icon": "efs.png",
    "color": (227, 86, 0),  # 赤茶色
    "description": "複数のEC2インスタンスで共有できるファイルシステムを提供するサービス。",
    "skills": [
        {"name": "ファイルシステム作成", "power": 25, "cost": 10, "description": "新しいファイルシステムを作成して防御"},
        {"name": "マウントターゲット", "power": 45, "cost": 20, "description": "マウントターゲットを設定して攻撃"}
    ],
    "recruitment_quest": "efs_quest",
    "dialog": "私はEFS、AWSの共有ファイルシステムサービスだ。複数のインスタンスでファイルを共有したいなら任せてくれ。"
}

AWS_SERVICES["glacier"] = {
    "name": "Glacier",
    "full_name": "Amazon Glacier",
    "category": "Storage",
    "hp": 120,
    "max_hp": 120,
    "mp": 60,
    "max_mp": 60,
    "attack": 10,
    "defense": 18,
    "level": 1,
    "icon": "glacier.png",
    "color": (227, 86, 0),  # 赤茶色
    "description": "長期保存用の低コストストレージを提供するサービス。",
    "skills": [
        {"name": "アーカイブ作成", "power": 22, "cost": 8, "description": "データをアーカイブして防御"},
        {"name": "ボールト保護", "power": 42, "cost": 18, "description": "ボールトを保護して強力な防御"}
    ],
    "recruitment_quest": "glacier_quest",
    "dialog": "私はGlacier、AWSの長期保存ストレージサービスだ。低コストでデータを長期保存したいなら任せてくれ。"
}

AWS_SERVICES["storage_gateway"] = {
    "name": "Storage Gateway",
    "full_name": "AWS Storage Gateway",
    "category": "Storage",
    "hp": 110,
    "max_hp": 110,
    "mp": 70,
    "max_mp": 70,
    "attack": 14,
    "defense": 14,
    "level": 1,
    "icon": "storage_gateway.png",
    "color": (227, 86, 0),  # 赤茶色
    "description": "オンプレミスとAWSストレージを橋渡しするハイブリッドストレージサービス。",
    "skills": [
        {"name": "ファイルゲートウェイ", "power": 26, "cost": 11, "description": "ファイルゲートウェイを設定して攻撃"},
        {"name": "ボリュームゲートウェイ", "power": 46, "cost": 21, "description": "ボリュームゲートウェイを使って強力な攻撃"}
    ],
    "recruitment_quest": "storage_gateway_quest",
    "dialog": "私はStorage Gateway、AWSのハイブリッドストレージサービスだ。オンプレミスとクラウドを繋ぎたいなら任せてくれ。"
}

AWS_SERVICES["redshift"] = {
    "name": "Redshift",
    "full_name": "Amazon Redshift",
    "category": "Database",
    "hp": 115,
    "max_hp": 115,
    "mp": 75,
    "max_mp": 75,
    "attack": 16,
    "defense": 12,
    "level": 1,
    "icon": "redshift.png",
    "color": (61, 133, 198),  # 青
    "description": "データウェアハウスサービスとして、大規模なデータ分析を高速に実行できる。",
    "skills": [
        {"name": "クラスター作成", "power": 28, "cost": 13, "description": "新しいクラスターを作成して攻撃"},
        {"name": "並列処理", "power": 48, "cost": 23, "description": "並列処理で高速に攻撃"}
    ],
    "recruitment_quest": "redshift_quest",
    "dialog": "私はRedshift、AWSのデータウェアハウスサービスだ。大規模なデータ分析が必要なら任せてくれ。"
}

AWS_SERVICES["waf"] = {
    "name": "WAF",
    "full_name": "Web Application Firewall",
    "category": "Security",
    "hp": 100,
    "max_hp": 100,
    "mp": 80,
    "max_mp": 80,
    "attack": 12,
    "defense": 16,
    "level": 1,
    "icon": "waf.png",
    "color": (232, 116, 0),  # オレンジ
    "description": "ウェブアプリケーションを攻撃から守るファイアウォールサービス。",
    "skills": [
        {"name": "ルール作成", "power": 24, "cost": 10, "description": "保護ルールを作成して防御"},
        {"name": "攻撃ブロック", "power": 44, "cost": 20, "description": "攻撃をブロックして反撃"}
    ],
    "recruitment_quest": "waf_quest",
    "dialog": "私はWAF、AWSのウェブアプリケーションファイアウォールだ。アプリケーションを保護したいなら任せてくれ。"
}

AWS_SERVICES["shield"] = {
    "name": "Shield",
    "full_name": "AWS Shield",
    "category": "Security",
    "hp": 120,
    "max_hp": 120,
    "mp": 60,
    "max_mp": 60,
    "attack": 10,
    "defense": 20,
    "level": 1,
    "icon": "shield.png",
    "color": (232, 116, 0),  # オレンジ
    "description": "DDoS攻撃からアプリケーションを保護するサービス。",
    "skills": [
        {"name": "DDoS保護", "power": 22, "cost": 8, "description": "DDoS攻撃から保護して防御"},
        {"name": "シールド高度保護", "power": 42, "cost": 18, "description": "高度な保護で強力な防御"}
    ],
    "recruitment_quest": "shield_quest",
    "dialog": "私はShield、AWSのDDoS保護サービスだ。DDoS攻撃から守りたいなら任せてくれ。"
}

AWS_SERVICES["cloudwatch"] = {
    "name": "CloudWatch",
    "full_name": "Amazon CloudWatch",
    "category": "Management",
    "hp": 105,
    "max_hp": 105,
    "mp": 85,
    "max_mp": 85,
    "attack": 12,
    "defense": 14,
    "level": 1,
    "icon": "cloudwatch.png",
    "color": (100, 150, 200),  # 青
    "description": "AWSリソースとアプリケーションのモニタリングサービス。メトリクス収集、ログ分析、アラーム設定ができる。",
    "skills": [
        {"name": "メトリクス監視", "power": 25, "cost": 10, "description": "リソースのメトリクスを監視して攻撃"},
        {"name": "アラーム発報", "power": 45, "cost": 20, "description": "アラームを発報して強力な攻撃"}
    ],
    "recruitment_quest": "cloudwatch_quest",
    "dialog": "私はCloudWatch、AWSのモニタリングサービスだ。リソースの監視が必要なら任せてくれ。"
}

AWS_SERVICES["cloudformation"] = {
    "name": "CloudFormation",
    "full_name": "AWS CloudFormation",
    "category": "Management",
    "hp": 110,
    "max_hp": 110,
    "mp": 80,
    "max_mp": 80,
    "attack": 13,
    "defense": 13,
    "level": 1,
    "icon": "cloudformation.png",
    "color": (100, 150, 200),  # 青
    "description": "インフラをコードとして管理できるサービス。テンプレートを使ってリソースを簡単にデプロイできる。",
    "skills": [
        {"name": "スタック作成", "power": 26, "cost": 11, "description": "リソーススタックを作成して攻撃"},
        {"name": "テンプレート展開", "power": 46, "cost": 21, "description": "テンプレートを展開して強力な攻撃"}
    ],
    "recruitment_quest": "cloudformation_quest",
    "dialog": "私はCloudFormation、AWSのIaCサービスだ。インフラをコードで管理したいなら任せてくれ。"
}

AWS_SERVICES["stepfunctions"] = {
    "name": "Step Functions",
    "full_name": "AWS Step Functions",
    "category": "Application Integration",
    "hp": 100,
    "max_hp": 100,
    "mp": 90,
    "max_mp": 90,
    "attack": 14,
    "defense": 12,
    "level": 1,
    "icon": "stepfunctions.png",
    "color": (150, 100, 200),  # 紫
    "description": "サーバーレスワークフローを視覚的に構築できるサービス。複雑な処理を簡単に連携できる。",
    "skills": [
        {"name": "ステートマシン", "power": 27, "cost": 12, "description": "ステートマシンを実行して攻撃"},
        {"name": "並列処理", "power": 47, "cost": 22, "description": "並列処理で強力な攻撃"}
    ],
    "recruitment_quest": "stepfunctions_quest",
    "dialog": "私はStep Functions、AWSのワークフローサービスだ。複雑な処理の連携が必要なら任せてくれ。"
}

AWS_SERVICES["sqs"] = {
    "name": "SQS",
    "full_name": "Simple Queue Service",
    "category": "Application Integration",
    "hp": 95,
    "max_hp": 95,
    "mp": 85,
    "max_mp": 85,
    "attack": 12,
    "defense": 14,
    "level": 1,
    "icon": "sqs.png",
    "color": (150, 100, 200),  # 紫
    "description": "フルマネージド型のメッセージキューイングサービス。マイクロサービス間の疎結合な通信を実現。",
    "skills": [
        {"name": "メッセージ送信", "power": 24, "cost": 9, "description": "メッセージを送信して攻撃"},
        {"name": "キュー処理", "power": 44, "cost": 19, "description": "キューを処理して強力な攻撃"}
    ],
    "recruitment_quest": "sqs_quest",
    "dialog": "私はSQS、AWSのメッセージキューイングサービスだ。疎結合な通信が必要なら任せてくれ。"
}
