from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.services.character_service import CharacterService
from app.database import get_db
from app.dtos.character_dto import CharacterResponseDTO

character_router = APIRouter()

@character_router.get("/characters")
async def get_characters(
    page: int = 1,
    page_size: int = 10,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    获取汉字列表，支持分页和分类筛选
    """
    service = CharacterService(db)
    return service.get_characters_page(page, page_size, category)

@character_router.get("/characters/categories")
async def get_character_categories(
    db: Session = Depends(get_db)
):
    """
    获取所有汉字分类统计
    """
    service = CharacterService(db)
    return service.get_category_stats()
