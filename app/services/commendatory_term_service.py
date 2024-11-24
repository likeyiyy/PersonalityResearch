from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, List
from collections import defaultdict
from app.models.commendatory_term import CommendatoryTerm
from app.dtos.commendatory_term_dto import CommendatoryTermResponseDTO

class CommendatoryTermService:
    def __init__(self, db: Session):
        self.db = db

    def get_words_page(self, page: int, page_size: int, category: str = None):
        query = self.db.query(CommendatoryTerm)
        
        if category:
            categories = category.split('/')
            if len(categories) >= 1:
                query = query.filter(CommendatoryTerm.level_1_category == categories[0])
            if len(categories) >= 2:
                query = query.filter(CommendatoryTerm.level_2_category == categories[1])
            if len(categories) >= 3:
                query = query.filter(CommendatoryTerm.level_3_category == categories[2])

        total = query.count()
        words = (query
                .order_by(CommendatoryTerm.word)
                .offset((page - 1) * page_size)
                .limit(page_size)
                .all())

        return {
            "total": total,
            "data": [CommendatoryTermResponseDTO.model_validate(word) for word in words],
            "page": page,
            "page_size": page_size
        }

    def get_category_stats(self) -> List[Dict]:
        stats = defaultdict(lambda: {"total_count": 0, "sub_categories": {}})
        
        categories = (self.db.query(
            CommendatoryTerm.level_1_category,
            CommendatoryTerm.level_2_category,
            func.count('*').label('count'))
            .group_by(
                CommendatoryTerm.level_1_category,
                CommendatoryTerm.level_2_category)
            .all())

        for level_1, level_2, count in categories:
            if level_1:
                stats[level_1]["total_count"] += count
                if level_2:
                    stats[level_1]["sub_categories"][level_2] = count

        result = [{
            "main_category": main,
            "total_count": data["total_count"],
            "sub_categories": [
                {"name": sub, "count": count}
                for sub, count in data["sub_categories"].items()
            ]
        } for main, data in stats.items()]
        
        result.sort(key=lambda x: x["total_count"], reverse=True)
        return result 