from typing import Optional
from pydantic import BaseModel, Field

class Movie(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = Field(max_length=50, min_length=1)
    overview: Optional[str] = Field(max_length=50, min_length=15)
    year: Optional[str] = Field()
    rating: Optional[float] = Field(ge=0, le=10)
    category: Optional[str] = Field(min_length=5, max_length=30)

    class Config():
        schema_extra = {
            "example": {
                "title": "default_title",
                "overview": "default_overview",
                "year": 0,
                "rating": 0.0,
                "category": "default_category"
            }
        }