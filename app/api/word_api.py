from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.services.word_service import WordService
from app.database import get_db
from app.dtos.word_dto import WordResponseDTO

word_router = APIRouter()

@word_router.get("/words")
async def get_words(
    page: int = 1,
    page_size: int = 10,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    service = WordService(db)
    return service.get_words_page(category, page, page_size)

@word_router.get("/words/categories")
async def get_word_categories(db: Session = Depends(get_db)):
    service = WordService(db)
    return service.get_category_stats()

