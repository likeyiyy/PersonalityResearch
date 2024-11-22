
from sqlalchemy import Integer, Column, String, Boolean, Float, DateTime
from datetime import datetime
from app.database import Base


class ChineseCharacterDetail(Base):
    __tablename__ = "chinese_characters_detail"

    id = Column(Integer, primary_key=True, index=True)
    character = Column(String(1), index=True)  # 单个汉字
    
    # 三级分类
    level_1_category = Column(String(20))  # 一级分类
    level_2_category = Column(String(20))  # 二级分类
    level_3_category = Column(String(20))  # 三级分类
    
    # 字义相关
    description = Column(String, nullable=True)
    
    # AI分类相关
    confidence = Column(Float)
    classification_reason = Column(String(200))
    example = Column(String(100))
    
    # 管理字段
    is_reviewed = Column(Boolean, default=False)  # 是否已人工审核
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
