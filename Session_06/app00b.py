# run this streamlit app: streamlit run app00b.py

import streamlit as st
import pandas as pd

# Load data
players = pd.read_parquet("player_season_stats_2024_2025.parquet")
players.drop(columns=["league_id", "team_id", "player_id", "season_id", "season", "position"], inplace=True)

# Sidebar
with st.sidebar:
    
    # Dropdown for Position
    selected_position = st.selectbox(
        "Tactical Position",
        ["All", "GK", "D", "M", "F"]
    )

    # Slider for Minutes Played
    minutes_played = st.slider(
        "Minutes Played",
        min_value=0,
        max_value=38*90,
        value=180
    )
    
# Filter dataframe based on selected position and minutes played
if selected_position == "All":
    filtered_players = players[players['minutes'] >= minutes_played]
else:
    filtered_players = players[
        (players['primary_position'] == selected_position) & 
        (players['minutes'] >= minutes_played)
    ]

# Main content area
st.title("Player Scouting Dashboard")
st.dataframe(players)
