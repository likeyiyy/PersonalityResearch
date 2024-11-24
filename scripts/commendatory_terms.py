import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.commendatory_term import CommendatoryTerm
import sys

# JSON数据结构示例
sample_data = {
    "品质类褒义词": [
        {
            "二级分类": "道德品质",
            "三级分类": [
                {
                    "name": "奸诈类",
                    "examples": ["奸诈", "狡猾", "阴险", "诡诈", "狡诈"]
                },
                # ... 更多三级分类
            ]
        },
        # ... 更多二级分类
    ]
}

def import_commendatory_terms(json_data):
    # 数据库连接配置
    DATABASE_URL = "mysql+pymysql://root:gllue123@localhost/word_analysis"
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        # 遍历JSON数据并插入数据库
        for level_1, categories in json_data.items():
            for level_2_data in categories:
                level_2 = level_2_data["二级分类"]
                for level_3_data in level_2_data["三级分类"]:
                    level_3 = level_3_data["name"]
                    for word in level_3_data["examples"]:
                        term = CommendatoryTerm(
                            word=word,
                            level_1_category=level_1,
                            level_2_category=level_2,
                            level_3_category=level_3
                        )
                        session.add(term)
        
        session.commit()
        print("数据导入成功！")
    
    except Exception as e:
        session.rollback()
        print(f"导入出错: {str(e)}")
    
    finally:
        session.close()

# 使用方法
if __name__ == "__main__":
    # json文件路径从参数读取
    json_file_path = sys.argv[1]
    # 可以从文件读取JSON数据
    with open(json_file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
    import_commendatory_terms(json_data)
