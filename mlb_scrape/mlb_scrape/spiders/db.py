from pymongo import MongoClient

uri = "mongodb://mlb:hellodata@18.42.2.112/?authMechanism=SCRAM-SHA-1"
client = MongoClient(uri).baseball

def insert(data, dbName='game_data'):
    getattr(client, dbName).insert_many(data)
