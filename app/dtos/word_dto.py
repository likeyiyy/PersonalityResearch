from pydantic import BaseModel
from typing import Optional

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