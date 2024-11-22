from dotenv import load_dotenv
import os
from openai import OpenAI
from typing import List, Dict


load_dotenv()

CHAT_API_KEY = os.getenv("CHAT_API_KEY")
CHAT_BASE_URL = os.getenv("CHAT_BASE_URL")



def check_human_descriptive_words(words: List[str]) -> Dict[str, bool]:
    client = OpenAI(api_key=CHAT_API_KEY, base_url=CHAT_BASE_URL)

    # 构建系统提示和用户提示
    system_prompt = """你是一个判断中文词语是否形容人的助手。
判断标准：
1. 形容外貌的词语返回true
2. 形容性格、品德的词语返回true
3. 任何只要是形容人的词语都返回true
4. 其他词语返回false
对于输入的每个词语，请返回该词语作为key，判断结果(true/false)作为value的JSON对象。"""

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
        return result

    except Exception as e:
        print(f"Error occurred: {e}")
        return {}

# 使用示例
if __name__ == "__main__":
    test_words = ["昤", "癀", "銄", "疝", "鎓"]
    result = check_human_descriptive_words(test_words)
    print(result)
