import json
from pymongo import MongoClient

with open("configs/config.json", 'r') as file:
    config = json.load(file)


def get_mongo_client():
    return MongoClient(config['MONGO_URI'])


def get_resume_database(db_name="resume_db"):
    client = get_mongo_client()
    return client[db_name]


def get_key_database(db_name="key_db"):
    client = get_mongo_client()
    return client[db_name]
