# run this streamlit app: streamlit run app00a.py

import streamlit as st
import pandas as pd

# Load data
players = pd.read_parquet("player_season_stats_2024_2025.parquet")
players.drop(columns=["league_id", "team_id", "player_id", "season_id", "season", "position"], inplace=True)

# Main content area
st.title("Player Scouting Dashboard")
st.dataframe(players)
