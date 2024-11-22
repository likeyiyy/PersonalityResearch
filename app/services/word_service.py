from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, Dict, List, TypedDict
from collections import defaultdict
from app.models.word import WordClassificationDB
from app.dtos.word_dto import WordResponseDTO

class SubCategoryStats(TypedDict):
    name: str
    count: int

class CategoryStats(TypedDict):
    total_count: int
    sub_categories: Dict[str, int]

class WordService:
    def __init__(self, db: Session):
        self.db = db

    def get_categories(self) -> Dict[str, List[str]]:
        """获取所有分类选项"""
        categories = (
            self.db.query(
                WordClassificationDB.main_category,
                WordClassificationDB.sub_category,
                func.count('*').label('count')
            )
            .filter(WordClassificationDB.main_category.isnot(None))
            .group_by(
                WordClassificationDB.main_category,
                WordClassificationDB.sub_category
            )
            .order_by(func.count('*').desc())
            .all()
        )

        result: Dict[str, List[str]] = {}
        for main_cat, sub_cat, count in categories:
            if main_cat not in result:
                result[main_cat] = []
            if sub_cat:
                result[main_cat].append(sub_cat)
        return result

    def get_words_page(
        self,
        category: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> Dict:
        """获取词语列表，支持分页和筛选"""
        query = self.db.query(WordClassificationDB)

        if category:
            categories = category.split('/')
            if len(categories) >= 1:
                query = query.filter(WordClassificationDB.main_category == categories[0])
            if len(categories) >= 2:
                query = query.filter(WordClassificationDB.sub_category == categories[1])

        total = query.count()
        words = (
            query
            .order_by(WordClassificationDB.word)
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        return {
            "total": total,
            "data": [WordResponseDTO.model_validate(word) for word in words],
            "page": page,
            "page_size": page_size
        }

    def get_category_stats(self) -> List[Dict]:
        """获取所有分类及其统计信息"""
        stats: Dict[str, CategoryStats] = defaultdict(
            lambda: {"total_count": 0, "sub_categories": {}}
        )

        categories = (
            self.db.query(
                WordClassificationDB.main_category,
                WordClassificationDB.sub_category,
                func.count('*').label('count')
            )
            .filter(WordClassificationDB.main_category.isnot(None))
            .group_by(
                WordClassificationDB.main_category,
                WordClassificationDB.sub_category
            )
            .order_by(func.count('*').desc())
            .all()
        )

        for main_cat, sub_cat, count in categories:
            if main_cat:
                stats[main_cat]["total_count"] += count
                if sub_cat:
                    stats[main_cat]["sub_categories"][sub_cat] = count

        result = [
            {
                "main_category": main,
                "total_count": data["total_count"],
                "sub_categories": [
                    {"name": sub, "count": count}
                    for sub, count in data["sub_categories"].items()
                ]
            }
            for main, data in stats.items()
        ]
        result.sort(key=lambda x: x["total_count"], reverse=True)
        return result

