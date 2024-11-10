from pydantic import BaseModel, Field


class TrackingData(BaseModel):
    game_id: int = Field(alias="gameid")
    play_id: int = Field(alias="playid")
    nfl_id: int = Field(alias="nflid")
    play_direction: str = Field(alias="playdirection")
    club: str
    frame_id: int = Field(alias="frameid")
    s: float
    a: float
    dir: float
    dis: float
    display_name: str = Field(alias="displayname")
    x: float
    y: float

    class Config:
        from_attributes = True
        populate_by_name = True
