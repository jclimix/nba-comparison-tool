from flask import Flask, render_template, request
from pprint import pprint
import pandas as pd
from scipy.stats import percentileofscore
from tabulate import tabulate
from waitress import serve

app = Flask(__name__)

def season_player_info(season, player_id):
    base_stats_path = f'player_stats/base_stats/nba_stats_{season}.csv'
    adv_stats_path = f'player_stats/adv_stats/nba_adv_stats_{season}.csv'
    
    base_stats_df = pd.read_csv(base_stats_path)
    adv_stats_df = pd.read_csv(adv_stats_path)
    
    base_stats_df = base_stats_df[base_stats_df['PLAYER_ID'] != 'AVERAGE']
    adv_stats_df = adv_stats_df[adv_stats_df['PLAYER_ID'] != 'AVERAGE']
    
    player_base_stats = base_stats_df[base_stats_df['PLAYER_ID'] == player_id].iloc[0]
    player_adv_stats = adv_stats_df[adv_stats_df['PLAYER_ID'] == player_id].iloc[0]

    stat_weights = {
        'PTS': 20, 'AST': 15, 'REB': 15, 'STL': 9, 'BLK': 9, 
        'FG_PCT': 9, 'FG3_PCT': 12, 'FT_PCT': 7, 
        'NET_RATING': 15, 'EFG_PCT': 8, 'TS_PCT': 10, 'PIE': 20
    }

    percentiles = {}
    overall_score = 0
    total_weight = sum(stat_weights.values())
    
    for stat, weight in stat_weights.items():
        if stat in ['NET_RATING', 'EFG_PCT', 'TS_PCT', 'PIE']:
            data = adv_stats_df[stat].astype(float)
            value = float(player_adv_stats[stat])
        else:
            data = base_stats_df[stat].astype(float)
            value = float(player_base_stats[stat])
        
        percentile = percentileofscore(data, value, kind='rank') / 100
        normalized = max(50.0, min(99.9, 0.12 + 99.9 * percentile))
        
        percentiles[stat] = normalized
        overall_score += normalized * (weight / total_weight)
    
    return percentiles, overall_score, player_base_stats, player_adv_stats

def get_player_info(season, player_id):
    file_path = f'player_stats/base_stats/nba_stats_{season}.csv'
    player_stats_df = pd.read_csv(file_path)
    player_info = player_stats_df[player_stats_df['PLAYER_ID'] == player_id]
    player_name = player_info.iloc[0]['PLAYER_NAME']
    player_age = player_info.iloc[0]['AGE']
    player_team = player_info.iloc[0]['TEAM_ABBREVIATION']
    return player_name, player_age, player_team

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare():
    player_id_A = request.form['player_id_A']
    player_id_B = request.form['player_id_B']
    season_A = request.form['season_A']
    season_B = request.form['season_B']

    percentiles_A, overall_score_A, base_stats_A, adv_stats_A = season_player_info(season_A, player_id_A)
    percentiles_B, overall_score_B, base_stats_B, adv_stats_B = season_player_info(season_B, player_id_B)

    player_name_A, player_age_A, player_team_A = get_player_info(season_A, player_id_A)
    player_name_B, player_age_B, player_team_B = get_player_info(season_B, player_id_B)

    results_data = {
        f'P1-Stats ({season_A})': [round(base_stats_A['PTS'], 1), round(base_stats_A['AST'], 1), round(base_stats_A['REB'], 1),
                                   round(base_stats_A['STL'], 1), round(base_stats_A['BLK'], 1), f"{round(base_stats_A['FG_PCT'], 3)}",
                                   f"{round(base_stats_A['FG3_PCT'], 3)}", f"{round(base_stats_A['FT_PCT'], 3)}", 
                                   round(adv_stats_A['NET_RATING'], 1), f"{round(adv_stats_A['EFG_PCT'], 3)}",
                                   f"{round(adv_stats_A['TS_PCT'], 3)}", round(adv_stats_A['PIE'], 3)],
        f'P1-Percentile ({season_A})': [round(percentiles_A['PTS'], 1), round(percentiles_A['AST'], 1), round(percentiles_A['REB'], 1),
                                        round(percentiles_A['STL'], 1), round(percentiles_A['BLK'], 1), f"{round(percentiles_A['FG_PCT'], 1)}",
                                        f"{round(percentiles_A['FG3_PCT'], 1)}", f"{round(percentiles_A['FT_PCT'], 1)}",
                                        round(percentiles_A['NET_RATING'], 1), f"{round(percentiles_A['EFG_PCT'], 1)}",
                                        f"{round(percentiles_A['TS_PCT'], 1)}", round(percentiles_A['PIE'], 1)],
        f'P2-Stats ({season_B})': [round(base_stats_B['PTS'], 1), round(base_stats_B['AST'], 1), round(base_stats_B['REB'], 1),
                                   round(base_stats_B['STL'], 1), round(base_stats_B['BLK'], 1), f"{round(base_stats_B['FG_PCT'], 3)}",
                                   f"{round(base_stats_B['FG3_PCT'], 3)}", f"{round(base_stats_B['FT_PCT'], 3)}", 
                                   round(adv_stats_B['NET_RATING'], 1), f"{round(adv_stats_B['EFG_PCT'], 3)}",
                                   f"{round(adv_stats_B['TS_PCT'], 3)}", round(adv_stats_B['PIE'], 3)],
        f'P2-Percentile ({season_B})': [round(percentiles_B['PTS'], 1), round(percentiles_B['AST'], 1), round(percentiles_B['REB'], 1),
                                        round(percentiles_B['STL'], 1), round(percentiles_B['BLK'], 1), f"{round(percentiles_B['FG_PCT'], 1)}",
                                        f"{round(percentiles_B['FG3_PCT'], 1)}", f"{round(percentiles_B['FT_PCT'], 1)}",
                                        round(percentiles_B['NET_RATING'], 1), f"{round(percentiles_B['EFG_PCT'], 1)}",
                                        f"{round(percentiles_B['TS_PCT'], 1)}", round(percentiles_B['PIE'], 1)],
        'Diff (Percentile)': [round(percentiles_B['PTS'] - percentiles_A['PTS'], 2),
                              round(percentiles_B['AST'] - percentiles_A['AST'], 2),
                              round(percentiles_B['REB'] - percentiles_A['REB'], 2),
                              round(percentiles_B['STL'] - percentiles_A['STL'], 2),
                              round(percentiles_B['BLK'] - percentiles_A['BLK'], 2),
                              round(percentiles_B['FG_PCT'] - percentiles_A['FG_PCT'], 2),
                              round(percentiles_B['FG3_PCT'] - percentiles_A['FG3_PCT'], 2),
                              round(percentiles_B['FT_PCT'] - percentiles_A['FT_PCT'], 2),
                              round(percentiles_B['NET_RATING'] - percentiles_A['NET_RATING'], 2),
                              round(percentiles_B['EFG_PCT'] - percentiles_A['EFG_PCT'], 2),
                              round(percentiles_B['TS_PCT'] - percentiles_A['TS_PCT'], 2),
                              round(percentiles_B['PIE'] - percentiles_A['PIE'], 2)]
    }

    # Add overall score to the results data
    results_data[f'P1-Stats ({season_A})'].append('')
    results_data[f'P1-Percentile ({season_A})'].append(round(overall_score_A + 5, 1))
    results_data[f'P2-Stats ({season_B})'].append('')
    results_data[f'P2-Percentile ({season_B})'].append(round(overall_score_B + 5, 1))
    results_data['Diff (Percentile)'].append(round(overall_score_B - overall_score_A, 1))

    # Create DataFrame with index
    index_labels = ['PTS', 'AST', 'REB', 'STL', 'BLK', 'FG_PCT', 'FG3_PCT', 'FT_PCT', 'NET_RATING', 'EFG_PCT', 'TS_PCT', 'PIE', 'OVR']
    results_df = pd.DataFrame(results_data, index=index_labels)

    # Generate HTML table
    table = tabulate(results_df, headers='keys', tablefmt='html', floatfmt=".1f")

    return render_template('compare.html', season_A=season_A, season_B=season_B, player_name_A=player_name_A, player_name_B=player_name_B, player_age_A=player_age_A, player_age_B=player_age_B, table=table)


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)
