from pydantic import BaseModel


class Week(BaseModel):
    week: int

    class Config:
        from_attributes = True  # Allows Pydantic to work directly with ORM models


class WeekResponse(BaseModel):
    weeks: list[int]

    class Config:
        from_attributes = True  # Allows Pydantic to work directly with ORM models
