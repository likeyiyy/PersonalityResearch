from dotenv import load_dotenv
import os
from chat_sdk import check_human_descriptive_words
import pymysql
from urllib.parse import urlparse
import time
from typing import List, Dict
from datetime import datetime
import json


load_dotenv()


def parse_mysql_uri(uri):
    """解析MySQL URI"""
    result = urlparse(uri)
    username = result.username
    password = result.password
    database = result.path[1:]  # 移除开头的 /
    hostname = result.hostname
    port = result.port or 3306

    return {
        'host': hostname,
        'user': username,
        'password': password,
        'database': database,
        'port': port
    }

def get_db_connection():
    # 从环境变量获取MySQL URI
    mysql_uri = os.getenv('MYSQL_URI', 'mysql://root:gllue123@127.0.0.1:3306/ht39')
    db_config = parse_mysql_uri(mysql_uri)

    return pymysql.connect(
        **db_config,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )


def process_words_batch(words: List[str], batch_size: int = 200) -> Dict[str, bool]:
    """
    批量处理词语并存储结果
    :param words: 待处理的词语列表
    :param batch_size: 批次大小，默认200
    :return: 所有处理结果的字典
    """
    all_results = json.load(open('word_classification_results.json', 'r', encoding='utf-8'))
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 将词语列表分成多个批次
        for i in range(0, len(words), batch_size):
            batch = words[i:i + batch_size]
            print(f"Processing batch {i//batch_size + 1}, words {i} to {min(i+batch_size, len(words))}")

            # 使用已有的check_human_descriptive_words处理当前批次
            batch_result = json.loads(check_human_descriptive_words(batch))

            all_results.update(batch_result)

            # 准备数据并插入数据库
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            insert_sql = "INSERT INTO word_classifications (word, is_human_descriptive, created_at) VALUES (%s, %s, %s)"

            values = [
                (word, 1 if is_descriptive else 0, current_time)
                for word, is_descriptive in batch_result.items()
            ]

            cursor.executemany(insert_sql, values)
            conn.commit()

            # 保存当前进度到JSON
            save_results_to_json(all_results)

            # 添加适当的延时
            time.sleep(1)

    except Exception as e:
        print(f"Error occurred: {e}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()

    return all_results

def save_results_to_json(results: Dict[str, bool]):
    """保存结果到JSON文件"""
    with open('word_classification_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    from loader import all_word_list
    words_to_process = all_word_list
    results = process_words_batch(words_to_process)
    print(f"Total processed words: {len(results)}")
