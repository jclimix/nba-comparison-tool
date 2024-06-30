import pandas as pd

def add_averages_to_csv(file_path):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    
    # Find the indices of the "TEAM_ABBREVIATION" and "Season" columns
    team_abbreviation_index = df.columns.get_loc("TEAM_ABBREVIATION")
    season_index = df.columns.get_loc("Season")
    
    # Calculate the average for each column between "TEAM_ABBREVIATION" and "Season"
    averages = df.iloc[:, team_abbreviation_index + 1:season_index].mean()
    
    # Create a new row with "PLAYER_ID" as "AVERAGE" and the calculated averages
    average_row = pd.DataFrame([["AVERAGE"] + [None] * team_abbreviation_index + averages.tolist() + [None]], columns=df.columns)
    
    # Append the new row to the DataFrame
    df = pd.concat([df, average_row], ignore_index=True)
    
    return df

# Function to process all seasons from 2010-11 to 2023-24
def process_seasons():
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
    
    for season in seasons:
        file_path = f'player_stats/adv_stats/nba_adv_stats_{season}.csv'
        df = add_averages_to_csv(file_path)
        df.to_csv(file_path, index=False)
        print(f"Averages added to {file_path}")

# Call the function to process all seasons
process_seasons()
