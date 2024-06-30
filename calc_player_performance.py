import pandas as pd
from scipy.stats import percentileofscore

player_id = '2544'
season_A = '2019-20'
season_B = '2023-24'

def season_A_player_info(season_A, player_id):
    file_path = f'player_stats/base_stats/nba_stats_{season_A}.csv'
    player_stats_df = pd.read_csv(file_path)
    player_info = player_stats_df[player_stats_df['PLAYER_ID'] == player_id]
    player_name = player_info.iloc[0]['PLAYER_NAME']
    player_age_A = player_info.iloc[0]['AGE']
    player_team_A = player_info.iloc[0]['TEAM_ABBREVIATION']
    return player_name, player_age_A, player_team_A

def season_B_player_info(season_B, player_id):
    file_path = f'player_stats/base_stats/nba_stats_{season_B}.csv'
    player_stats_df = pd.read_csv(file_path)
    player_info = player_stats_df[player_stats_df['PLAYER_ID'] == player_id]
    player_name = player_info.iloc[0]['PLAYER_NAME']
    player_age_B = player_info.iloc[0]['AGE']
    player_team_B = player_info.iloc[0]['TEAM_ABBREVIATION']
    return player_name, player_age_B, player_team_B

def calculate_percentile(value, data):
    return percentileofscore(data, value, kind='rank') / 100

def normalize_percentile(percentile):
    return max(50.0, min(99.9, 50.0 + 49.9 * percentile))

def season_A_get_normalized_percentiles(season_A, player_id):
    base_stats_path = f'player_stats/base_stats/nba_stats_{season_A}.csv'
    adv_stats_path = f'player_stats/adv_stats/nba_adv_stats_{season_A}.csv'
    
    base_stats_df = pd.read_csv(base_stats_path)
    adv_stats_df = pd.read_csv(adv_stats_path)
    
    base_stats_df = base_stats_df[base_stats_df['PLAYER_ID'] != 'AVERAGE']
    adv_stats_df = adv_stats_df[adv_stats_df['PLAYER_ID'] != 'AVERAGE']
    
    player_base_stats = base_stats_df[base_stats_df['PLAYER_ID'] == player_id].iloc[0]
    player_adv_stats = adv_stats_df[adv_stats_df['PLAYER_ID'] == player_id].iloc[0]

    stat_weights = {
        'PTS': 12, 'AST': 8, 'REB': 8, 'STL': 6, 'BLK': 7, 
        'FG_PCT': 8, 'FG3_PCT': 8, 'FT_PCT': 8, 
        'NET_RATING': 6, 'EFG_PCT': 10, 'TS_PCT': 10, 'PIE': 9
    }
    
    percentiles = {}
    overall_score = 0
    total_weight = sum(stat_weights.values())
    
    for stat, weight in stat_weights.items():
        if stat in base_stats_df.columns:
            data = base_stats_df[stat].astype(float)
            value = float(player_base_stats[stat])
        else:
            data = adv_stats_df[stat].astype(float)
            value = float(player_adv_stats[stat])
        
        percentile = calculate_percentile(value, data)
        normalized = normalize_percentile(percentile)
        
        percentiles[stat] = normalized
        overall_score += normalized * (weight / total_weight)
    
    return percentiles, overall_score

def season_B_get_normalized_percentiles(season_B, player_id):
    base_stats_path = f'player_stats/base_stats/nba_stats_{season_B}.csv'
    adv_stats_path = f'player_stats/adv_stats/nba_adv_stats_{season_B}.csv'
    
    base_stats_df = pd.read_csv(base_stats_path)
    adv_stats_df = pd.read_csv(adv_stats_path)
    
    base_stats_df = base_stats_df[base_stats_df['PLAYER_ID'] != 'AVERAGE']
    adv_stats_df = adv_stats_df[adv_stats_df['PLAYER_ID'] != 'AVERAGE']
    
    player_base_stats = base_stats_df[base_stats_df['PLAYER_ID'] == player_id].iloc[0]
    player_adv_stats = adv_stats_df[adv_stats_df['PLAYER_ID'] == player_id].iloc[0]

    stat_weights = {
        'PTS': 12, 'AST': 8, 'REB': 8, 'STL': 6, 'BLK': 7, 
        'FG_PCT': 8, 'FG3_PCT': 8, 'FT_PCT': 8, 
        'NET_RATING': 6, 'EFG_PCT': 10, 'TS_PCT': 10, 'PIE': 9
    }
    
    percentiles = {}
    overall_score = 0
    total_weight = sum(stat_weights.values())
    
    for stat, weight in stat_weights.items():
        if stat in base_stats_df.columns:
            data = base_stats_df[stat].astype(float)
            value = float(player_base_stats[stat])
        else:
            data = adv_stats_df[stat].astype(float)
            value = float(player_adv_stats[stat])
        
        percentile = calculate_percentile(value, data)
        normalized = normalize_percentile(percentile)
        
        percentiles[stat] = normalized
        overall_score += normalized * (weight / total_weight)
    
    return percentiles, overall_score

player_name, player_age_A, player_team_A = season_A_player_info(season_A, player_id)
percentiles, overall_score = season_A_get_normalized_percentiles(season_A, player_id)

print(f"Player Info:")
print(f"Name: {player_name} | Age: {player_age_A} | Team: {player_team_A} | Season: {season_A}")
print(f"Stat Comparison:")
for stat, percentile in percentiles.items():
    print(f"{stat}: {percentile:.1f}")

print(f"\nOverall Score (dec): {overall_score:.2f}")
print(f"{overall_score:.0f} OVR\n")

player_name, player_age_B, player_team_B = season_B_player_info(season_B, player_id)
percentiles, overall_score = season_B_get_normalized_percentiles(season_B, player_id)

print(f"Player Info:")
print(f"Name: {player_name} | Age: {player_age_B} | Team: {player_team_B}| Season: {season_B}")
print(f"Stat Comparison:")
for stat, percentile in percentiles.items():
    print(f"{stat}: {percentile:.1f}")

print(f"\nOverall Score (dec): {overall_score:.2f}")
print(f"{overall_score:.0f} OVR\n")