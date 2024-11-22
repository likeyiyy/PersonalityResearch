from dotenv import load_dotenv
import os
from chat_sdk import classify_chinese_character
from typing import List
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import ChineseCharacterDB, Base
from sqlalchemy.exc import IntegrityError

load_dotenv()

def get_db_engine():
    mysql_uri = os.getenv('MYSQL_URI', 'mysql://root:gllue123@127.0.0.1:3306/ht39')
    engine = create_engine(mysql_uri)
    Base.metadata.create_all(bind=engine)
    return engine

def process_batch(batch: List[str], thread_id: int, Session) -> None:
    """处理单个批次的汉字"""
    print(f"Thread {thread_id} processing batch of {len(batch)} characters")
    
    try:
        # 获取AI分类结果
        batch_result = classify_chinese_character(batch)
        
        # 创建新的会话
        session = Session()
        
        try:
            # 准备数据并插入数据库
            for char, result in batch_result.items():
                char_record = ChineseCharacterDB(
                    character=char,
                    level_1_category=result.get('level_1_category'),
                    level_2_category=result.get('level_2_category'),
                    level_3_category=result.get('level_3_category'),
                    description=result.get('description'),
                    classification_reason=result.get('classification_reason'),
                    confidence=result.get('confidence'),
                    example=result.get('example'),
                    created_at=datetime.now()
                )
                session.add(char_record)
            
            session.commit()
            print(f"Thread {thread_id} successfully processed {len(batch_result)} characters")
            
        except IntegrityError as e:
            print(f"Integrity error in thread {thread_id}: {e}")
            session.rollback()
        except Exception as e:
            print(f"Error in thread {thread_id}: {e}")
            session.rollback()
        finally:
            session.close()
            
    except Exception as e:
        print(f"Error in AI processing thread {thread_id}: {e}")

def process_chars_batch_parallel(chars: List[str], batch_size: int = 50, max_workers: int = 10) -> None:
    """使用线程池并行处理汉字列表"""
    # 创建数据库引擎和会话工厂
    engine = get_db_engine()
    Session = sessionmaker(bind=engine)
    
    # 将汉字列表分成批次
    batches = [chars[i:i + batch_size] for i in range(0, len(chars), batch_size)]
    print(f"Total batches: {len(batches)}")

    # 使用线程池处理批次
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(process_batch, batch, i, Session)
            for i, batch in enumerate(batches)
        ]

        # 等待所有任务完成
        for future in futures:
            try:
                future.result()
            except Exception as e:
                print(f"Batch processing failed: {e}")

def get_existing_chars(Session):
    """从数据库获取已处理的汉字列表"""
    session = Session()
    try:
        existing_chars = {char[0] for char in session.query(ChineseCharacterDB.character).all()}
        return existing_chars
    finally:
        session.close()

if __name__ == "__main__":
    from loader import all_word_list

    # 创建数据库引擎和会话工厂
    engine = get_db_engine()
    Session = sessionmaker(bind=engine)
    
    # 获取需要处理的汉字
    try:
        existing_chars = get_existing_chars(Session)
        chars_to_process = list(set(all_word_list) - existing_chars)
        # 先测试几个汉字
        print(f"Total characters: {len(all_word_list)}")
        print(f"Existing characters: {len(existing_chars)}")
        print(f"New characters to process: {len(chars_to_process)}")

        if chars_to_process:
            process_chars_batch_parallel(chars_to_process, batch_size=50, max_workers=10)
        else:
            print("No new characters to process")

    finally:
        pass
