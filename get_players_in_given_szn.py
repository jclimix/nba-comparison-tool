from nba_api.stats.endpoints import commonallplayers
import pandas as pd

def get_active_players(season):
    # Retrieve all players for the given season
    all_players = commonallplayers.CommonAllPlayers(season=season, is_only_current_season=1)
    players_df = all_players.get_data_frames()[0]

    # Filter active players
    active_players_df = players_df[players_df['ROSTERSTATUS'] == 1]

    # Select relevant columns
    active_players_df = active_players_df[['PERSON_ID', 'DISPLAY_FIRST_LAST']]

    # Rename columns for clarity
    active_players_df.columns = ['Player ID', 'Player Name']

    return active_players_df

def main():
    season = input("Enter season (e.g. 2020-21): ")

    active_players_df = get_active_players(season)

    if active_players_df.empty:
        print(f"No active players found for season {season}.")
    else:
        print(active_players_df)

if __name__ == "__main__":
    main()
