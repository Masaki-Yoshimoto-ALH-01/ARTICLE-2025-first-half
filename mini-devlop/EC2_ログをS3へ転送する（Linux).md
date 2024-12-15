# EC2_ログをS3へ転送する（Linux)

## 概要
EC2内のアプリログ、OSログ、アクセスログなどを監査や運用保守ように外だししたいケースがある、
そのために必要となるAWS側の構築とEC2のLinux内での設定をサクッと作りました。

## 環境
EC2 OS/AMI
Linux/AmazonLinux2023

## 今回作るもの
- EC2内にS3に定期送信するLinuxShell
- 転送先のS3バケット
- VPC ゲートウェイエンドポイント（S3)
- IAMロール

VPC、サブネットなど必要ですが、NW周りは今回解説しません。

## 構成図
![構成図](mini-devlop/img/ec2-s3-sendlog.drawio.png)

- VPCとその外にあるS3へのアクセスはゲートウェイ型のVPCエンドポイントを使って行う。
- EC2にはS3の操作できるIAMロールをインスタンスプロファイルとして設定する。
- EC2内部ではAmazonLinuxにてAWS CLIが使用できるのでS3へのGet、PutをCLIで行うと色々転送も可能。
- EC２が配置されているサブネットに対してVPCのルートテーブルでS3EPに対してのルート設定を忘れると通信できないので注意（一敗済み）


# サクッと作る
## IAMロール
SSMでEC2に接続するためのロール
AWSマネージドポリシーの```AmazonSSMManagedInstanceCore``` と追加で以下のポリシー作ってIMAロールにアタッチしておく
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": "*"
        }
    ]
}
```
S3へのGet,Put,ListBucketくらいのポリシーを作ってロールにアタッチ
ロールにはEC2へのsts:AssumeRole忘れずに

## EC2内にS3に定期送信するshell
```
#!/bin/bash
set -ue

# Redirect /var/log/user-data.log and /dev/console
exec > >(tee /local/testsp/user-data.log | logger -t user-data -s 2>/dev/console) 2>&1

echo "--------------------------------------------------"
# S3バケット名
bucket_name="yoshi-test-buket"

# アクセスログファイルパス
access_log="/local/testsp/log/test1.log"


# 前日日付取得
# yesterday ="`date --date '1 day ago' "+%Y%m%d" `"
TODAY="`date +%Y%m%d`"
export_folder=$(date -d "$TODAY 1 day ago" +%Y%m%d)
echo "=============yesterday"
echo yesterday : $export_folder


# ファイル名に日時を付けてアップロード
aws s3 cp $access_log s3://$bucket_name/$export_folder/access_log-test.gz


# アクセスログを空にする
echo -n > $access_log
```

cron で定期駆動させておけば定期的にログを送ってくれる。


## 転送先のS3バケット
デフォルト設定で作成すれば良い。  
既存のものを使うならそれでもOK  
説明は特になし  

## VPC ゲートウェイエンドポイント（S3)
Geteway型のS3のVPCエンドポイントを作成する。
エンドポイントのルート紐付けにて、今回使うEC2のサブネットに紐づくルートテーブルに紐づけておくこと

## その他
本体はshellだけだが、周りの構成の作成手順をつらつら書くのはめんどくさそうなのでIaCにして添付  
ただしリージョンは東京で動く仕様  
- [cfnテンプレートはこちら](/Users/yoshimoto/yomo-maki-work/article/ARTICLE-2025-first-half/mini-devlop/cfn)  

以下のようなネスト構成のため、ルートスタックを起点に起動する  
・ec2-s3-log-send-root.yaml　→ルートスタック  
    ・ec2-create.yaml　→子スタック　EC2作成  
    ・s3-create.yaml　→子スタック　S3作成  
    ・vpc-create.yaml　→子スタック　VPC作成  


