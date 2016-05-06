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
game_data = db['game_data']
player_data = db['players']

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

def get_pitchers(year, mongodbnth, day):
    pitchers = []
    upcoming = upcoming_games.FetchGames(year, month, day)
    for game in upcoming:
        pitchers.append(game.home_pitcher)
        pitchers.append(game.away_pitcher)
    return pitchers

def get_opposing_lineup(team, year, month, day):
    date = datetime(year, month, day)
    all_players = player_data.find({ 'team_abbrev': team })
    at_bats = game_data.find({ 'batter': { '$in': [player['player_id'] for player in all_players] }, 'date': date })
    batter_ids = [at_bat['batter'] for at_bat in at_bats]
    return list(set(batter_ids))

pitchers = get_pitchers(2016,5,5)
result = hits_per_game(pitchers)
opposing_lineup = get_opposing_lineup('PIT', 2016,5,3)




