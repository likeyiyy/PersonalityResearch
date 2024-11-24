from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.services.commendatory_term_service import CommendatoryTermService
from app.database import get_db
from app.dtos.commendatory_term_dto import CommendatoryTermResponseDTO

commendatory_term_router = APIRouter()

@commendatory_term_router.get("/commendatory_terms")
async def get_commendatory_terms(
    page: int = 1,
    page_size: int = 10,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    获取褒义词列表，支持分页和分类筛选
    """
    service = CommendatoryTermService(db)
    return service.get_words_page(page, page_size, category)

@commendatory_term_router.get("/commendatory_terms/categories")
async def get_commendatory_term_categories(
    db: Session = Depends(get_db)
):
    """
    获取所有褒义词分类统计
    """
    service = CommendatoryTermService(db)
    return service.get_category_stats() 