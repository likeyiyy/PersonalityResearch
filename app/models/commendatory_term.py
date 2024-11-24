
from sqlalchemy import Integer, Column, String, Boolean, Float, DateTime
from datetime import datetime
from app.database import Base


class CommendatoryTerm(Base):
    __tablename__ = "commendatory_terms"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(10), index=True)  # 词语
    
    # 三级分类
    level_1_category = Column(String(20))  # 一级分类
    level_2_category = Column(String(20))  # 二级分类
    level_3_category = Column(String(20))  # 三级分类
    
    created_at = Column(DateTime, default=datetime.now)
