# AWS　個人アカウントのIAMユーザー設定（初心者向け）

## 概要
AWSアカウント作成して最初に考えるべきIAMユーザー設定。  
公式からは、ルートは使わない、作業用は最小限の権限の情報、他も似た感じ  
資格→独学→現場へと入ったが、個人アカウントについて３年ほど危ない運用していたので
とりあえずは脳死で安心な構成を考えてみた

## ユーザー構成
```
rootユーザー
└　管理ユーザー
  └ コンソール操作用ユーザー
  └ アクセスキー保有ユーザー
```

### それぞれのユーザー説明
- rootユーザー  
  アカウントの請求が来るユーザー  
  全ての操作が可能
- 管理ユーザー  
  請求以外のことができる「admin」権限を有するユーザー
- コンソール操作用ユーザー  
  日常作業の中で、AWSマネージメントコンソールを使う作業用のユーザー  
  アクセスキーの発行は不可
- アクセスキー保有ユーザー  
  作業端末などからアクセスキーを用いて操作する場合の作業ユーザー  
  マネコンの操作は不可

### MFA必須なユーザーの考え方
- rootユーザー、管理ユーザーは「必須」何も考えなくてもこれはやっておくべき。  
- その他は、IAMユーザーかつマネコン操作が可能なユーザーに対しては原則やっておくべき。  
- オワコンでない現場ならマネコン操作必要な作業ユーザーはaws organizations identity centerで管理できる状態で行うが、これは初学者には難しいと思いますので今回は話さない

###  乗っ取られた際の危険度、リスクの関係
いずれも、適切なMFAなどの設定、最小権限の付与、適切な運用が行われている場合
|IAMユーザー| 危険度 |漏洩リスク |
| ---- | ---- | ---- |
| root | 終わり |小 |
| 管理ユーザー | 極大 |小 |
| コンソール操作用ユーザー | 中 |小 |
| アクセスキー保有ユーザー | 小 |大 |
- AWSのアクセスキー漏洩は、よくある漏洩の話なので調べておくこと


###  各ユーザーの設定と権限例

#### root
  - 設定:実はあまり設定はなく「MFA」を設定程度  
  - 運用：日常使いは厳禁  
  - 使用用途；請求の確認程度  
  - 権限：-  

#### 管理ユーザー
  - 設定:ルート同様「MFA」を設定程度  
  - 運用：日常使いは厳禁  
  - 使用用途；IAMユーザー操作、このユーザーでしか操作できないIAMロールなどの作成操作  
  - 権限：admin  

#### コンソール操作用ユーザー
  - 設定:「MFA」を推奨  
  - 運用：日常使い用  
  - 使用用途；マネジメントコンソール作業用アカウント  
  - 権限：  アクセスキーの発行だけはできなくする。そのほかは好み  

一例(サービス系は除く)
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "*",
            "Resource": "*"
        },
        {
            "Effect": "Deny",
            "NotAction": [
                "iam:AddUserToGroup",
                "iam:RemoveUserFromGroup",
                "iam:UpdateUser",
                "iam:PutUserPermissionsBoundary",
                "iam:PutUserPolicy",
                "iam:DeleteUserPolicy",
                "iam:AttachUserPolicy",
                "iam:DeleteUser",
                "iam:DeleteUserPermissionsBoundary",
                "iam:DetachUserPolicy",
                "iam:CreateUser",
                "iam:CreateAccessKey",
                "iam:GetUser",
                "iam:ListAccessKeys",
                "iam:CreateVirtualMFADevice",
                "iam:EnableMFADevice",
                "iam:ListMFADevices",
                "iam:ListUsers",
                "iam:ListVirtualMFADevices",
                "iam:ResyncMFADevice",
                "iam:ChangePassword"
            ],
            "Resource": "*",
            "Condition": {
                "BoolIfExists": {
                    "aws:MultiFactorAuthPresent": "false"
                }
            }
        }
    ]
}
```
サービス系に制限入れるのであれば、EC2、RDSなどはインスタンスサイズに制限入れたりするといいと思われます

#### アクセスキー保有ユーザー
  - 設定：  マネジメントコンソールのアクセスを制限  
  - 運用：  AWSに外部から操作する専用の最小権限のIAMユーザー  
  - 使用用途：  ローカル端末からのアクセスキーを用いた操作など  
  - 権限：  CLI操作、Terraform専用のユーザーの場合で権限をガチガチに固めると使いずらいのでIAMユーザー系など縛りつつある程度の権限を持たせるなどがいいかもです。  
  「コンソール操作用ユーザー」に記載の一例からMFA認証の権限を抜くくらいで作るイメージ  
  アクセスキーでよく聞く話が、Gitへのアクセスキー暴露などがあるため「git-secrets」は入れておく


## 注意
個人で使用するアカウントの設定です。
現場作業の場合、セキュリティ指標などが決められてる（はず）なのでそれに沿ったレベルで設定が必要
ないのであれば、最小限を遵守



