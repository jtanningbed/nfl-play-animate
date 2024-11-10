from pydantic import BaseModel
from typing import List
from app.schemas.game import Game
from app.schemas.play import Play, PlaySummary
from app.schemas.tracking import TrackingData


class PlayResponse(BaseModel):
    game_data: List[Game]
    play_data: List[Play]
    tracking_data: List[TrackingData]

    class Config:
        from_attributes = True


class PlaySummaryResponse(BaseModel):
    plays: List[PlaySummary]

    class Config:
        from_attributes = True
