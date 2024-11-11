from pydantic import BaseModel
from app.schemas.game import Game
from app.schemas.play import Play, PlaySummary
from app.schemas.tracking import TrackingData


class PlayResponse(BaseModel):
    game_data: list[Game]
    play_data: list[Play]
    tracking_data: list[TrackingData]

    class Config:
        from_attributes = True


class PlaySummaryResponse(BaseModel):
    plays: list[PlaySummary]

    class Config:
        from_attributes = True
