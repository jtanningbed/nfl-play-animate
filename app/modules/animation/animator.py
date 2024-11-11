from dataclasses import dataclass
import pandas as pd
from app.modules.animation.colors import ColorManager
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import Sequence

from app.modules.animation.types import (
    PlayInfo,
    AnimationConfig,
    FrameInfo,
    ColorProvider,
    FrameData,
    PlayerData,
)

@dataclass
class PlayAnimator:
    """Handles the animation of NFL plays."""
    
    game_df: pd.DataFrame
    play_df: pd.DataFrame
    tracking_df: pd.DataFrame
    color_provider: ColorProvider
    config: AnimationConfig = AnimationConfig()

    def __post_init__(self) -> None:
        """Initialize play info and team colors after instance creation."""
        self.play_info = self._extract_play_info()
        self.team_colors = self._setup_team_colors()
        
    def _extract_play_info(self) -> PlayInfo:
        """Extract play information from the dataframes."""
        los = self.play_df["absolute_yardline_number"].values[0]
        yards_to_go = self.play_df["yards_to_go"].values[0]
        play_direction = self.tracking_df["play_direction"].values[0]
        
        first_down_marker = (
            los + yards_to_go if play_direction == "right" else los - yards_to_go
        )
        
        return PlayInfo(
            game_id=self.play_df["game_id"].values[0],
            play_id=self.play_df["play_id"].values[0],
            line_of_scrimmage=los,
            first_down_marker=first_down_marker,
            down=self.play_df["down"].values[0],
            quarter=self.play_df["quarter"].values[0],
            play_description=self._format_play_description(
                self.play_df["play_description"].values[0]
            ),
            play_direction=play_direction,
        )

    def _setup_team_colors(self) -> dict[str, list[str]]:
        """Set up team color schemes."""
        team_combos = list(set(self.tracking_df["club"].unique()) - {"football"})
        return self.color_provider.get_contrasting_pairs(team_combos[0], team_combos[1])

    def _format_play_description(self, description: str) -> str:
        """Format play description text with line breaks if needed."""
        words = description.split()
        if len(words) > 15 and len(description) > 115:
            return " ".join(words[:16]) + "<br>" + " ".join(words[16:])
        return description

    def _create_field_markers(self) -> list[go.Scatter]:
        """Create the field yard markers."""
        markers = []
        
        # Add yard numbers
        for y in [5, 53.5 - 5]:
            markers.append(
                go.Scatter(
                    x=np.arange(20, 110, 10),
                    y=[y] * 9,
                    mode="text",
                    text=list(
                        map(
                            str,
                            list(np.arange(20, 61, 10) - 10) + list(np.arange(40, 9, -10)),
                        )
                    ),
                    textfont_size=30,
                    textfont_family="Courier New, monospace",
                    textfont_color="#ffffff",
                    showlegend=False,
                    hoverinfo="none",
                )
            )
            
        # Add yard lines
        for x in range(10, 111, 5):
            markers.append(
                go.Scatter(
                    x=[x, x],
                    y=[0, 53.3],
                    mode="lines",
                    line=dict(color="white", width=1),
                    showlegend=False,
                    hoverinfo="none",
                )
            )
        return markers

    def _create_line_markers(self) -> list[go.Scatter]:
        """Create line of scrimmage and first down markers."""
        return [
            go.Scatter(
                x=[self.play_info.line_of_scrimmage] * 2,
                y=[0, 53.5],
                line_dash="dash",
                line_color="blue",
                showlegend=False,
                hoverinfo="none",
            ),
            go.Scatter(
                x=[self.play_info.first_down_marker] * 2,
                y=[0, 53.5],
                line_dash="dash",
                line_color="yellow",
                showlegend=False,
                hoverinfo="none",
            ),
        ]

    def _create_endzone_colors(self) -> list[go.Scatter]:
        """Create colored endzones."""
        endzone_colors = {
            0: self.team_colors[self.game_df["home_team_abbr"].values[0]][0],
            110: self.team_colors[self.game_df["visitor_team_abbr"].values[0]][0],
        }
        
        return [
            go.Scatter(
                x=[x_min, x_min, x_min + 10, x_min + 10, x_min],
                y=[0, 53.5, 53.5, 0, 0],
                fill="toself",
                fillcolor=endzone_colors[x_min],
                mode="lines",
                line=dict(color="white", width=3),
                opacity=1,
                showlegend=False,
                hoverinfo="skip",
            )
            for x_min in [0, 110]
        ]

    def _create_player_traces(self, frame_id: int) -> list[go.Scatter]:
        """Create player position traces for a given frame."""
        YDS_PER_SEC_TO_MPH = 2.04545
        traces = []
        
        for team in self.tracking_df["club"].unique():
            plot_df = self.tracking_df[
                (self.tracking_df["club"] == team)
                & (self.tracking_df["frame_id"] == frame_id)
            ]
            
            marker = go.scatter.Marker(
                color=self.team_colors[team][0],
                line=go.scatter.marker.Line(width=2, color=self.team_colors[team][1]),
                size=self.config.marker_size,
            )
            
            if team != "football":
                hover_text = [
                    f"Name: {player.display_name}<br>"
                    f"Speed: {round(player.speed * YDS_PER_SEC_TO_MPH, 2)} MPH<br>"
                    f"Acceleration: {round(player.acceleration * YDS_PER_SEC_TO_MPH, 2)} MPH/s<br>"
                    f"Direction: {round(player.direction, 2)}°<br>"
                    for player in (
                        PlayerData(
                            x=x, y=y, speed=s, acceleration=a,
                            direction=d, display_name=n
                        )
                        for x, y, s, a, d, n in zip(
                            plot_df["x"], plot_df["y"], plot_df["s"],
                            plot_df["a"], plot_df["dir"], plot_df["display_name"]
                        )
                    )
                ]
                
                traces.append(
                    go.Scatter(
                        x=plot_df["x"],
                        y=plot_df["y"],
                        mode="markers",
                        marker=marker,
                        name=team,
                        text=hover_text,
                        hoverinfo="text",
                        hoverlabel=dict(font=dict(size=16)),
                    )
                )
            else:
                traces.append(
                    go.Scatter(
                        x=plot_df["x"],
                        y=plot_df["y"],
                        mode="markers",
                        marker=marker,
                        name=team,
                        hoverinfo="none",
                    )
                )
                
        return traces

    def _create_frame(self, frame_id: int) -> FrameInfo:
        """Create a single animation frame."""
        data = (
            self._create_field_markers()
            + self._create_line_markers()
            + self._create_endzone_colors()
            + self._create_player_traces(frame_id)
        )
        
        return FrameInfo(
            frame_id=frame_id,
            data=data,
            name=str(frame_id)
        )

    def _create_animation_controls(self) -> tuple[list[dict], dict]:
        """Create animation control elements."""
        updatemenus = [{
            "buttons": [
                {
                    "args": [
                        None,
                        {
                            "frame": {
                                "duration": self.config.frame_duration,
                                "redraw": self.config.redraw
                            },
                            "fromcurrent": True,
                            "mode": "immediate",
                            "transition": {
                                "duration": self.config.transition_duration
                            },
                        },
                    ],
                    "label": "Play",
                    "method": "animate",
                },
                {
                    "args": [
                        [None],
                        {
                            "frame": {"duration": 0, "redraw": False},
                            "mode": "immediate",
                            "transition": {"duration": 0},
                        },
                    ],
                    "label": "Pause",
                    "method": "animate",
                },
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top",
        }]

        sliders = {
            "active": 0,
            "yanchor": "top",
            "xanchor": "left",
            "currentvalue": {
                "font": {"size": 20},
                "prefix": "Frame:",
                "visible": True,
                "xanchor": "right",
            },
            "transition": {
                "duration": self.config.slider_transition_duration,
                "easing": "cubic-in-out",
            },
            "pad": {"b": 10, "t": 50},
            "len": 0.9,
            "x": 0.1,
            "y": 0,
            "steps": [],
        }

        return updatemenus, sliders

    def _create_layout(self, updatemenus: list[dict], sliders: dict) -> go.Layout:
        """Create the plot layout."""
        return go.Layout(
            autosize=True,
            width=None,
            height=None,
            xaxis=dict(
                range=[0, 120],
                autorange=False,
                showticklabels=False,
                showgrid=False,
                zeroline=False,
                ticks="",
            ),
            yaxis=dict(
                range=[0, 53.3],
                autorange=False,
                showgrid=False,
                showticklabels=False,
                zeroline=False,
                ticks="",
            ),
            plot_bgcolor=self.config.field_color,
            paper_bgcolor="rgba(0,0,0,0)",
            updatemenus=updatemenus,
            sliders=[sliders],
            shapes=[
                dict(
                    type="rect",
                    x0=0,
                    y0=0,
                    x1=120,
                    y1=53.3,
                    fillcolor=self.config.field_color,
                    line_width=2,
                    layer="below",
                )
            ],
        )

    def _add_annotations(self, fig: go.Figure) -> None:
        """Add first down markers and team abbreviations to the figure."""
        # Add first down markers
        for y_val in [0, 53]:
            fig.add_annotation(
                x=self.play_info.first_down_marker,
                y=y_val,
                text=str(self.play_info.down),
                showarrow=False,
                font=dict(family="Courier New, monospace", size=16, color="black"),
                align="center",
                bordercolor="black",
                borderwidth=2,
                borderpad=4,
                bgcolor="#ff7f0e",
                opacity=1,
            )

        # Add team abbreviations
        for x_min, angle, team_key in [
            (0, 270, "home_team_abbr"),
            (110, 90, "visitor_team_abbr"),
        ]:
            fig.add_annotation(
                x=x_min + 5,
                y=53.5 / 2,
                text=self.game_df[team_key].values[0],
                showarrow=False,
                font=dict(family="Courier New, monospace", size=32, color="White"),
                textangle=angle,
            )

    def create_animation(self) -> go.Figure:
        """Create the complete play animation."""
        frame_ids = sorted(self.tracking_df["frame_id"].unique())
        frames = [self._create_frame(frame_id) for frame_id in frame_ids]
        
        updatemenus, sliders = self._create_animation_controls()
        
        return self._create_figure(frames, updatemenus, sliders)

    def _create_figure(
        self,
        frames: list[FrameInfo],
        updatemenus: list[dict],
        sliders: dict,
    ) -> go.Figure:
        """Create the final figure with all components."""
        
        # Add slider steps
        sliders["steps"] = [
            {
                "args": [
                    [frame.name],
                    {
                        "frame": {
                            "duration": self.config.frame_duration,
                            "redraw": self.config.redraw
                        },
                        "mode": "immediate",
                        "transition": {"duration": 0},
                    },
                ],
                "label": frame.name,
                "method": "animate",
            }
            for frame in frames
        ]
        
        layout = self._create_layout(updatemenus, sliders)
        
        fig = go.Figure(
            data=frames[0].data,
            layout=layout,
            frames=[go.Frame(data=f.data, name=f.name) for f in frames[1:]]
        )
        
        # Enable WebGL rendering and other display options
        fig.update_layout(template="plotly_dark")
        fig.update_traces(marker=dict(line=dict(width=0)))
        fig.update_layout(dragmode="pan")
        
        self._add_annotations(fig)
        
        return fig


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
