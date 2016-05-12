import requests
import json
from pymongo import MongoClient
from datetime import datetime
import pandas as pd
import sys

sys.path.append("../upcoming_games")
import upcoming_games

client = MongoClient('mongodb://mlb:hellodata@homunculus.mit.edu/?authMechanism=SCRAM-SHA-1')
db = client['baseball']
game_data = db['game_data_new']
player_data = db['players']
player_df = pd.DataFrame(list(player_data.find()))

def crosswalk(ballpark):
    bmap = {'tba': 'TB', 'lan': 'LAD',
        'nyn': 'NYM', 'nya': 'NYY', 'sfn': 'SF',
        'kca': 'KC', 'sdn': 'SD', 'sln': 'STL', 'ana': 'LAA',
        'chn': 'CHC', 'cha':'CWS', 'was': 'WSH',
    }
    if ballpark in bmap:
        return bmap[ballpark]
    return ballpark.upper()

def hits_by_ballpark():
    date = datetime(2016, 4, 3)
    records = list(game_data.find({'date': {'$gt': date}}))
    df = pd.DataFrame(records)
    df = df.groupby(["ballpark", "date"]).agg({"hits": sum}).reset_index()
    df = df.groupby(["ballpark"]).agg({ "hits": pd.Series.mean }).reset_index().sort('hits')
    df['ballpark'] = df.ballpark.apply(crosswalk)
    df.rename(columns={"ballpark": "team_abbrev"}, inplace=True)
    return df


def plate_appearances_by_team():
    date = datetime(2016, 4, 3)
    records = list(game_data.find({'date': {'$gt': date}}))
    df = pd.DataFrame(records)

    df = df.merge(player_df, left_on="batter", right_on="player_id", how='left')
    df = df.groupby(["team_abbrev", "date"]).agg({"plate_appearances": sum}).reset_index()
    df = df.groupby(["team_abbrev"]).agg({ "plate_appearances": pd.Series.mean }).reset_index().sort('plate_appearances')
    #df['pa_score'] = (df.plate_appearances - df.plate_appearances.mean()) / (df.plate_appearances.max() - df.plate_appearances.min())
    return df


def hits_per_game(pitchers):
    date = datetime(2015, 4, 9)
    pitcher_map = [{ "pitcher": str(pitcher.player_id), "name" : pitcher.first_name + " " + pitcher.last_name } for pitcher in pitchers]
    pitcher_df = pd.DataFrame(pitcher_map)

    records = list(game_data.find({'date': {'$gt': date}, 'pitcher': {'$in': list(pitcher_df.pitcher.values) }}))
    print len(records)
    df = pd.DataFrame(records)
    df = df.groupby(["pitcher", "game_id"]).agg({"hits": sum}).reset_index()
    df = df.groupby(["pitcher"]).agg({ "hits": pd.Series.mean }).reset_index()

    return df.merge(pitcher_df, on='pitcher').sort('hits')

def get_pitchers(year, month, day):
    pitchers = []
    upcoming = upcoming_games.FetchGames(year, month, day)
    for game in upcoming:
        pitchers.append([game.home_pitcher, game.away_team])
        pitchers.append([game.away_pitcher, game.home_team])
    return pitchers

def get_opposing_lineup(teamId, year, month, day, pId):
    import requests
    url = 'http://mlb.mlb.com/fantasylookup/rawjson/named.bts_hitdd_players.bam?year=2016&gameDate={}/{}/{}&teamId={}&pitcherId={}'.format(month, day, year, teamId, pId)
    return requests.get(url).json()

def scorify(df, col):
    return (df[col] - df[col].mean())/df[col].std()

day = 12
pitchers = get_pitchers(2016, 5, day)
my_df = []
for p,team in pitchers:
    print p
    opposing_lineup = get_opposing_lineup(team.team_id, 2016, 5, day, p.player_id)
    data = opposing_lineup['roster']['team']['player']
    for b in data:
        tmp = {"pitcher": p.player_id, "batter": b["id"], "h_ab": b["h_ab"], "h_avg":b["h_avg"]}
        my_df.append(tmp)

my_df = pd.DataFrame(my_df)
my_df = my_df[my_df.h_ab.astype(float) >= 10].copy()
my_df = my_df.merge(player_df, left_on="batter", right_on="player_id", how='left')

df1 = hits_by_ballpark()
df1 = df1.merge(plate_appearances_by_team(), on='team_abbrev', how='outer')
my_df = my_df.merge(df1, on="team_abbrev")
my_df['h_avg'] = my_df.h_avg.astype(float)
my_df['h_avg'] = scorify(my_df, 'h_avg')
my_df['hits'] = scorify(my_df, 'hits')
my_df['plate_appearances'] = scorify(my_df, 'plate_appearances')

my_df['score'] = 1.65 * my_df.h_avg + (0.075 * my_df.hits) + (0.055 * my_df.plate_appearances)
print my_df[['name', 'pitcher', 'score', 'team_abbrev']].sort('score')
