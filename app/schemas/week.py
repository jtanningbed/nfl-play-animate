from pydantic import BaseModel
from typing import List


class Week(BaseModel):
    week: int

    class Config:
        from_attributes = True  # Allows Pydantic to work directly with ORM models


class WeekResponse(BaseModel):
    weeks: List[int]

    class Config:
        from_attributes = True  # Allows Pydantic to work directly with ORM models
