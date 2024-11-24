from pydantic import BaseModel
from datetime import datetime

class CommendatoryTermResponseDTO(BaseModel):
    id: int
    word: str
    level_1_category: str
    level_2_category: str
    level_3_category: str
    created_at: datetime

    class Config:
        from_attributes = True 