from pydantic import BaseModel, Field
from datetime import time


class Play(BaseModel):
    game_id: int = Field(alias="gameid")
    play_id: int = Field(alias="playid")
    play_description: str = Field(alias="playdescription")
    down: int
    quarter: int
    absolute_yardline_number: int = Field(alias="absoluteyardlinenumber")
    yards_to_go: int = Field(alias="yardstogo")

    class Config:
        from_attributes = True  # Allows Pydantic to work directly with ORM models
        populate_by_name = True


class PlaySummary(BaseModel):
    play_id: int = Field(alias="playid")
    play_description: str = Field(alias="playdescription")
    quarter: int
    game_clock: time = Field(alias="gameclock")

    class Config:
        from_attributes = True  # Allows Pydantic to work directly with ORM models
        populate_by_name = True
