import db
import pandas as pd
import numpy as np
from datetime import datetime

# problem.  database output does not have pitcher or batter fields

gamedb = db.client.game_data_new
db.client.game_data_new2.remove()
seasonStart = datetime(2016, 1, 1, 1)
batterList = gamedb.find({"date": {"$gt": seasonStart}}).distinct('batter')
for batter_id in batterList:
    print batter_id
    # batter_id = '407812'
    data = [x for x in gamedb.find({'batter': batter_id, "date": {"$gt": seasonStart}})]
    df = pd.DataFrame(data)
    df = df.groupby(["game_id", "date"]).sum().reset_index()
    df = df.fillna(0)       # turn nan to 0
    df = df.sort_values(by='date', ascending=True)

    cumHits = df['hits'].cumsum()
    cumAtbats = df['atbats'].cumsum()
    cumBA = cumHits/cumAtbats
    if len(cumBA) > 1:
        cumBA[1:len(cumBA)-1] = cumBA[0:len(cumBA)-2]
    # ^ move all batting averages up a game so as only to take into account previous data for current game's BA
    cumBA[0] = np.nan
    df['cumBA'] = cumBA
    data = df.to_dict('records')
    db.client.game_data_new2.insert_many(data)

print True