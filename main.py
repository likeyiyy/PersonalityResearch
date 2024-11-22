from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from sqlalchemy.orm import Session
from database import get_db
import controllers


app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/categories")
async def get_categories(db: Session = Depends(get_db)):
    return controllers.get_categories(db)

@app.get("/api/words")
async def get_words(
    main_category: Optional[str] = None,
    sub_category: Optional[str] = None,
    is_human_descriptive: Optional[bool] = None,
    confidence_min: Optional[float] = None,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db)
):
    return controllers.get_words(
        db,
        main_category,
        sub_category,
        is_human_descriptive,
        confidence_min,
        page,
        page_size
    )

@app.get("/api/category-stats")
async def get_category_stats(db: Session = Depends(get_db)):
    return controllers.get_category_stats(db)

