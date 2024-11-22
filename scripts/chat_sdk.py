from dotenv import load_dotenv
import os
from openai import OpenAI
from typing import List, Dict
import json

load_dotenv()

CHAT_API_KEY = os.getenv("CHAT_API_KEY")
CHAT_BASE_URL = os.getenv("CHAT_BASE_URL")



def check_human_descriptive_words(words: List[str]) -> Dict[str, Dict]:
    client = OpenAI(api_key=CHAT_API_KEY, base_url=CHAT_BASE_URL)

    # 构建系统提示和用户提示
    system_prompt = """你是一个中文词语分析专家。对于每个词语，请分析以下内容：
1. is_human_descriptive: 是否是形容人的词语(true/false)
2. main_category: 主类别（外貌/性格品德/能力才智/情绪状态/社交特征/生理状态/非人物描述）
3. sub_category: 具体子类别
4. description: 词语的详细解释，包括具体含义和使用场景
5. reason: 为什么做出这样的分类判断，判断依据是什么
6. confidence: 判断的置信度(0-1)
7. example: 一个简短的使用示例

如果遇到难以准确分类的词语，请在reason中详细说明原因。
请返回JSON格式，每个词语作为key，包含上述所有信息作为value
    """

    # 构建用户提示
    user_prompt = f"请判断以下词语是否是形容人的词语，返回json格式的结果: {words}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 或使用其他支持response_format的模型
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0
        )

        # 解析返回结果
        result = response.choices[0].message.content
        return json.loads(result)

    except Exception as e:
        print(f"Error occurred: {e}")
        return {}

def classify_chinese_character(characters: List[str]) -> Dict[str, Dict]:
    client = OpenAI(api_key=CHAT_API_KEY, base_url=CHAT_BASE_URL)

    system_prompt = """你是一个中文汉字分析专家。对于每个汉字，请分析以下内容：
1. level_1_category: 一级分类（如：最抽象的层级， 不能是词性，而要是根据汉字本身的含义进行分类）
2. level_2_category: 二级分类（如：中等抽象的级别）
3. level_3_category: 三级分类（具体细分类别）
4. description: 汉字的详细解释，包括基本含义和使用场景
5. classification_reason: 为什么做出这样的分类判断，判断依据是什么
6. confidence: 判断的置信度(0-1)
7. example: 一个包含该汉字的简短词语或句子示例

请注意：
- 分类要准确且具有逻辑性
- 解释要简洁清晰
- 示例要贴近日常使用
- 如果遇到难以准确分类的汉字，请在classification_reason中详细说明原因

请返回JSON格式，每个汉字作为key，包含上述所有信息作为value。
    """

    user_prompt = f"请对以下汉字进行分类分析，返回json格式的结果: {characters}"

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 使用最新的GPT-4模型
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0  # 降低随机性，提高一致性
        )

        result = response.choices[0].message.content
        return json.loads(result)

    except Exception as e:
        print(f"Error occurred while classifying characters: {e}")
        return {}

# 使用示例
if __name__ == "__main__":
    test_words = ["高", "壮", "仁", "树", "山", "天", "地", "人", "孝", "笑"]
    result = classify_chinese_character(test_words)
    print(result)
