from typing import Literal, Protocol
from dataclasses import dataclass
from typing import TypeAlias
import plotly.graph_objects as go

PlayDirection = Literal["left", "right"]
FrameData: TypeAlias = list[go.Scatter]

@dataclass(frozen=True)
class PlayInfo:
    game_id: int
    play_id: int
    line_of_scrimmage: float
    first_down_marker: float
    down: int
    quarter: int
    play_description: str
    play_direction: PlayDirection

@dataclass(frozen=True)
class AnimationConfig:
    frame_duration: int = 100
    transition_duration: int = 0
    slider_transition_duration: int = 300
    redraw: bool = True
    marker_size: int = 15
    field_color: str = "#00B140"

@dataclass(frozen=True)
class FrameInfo:
    frame_id: int
    data: FrameData
    name: str

class ColorProvider(Protocol):
    def get_contrasting_pairs(self, team1: str, team2: str) -> dict[str, list[str]]: ...

@dataclass(frozen=True)
class PlayerData:
    x: float
    y: float
    speed: float
    acceleration: float
    direction: float
    display_name: str
