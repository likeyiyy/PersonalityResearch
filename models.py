from sqlalchemy import Integer, Column, String, Boolean, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

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
