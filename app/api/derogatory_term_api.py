from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.services.derogatory_term_service import DerogatoryTermService
from app.database import get_db
from app.dtos.derogatory_term_dto import DerogatoryTermResponseDTO

derogatory_term_router = APIRouter()

@derogatory_term_router.get("/derogatory_terms")
async def get_derogatory_terms(
    page: int = 1,
    page_size: int = 10,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    获取贬义词列表，支持分页和分类筛选
    """
    service = DerogatoryTermService(db)
    return service.get_words_page(page, page_size, category)

@derogatory_term_router.get("/derogatory_terms/categories")
async def get_derogatory_term_categories(
    db: Session = Depends(get_db)
):
    """
    获取所有贬义词分类统计
    """
    service = DerogatoryTermService(db)
    return service.get_category_stats()
