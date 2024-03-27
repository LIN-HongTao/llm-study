from tool import get_completion_from_messages
from openai.types.chat import ChatCompletionMessageParam
from typing import Iterable


############################## 一、 提取产品和类别 ##############################
delimiter = "####"

system_message = f"""
您将获得客户服务查询。
客户服务查询将使用{delimiter}字符作为分隔符。
请仅输出一个可解析的Python列表，列表每一个元素是一个JSON对象，每个对象具有以下格式：
'category': <包括以下几个类别：Computers and Laptops、Smartphones and Accessories、Televisions and Home Theater Systems、Gaming Consoles and Accessories、Audio Equipment、Cameras and Camcorders>,
以及
'products': <必须是下面的允许产品列表中找到的产品列表>

类别和产品必须在客户服务查询中找到。
如果提到了某个产品，它必须与允许产品列表中的正确类别关联。
如果未找到任何产品或类别，则输出一个空列表。
除了列表外，不要输出其他任何信息！

允许的产品：

Computers and Laptops category:
TechPro Ultrabook
BlueWave Gaming Laptop
PowerLite Convertible
TechPro Desktop
BlueWave Chromebook

Smartphones and Accessories category:
SmartX ProPhone
MobiTech PowerCase
SmartX MiniPhone
MobiTech Wireless Charger
SmartX EarBuds

Televisions and Home Theater Systems category:
CineView 4K TV
SoundMax Home Theater
CineView 8K TV
SoundMax Soundbar
CineView OLED TV

Gaming Consoles and Accessories category:
GameSphere X
ProGamer Controller
GameSphere Y
ProGamer Racing Wheel
GameSphere VR Headset

Audio Equipment category:
AudioPhonic Noise-Canceling Headphones
WaveSound Bluetooth Speaker
AudioPhonic True Wireless Earbuds
WaveSound Soundbar
AudioPhonic Turntable

Cameras and Camcorders category:
FotoSnap DSLR Camera
ActionCam 4K
FotoSnap Mirrorless Camera
ZoomMaster Camcorder
FotoSnap Instant Camera
    
只输出对象列表，不包含其他内容。
"""

user_message_1 = f"""
请告诉我关于 smartx pro phone 和 the fotosnap camera 的信息。
另外，请告诉我关于你们的tvs的情况。 """

messages: Iterable[ChatCompletionMessageParam] = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": f"{delimiter}{user_message_1}{delimiter}"},
]

category_and_product_response_1 = get_completion_from_messages(messages)

# print(category_and_product_response_1)


############################## 二、检索详细信息 ##############################:
import json
from pathlib import Path


def get_product_by_name(name: str):
    """
    根据产品名称获取产品

    参数:
    name: 产品名称
    """
    return products.get(name, None)


def get_products_by_category(category: str):
    """
    根据类别获取产品

    参数:
    category: 产品类别
    """
    return [product for product in products.values() if product["类别"] == category]


# 读取产品信息
with Path("file/products_zh.json").open("r", encoding="utf-8") as file:
    products = json.load(file)

# print(get_product_by_name("TechPro Ultrabook"))
# print(get_products_by_category("电脑和笔记本"))


############################## 三、生成查询答案 ##############################:
def read_string_to_list(input_string: str | None):
    """
    将输入的字符串转换为 Python 列表。

    参数:
    input_string: 输入的字符串，应为有效的 JSON 格式。

    返回:
    list 或 None: 如果输入字符串有效，则返回对应的 Python 列表，否则返回 None。
    """
    if input_string is None:
        return None

    try:
        # 将输入字符串中的单引号替换为双引号，以满足 JSON 格式的要求
        input_string = input_string.replace("'", '"')
        data = json.loads(input_string)
        return data
    except json.JSONDecodeError:
        print("Error: Invalid JSON string")
        return None


category_and_product_list = read_string_to_list(category_and_product_response_1)


def generate_output_string(data_list: list[dict[str, str]] | None):
    """
    根据输入的数据列表生成包含产品或类别信息的字符串。

    参数:
    data_list: 包含字典的列表，每个字典都应包含 "products" 或 "category" 的键。

    返回:
    output_string: 包含产品或类别信息的字符串。
    """
    output_string = ""
    if data_list is None:
        return output_string

    for data in data_list:
        try:
            if "products" in data and data["products"]:
                products_list = data["products"]
                for product_name in products_list:
                    product = get_product_by_name(product_name)
                    if product:
                        output_string += json.dumps(product, indent=4, ensure_ascii=False) + "\n"
                    else:
                        print(f"Error: Product '{product_name}' not found")
            elif "category" in data:
                category_name = data["category"]
                category_products = get_products_by_category(category_name)
                for product in category_products:
                    output_string += json.dumps(product, indent=4, ensure_ascii=False) + "\n"
            else:
                print("Error: Invalid object format")
        except Exception as e:
            print(f"Error: {e}")

    return output_string


product_information_for_user_message_1 = generate_output_string(category_and_product_list)

category_and_product_list = read_string_to_list(category_and_product_response_1)

system_message = f"""
您是一家大型电子商店的客服助理。
请以友好和乐于助人的口吻回答问题，并尽量简洁明了。
请确保向用户提出相关的后续问题。
"""

user_message_1 = f"""
请告诉我关于 smartx pro phone 和 the fotosnap camera 的信息。
另外，请告诉我关于你们的tvs的情况。
"""

messages = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": user_message_1},
    {
        "role": "assistant",
        "content": f"""相关产品信息:\n\
              {product_information_for_user_message_1}""",
    },
]

final_response = get_completion_from_messages(messages)
print(final_response)
