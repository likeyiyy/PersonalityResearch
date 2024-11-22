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


def process_words_batch(words: List[str], batch_size: int = 50):
    """
    批量处理词语并存储结果
    :param words: 待处理的词语列表
    :param batch_size: 批次大小，默认200
    :return: 所有处理结果的字典
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 将词语列表分成多个批次
        for i in range(0, len(words), batch_size):
            batch = words[i:i + batch_size]
            print(f"Processing batch {i//batch_size + 1}, words {i} to {min(i+batch_size, len(words))}")

            # 使用已有的check_human_descriptive_words处理当前批次
            batch_result = check_human_descriptive_words(batch)

            # 准备数据并插入数据库
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            insert_sql = """
                INSERT INTO word_classifications_detail (
                    word,
                    is_human_descriptive,
                    main_category,
                    sub_category,
                    description,
                    reason,
                    confidence,
                    example,
                    created_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            values = [
                (
                    word,
                    1 if result['is_human_descriptive'] else 0,
                    result.get('main_category', None),
                    result.get('sub_category', None),
                    result.get('description', None),
                    result.get('reason', None),
                    result.get('confidence', None),
                    result.get('example', None),
                    current_time
                )
                for word, result in batch_result.items()
            ]

            cursor.executemany(insert_sql, values)
            conn.commit()
            # 添加适当的延时
            time.sleep(1)

    except Exception as e:
        print(f"Error occurred: {e}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()

def get_existing_words(conn):
    """从数据库获取已处理的词列表"""
    cursor = conn.cursor()
    cursor.execute("SELECT word FROM word_classifications_detail")
    existing_words = {row['word'] for row in cursor.fetchall()}
    cursor.close()
    return existing_words


if __name__ == "__main__":
    from loader import all_word_list

    # 获取数据库连接
    conn = get_db_connection()

    try:
        # 获取已处理的词
        existing_words = get_existing_words(conn)

        # 找出需要处理的新词
        words_to_process = list(set(all_word_list) - existing_words)

        print(f"Total words: {len(all_word_list)}")
        print(f"Existing words: {len(existing_words)}")
        print(f"New words to process: {len(words_to_process)}")

        if words_to_process:
            process_words_batch(words_to_process)
        else:
            print("No new words to process")

    finally:
        conn.close()
