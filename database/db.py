from pymongo import MongoClient

uri = "mongodb://mlb:hellodata@18.42.2.112/?authMechanism=SCRAM-SHA-1"
client = MongoClient(uri).baseball

def insert(data):
    client.game_data.insert_many(data)
