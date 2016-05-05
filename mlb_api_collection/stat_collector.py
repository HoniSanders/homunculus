import requests
import json
from pymongo import MongoClient
import time

url_format = "http://mlb.mlb.com/pubajax/wf/flow/stats.splayer?season={0}&sort_order=%27desc%27&sort_column=%27avg%27&stat_type={1}&page_type=SortablePlayer&game_type=%27R%27&player_pool=ALL&season_type=ANY&sport_code=%27mlb%27&results=1000&recSP={2}&recPP=500"

client = MongoClient('mongodb://mlb:hellodata@homunculus.mit.edu/?authMechanism=SCRAM-SHA-1')
db = client['baseball']
collection = db['player_stats']

def collectStats(year, stat_type):
    current_page = 1
    url = url_format.format(year, stat_type, str(current_page))
    if stat_type == 'pitching':
        url += '&position=%27{0}%27'.format('1')
    print url
    
    time.sleep(5)
    json_results = requestWithRetry(url)

    num_results = json_results['recs']

    while num_results != '0':
        for player in json_results['row']:
            player['season'] = year
        collection.insert_many(json_results['row'])
        current_page += 1
        url = url_format.format(year, stat_type, str(current_page))
        print url
        time.sleep(5)
        json_results = requestWithRetry(url)
        num_results = json_results['recs']

def requestWithRetry(url):
    retry_count = 0
    while True:
        try:
            results = requests.get(url)
            return json.loads(results.text)['stats_sortable_player']['queryResults']
            break
        except ValueError:
            print "Exception on request. url attempted: ", url
            if retry_count == 5:
                exit(1)
            retry_count += 1
            time.sleep(30)  

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
end_year = 2016

for year in range(start_year, end_year + 1):
    print year
    collectStats(str(year), "pitching")
    collectStats(str(year), "hitting")