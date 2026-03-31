# run this streamlit app: streamlit run app02.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

# Create tabs
tab1, tab2 = st.tabs(["xG vs. Goals", "Custom Analysis"])

with tab1:
    # Plotly bar chart with the number of players per team
    filtered_players_grpd = filtered_players.groupby('league').size().reset_index(name='count')
    filtered_players_grpd = filtered_players_grpd.sort_values('count', ascending=False).head(20)
    fig2 = px.bar(filtered_players_grpd, x='league', y='count')
    st.plotly_chart(fig2)

    # Plotly scatter plot with xg on the x-axis and goals on the y-axis
    fig1 = px.scatter(filtered_players, x='xg', y='goals', color='primary_position',
                     hover_data=['team', 'league'],
                     hover_name='player')

    # 45 degree line
    max_value = max(filtered_players['xg'].max(), filtered_players['goals'].max())
    fig1.add_shape(
        type="line",
        x0=0, y0=0,
        x1=max_value, y1=max_value,
        line=dict(color="black", width=1)
    )

    st.plotly_chart(fig1)

with tab2:
    # Customizable scatter plot
    col1, col2 = st.columns(2)
    
    with col1:
        x_axis = st.selectbox(
            "Select X-axis variable",
            options=['minutes', 'goals', 'assists', 'shots', 'xg', 'xa', 'key_passes']
        )
    
    with col2:
        y_axis = st.selectbox(
            "Select Y-axis variable",
            options=['minutes', 'goals', 'assists', 'shots', 'xg', 'xa', 'key_passes']
        )

    fig3 = px.scatter(filtered_players, x=x_axis, y=y_axis,
                     hover_data=['team', 'league'],
                     hover_name='player')
    
    st.plotly_chart(fig3)
    st.write("N: ", filtered_players.shape[0])
