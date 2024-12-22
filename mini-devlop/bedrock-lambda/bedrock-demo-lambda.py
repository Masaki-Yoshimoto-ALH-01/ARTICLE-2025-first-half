# Pyhton外部モジュールのインポート
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage


# Lambda実行時に呼ばれる関数
def lambda_handler(event, context):
    return invoke_bedrock(event['prompt'])

# Bedrock呼び出し関数
def invoke_bedrock(prompt: str):
    # ChatBedrockを生成
    chat = ChatBedrock(
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",
        model_kwargs={"max_tokens": 1000},
    )

    # メッセージを定義
    messages = [
        SystemMessage(content="あなたはプロのエンジニアです。"),
        HumanMessage(content=prompt),
    ]

    # モデル呼び出し
    response = chat.invoke(messages)
    return response.content
