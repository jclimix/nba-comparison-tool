from nba_api.stats.endpoints import playergamelog, boxscoreadvancedv2
import pandas as pd

def get_pie_score(player_id, season):
    # Get the player's game log for the season
    game_log = playergamelog.PlayerGameLog(player_id=player_id, season=season)
    game_log_df = game_log.get_data_frames()[0]

    if game_log_df.empty:
        print(f"No game log available for season {season} for player ID {player_id}")
        return None

    # Retrieve all game IDs for the season
    game_ids = game_log_df['Game_ID'].unique()

    # Initialize variables to calculate cumulative PIE
    total_pie = 0
    num_games = len(game_ids)

    for game_id in game_ids:
        boxscore = boxscoreadvancedv2.BoxScoreAdvancedV2(game_id=game_id)
        boxscore_df = boxscore.get_data_frames()[0]

        player_stats = boxscore_df[boxscore_df['PLAYER_ID'] == player_id]
        if not player_stats.empty:
            total_pie += player_stats['PIE'].values[0]

    if num_games == 0:
        return 0

    # Calculate average PIE
    average_pie = total_pie / num_games
    return average_pie

def main():
    player_id = input("Enter player ID: ")
    season = input("Enter season (e.g. 2020-21): ")

    pie_score = get_pie_score(player_id, season)

    if pie_score is not None:
        print(f"PIE Score for player ID {player_id} in {season}: {pie_score}")

if __name__ == "__main__":
    main()
