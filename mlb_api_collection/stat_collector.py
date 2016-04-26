import requests
import json
from pymongo import MongoClient

url_format = "http://mlb.mlb.com/pubajax/wf/flow/stats.splayer?season={0}&sort_order=%27desc%27&sort_column=%27avg%27&stat_type={1}&page_type=SortablePlayer&game_type=%27R%27&player_pool=ALL&season_type=ANY&sport_code=%27mlb%27&results=1000&position=%272%27&recSP=1&recPP=1000"

client = MongoClient('mongodb://mlb:hellodata@homunculus.mit.edu/?authMechanism=SCRAM-SHA-1')
db = client['baseball']

def collectStats(year, stat_type, position):
    url = url_format.format(year, stat_type, position)
    print url
    num_added = 0
    results = requests.get(url)
    num_results = json_results['totalSize']

    while num_added < num_results:
        json_results = json.loads(results.text)['stats_sortable_player']['queryResults']
       

        collection = db['player_stats']
        collection.insert_many(json_results['row'])
        num_added += json_results['recs']

        results = requests.get(url)


# PITCHER = "'1'",
# CATCHER = "'2'",
# FIRST_BASEMAN = "'3'",
# SECOND_BASEMAN = "'4'",
# THIRD_BASEMAN = "'5'",
# SHORTSTOP = "'6'",
# LEFT_FIELDER = "'7'",
# CENTER_FIELDER = "'8'",
# RIGHT_FIELDER = "'9'",
# DESIGNATED_HITTER = "'D'",
# ALL_OUTFIELD = "'O'",

start_year = 2000
end_year = 2000

positions = range(2,3)
positions.append('D') 

for i in positions:
    for year in range(start_year, end_year + 1):
        print year
        if i == 1:
            collectStats(str(year), "pitching", str(i))
        collectStats(str(year), "hitting", str(i))