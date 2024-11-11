from app.modules.animation.colors import ColorManager
from app.modules.animation.animator import PlayAnimator
from app.modules.animation.types import AnimationConfig
import plotly.graph_objects as go
import pandas as pd


def animate_play(
    selected_game_df: pd.DataFrame,
    selected_play_df: pd.DataFrame,
    selected_tracking_df: pd.DataFrame,
    frame_duration: int = 100,
    transition_duration: int = 0,
    slider_transition_duration: int = 300,
    redraw: bool = True,
) -> go.Figure:
    """Create an animated visualization of an NFL play."""
    config = AnimationConfig(
        frame_duration=frame_duration,
        transition_duration=transition_duration,
        slider_transition_duration=slider_transition_duration,
        redraw=redraw,
    )

    animator = PlayAnimator(
        game_df=selected_game_df,
        play_df=selected_play_df,
        tracking_df=selected_tracking_df,
        color_provider=ColorManager(),
        config=config,
    )

    return animator.create_animation()
