from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.services.word2_service import Word2Service
from app.database import get_db
from app.dtos.chinese_word_dto import ChineseWordResponseDTO

word2_router = APIRouter()

@word2_router.get("/words2")
async def get_words(
    page: int = 1,
    page_size: int = 10,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    获取汉字列表，支持分页和分类筛选
    """
    service = Word2Service(db)
    return service.get_words_page(page, page_size, category)

@word2_router.get("/words2/categories")
async def get_word_categories(
    db: Session = Depends(get_db)
):
    """
    获取所有汉字分类统计
    """
    service = Word2Service(db)
    return service.get_category_stats()