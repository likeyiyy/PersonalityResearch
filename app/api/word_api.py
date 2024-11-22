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
    main_category: Optional[str] = None,
    sub_category: Optional[str] = None,
    is_human_descriptive: Optional[bool] = None,
    confidence_min: Optional[float] = None,
    db: Session = Depends(get_db)
):
    service = WordService(db)
    return service.get_words_page(main_category, sub_category, is_human_descriptive, confidence_min, page, page_size)

@word_router.get("/words/categories")
async def get_word_categories(db: Session = Depends(get_db)):
    service = WordService(db)
    return service.get_category_stats()

@word_router.put("/words/{word_id}")
async def update_word(
    word_id: int,
    word_update: WordResponseDTO,
    db: Session = Depends(get_db)
):
    service = WordService(db)
    try:
        return service.update_word(word_id, word_update.dict(exclude_unset=True))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) 