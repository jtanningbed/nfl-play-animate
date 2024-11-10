import plotly.graph_objects as go
import numpy as np
from app.modules.colors import ColorPairs


def extract_play_info(selected_play_df, selected_tracking_df):
    line_of_scrimmage = selected_play_df["absolute_yardline_number"].values[0]
    yards_to_go = selected_play_df["yards_to_go"].values[0]
    play_direction = selected_tracking_df["play_direction"].values[0]
    first_down_marker = (
        line_of_scrimmage + yards_to_go
        if play_direction == "right"
        else line_of_scrimmage - yards_to_go
    )

    return {
        "game_id": selected_play_df["game_id"].values[0],
        "play_id": selected_play_df["play_id"].values[0],
        "line_of_scrimmage": line_of_scrimmage,
        "first_down_marker": first_down_marker,
        "down": selected_play_df["down"].values[0],
        "quarter": selected_play_df["quarter"].values[0],
        "play_description": format_play_description(
            selected_play_df["play_description"].values[0]
        ),
    }


def format_play_description(description):
    if len(description.split(" ")) > 15 and len(description) > 115:
        return (
            " ".join(description.split(" ")[0:16])
            + "<br>"
            + " ".join(description.split(" ")[16:])
        )
    return description


def create_animation_controls(
    frame_duration=100,
    transition_duration=0,
    slider_transition_duration=300,
    redraw=False,
):
    updatemenus_dict = [
        {
            "buttons": [
                {
                    "args": [
                        None,
                        {
                            "frame": {"duration": frame_duration, "redraw": redraw},
                            "fromcurrent": True,
                            "mode": "immediate",
                            "transition": {"duration": transition_duration},
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
        }
    ]

    sliders_dict = {
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
            "duration": slider_transition_duration,
            "easing": "cubic-in-out",
        },
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": [],
    }

    return updatemenus_dict, sliders_dict


def create_field_markers():
    markers = []
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
        # Add explicit yard lines
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


def create_line_markers(line_of_scrimmage, first_down_marker):
    return [
        go.Scatter(
            x=[line_of_scrimmage, line_of_scrimmage],
            y=[0, 53.5],
            line_dash="dash",
            line_color="blue",
            showlegend=False,
            hoverinfo="none",
        ),
        go.Scatter(
            x=[first_down_marker, first_down_marker],
            y=[0, 53.5],
            line_dash="dash",
            line_color="yellow",
            showlegend=False,
            hoverinfo="none",
        ),
    ]


def create_endzone_colors(color_orders, selected_game_df):
    endzoneColors = {
        0: color_orders[selected_game_df["home_team_abbr"].values[0]][0],
        110: color_orders[selected_game_df["visitor_team_abbr"].values[0]][0],
    }
    return [
        go.Scatter(
            x=[x_min, x_min, x_min + 10, x_min + 10, x_min],
            y=[0, 53.5, 53.5, 0, 0],
            fill="toself",
            fillcolor=endzoneColors[x_min],
            mode="lines",
            line=dict(color="white", width=3),
            opacity=1,
            showlegend=False,
            hoverinfo="skip",
        )
        for x_min in [0, 110]
    ]


def create_layout(play_info, updatemenus_dict, sliders_dict):
    return go.Layout(
        autosize=True,
        width=None,  # Allow dynamic resizing
        height=None,  # Allow dynamic resizing
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
        plot_bgcolor="#00B140",  # Field green color
        paper_bgcolor="rgba(0,0,0,0)",  # Transparent paper background
        updatemenus=updatemenus_dict,
        sliders=[sliders_dict],
        shapes=[
            # Rectangle for the playing field
            dict(
                type="rect",
                x0=0,
                y0=0,
                x1=120,
                y1=53.3,
                fillcolor="#00B140",  # Field green color
                line_width=2,
                layer="below",
            )
        ],
    )


def plot_players(selected_tracking_df, frame_id, color_orders):
    # Conversion factor
    YDS_PER_SEC_TO_MPH = 2.04545  # Convert yards/second to miles/hour (also applies to yards/second^2 to miles/hour/second)

    data = []
    for team in selected_tracking_df["club"].unique():
        plot_df = selected_tracking_df[
            (selected_tracking_df["club"] == team)
            & (selected_tracking_df["frame_id"] == frame_id)
        ]

        marker = go.scatter.Marker(
            color=color_orders[team][0],
            line=go.scatter.marker.Line(width=2, color=color_orders[team][1]),
            size=15,
        )

        if team != "football":
            hover_text_array = [
                f"Name: {displayName}<br>"
                f"Speed: {round(s * YDS_PER_SEC_TO_MPH, 2)} MPH<br>"
                f"Acceleration: {round(a * YDS_PER_SEC_TO_MPH, 2)} MPH/s<br>"
                f"Direction: {round(dir, 2)}°<br>"
                for displayName, s, a, dir in zip(
                    plot_df["display_name"], plot_df["s"], plot_df["a"], plot_df["dir"]
                )
            ]
            data.append(
                go.Scatter(
                    x=plot_df["x"],
                    y=plot_df["y"],
                    mode="markers",
                    marker=marker,
                    name=team,
                    text=hover_text_array,  # Use 'text' instead of 'hovertext'
                    hoverinfo="text",
                    hoverlabel=dict(
                        font=dict(
                            size=16  # Increase font size for hover text tooltip
                        )
                    ),
                )
            )
        else:
            data.append(
                go.Scatter(
                    x=plot_df["x"],
                    y=plot_df["y"],
                    mode="markers",
                    marker=marker,
                    name=team,
                    hoverinfo="none",
                )
            )

    return data


def animate_play(
    selected_game_df,
    selected_play_df,
    selected_tracking_df,
    frame_duration=100,
    transition_duration=0,
    slider_transition_duration=300,
    redraw=True,
):
    play_info = extract_play_info(selected_play_df, selected_tracking_df)

    team_combos = list(set(selected_tracking_df["club"].unique()) - set(["football"]))
    color_orders = ColorPairs(team_combos[0], team_combos[1])

    updatemenus_dict, sliders_dict = create_animation_controls(
        frame_duration=frame_duration,
        transition_duration=transition_duration,
        slider_transition_duration=slider_transition_duration,
        redraw=redraw,
    )

    frame_ids = sorted(selected_tracking_df["frame_id"].unique())
    frames = []
    for frame_id in frame_ids:
        data = (
            create_field_markers()
            + create_line_markers(
                play_info["line_of_scrimmage"], play_info["first_down_marker"]
            )
            + create_endzone_colors(color_orders, selected_game_df)
            + plot_players(selected_tracking_df, frame_id, color_orders)
        )

        sliders_dict["steps"].append(
            {
                "args": [
                    [frame_id],  # adjusted to account for zero-based indexing
                    {
                        "frame": {"duration": 100, "redraw": True},
                        "mode": "immediate",
                        "transition": {"duration": 0},
                    },
                ],
                "label": str(frame_id),
                "method": "animate",
            }
        )
        frames.append(go.Frame(data=data, name=str(frame_id)))

    layout = create_layout(play_info, updatemenus_dict, sliders_dict)

    fig = go.Figure(data=frames[0]["data"], layout=layout, frames=frames[1:])

    # Enable WebGL rendering
    fig.update_layout(template="plotly_dark")
    fig.update_traces(marker=dict(line=dict(width=0)))
    fig.update_layout(dragmode="pan")

    # Add First Down Markers and Team Abbreviations (these could also be separate functions)
    for y_val in [0, 53]:
        fig.add_annotation(
            x=play_info["first_down_marker"],
            y=y_val,
            text=str(play_info["down"]),
            showarrow=False,
            font=dict(family="Courier New, monospace", size=16, color="black"),
            align="center",
            bordercolor="black",
            borderwidth=2,
            borderpad=4,
            bgcolor="#ff7f0e",
            opacity=1,
        )

    for x_min, angle, team_key in [
        (0, 270, "home_team_abbr"),
        (110, 90, "visitor_team_abbr"),
    ]:
        fig.add_annotation(
            x=x_min + 5,
            y=53.5 / 2,
            text=selected_game_df[team_key].values[0],
            showarrow=False,
            font=dict(family="Courier New, monospace", size=32, color="White"),
            textangle=angle,
        )

    return fig
