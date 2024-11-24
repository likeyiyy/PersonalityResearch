from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, List, Optional
from app.models.derogatory_term import DerogatoryTerm
from app.dtos.derogatory_term_dto import DerogatoryTermResponseDTO

class DerogatoryTermService:
    def __init__(self, db: Session):
        self.db = db

    def get_words_page(
        self,
        page: int,
        page_size: int,
        category: Optional[str] = None
    ) -> Dict:
        query = self.db.query(DerogatoryTerm)
        
        if category:
            categories = category.split('/')
            if len(categories) >= 1:
                query = query.filter(DerogatoryTerm.level_1_category == categories[0])
            if len(categories) >= 2:
                query = query.filter(DerogatoryTerm.level_2_category == categories[1])
            if len(categories) >= 3:
                query = query.filter(DerogatoryTerm.level_3_category == categories[2])

        total = query.count()
        words = query.order_by(DerogatoryTerm.word).offset((page - 1) * page_size).limit(page_size).all()
        
        return {
            'data': [DerogatoryTermResponseDTO.model_validate(word) for word in words],
            'total': total,
            'page': page,
            'pageSize': page_size
        }

    def get_category_stats(self) -> List[Dict]:
        categories = self.db.query(
            DerogatoryTerm.level_1_category,
            DerogatoryTerm.level_2_category,
            DerogatoryTerm.level_3_category,
            func.count(DerogatoryTerm.id).label('count')
        ).group_by(
            DerogatoryTerm.level_1_category,
            DerogatoryTerm.level_2_category,
            DerogatoryTerm.level_3_category
        ).all()

        result = []
        for cat in categories:
            level1, level2, level3, count = cat
            
            # Find or create level 1 category
            level1_cat = None
            for c in result:
                if c['main_category'] == level1:
                    level1_cat = c
                    break
            if not level1_cat:
                level1_cat = {
                    'main_category': level1,
                    'total_count': 0,
                    'sub_categories': []
                }
                result.append(level1_cat)
            
            # Find or create level 2 category
            level2_cat = None
            for c in level1_cat['sub_categories']:
                if c['name'] == level2:
                    level2_cat = c
                    break
            if not level2_cat:
                level2_cat = {
                    'name': level2,
                    'count': 0,
                    'sub_categories': []
                }
                level1_cat['sub_categories'].append(level2_cat)
            
            # Add count to totals
            level1_cat['total_count'] += count
            level2_cat['count'] += count
            
            # Add level 3 category if exists
            if level3:
                level2_cat['sub_categories'].append({
                    'name': level3,
                    'count': count
                })

        # Sort by counts
        result.sort(key=lambda x: x['total_count'], reverse=True)
        for l1 in result:
            l1['sub_categories'].sort(key=lambda x: x['count'], reverse=True)
            for l2 in l1['sub_categories']:
                l2['sub_categories'].sort(key=lambda x: x['count'], reverse=True)
                
        return result