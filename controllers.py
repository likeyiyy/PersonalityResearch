from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .models import WordClassificationDB
from .database import get_db  # 假设你将数据库连接逻辑放在一个单独的文件中
from collections import defaultdict

router = APIRouter()

@router.get("/api/categories")
async def get_categories(db: Session = Depends(get_db)):
    """获取所有分类选项"""
    categories = (
        db.query(
            WordClassificationDB.main_category,
            WordClassificationDB.sub_category
        )
        .filter(WordClassificationDB.main_category.isnot(None))
        .distinct()
        .all()
    )

    # 组织成层级结构
    result = {}
    for main_cat, sub_cat in categories:
        if main_cat not in result:
            result[main_cat] = []
        if sub_cat:
            result[main_cat].append(sub_cat)
    return result

@router.get("/api/words")
async def get_words(...):  # 省略参数
    """获取词语列表，支持分页和筛选"""
    # 省略实现

@router.get("/api/category-stats")
async def get_category_stats():
    """获取所有分类及其统计信息"""
    # 省略实现
