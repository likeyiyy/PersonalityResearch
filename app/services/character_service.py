from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, List, Optional
from app.models.character import ChineseCharacterDetail
from app.dtos.character_dto import CharacterResponseDTO

class CharacterService:
    def __init__(self, db: Session):
        self.db = db

    def get_characters_page(
        self,
        page: int,
        page_size: int,
        category: Optional[str] = None
    ) -> Dict:
        query = self.db.query(ChineseCharacterDetail)
        
        if category:
            categories = category.split('/')
            if len(categories) >= 1:
                query = query.filter(ChineseCharacterDetail.level_1_category == categories[0])
            if len(categories) >= 2:
                query = query.filter(ChineseCharacterDetail.level_2_category == categories[1])
            if len(categories) >= 3:
                query = query.filter(ChineseCharacterDetail.level_3_category == categories[2])

        total = query.count()
        characters = query.offset((page - 1) * page_size).limit(page_size).all()
        
        return {
            'data': [CharacterResponseDTO.from_orm(char).dict() for char in characters],
            'total': total,
            'page': page,
            'pageSize': page_size
        }

    def get_category_stats(self) -> Dict:
        categories = self.db.query(
            ChineseCharacterDetail.level_1_category,
            ChineseCharacterDetail.level_2_category,
            ChineseCharacterDetail.level_3_category,
            func.count(ChineseCharacterDetail.id).label('count')
        ).group_by(
            ChineseCharacterDetail.level_1_category,
            ChineseCharacterDetail.level_2_category,
            ChineseCharacterDetail.level_3_category
        ).all()

        category_tree = {}
        for cat in categories:
            if cat[0] not in category_tree:
                category_tree[cat[0]] = {'count': 0, 'children': {}}
            if cat[1] not in category_tree[cat[0]]['children']:
                category_tree[cat[0]]['children'][cat[1]] = {'count': 0, 'children': {}}
            category_tree[cat[0]]['children'][cat[1]]['children'][cat[2]] = cat[3]
            category_tree[cat[0]]['children'][cat[1]]['count'] += cat[3]
            category_tree[cat[0]]['count'] += cat[3]

        return category_tree 