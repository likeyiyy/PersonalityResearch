from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ChineseWordResponseDTO(BaseModel):
    id: int
    word: str
    level_1_category: str
    level_2_category: str
    level_3_category: str
    description: Optional[str]
    confidence: float
    classification_reason: str
    example: Optional[str]
    is_reviewed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 