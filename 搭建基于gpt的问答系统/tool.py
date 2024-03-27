from openai import AzureOpenAI
import openai
from openai.types.chat import ChatCompletionMessageParam
import pandas as pd

import os
from typing import Iterable
from io import StringIO

os.environ["API_BASE"] = "https://itg-openai.openai.azure.com"
os.environ["OPENAI_API_KEY"] = "56dc0c1bcd3c4001bd263068f858ae91"
os.environ["API_TYPE"] = "azure"
os.environ["BRANCH"] = "uat"
os.environ["API_VERSION"] = "0613"
os.environ["SPEECH_REGION"] = "eastasia"
os.environ["SPEECH_KEY"] = "1c95810d04e04fc69b955a2717c20325"

client = AzureOpenAI(
    azure_endpoint="https://itg-openai.openai.azure.com", api_key=os.getenv("OPENAI_API_KEY"), api_version="2024-02-01"
)


def get_completion_from_messages(
    messages: Iterable[ChatCompletionMessageParam],
    model: str = "itg-chat-16k",
    temperature: int = 0,
    max_tokens: int = 500,
):
    """
    封装一个支持更多参数的自定义访问 OpenAI GPT3.5 的函数

    参数:
    messages: 这是一个消息列表，每个消息都是一个字典，包含 role(角色）和 content(内容)。角色可以是'system'、'user' 或 'assistant’，内容是角色的消息。
    model: 调用的模型，默认为 gpt-3.5-turbo(ChatGPT)，有内测资格的用户可以选择 gpt-4
    temperature: 这决定模型输出的随机程度，默认为0，表示输出将非常确定。增加温度会使输出更随机。
    max_tokens: 这决定模型输出的最大的 token 数。
    """
    response = client.chat.completions.create(
        model=model, messages=messages, temperature=temperature, max_tokens=max_tokens  # model = "deployment_name".
    )

    return response.choices[0].message.content


def get_completion_and_token_count(
    messages: Iterable[ChatCompletionMessageParam],
    model: str = "itg-chat-16k",
    temperature: int = 0,
    max_tokens: int = 500,
):
    """
    使用 OpenAI 的 GPT-3 模型生成聊天回复，并返回生成的回复内容以及使用的 token 数量。

    参数:
    messages: 聊天消息列表。
    model: 使用的模型名称。默认为"gpt-3.5-turbo"。
    temperature: 控制生成回复的随机性。值越大，生成的回复越随机。默认为 0。
    max_tokens: 生成回复的最大 token 数量。默认为 500。

    返回:
    content: 生成的回复内容。
    token_dict: 包含'prompt_tokens'、'completion_tokens'和'total_tokens'的字典，分别表示提示的 token 数量、生成的回复的 token 数量和总的 token 数量。
    """
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    content = response.choices[0].message.content

    token_dict = {
        "prompt_tokens": response.usage.prompt_tokens if response.usage else -1,
        "completion_tokens": response.usage.completion_tokens if response.usage else -1,
        "total_tokens": response.usage.total_tokens if response.usage else -1,
    }

    return content, token_dict
