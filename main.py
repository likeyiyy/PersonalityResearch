from fastapi import FastAPI, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy import Integer, create_engine, Column, String, Boolean, Float, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# 数据库配置
SQLALCHEMY_DATABASE_URL = os.getenv("MYSQL_URI", "mysql://root:gllue123@127.0.0.1:3306/ht39")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy 模型
class WordClassificationDB(Base):
    __tablename__ = "word_classifications_detail"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(10), index=True)
    is_human_descriptive = Column(Boolean)
    main_category = Column(String(30), nullable=True)
    sub_category = Column(String(30), nullable=True)
    description = Column(String, nullable=True)
    reason = Column(String, nullable=True)
    confidence = Column(Float, nullable=True)
    example = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

# Pydantic 模型
class WordClassification(BaseModel):
    word: str
    is_human_descriptive: bool
    main_category: Optional[str]
    sub_category: Optional[str]
    description: Optional[str]
    reason: Optional[str]
    confidence: Optional[float]
    example: Optional[str]

    class Config:
        from_attributes = True

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 依赖项
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/categories")
async def get_categories(db: Session = Depends(get_db)):
    """获取所有分类选项"""
    categories = (
        db.query(
            WordClassificationDB.main_category,
            WordClassificationDB.sub_category
        )
        .filter(WordClassificationDB.main_category.isnot(None))
        .distinct()
        .all()
    )

    # 组织成层级结构
    result = {}
    for main_cat, sub_cat in categories:
        if main_cat not in result:
            result[main_cat] = []
        if sub_cat:
            result[main_cat].append(sub_cat)
    return result

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
    """获取词语列表，支持分页和筛选"""
    query = db.query(WordClassificationDB)

    # 添加筛选条件
    if main_category:
        query = query.filter(WordClassificationDB.main_category == main_category)
    if sub_category:
        query = query.filter(WordClassificationDB.sub_category == sub_category)
    if is_human_descriptive is not None:
        query = query.filter(WordClassificationDB.is_human_descriptive == is_human_descriptive)
    if confidence_min:
        query = query.filter(WordClassificationDB.confidence >= confidence_min)

    # 获取总数
    total = query.count()

    # 获取分页数据
    words = (
        query
        .order_by(WordClassificationDB.word)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return {
        "total": total,
        "items": [WordClassification.from_orm(word) for word in words],
        "page": page,
        "page_size": page_size
    }
