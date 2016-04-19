import requests
import json
from datetime import datetime
from pymongo import MongoClient

client = MongoClient('mongodb://mlb:hellodata@homunculus.mit.edu/?authMechanism=SCRAM-SHA-1')
db = client['baseball']
collection = db['injury_data']

injury_data = requests.get('http://mlb.mlb.com/fantasylookup/json/named.wsfb_news_injury.bam')

latest_injuries = collection.find_one({'latest': True})
latest_batch = latest_injuries['batch'] if latest_injuries else -1

new_batch = latest_batch + 1

result = collection.update_many(
    { "latest": True },
    {
        "$set": {"latest": False },
    }
)

injury_json = json.loads(injury_data.text)
for injury in injury_json['wsfb_news_injury']['queryResults']['row']:
    injury['scraped_date'] = datetime.utcnow().strftime('%x %X')
    injury['latest'] = True
    injury['batch'] = new_batch
    collection.insert_one(injury)



