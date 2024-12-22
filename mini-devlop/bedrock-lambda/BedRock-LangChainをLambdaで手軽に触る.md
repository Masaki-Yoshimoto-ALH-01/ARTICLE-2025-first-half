# BedRockのLangChainをLambdaでサクッと動かす

## 概要
LambdaでLangChain動かすためには、Lambdaレイヤーが必要になるので、Dockerイメージから作る  
今回はLambdaのランタイムをPython3.12でやるのでそのバージョンに合わせる。  
作業端末にPython入っとれば良いが、わざわざPython入れるのもバージョン上げるのも億劫でDockerは入ってたのでDocker使う（やっぱりDockerは便利）


## 手順
1. Dockerファイル作成  
    Lambdaコード書くだけでは動かない→原因はLangChainのimportに一手間必要のため  
    一手間→レイヤーの準備が必要→今回はDockerで作成
2. Docker ビルド  
    ```
        docker build -t {イメージ名} . -f {Dockerファイル名}
        例: docker build -t langcain-3.12 . -f Dockerfile-langcain-3.12
    ```
3. Lambdaレイヤーとしてzipファイルにする
    ```
    docker run -v "${PWD}":/work {イメージ名}
    例：docker run -v "${PWD}":/work langchain-3.12
    ```

## 環境
Lambda ランタイム Python3.12
LangChain 0.2.11

## 今回作るもの
- シンプルにpromptをBedRockに渡して返答してもらうもの
渡すpromptは
    - User Prompt（ユーザープロンプト）
        実際にユーザーが入力する内容

    - System Prompt（システムプロンプト）
        LLMの応答スタイルや振る舞いを制御するもの
        モデルに対しての特定のルールみたいな指示
        例：
        「あなたは親切で、丁寧な言葉で返答してください。」
        「あなたは数学の専門家として振る舞ってください。」
        「暴力的な言葉や攻撃的な表現を避けてください。」

今回はpromptをChainさせたりはしない


# サクッと作る
[コードはここ](article/ARTICLE-2025-first-half/mini-devlop/bedrock-lambda/bedrock-demo-lambda.py)

動作時には以下のような感じでプロンプトを渡します。

```
{
  "message": "仕事中眠たい時どうしたらいいのですか？",
}
```



