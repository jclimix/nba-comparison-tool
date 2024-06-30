import pandas as pd
from nba_api.stats.endpoints import leaguedashplayerstats

def get_advanced_player_stats(season, output_file):
    # Fetch advanced player stats for the given season with permode as 'PerGame'
    player_stats = leaguedashplayerstats.LeagueDashPlayerStats(
        season=season,
        per_mode_detailed='PerGame',
        measure_type_detailed_defense='Advanced'
    ).get_data_frames()[0]

    # Add a column for the current season
    player_stats['Season'] = season
    
    # Save the DataFrame to a CSV file
    player_stats.to_csv(output_file, index=False)
    print(f"Advanced player stats for season {season} saved to {output_file}")

# Example usage
seasons = [
    '2010-11',
    '2011-12',
    '2012-13',
    '2013-14',
    '2014-15',
    '2015-16',
    '2016-17',
    '2017-18',
    '2018-19',
    '2019-20',
    '2020-21',
    '2021-22',
    '2022-23',
    '2023-24'
]

i = 0

for season in seasons:
    output_file = f'nba_adv_stats_{season}.csv'
    get_advanced_player_stats(season, output_file)
    i+=1
