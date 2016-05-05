import datetime
import json
import pandas as pd
import re

import db
import os

# TODO: cleanup error handling, remove hard-coded data path, better var names

def process(filepath, filename):
    try:
        rawdata = json.load(open(filepath))
    except:
        print "JSON parse ERROR!", filename
        return
    x = []
    for inning in rawdata['data']['game']['inning']:
        if isinstance(inning, basestring): continue
        for half in ['top', 'bottom']:
            if half in inning and 'atbat' in inning[half]:
                x += inning[half]['atbat']

    try:
        df = pd.DataFrame(x)
    except:
        print "DataFrame ERROR!", filename
        return

    df['count'] = 1

    if 'batter' not in df.columns:
        print "No Batters ERROR!", filename
        return

    df2 = df.groupby(['batter', 'pitcher', 'event']).agg({'count':sum})
    df2 = df2.reset_index()
    df2 = df2.pivot_table(index=['batter','pitcher'], columns='event', values='count')
    df2 = df2.reset_index()
    df2["plate_appearances"] = df2.sum(axis=1)
    eventTypes = ["Batter Interference", "Bunt Groundout", "Bunt Lineout", "Bunt Pop Out", "Catcher Interference",
                   "Double", "Double Play", "Fan interference", "Field Error", "Fielders Choice", "Fielders Choice Out",
                   "Flyout", "Forceout", "Grounded Into DP", "Groundout", "Hit By Pitch", "Home Run", "Intent Walk",
                   "Lineout", "Pop Out", "Runner Out", "Sac Bunt", "Sac Fly", "Sac Fly DP", "Sacrifice Bunt DP",
                   "Single", "Strikeout", "Strikeout - DP", "Triple", "Triple Play", "Walk",
                   ]
    atbatTypes = ["Bunt Groundout", "Bunt Lineout", "Bunt Pop Out",
                   "Double", "Double Play", "Field Error", "Fielders Choice", "Fielders Choice Out",
                   "Flyout", "Forceout", "Grounded Into DP", "Groundout", "Home Run",
                   "Lineout", "Pop Out", "Runner Out",
                   "Single", "Strikeout", "Strikeout - DP", "Triple", "Triple Play",
                   ]
    hitTypes = ["Single", "Double", "Triple", "Home Run"]
    tmp = list(set.intersection(set(hitTypes), set(df2.columns)))
    df2['hits'] = df2[tmp].sum(axis=1)

    tmp = list(set.intersection(set(atbatTypes), set(df2.columns)))
    df2['atbats'] = df2[tmp].sum(axis=1)

    df2["game_id"] = filename.split(".json")[0]
    match = re.match('gid_(\d+)_(\d+)_(\d+).*', filename)
    df2["date"] ="{}/{}/{}".format( match.group(2) , match.group(3), match.group(1))
    df2["date"] = pd.to_datetime(df2["date"])
    stadium = re.match('gid_\d+_\d+_\d+_\w+mlb_(\w+)mlb.*', filename)
    df2["ballpark"] = stadium.group(1)
    data = df2.to_dict('records')
    db.insert(data)

for year in ["2015"]:
    # make this an ENV var
    base_dir = '/Users/jspeiser/Google Drive/beat-the-streak/{}'.format(year)
    for filename in os.listdir(base_dir):
        process(os.path.join(base_dir, filename), filename)
