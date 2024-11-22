from sqlalchemy import Integer, Column, String, Boolean, Float, DateTime
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from database import Base

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
