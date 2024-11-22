from dotenv import load_dotenv
import os
from chat_sdk import check_human_descriptive_words
import pymysql
from urllib.parse import urlparse
import time
from typing import List, Dict
from datetime import datetime
import json
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import threading


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

def process_batch(batch: List[str], thread_id: int) -> None:
    """处理单个批次的词语"""
    print(f"Thread {thread_id} processing batch of {len(batch)} words")

    # 每个线程创建自己的数据库连接
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
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

    except Exception as e:
        print(f"Error in thread {thread_id}: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

def process_words_batch_parallel(words: List[str], batch_size: int = 50, max_workers: int = 10) -> None:
    """使用线程池并行处理词语列表"""
    # 将词语列表分成批次
    batches = [words[i:i + batch_size] for i in range(0, len(words), batch_size)]
    print(f"Total batches: {len(batches)}")

    # 使用线程池处理批次
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交任务到线程池，并传入线程ID
        futures = [
            executor.submit(process_batch, batch, i)
            for i, batch in enumerate(batches)
        ]

        # 等待所有任务完成
        for future in futures:
            try:
                future.result()  # 这里会抛出任务中的异常
            except Exception as e:
                print(f"Batch processing failed: {e}")

def get_existing_words(conn):
    """从数据库获取已处理的词列表"""
    cursor = conn.cursor()
    cursor.execute("SELECT word FROM word_classifications_detail")
    existing_words = {row['word'] for row in cursor.fetchall()}
    cursor.close()
    return existing_words


if __name__ == "__main__":
    from loader import all_word_list

    # 获取需要处理的词语
    conn = get_db_connection()
    try:
        existing_words = get_existing_words(conn)
        words_to_process = list(set(all_word_list) - existing_words)

        print(f"Total words: {len(all_word_list)}")
        print(f"Existing words: {len(existing_words)}")
        print(f"New words to process: {len(words_to_process)}")

        if words_to_process:
            # 使用4个线程并行处理
            process_words_batch_parallel(words_to_process, batch_size=50, max_workers=10)
        else:
            print("No new words to process")

    finally:
        conn.close()
