from pymongo import MongoClient

uri = "mongodb://mlb:hellodata@18.42.5.175/?authMechanism=SCRAM-SHA-1"
client = MongoClient(uri).baseball
print dir(client)

def insert(data):
    client.game_data.insert_many(data)
