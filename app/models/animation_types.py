from typing import TypedDict, NotRequired, Literal
from dataclasses import dataclass
from typing import TypeAlias
import pandas as pd
import plotly.graph_objects as go
from numpy.typing import NDArray
import numpy as np

PlayDirection = Literal["left", "right"]
FrameData: TypeAlias = list[go.Scatter]

class TeamColors(TypedDict):
    primary: str
    secondary: str
    tertiary: NotRequired[str]

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
