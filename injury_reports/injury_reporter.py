import requests
import json
from datetime import datetime
from pymongo import MongoClient

print "*** Starting injury scrape at", datetime.now(), "***"

client = MongoClient('mongodb://mlb:hellodata@homunculus.mit.edu/?authMechanism=SCRAM-SHA-1')
db = client['baseball']
collection = db['injury_data']

injury_data = requests.get('http://mlb.mlb.com/fantasylookup/json/named.wsfb_news_injury.bam')
print "Successfully pulled injury data from mlb.com"

latest_injuries = collection.find_one({'latest': True})
latest_batch = latest_injuries['batch'] if latest_injuries else -1
print "Latest batch prior to this scrape: ", latest_batch

new_batch = latest_batch + 1

print "Setting previous latest batch to false..."
result = collection.update_many(
    { "latest": True },
    {
        "$set": {"latest": False },
    }
)
print "Done setting latest to false"

injury_json = json.loads(injury_data.text)

print "Adding new batch to db..."
for injury in injury_json['wsfb_news_injury']['queryResults']['row']:
    injury['scraped_date'] = datetime.utcnow().strftime('%x %X')
    injury['latest'] = True
    injury['batch'] = new_batch
    collection.insert_one(injury)
print "Done adding new batch to db"

print "*** Finished injury scrape at", datetime.now(), "***"


