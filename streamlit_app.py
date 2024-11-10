import streamlit as st
import requests
import pandas as pd
from app.modules.animate import animate_play

# Set page configuration for a wider layout
st.set_page_config(layout="wide")

st.title("NFL Play Animator")

# Fetch weeks from the API
response = requests.get("http://localhost:8000/api/weeks")
weeks = response.json()["weeks"]

# Dropdown for weeks
selected_week = st.selectbox("Select Week", weeks, format_func=lambda w: f"Week {w}")

# Fetch games for the selected week
game_response = requests.get(f"http://localhost:8000/api/games/{selected_week}")
games = game_response.json()["games"]

# Dropdown for games, with display of Home vs. Visitor
game_names = [f"{game['hometeamabbr']} vs {game['visitorteamabbr']}" for game in games]
game_ids = {name: game["gameid"] for name, game in zip(game_names, games)}
selected_game_name = st.selectbox("Select Game", game_names)
selected_game_id = game_ids[selected_game_name]

# Fetch plays for the selected game
plays_response = requests.get(f"http://localhost:8000/api/plays/{selected_game_id}")
plays = plays_response.json()["plays"]

# Dropdown for plays, ordered by quarter and game clock
play_descriptions = [
    f"{play['quarter']}Q {play['gameclock']} {play['playdescription']}"
    for play in plays
]
play_ids = {desc: play["playid"] for desc, play in zip(play_descriptions, plays)}
selected_play_desc = st.selectbox("Select Play", play_descriptions)
selected_play_id = play_ids[selected_play_desc]

if st.button("Animate Play"):
    response = requests.get(
        f"http://localhost:8000/api/play/{selected_game_id}/{selected_play_id}"
    )
    data = response.json()

    # Convert data back to DataFrames
    game_data = pd.DataFrame(data["game_data"])
    play_data = pd.DataFrame(data["play_data"])
    tracking_data = pd.DataFrame(data["tracking_data"])

    # Display play information
    st.subheader("Play Information")
    st.write(f"Game ID: {selected_game_id}")
    st.write(f"Play ID: {selected_play_id}")
    if not play_data.empty:
        st.write(
            f"Play Description: {play_data['quarter'].iloc[0]}Q {play_data['playdescription'].iloc[0]}"
        )

    # Call animate_play function
    fig = animate_play(game_data, play_data, tracking_data)

    # Display the figure
    # Update layout for correct aspect ratio
    fig.update_layout(
        autosize=True,
        # width=1000,
        # height=600,
        margin=dict(l=0, r=0, b=0, t=30),
        yaxis=dict(scaleanchor="x", scaleratio=1),
    )

    # Custom CSS for maintaining aspect ratio
    st.markdown(
        """
        <style>
        .stPlotlyChart {
            width: 100%;
            height: 0;
            padding-bottom: 42%; /* Adjust this value to change the aspect ratio */
            position: relative;
            transform-origin: top left; /* Ensure scaling is from the top left corner */
            transform: scale(0.75); /* Scale down by 75% */
        }
        .stPlotlyChart > div {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # Display the figure in a container with controlled width
    container = st.container()
    with container:
        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "responsive": True,
                "displayModeBar": False,  # Hide the mode bar for cleaner look
            },
        )
