# coding: utf-8
import json
import urllib
import requests
from datetime import datetime
from datetime import date, timedelta
import time

now_time = datetime.now()
year = str(now_time.year)
month = str(now_time.month).zfill(2)
day = str(now_time.day).zfill(2)

data=requests.get('http://mlb.mlb.com/fantasylookup/rawjson/named.bts_tmplt_hitdd_teams.bam?year={2}&gameDate={0}%2F{1}%2F{2}'.format(month,day,year)).text
x = json.loads(data)


teams=x["dailyTeams"]["gameDate"]["team"]
gameDate = urllib.quote_plus(x["dailyTeams"]["gameDate"]["id"])

overall_prb = 0.0
overall_hitter = None
overall_hits = None
overall_ab = None

tops = []

d = datetime(2016, 1, 1, 1)
import db
import pandas as pd
data = [x for x in db.client.game_data.find({"date": {"$gt": d}})]
df = pd.DataFrame(data)
df = df.groupby(["batter", "pitcher"]).sum().reset_index()

for team in teams:
    tid = team['id']
    pitcher = team['pitcher']['id']
    phits = team["pitcher"]["hits"]
    phits = int(phits) if phits else 0
    pinn = team["pitcher"]["innings"]
    if "." in pinn:
        if pinn.endswith(".2"):
            pinn = int(pinn[:-2]) + (2.0/3)
        elif pinn.endswith(".1"):
            pinn = int(pinn[:-2]) + (1.0/3)
        else:
            raise Exception("BAD INNINGS!")
    else:
        pinn = int(pinn) if pinn else .9 # -- hmm

    hpi = (phits * 1.0) / pinn
    url = 'http://mlb.mlb.com/fantasylookup/rawjson/named.bts_hitdd_players.bam?year={}&gameDate={}&teamId={}&pitcherId={}'.format(year, gameDate, tid, pitcher)
    ''' h_hits / h_ab'''
    raw = requests.get(url).text
    time.sleep(.05)
    data = json.loads(raw)

    max_p = 0.0
    max_hitter = None
    max_hits =None
    max_ab =None

    for player in data["roster"]["team"]["player"]:
        batter_id = player["id"]
        stats = df[(df.batter == batter_id) & (df.pitcher == pitcher) & (df.hits > 0)]
        if not stats.empty:
            print player["name"], stats[["at_bats", "hits"]], float(player["h_avg"]), float(player["avg"])
            # test = stats[['at_bats', 'hits']]
            # raise Exception(test)
        # raise Exception(player)
        havg = float(player["h_avg"])
        avg = float(player["avg"])


print "OVERALL BEST:", overall_hitter, overall_prb, overall_hits, overall_ab
print sorted(tops, key=lambda x: x[1], reverse=True)[:5]
