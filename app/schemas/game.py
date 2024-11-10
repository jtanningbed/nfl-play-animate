from pydantic import BaseModel, Field
from typing import List


class Game(BaseModel):
    game_id: int = Field(alias="gameid")
    home_team_abbr: str = Field(alias="hometeamabbr")
    visitor_team_abbr: str = Field(alias="visitorteamabbr")

    class Config:
        from_attributes = True  # Allows Pydantic to work directly with ORM models
        populate_by_name = True


class GameResponse(BaseModel):
    games: List[Game]

    class Config:
        from_attributes = True
