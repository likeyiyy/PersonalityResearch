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

# 使用示例
if __name__ == "__main__":
    test_words = ["高", "壮", "仁", "树", "山"]
    result = check_human_descriptive_words(test_words)
    print(result)
